from tkinter import W
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
from scipy.ndimage.filters import uniform_filter1d


class LTScan(QtCore.QThread):
    """
    Class thread that handles the spectrum measurement
    """

    # Define costum signals
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
    # With pyside2 https://wiki.qt.io/Qt_for_Python_Signals_and_Slots
    update_lt_scan_plot = QtCore.Signal(list, list, list)
    update_progress_bar = QtCore.Signal(str, float)
    pause_thread_lt_scan = QtCore.Signal(str)

    def __init__(
        self,
        arduino,
        source,
        oscilloscope,
        measurement_parameters,
        setup_parameters,
        parent=None,
    ):
        super(LTScan, self).__init__()
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
        self.update_lt_scan_plot.connect(parent.update_lt_plot)
        self.update_progress_bar.connect(parent.progressBar.setProperty)
        self.pause_thread_lt_scan.connect(parent.pause_lt_measurement)

        # Define dataframe to store data in
        self.df_data = pd.DataFrame(
            columns=["time", "current", "me_voltage", "hf_field"]
        )

        self.is_killed = False
        self.last_file_path = ""

        self.source.set_current(2, channel=2)
        if measurement_parameters["constant_magnetic_field_mode"]:
            pid_parameters = np.array(
                self.global_parameters["pid_parameters"].split(","), dtype=float
            )
            self.source.start_constant_magnetic_field_mode(
                pid_parameters,
                self.measurement_parameters["hf_voltage"],
                self.measurement_parameters["voltage_compliance"],
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
        Class that does an hf field sweep
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

        # Init data saving
        self.save_data_init()

        # Measure time elapsed
        start_time = time.time()

        # self.parent.oscilloscope_thread.pause = True
        # self.parent.oscilloscope_thread.pause = True
        self.source.set_voltage(20, channel=1)
        self.source.set_magnetic_field(
            self.measurement_parameters["dc_magnetic_field"], channel=1
        )
        self.source.output(True, channel=1)

        # # Set voltage and current (they shall remain constant over the entire sweep)
        # self.hf_source.set_voltage(self.measurement_parameters["voltage"])
        # if not self.measurement_parameters["constant_magnetic_field_mode"]:
        #     self.hf_source.set_current(
        #         self.measurement_parameters["current_compliance"]
        #     )

        # Set frequency
        self.arduino.set_frequency(
            self.measurement_parameters["frequency"],
            self.measurement_parameters["autoset_capacitance"],
        )

        # Activate output (necessary to adjust field)
        self.source.output(True, channel=2)
        if not self.measurement_parameters["constant_magnetic_field_mode"]:
            self.source.set_voltage(
                self.measurement_parameters["hf_voltage"], channel=2
            )
        else:
            # Adjust the magnetic field
            pid_voltage, elapsed_time = self.source.adjust_magnetic_field(
                self.global_parameters["pickup_coil_windings"],
                self.global_parameters["pickup_coil_radius"],
                self.measurement_parameters["frequency"],
                self.oscilloscope,
                break_if_too_long=False,
                channel=2,
            )

            # Return total adjustment time to let user know how long it took
            # total_adjustment_time += elapsed_time

        self.source.output(True, channel=1)
        time.sleep(1)

        # # If constant magnetic field was chosen, adjust it
        # if self.measurement_parameters["constant_magnetic_field_mode"]:
        #     self.hf_source.adjust_magnetic_field(
        #         self.global_parameters["pickup_coil_windings"],
        #         self.global_parameters["pickup_coil_radius"],
        #         self.measurement_parameters["frequency"],
        #         self.oscilloscope,
        #         break_if_too_long=True,
        #     )

        # Counter to iterate over array where data is stored
        time_step_list = np.arange(
            0,
            self.measurement_parameters["total_time"] + 1,
            self.measurement_parameters["time_step"],
        )

        self.osci_data = pd.DataFrame(
            columns=np.concatenate(
                (
                    np.array(["cal_time", "cal_field", "cal"]),
                    np.concatenate(
                        np.stack(
                            (
                                [s + "_time" for s in time_step_list.astype(str)],
                                [s + "_field" for s in time_step_list.astype(str)],
                                time_step_list.astype(str),
                            ),
                            axis=-1,
                        )
                    ),
                ),
            )
        )

        # First do one calibration field measurement (to subtract in the end)

        # self.oscilloscope.auto_scale(1)
        (
            self.osci_data["cal_time"],
            osci_data_raw,
        ) = self.oscilloscope.get_data("CHAN1")
        (
            time_data,
            self.osci_data["cal_field"],
        ) = self.oscilloscope.get_data("CHAN2")
        # Function to do moving average

        self.osci_data["cal"] = uniform_filter1d(osci_data_raw, 20)

        self.source.output(False, channel=2)
        # After calibration, tell user to insert OLED
        self.pause = "True"
        self.pause_thread_lt_scan.emit("on")

        while self.pause == "True":
            time.sleep(0.1)
            if self.pause == "break":
                # Take the time at the beginning to measure the length of the entire
                # measurement
                absolute_starting_time = time.time()
                break
            elif self.pause == "return":
                return

        self.source.output(True, channel=2)

        initial_time = time.time()
        i = 0

        while (time.time() - initial_time) <= (
            self.measurement_parameters["total_time"] + 0.1
        ):
            if (time.time() - initial_time) >= time_step_list[i]:
                # Readjust magnetic field to initial value
                """
                if self.measurement_parameters["constant_magnetic_field_mode"]:
                    # Adjust the magnetic field
                    pid_voltage, elapsed_time = self.source.adjust_magnetic_field(
                        self.global_parameters["pickup_coil_windings"],
                        self.global_parameters["pickup_coil_radius"],
                        self.measurement_parameters["frequency"],
                        self.oscilloscope,
                        break_if_too_long=True,
                        channel=2,
                    )
                """

                self.df_data.loc[i, "time"] = time.time() - initial_time

                # Measure the voltage and current (and possibly parameters on the osci)
                # me_voltage = float(self.oscilloscope.measure_vmax(channel=1))
                # self.oscilloscope.auto_scale(1)
                (
                    self.osci_data[str(time_step_list[i]) + "_time"],
                    raw_field,
                ) = self.oscilloscope.get_data("CHAN1")
                self.osci_data[str(time_step_list[i]) + "_field"] = (
                    pf.calculate_magnetic_field_from_Vind(
                        self.global_parameters["pickup_coil_windings"],
                        self.global_parameters["pickup_coil_radius"] * 1e-3,
                        raw_field,
                        float(self.measurement_parameters["frequency"]) * 1e3,
                    )
                    * 1e3
                )
                (
                    time_data,
                    osci_data_raw,
                ) = self.oscilloscope.get_data("CHAN2")

                self.osci_data[str(time_step_list[i])] = uniform_filter1d(
                    osci_data_raw, 20
                )

                me_voltage = np.max(
                    self.osci_data[str(time_step_list[i])] - self.osci_data["cal"]
                )

                # Set the variables in the dataframe
                (
                    voltage,
                    self.df_data.loc[i, "current"],
                ) = self.source.read_values(channel=2)

                self.df_data.loc[i, "me_voltage"] = me_voltage
                self.df_data.loc[i, "hf_field"] = np.max(
                    self.osci_data[str(time_step_list[i]) + "_field"]
                )

                # Update progress bar
                self.update_progress_bar.emit(
                    "value", int((i + 1) / len(time_step_list) * 100)
                )

                self.update_lt_scan_plot.emit(
                    self.df_data["time"],
                    self.df_data["me_voltage"],
                    self.df_data["hf_field"],
                )
                self.save_data_individually()

                # Increase iterator
                i += 1

            else:
                if self.is_killed:
                    # Close the connection to the spectrometer
                    self.source.output(False, channel=2)
                    self.source.set_voltage(1, channel=2)
                    self.source.output(False, channel=1)
                    self.arduino.set_frequency(1000, True)
                    self.save_data_osci()
                    # self.parent.oscilloscope_thread.pause = False
                    self.quit()
                    return

                time.sleep(0.1)

        self.source.output(False, channel=2)
        self.source.output(False, channel=1)
        self.save_data_osci()
        self.parent.ltw_start_measurement_pushButton.setChecked(False)
        self.arduino.set_frequency(1000, True)

        # self.parent.oscilloscope_thread.pause = False

    def kill(self):
        """
        Kill thread while running
        """
        self.is_killed = True

    def save_data_init(self):
        """
        Function to save the measured data to file. This should probably be
        integrated into the AutotubeMeasurement class
        """
        line02 = (
            "Base Capacitance: "
            + str(self.global_parameters["base_capacitance"])
            + " pF\t Coil Inductance: "
            + str(self.global_parameters["coil_inductance"])
            + " mH\t Device Size: "
            + str(self.setup_parameters["device_size"])
            + " mm"
        )
        line03 = (
            "Maximum Voltage:   "
            + str(self.measurement_parameters["voltage_compliance"])
            + " V   "
        )
        if self.measurement_parameters["constant_magnetic_field_mode"]:
            line03 += (
                "Constant HF Magnetic Field:   "
                + str(self.measurement_parameters["hf_voltage"])
                + " V"
            )
        else:
            line03 += (
                "DC Magnetic Field Bias:   "
                + str(self.measurement_parameters["dc_magnetic_field"])
                + " A"
            )

        line04 = (
            "Frequency: " + str(self.measurement_parameters["frequency"]) + " kHz \t"
            "Measurement Interval:   "
            + str(self.measurement_parameters["time_step"])
            + " s \t"
            + "Total Measurement Time:   "
            + str(self.measurement_parameters["total_time"])
            + " s \t"
        )
        line05 = "### Measurement data ###"
        line06 = (
            "Time\t Current\t ME Voltage\t HF Field (pickup not necessarily centred)"
        )
        line07 = "s\t A\t V\t V (a.u.)\n"

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
            + "_lt"
            + ".csv"
        )

        self.df_data["time"] = self.df_data["time"].map(lambda x: "{0:.3f}".format(x))

        self.last_file_path = cf.save_file(
            self.df_data, file_path, header_lines, return_file_path=True
        )

    def save_data_osci(self):
        line02 = (
            "Base Capacitance: "
            + str(self.global_parameters["base_capacitance"])
            + " pF\t Coil Inductance: "
            + str(self.global_parameters["coil_inductance"])
            + " mH\t Device Size: "
            + str(self.setup_parameters["device_size"])
            + " mm"
        )
        line03 = (
            "Maximum Voltage:   "
            + str(self.measurement_parameters["voltage_compliance"])
            + " V   "
        )
        if self.measurement_parameters["constant_magnetic_field_mode"]:
            line03 += (
                "Constant HF Magnetic Field:   "
                + str(self.measurement_parameters["hf_voltage"])
                + " V"
            )
        else:
            line03 += (
                "DC Magnetic Field Bias:   "
                + str(self.measurement_parameters["dc_magnetic_field"])
                + " A"
            )

        line04 = (
            "Frequency: " + str(self.measurement_parameters["frequency"]) + " kHz \t"
            "Measurement Interval:   "
            + str(self.measurement_parameters["time_step"])
            + " s \t"
            + "Total Measurement Time:   "
            + str(self.measurement_parameters["total_time"])
            + " s \t"
        )
        line05 = "### Measurement data ###"

        header_lines_full = [
            line02,
            line03,
            line04,
            line05,
        ]
        file_path_full = (
            self.setup_parameters["folder_path"]
            + dt.date.today().strftime("%Y-%m-%d_")
            + self.setup_parameters["batch_name"]
            + "_d"
            + str(self.setup_parameters["device_number"])
            + "_lt-osci"
            + ".csv"
        )
        cf.save_file(
            self.osci_data, file_path_full, header_lines_full, save_header=True
        )

    def save_data_individually(self):
        """
        Function to save the measured data line by line to file.
        """

        # self.df_data["time"] = self.df_data["time"].map(lambda x: "{0:.3f}".format(x))
        # self.df_data["hf_field"] = self.df_data["hf_field"].map(
            # lambda x: "{0:.3f}".format(x)
        # )
        # self.df_data["me_voltage"] = self.df_data["me_voltage"].map(
            # lambda x: "{0:.4f}".format(x)
        # )
        # Append to file
        self.df_data.iloc[-1:].to_csv(
            self.last_file_path,
            index=False,
            header=False,
            mode="a",  # append data to csv file
            sep="\t",
        )

        # with open(file_path, "a") as the_file:
        #     the_file.write("\n".join(header_lines))

        # # Now write pandas dataframe to file
        # self.df_data.to_csv(file_path, index=False, mode="a", header=False, sep="\t")
