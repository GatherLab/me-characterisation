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


class PulsingSweep(QtCore.QThread):
    """
    Class thread that handles the spectrum measurement
    """

    # Define costum signals
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
    # With pyside2 https://wiki.qt.io/Qt_for_Python_Signals_and_Slots
    update_time_position_signal = QtCore.Signal(float)
    update_progress_bar = QtCore.Signal(str, float)

    def __init__(
        self,
        arduino,
        hf_source,
        dc_source,
        oscilloscope,
        pulsing_data,
        pulsing_sweep_parameters,
        parent=None,
    ):
        super(PulsingSweep, self).__init__()
        # Variable to kill thread

        # Assign hardware and reset
        self.arduino = arduino
        self.arduino.init_serial_connection()
        self.hf_source = hf_source
        self.dc_source = dc_source
        self.oscilloscope = oscilloscope
        self.parent = parent

        self.pulsing_data = pulsing_data
        # make sure indexes pair with number of rows
        self.pulsing_data = self.pulsing_data.reset_index()
        self.pulsing_sweep_parameters = pulsing_sweep_parameters

        self.global_parameters = cf.read_global_settings()

        # Connect signal to the updater from the parent class
        self.update_time_position_signal.connect(parent.update_time_position)
        self.update_progress_bar.connect(parent.progressBar.setProperty)

        self.is_killed = False

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
        self.hf_source.set_current(2)

        # Activation can not be done via the HF output since it is simply too
        # slow
        self.dc_source.output(True)
        self.hf_source.output(True)
        time.sleep(1)
        if self.pulsing_sweep_parameters["constant_mode"]:
            # Takes about 0.2 s
            self.dc_source.set_magnetic_field(
                float(self.pulsing_sweep_parameters["dc_field"])
            )

            # Takes about 20 ms
            self.hf_source.set_voltage(
                float(self.pulsing_sweep_parameters["hf_voltage"])
            )

            # Takes about 0.5s
            self.arduino.set_frequency(
                float(self.pulsing_sweep_parameters["frequency"]),
                True,
            )

        start_time = time.time()
        time_step = 0.01
        for index, row in self.pulsing_data.iterrows():
            if row["signal"] == "ON":

                # Takes about 5ms
                self.arduino.trigger_frequency_generation(1)
                i = 0

                while (time.time() - start_time) < float(row["time"]):

                    if self.is_killed:
                        # Close the connection to the spectrometer
                        self.hf_source.output(False)
                        self.hf_source.set_voltage(1)
                        self.dc_source.output(False)
                        self.arduino.set_frequency(1000, True)
                        # self.parent.oscilloscope_thread.pause = False
                        self.quit()
                        return

                    time.sleep(time_step)

                    # Update graph with current position in time
                    if i % 5 == 0:
                        self.update_time_position_signal.emit(time.time() - start_time)
                    # print(str(time.time() - start_time) + " ON")
                    i += 1

            elif row["signal"] == "OFF":
                self.arduino.trigger_frequency_generation(0)
                set_bool = True

                i = 0
                while (time.time() - start_time) < float(row["time"]):

                    # Make sure the adjustment of the sources is preparing
                    # already the next on cycle
                    ref = time.time()
                    if not self.pulsing_sweep_parameters["constant_mode"]:
                        if (time.time() - start_time) > (
                            float(row["time"]) - 1
                        ) and set_bool:
                            try:
                                # Takes about 0.2 s
                                self.dc_source.set_magnetic_field(
                                    float(self.pulsing_data.iloc[index + 1]["dc_field"])
                                )

                                # Takes about 20 ms
                                self.hf_source.set_voltage(
                                    float(self.pulsing_data.iloc[index + 1]["hf_field"])
                                )

                                # Takes about 0.5s
                                self.arduino.set_frequency(
                                    float(
                                        self.pulsing_data.iloc[index + 1]["frequency"]
                                    ),
                                    True,
                                )

                                set_bool = False
                            except:
                                cf.log_message("Last off cycle reached")

                            set_bool = False
                            cf.log_message(
                                "Setting dc and hf field source and frequency took "
                                + str(time.time() - ref)
                                + " s"
                            )

                    if self.is_killed:
                        # Close the connection to the spectrometer
                        self.hf_source.output(False)
                        self.hf_source.set_voltage(1)
                        self.dc_source.output(False)
                        self.arduino.set_frequency(1000, True)
                        # self.parent.oscilloscope_thread.pause = False
                        self.quit()
                        return

                    time.sleep(time_step)

                    if i % 5 == 0:
                        self.update_time_position_signal.emit(time.time() - start_time)
                    # print(str(time.time() - start_time) + " ON")
                    i += 1
            else:
                cf.log_message(
                    "The signal command in row "
                    + str(index)
                    + " is not a valid command!"
                )
            print(time.time() - start_time)

        self.hf_source.output(False)
        self.dc_source.output(False)
        self.arduino.set_frequency(1000, True)

        self.parent.pulsew_start_measurement_pushButton.setChecked(False)

        # self.parent.oscilloscope_thread.pause = False

    def kill(self):
        """
        Kill thread while running
        """
        self.is_killed = True
