from PySide2 import QtCore

import time
import datetime as dt
import numpy as np
import pandas as pd

import core_functions as cf
from physics_functions import ResonanceFit, calculate_resonance_frequency

import matplotlib as mpl
from scipy.optimize import curve_fit


class CapacitanceScan(QtCore.QThread):
    """
    Class thread that handles the spectrum measurement
    """

    # Define costum signals
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
    # With pyside2 https://wiki.qt.io/Qt_for_Python_Signals_and_Slots
    update_spectrum_signal = QtCore.Signal(list, list, list, str, bool, str, bool)
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
        self.update_spectrum_signal.connect(parent.update_capacitance_spectrum)
        self.update_progress_bar.connect(parent.progressBar.setProperty)

        # Read global paramters
        self.global_settings = cf.read_global_settings()

        self.df_data = pd.DataFrame(columns=["frequency", "voltage", "current"])
        self.df_resonance_fit = pd.DataFrame(
            columns=[
                "capacitance",
                "resonance_frequency",
                "maximum_current",
                "quality_factor",
            ]
        )
        self.is_killed = False

    def run(self):
        """
        Class that does a frequency sweep
        """

        import pydevd

        pydevd.settrace(suspend=False)

        # Set voltage and current (they shall remain constant over the entire sweep)
        self.source.set_voltage(self.measurement_parameters["voltage"], channel=2)
        self.source.set_current(
            self.measurement_parameters["current_compliance"], channel=2
        )

        # Clear axis before the measurement
        self.parent.capw_ax.cla()
        self.parent.capw_ax.set_ylabel("Current (A)")
        self.parent.capw_ax.set_xlabel("Frequency (kHz)")
        self.parent.capw_ax.grid(True)
        self.parent.capw_ax.axhline(linewidth=1, color="black")
        self.parent.capw_ax.axvline(linewidth=1, color="black")

        # Make sure to choose closest resonance frequencies to a given step size
        available_caps = pd.DataFrame(
            columns=["constituents", "arduino_pins", "sum", "resonance_frequency"]
        )

        for freq in np.arange(
            self.measurement_parameters["minimum_frequency"],
            self.measurement_parameters["maximum_frequency"],
            self.measurement_parameters["resonance_frequency_step"],
        ):
            temp_series = pd.Series(
                self.arduino.all_capacitances_df.iloc[
                    (self.arduino.all_capacitances_df.resonance_frequency - freq)
                    .abs()
                    .argsort()[:1]
                ].values[0],
                index=["constituents", "arduino_pins", "sum", "resonance_frequency"],
            )
            available_caps = pd.concat(
                [available_caps, pd.DataFrame([temp_series])], ignore_index=True
            )

        # First check the given minimum and maximum value for the capacitance
        selected_available_cap = available_caps["sum"].to_numpy()

        # Sort out that only the closest to a step size are taken

        # Set a new color for the plot
        cmap = mpl.cm.get_cmap("viridis", np.size(selected_available_cap))
        device_color = np.array(
            [mpl.colors.rgb2hex(cmap(i)) for i in range(cmap.N)], dtype=object
        )

        cf.log_message("Capacitances that are scanned " + str(selected_available_cap))

        # Count up the colors
        color_counter = 0
        # Helper variable for correct plotting
        first_bool = True

        # Sweep over all selected capacitances
        for capacitance in selected_available_cap:
            # Now set the capacitance
            self.arduino.set_capacitance(capacitance)
            self.source.output(True, channel=2)

            # Define dataframe to store data in
            del self.df_data
            self.df_data = pd.DataFrame(columns=["frequency", "voltage", "current"])

            # Counter for data storage
            i = 0

            # Sweep over all frequencies within a range around the predicted
            # resonance frequency. It is calculated from inductance and set
            # capacitance. It is recommended to provide an effective inductance
            # from experimental parameters in the settings to obtain good
            # results
            predicted_resonance_frequency = np.round(
                calculate_resonance_frequency(
                    capacitance * 1e-12, self.global_settings["coil_inductance"] * 1e-3
                )
                / 1e3,
                1,
            )

            min_frequency = (
                predicted_resonance_frequency
                - self.measurement_parameters["frequency_margin"]
            )
            max_frequency = (
                predicted_resonance_frequency
                + self.measurement_parameters["frequency_margin"]
            )

            frequencies = np.arange(
                min_frequency,
                max_frequency,
                self.measurement_parameters["frequency_step"],
            )
            self.arduino.trigger_frequency_generation(True)

            # frequency = self.measurement_parameters["minimum_frequency"]
            for frequency in frequencies:
                # while frequency <= self.measurement_parameters["maximum_frequency"]:
                # for frequency in self.df_data["frequency"]:
                # cf.log_message("Frequency set to " + str(frequency) + " kHz")

                # Set frequency
                self.arduino.set_frequency(frequency)

                # Wait a bit
                time.sleep(self.measurement_parameters["frequency_settling_time"])

                # Measure the voltage and current (and posssibly paramters on the osci)
                voltage, current = self.source.read_values(channel=2)

                # Now measure Vpp from channel one on the oscilloscope
                # vpp = float(self.oscilloscope.measure_vpp())

                # Set the variables in the dataframe
                self.df_data.loc[i, "voltage"] = voltage
                self.df_data.loc[i, "current"] = current
                self.df_data.loc[i, "frequency"] = frequency
                # self.df_data.loc[i, "vpp"] = vpp

                # Update progress bar
                self.update_progress_bar.emit(
                    "value",
                    int(
                        (color_counter + (i + 1) / len(frequencies))
                        / len(selected_available_cap)
                        * 100
                    ),
                )

                # print(color_counter)
                # print(i)
                # print(len(self.df_data["frequency"]))
                # print(len(selected_available_cap))

                self.update_spectrum_signal.emit(
                    self.df_data["frequency"],
                    self.df_data["current"],
                    [
                        self.measurement_parameters["minimum_frequency"]
                        - self.measurement_parameters["frequency_margin"],
                        self.measurement_parameters["maximum_frequency"]
                        + self.measurement_parameters["frequency_margin"],
                    ],
                    str(capacitance) + " pF",
                    first_bool,
                    device_color[color_counter],
                    False
                    # self.df_data["vpp"],
                )

                # Now compute the slope to adjust the step hight on the fly
                # if i > 0:
                #     slope = abs(
                #         (
                #             self.df_data.loc[i, "current"]
                #             - self.df_data.loc[i - 1, "current"]
                #         )
                #         / (
                #             self.df_data.loc[i, "frequency"]
                #             - self.df_data.loc[i - 1, "frequency"]
                #         )
                #     )

                # frequency = frequency + self.measurement_parameters["frequency_step"]

                i += 1
                first_bool = False

                if self.is_killed:
                    # Close the connection to the spectrometer
                    self.source.output(False, channel=2)
                    self.source.set_voltage(5, channel=2)
                    self.arduino.trigger_frequency_generation(False)
                    # Save all resonance data you have
                    self.save_resonance_data()
                    self.quit()
                    return

            self.arduino.trigger_frequency_generation(True)
            # self.hf_source.output(False)
            self.save_data(str(capacitance) + "pF")

            # Helper variable for correct plotting
            first_bool = True

            # If selected by the user, do a fit of the data
            # around the expected range, get all resonance frequencies and save
            # to file
            try:
                fit_class = ResonanceFit(
                    resistance=self.global_settings["circuit_resistance"],
                    voltage=self.measurement_parameters["voltage"],
                )
                popt, pcov = fit_class.fit(
                    self.df_data["frequency"].to_numpy(),
                    self.df_data["current"].to_numpy(),
                )

                self.df_resonance_fit.loc[color_counter, "capacitance"] = capacitance
                self.df_resonance_fit.loc[color_counter, "resonance_frequency"] = popt[
                    0
                ]
                self.df_resonance_fit.loc[
                    color_counter, "maximum_current"
                ] = self.df_data["current"].max()
                self.df_resonance_fit.loc[color_counter, "quality_factor"] = popt[1]

                # Extend the plotted range
                x_fit = np.linspace(
                    self.df_data["frequency"].min(),
                    self.df_data["frequency"].max(),
                    500,
                )

                # Plot Fit
                self.update_spectrum_signal.emit(
                    x_fit,
                    fit_class.func(x_fit, *popt),
                    [
                        self.measurement_parameters["minimum_frequency"]
                        - self.measurement_parameters["frequency_margin"],
                        self.measurement_parameters["maximum_frequency"]
                        + self.measurement_parameters["frequency_margin"],
                    ],
                    str(capacitance) + "pF fit",
                    first_bool,
                    device_color[color_counter],
                    True
                    # self.df_data["vpp"],
                )
            except:
                self.df_resonance_fit.loc[color_counter, "capacitance"] = capacitance
                self.df_resonance_fit.loc[color_counter, "resonance_frequency"] = 0
                self.df_resonance_fit.loc[
                    color_counter, "maximum_current"
                ] = self.df_data["current"].max()
                self.df_resonance_fit.loc[color_counter, "quality_factor"] = 0

            color_counter += 1

        self.arduino.trigger_frequency_generation(False)
        self.source.output(False, channel=2)
        self.save_resonance_data()
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
        Function to save the measured data to file.
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
            "Min. Frequency:   "
            + str(self.measurement_parameters["minimum_frequency"])
            + " kHz \t"
            + "Max. Frequency:   "
            + str(self.measurement_parameters["maximum_frequency"])
            + " kHz \t"
            + "Frequency Step:   "
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

    def save_resonance_data(self):
        """
        Function to save the fitted data of the resonances
        """

        # Define Header
        line03 = (
            "Voltage:   "
            + str(self.measurement_parameters["voltage"])
            + " V   "
            + "Current:   "
            + str(self.measurement_parameters["current_compliance"])
            + " A   "
        )
        line04 = (
            "Min. Frequency:   "
            + str(self.measurement_parameters["minimum_frequency"])
            + " kHz \t"
            + "Max. Frequency:   "
            + str(self.measurement_parameters["maximum_frequency"])
            + " kHz \t"
            + "Circuit Resistance:   "
            + str(self.global_settings["circuit_resistance"])
            + " Ohm \t"
            + "Settling Time:   "
            + str(self.measurement_parameters["frequency_settling_time"])
            + " s \t"
        )
        line05 = "### Measurement data ###"
        line06 = "Capacitance\t Resonance Frequency\t Maximum Current\t Quality Factor"
        line07 = "pF\t kHz\t A\t\n"

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
            + "_resonances"
            + ".csv"
        )
        cf.save_file(self.df_resonance_fit, file_path, header_lines)
        print(self.df_resonance_fit)
        cf.log_message("Resonance frequencies saved")
