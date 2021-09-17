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


class PIDScan(QtCore.QThread):
    """
    Class thread that handles the spectrum measurement
    """

    # Define costum signals
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
    # With pyside2 https://wiki.qt.io/Qt_for_Python_Signals_and_Slots
    update_pid_graph_signal = QtCore.Signal(list, list)
    update_progress_bar = QtCore.Signal(str, float)

    def __init__(
        self,
        arduino,
        hf_source,
        oscilloscope,
        measurement_parameters,
        # setup_parameters,
        parent=None,
    ):
        super(PIDScan, self).__init__()
        # Variable to kill thread

        # Assign hardware and reset
        self.arduino = arduino
        self.arduino.init_serial_connection()
        self.hf_source = hf_source
        self.oscilloscope = oscilloscope
        self.parent = parent

        self.measurement_parameters = measurement_parameters
        # self.setup_parameters = setup_parameters

        self.global_parameters = cf.read_global_settings()

        # Connect signal to the updater from the parent class
        self.update_pid_graph_signal.connect(parent.update_pid_graph)
        self.update_progress_bar.connect(parent.progressBar.setProperty)

        # Define dataframe to store data in
        self.df_data = pd.DataFrame(columns=["time", "magnetic_field"])

        self.is_killed = False

        # If
        pid_parameters = np.array(
            self.global_parameters["pid_parameters"].split(","), dtype=float
        )

        self.pid = PID(
            pid_parameters[0],
            pid_parameters[1],
            pid_parameters[2],
            setpoint=self.measurement_parameters["magnetic_field"],
        )
        # Minimum of one volt is required by the voltcraft hf_source
        self.pid.output_limits = (1, self.measurement_parameters["voltage"])

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
        Class that does a pid tuning scan
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

        self.parent.oscilloscope_thread.pause = True

        self.hf_source.set_voltage(1)
        self.hf_source.set_current(2)
        total_adjustment_time = 0

        # Set frequency
        self.arduino.set_frequency(
            self.measurement_parameters["frequency"],
            self.measurement_parameters["autoset_capacitance"],
        )

        # Activate output only when frequency was set
        self.hf_source.output(True)

        # In constant magnetic field mode, regulate the voltage until a
        # magnetic field is reached
        start_time = time.time()
        i = 0
        a = 0
        while True:
            # Generate step-response data to tune with https://pidtuner.com/
            # Time (frequency hijacked)
            # time_it = round(time.time() - start_time, 2)
            # self.df_data.loc[i, "frequency"] = time_it

            # if i == 0:
            #     self.hf_source.output(False)
            #     voltage = 0
            # elif i == 20:
            #     voltage = 2
            #     self.hf_source.set_voltage(2)
            #     self.hf_source.output(True)
            # elif i == 30:
            #     voltage = 0
            #     self.hf_source.output(False)
            # elif i == 50:
            #     voltage = 4
            #     self.hf_source.set_voltage(4)
            #     self.hf_source.output(True)
            # elif i == 60:
            #     voltage = 0
            #     self.hf_source.output(False)
            # elif i == 70:
            #     self.save_data()
            #     print("Data saved")

            # Calculate the magnetic field using a pickup coil
            magnetic_field = (
                pf.calculate_magnetic_field_from_Vind(
                    self.global_parameters["pickup_coil_windings"],
                    self.global_parameters["pickup_coil_radius"] * 1e-3,
                    float(self.oscilloscope.measure_vmax(1)),
                    self.measurement_parameters["frequency"] * 1e3,
                )
                * 1e3
            )

            # Plot a graph (for PID tuning)
            self.df_data.loc[i, "time"] = time.time() - start_time
            # self.df_data.loc[i, "voltage"] = 1
            # self.df_data.loc[i, "current"] = 1

            self.df_data.loc[i, "magnetic_field"] = magnetic_field
            # self.df_data.loc[i, "vmax"] = 1

            self.update_pid_graph_signal.emit(
                self.df_data["time"],
                self.df_data["magnetic_field"],
                # self.df_data["vmax"],
            )

            # ask for optimum value of pid
            pid_voltage = self.pid(magnetic_field)

            # Set the voltage to that value (rounded to the accuracy of the
            # hf_source)
            self.hf_source.set_voltage(round(pid_voltage, 2))

            # Wait for a bit so that the hardware can react
            time.sleep(0.05)

            # If the magnetic field and the setpoint deviate by less than 0.02,
            # increase a else set it back to zero
            if math.isclose(self.pid.setpoint, magnetic_field, rel_tol=0.03):
                a += 1
            else:
                a = 0

            # Only break if this is the case for several iterations (5 are
            # needed to obtain a stable operation)
            if a >= 5:
                break

            if self.is_killed:
                # Close the connection to the spectrometer
                self.hf_source.output(False)
                self.hf_source.set_voltage(5)
                self.parent.oscilloscope_thread.pause = False
                self.quit()
                return

            i += 1

        total_adjustment_time = time.time() - start_time

        # Update progress bar
        # self.update_progress_bar.emit("value", int((i + 1) / len(frequencies) * 100))

        self.hf_source.output(False)
        # self.save_data()
        self.parent.pidw_start_measurement_pushButton.setChecked(False)

        self.parent.oscilloscope_thread.pause = False

        cf.log_message("PID adjustment took " + str(round(total_adjustment_time, 2)))
        # self.parent.setup_thread.pause = False
        # self.parent.oscilloscope_thread.pause = False

    def kill(self):
        """
        Kill thread while running
        """
        self.is_killed = True

    # def save_data(self):
    #     """
    #     Function to save the measured data to file. This should probably be
    #     integrated into the AutotubeMeasurement class
    #     """

    #     # Define Header
    #     line02 = (
    #         "Base Capacitance:"
    #         + str(self.global_parameters["base_capacitance"])
    #         + " pF\t Coil Inductance:"
    #         + str(self.global_parameters["coil_inductance"])
    #         + " mH"
    #     )
    #     line03 = (
    #         "Voltage:   "
    #         + str(self.measurement_parameters["voltage"])
    #         + " V   "
    #         + "Current:   "
    #         + str(self.measurement_parameters["current_compliance"])
    #     )
    #     line04 = (
    #         "Min. Frequency:   "
    #         + str(self.measurement_parameters["minimum_frequency"])
    #         + " kHz \t"
    #         + "Max. Frequency:   "
    #         + str(self.measurement_parameters["maximum_frequency"])
    #         + " kHz \t"
    #         + "Frequency Step:   "
    #         + str(self.measurement_parameters["frequency_step"])
    #         + " kHz \t"
    #     )
    #     line05 = "### Measurement data ###"
    #     line06 = "Frequency\t Voltage\t Current\t Magnetic Field\t Vmax_ind"
    #     line07 = "Hz\t V\t A\t mT\t V\n"

    #     header_lines = [
    #         line02,
    #         line03,
    #         line04,
    #         line05,
    #         line06,
    #         line07,
    #     ]

    #     # Write header lines to file
    #     file_path = (
    #         self.setup_parameters["folder_path"]
    #         + dt.date.today().strftime("%Y-%m-%d_")
    #         + self.setup_parameters["batch_name"]
    #         + "_d"
    #         + str(self.setup_parameters["device_number"])
    #         + ".csv"
    #     )
    #     cf.save_file(self.df_data, file_path, header_lines)

    # with open(file_path, "a") as the_file:
    #     the_file.write("\n".join(header_lines))

    # # Now write pandas dataframe to file
    # self.df_data.to_csv(file_path, index=False, mode="a", header=False, sep="\t")
