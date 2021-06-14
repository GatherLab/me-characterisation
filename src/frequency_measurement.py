from PySide2 import QtCore

import time
import datetime as dt
import numpy as np
import pandas as pd
import math

# import json
# import os.path
# from pathlib import Path

import core_functions as cf
import physics_functions as pf

from simple_pid import PID


class FrequencyScan(QtCore.QThread):
    """
    Class thread that handles the spectrum measurement
    """

    # Define costum signals
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
    # With pyside2 https://wiki.qt.io/Qt_for_Python_Signals_and_Slots
    update_spectrum_signal = QtCore.Signal(list, list, list, list)
    update_progress_bar = QtCore.Signal(str, float)

    def __init__(
        self,
        arduino,
        source,
        oscilloscope,
        measurement_parameters,
        setup_parameters,
        parent=None,
    ):
        super(FrequencyScan, self).__init__()
        # Variable to kill thread

        # Assign hardware and reset
        self.arduino = arduino
        self.arduino.init_serial_connection()
        self.source = source
        self.oscilloscope = oscilloscope
        self.parent = parent

        self.measurement_parameters = measurement_parameters
        self.setup_parameters = setup_parameters

        self.global_parameters = cf.read_global_settings()

        # Connect signal to the updater from the parent class
        self.update_spectrum_signal.connect(parent.update_spectrum)
        self.update_progress_bar.connect(parent.progressBar.setProperty)

        # Define dataframe to store data in
        self.df_data = pd.DataFrame(
            columns=["frequency", "voltage", "current", "magnetic_field", "vmax"]
        )

        self.is_killed = False

        # If
        if measurement_parameters["constant_magnetic_field_mode"]:
            pid_parameters = np.array(
                self.global_parameters["pid_parameters"].split(","), dtype=float
            )
            self.source.start_constant_magnetic_field_mode(
                pid_parameters,
                self.measurement_parameters["current_compliance"],
                self.measurement_parameters["voltage"],
            )

            # with open(
            # os.path.join(Path(__file__).parent.parent, "usr", "pid_tuning.json")
            # ) as json_file:
            # data = json.load(json_file)
            # pid_parameters = np.array(
            #     self.global_parameters["pid_parameters"].split(","), dtype=float
            # )
            # self.pid = PID(
            #     pid_parameters[0],
            #     pid_parameters[1],
            #     pid_parameters[2],
            #     setpoint=self.measurement_parameters["current_compliance"],
            # )
            # self.pid.output_limits = (1, self.measurement_parameters["voltage"])
            # self.pid.proportional_on_measurement = True

    def run(self):
        """
        Class that does a frequency sweep
        """
        # self.parent.setup_thread.pause = True
        # self.parent.oscilloscope_thread.pause = True

        # First define the frequencies the program shall sweep over
        # self.df_data["frequency"] = np.arange(
        # self.measurement_parameters["minimum_frequency"],
        # self.measurement_parameters["maximum_frequency"],
        # self.measurement_parameters["frequency_step"],
        # )
        import pydevd

        pydevd.settrace(suspend=False)

        # Measure time elapsed
        start_time = time.time()

        self.parent.oscilloscope_thread.pause = True

        # Set voltage and current (they shall remain constant over the entire sweep)
        self.source.set_voltage(self.measurement_parameters["voltage"])
        if not self.measurement_parameters["constant_magnetic_field_mode"]:
            self.source.set_current(self.measurement_parameters["current_compliance"])
        else:
            # Calculate the average time it took to adjust the magnetic field
            total_adjustment_time = 0

        # Define arrays in which the data shall be stored in
        i = 0

        # Sweep over all frequencies
        frequencies = np.arange(
            self.measurement_parameters["minimum_frequency"],
            self.measurement_parameters["maximum_frequency"],
            self.measurement_parameters["frequency_step"],
        )
        for frequency in frequencies:
            # for frequency in self.df_data["frequency"]:
            # cf.log_message("Frequency set to " + str(frequency) + " kHz")

            # Set frequency
            self.arduino.set_frequency(
                frequency, self.measurement_parameters["autoset_capacitance"]
            )

            # Activate output only when frequency was set
            if i == 0:
                self.source.output(True)
                time.sleep(1)

            # In constant magnetic field mode, regulate the voltage until a
            # magnetic field is reached
            if self.measurement_parameters["constant_magnetic_field_mode"]:
                # start_time = time.time()
                # i = 0
                # a = 0
                # while True:
                # Generate step-response data to tune with https://pidtuner.com/
                # Time (frequency hijacked)
                # time_it = round(time.time() - start_time, 2)
                # self.df_data.loc[i, "frequency"] = time_it

                # if i == 0:
                #     self.source.output(False)
                #     voltage = 0
                # elif i == 20:
                #     voltage = 2
                #     self.source.set_voltage(2)
                #     self.source.output(True)
                # elif i == 30:
                #     voltage = 0
                #     self.source.output(False)
                # elif i == 50:
                #     voltage = 4
                #     self.source.set_voltage(4)
                #     self.source.output(True)
                # elif i == 60:
                #     voltage = 0
                #     self.source.output(False)
                # elif i == 70:
                #     self.save_data()
                #     print("Data saved")

                pid_voltage, elapsed_time = self.source.adjust_magnetic_field(
                    self.global_parameters["pickup_coil_windings"],
                    self.global_parameters["pickup_coil_radius"],
                    frequency,
                    self.oscilloscope,
                    break_if_too_long=True,
                )

                # # Plot a graph (for PID tuning)
                # self.df_data.loc[i, "voltage"] = 1
                # self.df_data.loc[i, "current"] = 1

                # self.df_data.loc[i, "magnetic_field"] = magnetic_field
                # self.df_data.loc[i, "vmax"] = 1

                # self.update_spectrum_signal.emit(
                #     self.df_data["frequency"],
                #     self.df_data["current"],
                #     self.df_data["magnetic_field"],
                #     self.df_data["vmax"],
                # )
                total_adjustment_time += elapsed_time
                # if (
                #     self.measurement_parameters["frequency_settling_time"]
                #     > elapsed_time
                # ):
                time.sleep(self.measurement_parameters["frequency_settling_time"])
            else:
                # Wait for the settling time so that current can be adjusted
                time.sleep(self.measurement_parameters["frequency_settling_time"])

            # Measure the voltage and current (and possibly parameters on the osci)
            voltage, current, mode = self.source.read_values()

            vmax = float(self.oscilloscope.measure_vmax("CHAN2"))

            # Calculate the magnetic field using a pickup coil
            magnetic_field = (
                pf.calculate_magnetic_field_from_Vind(
                    self.global_parameters["pickup_coil_windings"],
                    self.global_parameters["pickup_coil_radius"] * 1e-3,
                    float(self.oscilloscope.measure_vmax("CHAN1")),
                    frequency * 1e3,
                )
                * 1e3
            )

            # Set the variables in the dataframe
            self.df_data.loc[i, "voltage"] = voltage
            self.df_data.loc[i, "current"] = current
            self.df_data.loc[i, "frequency"] = frequency
            self.df_data.loc[i, "magnetic_field"] = magnetic_field
            self.df_data.loc[i, "vmax"] = vmax

            # Update progress bar
            self.update_progress_bar.emit(
                "value", int((i + 1) / len(frequencies) * 100)
            )

            self.update_spectrum_signal.emit(
                self.df_data["frequency"],
                self.df_data["current"],
                self.df_data["magnetic_field"],
                self.df_data["vmax"],
            )

            # Increase iterator
            i += 1

            if self.is_killed:
                # Close the connection to the spectrometer
                self.source.output(False)
                self.source.set_voltage(5)
                self.parent.oscilloscope_thread.pause = False
                self.quit()
                return

        self.source.output(False)
        self.save_data()
        self.parent.specw_start_measurement_pushButton.setChecked(False)

        self.parent.oscilloscope_thread.pause = False

        if self.measurement_parameters["constant_magnetic_field_mode"]:
            cf.log_message(
                "Frequency scan ended with an average magnetic field adjustment time of "
                + str(round(total_adjustment_time / len(frequencies), 2))
                + " and a total measurement time of "
                + str(round(time.time() - start_time, 2))
            )
        # self.parent.setup_thread.pause = False
        # self.parent.oscilloscope_thread.pause = False

    def kill(self):
        """
        Kill thread while running
        """
        self.is_killed = True

    def save_data(self):
        """
        Function to save the measured data to file. This should probably be
        integrated into the AutotubeMeasurement class
        """

        # Define Header
        line02 = (
            "Base Capacitance:"
            + str(self.global_parameters["base_capacitance"])
            + " pF\t Coil Inductance:"
            + str(self.global_parameters["coil_inductance"])
            + " mH"
        )
        line03 = (
            "Voltage:   "
            + str(self.measurement_parameters["voltage"])
            + " V   "
            + "Current:   "
            + str(self.measurement_parameters["current_compliance"])
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
        line06 = "Frequency\t Voltage\t Current\t Magnetic Field\t Vmax_ind"
        line07 = "Hz\t V\t A\t mT\t V\n"

        header_lines = [
            line02,
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
            + ".csv"
        )
        self.df_data["magnetic_field"] = self.df_data["magnetic_field"].map(
            lambda x: "{0:.3f}".format(x)
        )

        cf.save_file(self.df_data, file_path, header_lines)

        # with open(file_path, "a") as the_file:
        #     the_file.write("\n".join(header_lines))

        # # Now write pandas dataframe to file
        # self.df_data.to_csv(file_path, index=False, mode="a", header=False, sep="\t")
