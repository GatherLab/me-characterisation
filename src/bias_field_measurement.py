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


class BiasScan(QtCore.QThread):
    """
    Class thread that handles the spectrum measurement
    """

    # Define costum signals
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
    # With pyside2 https://wiki.qt.io/Qt_for_Python_Signals_and_Slots
    update_bias_plot_signal = QtCore.Signal(list, list, list, list)
    update_progress_bar = QtCore.Signal(str, float)

    def __init__(
        self,
        arduino,
        hf_source,
        dc_source,
        oscilloscope,
        measurement_parameters,
        setup_parameters,
        parent=None,
    ):
        super(BiasScan, self).__init__()
        # Variable to kill thread

        # Assign hardware and reset
        self.arduino = arduino
        self.arduino.init_serial_connection()
        self.hf_source = hf_source
        self.dc_source = dc_source
        self.oscilloscope = oscilloscope
        self.parent = parent

        self.measurement_parameters = measurement_parameters
        self.setup_parameters = setup_parameters

        self.global_parameters = cf.read_global_settings()

        # Connect signal to the updater from the parent class
        self.update_bias_plot_signal.connect(parent.update_bias_plot)
        self.update_progress_bar.connect(parent.progressBar.setProperty)

        # Define dataframe to store data in
        self.df_data = pd.DataFrame(
            columns=["current", "bias_field", "me_voltage", "hf_magnetic_field"]
        )

        self.is_killed = False

        # If
        if measurement_parameters["constant_magnetic_field_mode"]:
            pid_parameters = np.array(
                self.global_parameters["pid_parameters"].split(","), dtype=float
            )
            self.hf_source.start_constant_magnetic_field_mode(
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
        Class that does a dc bias field sweep
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
        self.hf_source.set_voltage(self.measurement_parameters["voltage"])
        self.hf_source.set_current(2)
        if not self.measurement_parameters["constant_magnetic_field_mode"]:
            self.hf_source.set_current(
                self.measurement_parameters["current_compliance"]
            )

        # Set frequency
        self.arduino.set_frequency(
            self.measurement_parameters["frequency"],
            self.measurement_parameters["autoset_capacitance"],
        )

        # Activate output (necessary to adjust field)
        self.hf_source.output(True)
        time.sleep(1)

        # If constant magnetic field was chosen, adjust it
        if self.measurement_parameters["constant_magnetic_field_mode"]:
            self.hf_source.adjust_magnetic_field(
                self.global_parameters["pickup_coil_windings"],
                self.global_parameters["pickup_coil_radius"],
                self.measurement_parameters["frequency"],
                self.oscilloscope,
                break_if_too_long=True,
            )

        # Counter to iterate over array where data is stored
        i = 0

        # Sweep over all frequencies
        dc_field_list = np.arange(
            self.measurement_parameters["minimum_dc_field"],
            self.measurement_parameters["maximum_dc_field"]
            + self.measurement_parameters["dc_field_step"],
            self.measurement_parameters["dc_field_step"],
        )

        self.dc_source.output(True)

        time.sleep(1)

        for dc_field in dc_field_list:
            # for frequency in self.df_data["frequency"]:
            # cf.log_message("Frequency set to " + str(frequency) + " kHz")

            # Set DC Field
            self.dc_source.set_magnetic_field(dc_field)

            # Measure the voltage and current (and possibly parameters on the osci)
            me_voltage = float(self.oscilloscope.measure_vmax(channel="CHAN2"))

            # Calculate the magnetic field using a pickup coil
            magnetic_field = (
                pf.calculate_magnetic_field_from_Vind(
                    self.global_parameters["pickup_coil_windings"],
                    self.global_parameters["pickup_coil_radius"] * 1e-3,
                    float(self.oscilloscope.measure_vmax("CHAN1")),
                    self.measurement_parameters["frequency"] * 1e3,
                )
                * 1e3
            )

            # Set the variables in the dataframe
            (
                source_voltage,
                self.df_data.loc[i, "current"],
            ) = self.dc_source.read_values()
            self.df_data.loc[i, "bias_field"] = dc_field
            self.df_data.loc[i, "me_voltage"] = me_voltage
            # Directly in mW/mm^2
            # in mT
            self.df_data.loc[i, "hf_magnetic_field"] = magnetic_field

            # Update progress bar
            self.update_progress_bar.emit(
                "value", int((i + 1) / len(dc_field_list) * 100)
            )

            self.update_bias_plot_signal.emit(
                self.df_data["current"],
                self.df_data["bias_field"],
                self.df_data["me_voltage"],
                self.df_data["hf_magnetic_field"],
            )

            if self.is_killed:
                # Close the connection to the spectrometer
                self.hf_source.output(False)
                self.hf_source.set_voltage(1)
                self.dc_source.output(False)
                self.parent.oscilloscope_thread.pause = False
                self.quit()
                return

            # Increase iterator
            i += 1

            time.sleep(self.measurement_parameters["bias_field_settling_time"])

        self.hf_source.output(False)
        self.dc_source.output(False)
        self.save_data()
        self.parent.bw_start_measurement_pushButton.setChecked(False)

        self.parent.oscilloscope_thread.pause = False

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

        # Calculate optimium bias field (field with maximum response)
        optimum_bias_list = self.df_data.loc[
            self.df_data.me_voltage == self.df_data.me_voltage.max()
        ]

        optimum_bias_field = optimum_bias_list["bias_field"].iloc[
            int(len(optimum_bias_list) / 2)
        ]
        optimum_bias_current = optimum_bias_list["current"].iloc[
            int(len(optimum_bias_list) / 2)
        ]

        # Define Header
        line01 = (
            "Optimum Bias Field:   "
            + str(optimum_bias_field)
            + " mT\t At a Current of:   "
            + str(optimum_bias_current)
            + " A"
        )
        print(line01)

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
            + str(self.measurement_parameters["voltage"])
            + " V   "
        )
        if self.measurement_parameters["constant_magnetic_field_mode"]:
            line03 += (
                "Constant HF Magnetic Field:   "
                + str(self.measurement_parameters["current_compliance"])
                + " mT"
            )
        else:
            line03 += (
                "Constant Current:   "
                + str(self.measurement_parameters["current_compliance"])
                + " A"
            )

        line04 = (
            "Frequency: " + str(self.measurement_parameters["frequency"]) + " kHz \t"
            "Min. Bias Field:   "
            + str(self.measurement_parameters["minimum_dc_field"])
            + " kHz \t"
            + "Max. Bias Field:   "
            + str(self.measurement_parameters["maximum_dc_field"])
            + " kHz \t"
            + "Bias Field Step:   "
            + str(self.measurement_parameters["dc_field_step"])
            + " kHz \t"
        )
        line05 = "### Measurement data ###"
        line06 = "Current\t Bias Field\t ME Voltage\t Magnetic Field"
        line07 = "A\t mT\t V\t mT\n"

        header_lines = [
            line01,
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
            + "_bias"
            + ".csv"
        )
        self.df_data["hf_magnetic_field"] = self.df_data["hf_magnetic_field"].map(
            lambda x: "{0:.3f}".format(x)
        )

        cf.save_file(self.df_data, file_path, header_lines)

        # with open(file_path, "a") as the_file:
        #     the_file.write("\n".join(header_lines))

        # # Now write pandas dataframe to file
        # self.df_data.to_csv(file_path, index=False, mode="a", header=False, sep="\t")
