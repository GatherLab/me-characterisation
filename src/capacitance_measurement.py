from PySide2 import QtCore

import time
import datetime as dt
import numpy as np
import pandas as pd

import core_functions as cf

import matplotlib as mpl
from scipy.optimize import curve_fit


class CapacitanceScan(QtCore.QThread):
    """
    Class thread that handles the spectrum measurement
    """

    # Define costum signals
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
    # With pyside2 https://wiki.qt.io/Qt_for_Python_Signals_and_Slots
    update_spectrum_signal = QtCore.Signal(list, list, list, str, bool, str)
    update_progress_bar = QtCore.Signal(str, float)

    def __init__(
        self,
        arduino,
        source,
        # oscilloscope,
        measurement_parameters,
        setup_parameters,
        parent=None,
    ):
        super(CapacitanceScan, self).__init__()
        # Variable to kill thread

        # Assign hardware and reset
        self.arduino = arduino
        self.arduino.init_serial_connection()
        self.source = source
        # self.oscilloscope = oscilloscope
        self.parent = parent

        self.measurement_parameters = measurement_parameters
        self.setup_parameters = setup_parameters

        # Connect signal to the updater from the parent class
        self.update_spectrum_signal.connect(parent.update_spectrum)
        self.update_progress_bar.connect(parent.progressBar.setProperty)

        self.df_data = pd.DataFrame(columns=["frequency", "voltage", "current"])
        self.is_killed = False

    def run(self):
        """
        Class that does a frequency sweep
        """

        # Set voltage and current (they shall remain constant over the entire sweep)
        self.source.set_voltage(self.measurement_parameters["voltage"])
        self.source.set_current(self.measurement_parameters["current_compliance"])

        # Clear axis before the measurement
        self.parent.capw_ax.cla()
        self.parent.capw_ax.set_ylabel("Current (A)")
        self.parent.capw_ax.set_xlabel("Frequency (kHz)")
        self.parent.capw_ax.grid(True)
        self.parent.capw_ax.axhline(linewidth=1, color="black")
        self.parent.capw_ax.axvline(linewidth=1, color="black")

        # First check the given minimum and maximum value for the capacitance
        selected_available_cap = self.arduino.combinations_df.loc[
            np.logical_and(
                self.arduino.combinations_df["sum"]
                >= self.measurement_parameters["minimum_capacitance"],
                self.arduino.combinations_df["sum"]
                <= self.measurement_parameters["maximum_capacitance"],
            ),
            "sum",
        ].to_numpy()

        # Set a new color for the plot
        cmap = mpl.cm.get_cmap("viridis", np.size(selected_available_cap))
        device_color = np.array(
            [mpl.colors.rgb2hex(cmap(i)) for i in range(cmap.N)], dtype=object
        )

        cf.log_message("Capacitances that are scanned " + str(selected_available_cap))

        # Count up the colors
        color_counter = 0

        # Sweep over all selected capacitances
        for capacitance in selected_available_cap:
            # Now set the capacitance
            self.arduino.set_capacitance(capacitance)
            self.source.output(True)

            # In the future: If selected by the user, do a fit of the data
            # around the expected range, get all resonance frequencies and save
            # to file

            # Define dataframe to store data in
            del self.df_data
            self.df_data = pd.DataFrame(columns=["frequency", "voltage", "current"])

            # Counter for data storage
            i = 0

            # Helper variable for correct plotting
            first_bool = True

            # Sweep over all frequencies
            frequency = self.measurement_parameters["minimum_frequency"]
            while frequency <= self.measurement_parameters["maximum_frequency"]:
                # for frequency in self.df_data["frequency"]:
                # cf.log_message("Frequency set to " + str(frequency) + " kHz")

                # Set frequency
                self.arduino.set_frequency(frequency)

                # Wait a bit
                time.sleep(0.5)

                # Measure the voltage and current (and posssibly paramters on the osci)
                voltage, current, mode = self.source.read_values()

                # Now measure Vpp from channel one on the oscilloscope
                # vpp = float(self.oscilloscope.measure_vpp())

                # Set the variables in the dataframe
                self.df_data.loc[i, "voltage"] = voltage
                self.df_data.loc[i, "current"] = current
                self.df_data.loc[i, "frequency"] = frequency
                # self.df_data.loc[i, "vpp"] = vpp

                # Update progress bar
                self.update_progress_bar.emit(
                    "value", int((i + 1) / len(self.df_data["frequency"]) * 100)
                )

                self.update_spectrum_signal.emit(
                    self.df_data["frequency"],
                    self.df_data["current"],
                    [
                        self.measurement_parameters["minimum_frequency"],
                        self.measurement_parameters["maximum_frequency"],
                    ],
                    str(capacitance) + "pF",
                    first_bool,
                    device_color[color_counter]
                    # self.df_data["vpp"],
                )

                # Now compute the slope to adjust the step hight on the fly
                if i > 0:
                    slope = abs(
                        (
                            self.df_data.loc[i, "current"]
                            - self.df_data.loc[i - 1, "current"]
                        )
                        / (
                            self.df_data.loc[i, "frequency"]
                            - self.df_data.loc[i - 1, "frequency"]
                        )
                    )

                frequency = frequency + self.measurement_parameters["frequency_step"]

                i += 1
                first_bool = False

                if self.is_killed:
                    # Close the connection to the spectrometer
                    self.source.output(False)
                    self.source.set_voltage(5)
                    self.quit()
                    return

            self.source.output(False)
            self.save_data(str(capacitance) + "pF")
            color_counter += 1

        self.parent.capw_start_measurement_pushButton.setChecked(False)
        self.arduino.set_capacitance(self.arduino.base_capacitance)
        # self.parent.setup_thread.pause = False
        # self.parent.oscilloscope_thread.pause = False

    def kill(self):
        """
        Kill thread while running
        """
        self.is_killed = True

    def save_data(self, suffix):
        """
        Function to save the measured data to file. This should probably be
        integrated into the AutotubeMeasurement class
        """

        # Define Header
        line03 = (
            "Voltage:   "
            + str(self.measurement_parameters["voltage"])
            + " V   "
            + "Current:   "
            + str(self.measurement_parameters["current_compliance"])
            + " A   "
            + suffix
        )
        line04 = (
            "Min. Capacitance:   "
            + str(self.measurement_parameters["minimum_frequency"])
            + " kHz \t"
            + "Max. Capacitance:   "
            + str(self.measurement_parameters["maximum_frequency"])
            + " kHz \t"
            + "Capacitance Step:   "
            + str(self.measurement_parameters["frequency_step"])
            + " kHz \t"
        )
        line05 = "### Measurement data ###"
        line06 = "Frequency\t Voltage\t Current"
        line07 = "Hz\t V\t A\n"

        header_lines = [
            line03,
            line04,
            line05,
            line06,
            line07,
        ]

        # Write header lines to file
        file_path = (
            self.setup_parameters["folder_path"]
            + dt.date.today().strftime("%Y-%m-%d_")
            + self.setup_parameters["batch_name"]
            + "_d"
            + str(self.setup_parameters["device_number"])
            + "_"
            + suffix
            + ".csv"
        )
        cf.save_file(self.df_data, file_path, header_lines)

        # with open(file_path, "a") as the_file:
        #     the_file.write("\n".join(header_lines))

        # # Now write pandas dataframe to file
        # self.df_data.to_csv(file_path, index=False, mode="a", header=False, sep="\t")
