from UI_main_window import Ui_MainWindow
from settings import Settings
from loading_window import LoadingWindow

from frequency_measurement import FrequencyScan
from capacitance_measurement import CapacitanceScan
from setup import SetupThread
from oscilloscope_measurement import OscilloscopeThread

from hardware import RigolOscilloscope, VoltcraftSource, Arduino

import core_functions as cf

from PySide2 import QtCore, QtGui, QtWidgets

import time
import os
import json
import sys
import functools
from datetime import date
import datetime as dt
import logging
from logging.handlers import RotatingFileHandler

import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import math
import matplotlib as mpl

import webbrowser


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    This class contains the logic of the program and is explicitly seperated
    from the UI classes. However, it is a child class of Ui_MainWindow.
    """

    def __init__(self):
        """
        Initialise instance
        """
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # -------------------------------------------------------------------- #
        # -------------------------- Hardware Setup -------------------------- #
        # -------------------------------------------------------------------- #
        self.t = 0

        # Execute initialisation thread
        oscilloscope_address = "USB0::0x1AB1::0x0517::DS1ZE223304729::INSTR"
        # source_address = "ASRL4::INSTR"
        # arduino_address = "ASRL6::INSTR"
        loading_window = LoadingWindow(self)

        # Execute loading dialog
        loading_window.exec()

        # -------------------------------------------------------------------- #
        # ------------------------------ General ----------------------------- #
        # -------------------------------------------------------------------- #

        # Update statusbar
        cf.log_message("Initialising Program")
        self.tabWidget.currentChanged.connect(self.changed_tab_widget)

        # Hide by default and only show if a process is running
        self.progressBar.hide()

        # -------------------------------------------------------------------- #
        # --------------------------- Menubar -------------------------------- #
        # -------------------------------------------------------------------- #
        self.actionOptions.triggered.connect(self.show_settings)

        # Open the documentation in the browser (maybe in the future directly
        # open the readme file in the folder but currently this is so much
        # easier and prettier)
        self.actionDocumentation.triggered.connect(
            lambda: webbrowser.open(
                "https://github.com/GatherLab/me-measurement/blob/main/README.md"
            )
        )

        self.actionOpen_Log.triggered.connect(lambda: self.open_file("./usr/log.out"))

        # -------------------------------------------------------------------- #
        # --------------------------- Setup Widget --------------------------- #
        # -------------------------------------------------------------------- #
        self.sw_browse_pushButton.clicked.connect(self.browse_folder)

        # Setup and start setup thread that continuously reads out the voltage
        # and current of the source as well as the frequency of the Arduino
        self.setup_thread = SetupThread(self.source, self.arduino, self)
        self.setup_thread.start()

        self.sw_voltage_spinBox.valueChanged.connect(self.voltage_changed)
        self.sw_current_spinBox.valueChanged.connect(self.current_changed)
        self.sw_frequency_spinBox.valueChanged.connect(self.frequency_changed)
        self.sw_capacitance_spinBox.valueChanged.connect(self.capacity_changed)

        self.sw_source_output_pushButton.clicked.connect(self.toggle_source_output)
        self.sw_source_output_pushButton.setCheckable(True)

        # -------------------------------------------------------------------- #
        # -------------------- Frequency Sweep Widget ------------------------ #
        # -------------------------------------------------------------------- #
        self.specw_start_measurement_pushButton.clicked.connect(
            self.start_frequency_sweep
        )
        self.specw_start_measurement_pushButton.setCheckable(True)

        # -------------------------------------------------------------------- #
        # ------------------ Capacitance Sweep Widget ------------------------ #
        # -------------------------------------------------------------------- #
        self.capw_start_measurement_pushButton.clicked.connect(
            self.start_capacitance_sweep
        )
        self.capw_start_measurement_pushButton.setCheckable(True)

        # -------------------------------------------------------------------- #
        # ----------------------- Osciloscope Widget ------------------------- #
        # -------------------------------------------------------------------- #
        self.oscilloscope_thread = OscilloscopeThread(self.oscilloscope, parent=self)
        self.oscilloscope_thread.start()

        self.ow_stop_pushButton.clicked.connect(self.stop_osci)
        self.ow_auto_scale_pushButton.clicked.connect(self.auto_scale_osci)
        self.ow_start_measurement_pushButton.clicked.connect(self.save_osci)

        # -------------------------------------------------------------------- #
        # --------------------- Set Standard Parameters ---------------------- #
        # -------------------------------------------------------------------- #

        # Set standard parameters for setup
        self.sw_frequency_spinBox.setMinimum(8)
        self.sw_frequency_spinBox.setMaximum(150000)
        self.sw_frequency_spinBox.setKeyboardTracking(False)
        self.sw_frequency_spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.sw_frequency_spinBox.setValue(100)

        self.sw_capacitance_spinBox.setMinimum(0)
        self.sw_capacitance_spinBox.setMaximum(20000)
        self.sw_capacitance_spinBox.setKeyboardTracking(False)
        self.sw_capacitance_spinBox.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons
        )
        self.sw_capacitance_spinBox.setValue(3000)

        self.sw_voltage_spinBox.setMinimum(0)
        self.sw_voltage_spinBox.setMaximum(33)
        self.sw_voltage_spinBox.setKeyboardTracking(False)
        self.sw_voltage_spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.sw_voltage_spinBox.setValue(5)

        self.sw_current_spinBox.setMinimum(0)
        self.sw_current_spinBox.setMaximum(12)
        self.sw_current_spinBox.setKeyboardTracking(False)
        self.sw_current_spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.sw_current_spinBox.setValue(1)

        # Set standard parameters for spectral measurement
        self.specw_voltage_spinBox.setMinimum(0)
        self.specw_voltage_spinBox.setMaximum(33)
        self.specw_voltage_spinBox.setValue(8)

        self.specw_current_spinBox.setMinimum(0)
        self.specw_current_spinBox.setMaximum(12)
        self.specw_current_spinBox.setValue(0.3)

        self.specw_minimum_frequency_spinBox.setMinimum(8)
        self.specw_minimum_frequency_spinBox.setMaximum(150000)
        self.specw_minimum_frequency_spinBox.setValue(180)

        self.specw_maximum_frequency_spinBox.setMinimum(8)
        self.specw_maximum_frequency_spinBox.setMaximum(150000)
        self.specw_maximum_frequency_spinBox.setValue(320)

        self.specw_frequency_step_spinBox.setMinimum(0.05)
        self.specw_frequency_step_spinBox.setMaximum(1000)
        self.specw_frequency_step_spinBox.setValue(1)

        self.specw_frequency_settling_time_spinBox.setMinimum(0.01)
        self.specw_frequency_settling_time_spinBox.setMaximum(10)
        self.specw_frequency_settling_time_spinBox.setValue(1)

        # Set standard parameters for capacitance measurement
        self.capw_voltage_spinBox.setMinimum(0)
        self.capw_voltage_spinBox.setMaximum(33)
        self.capw_voltage_spinBox.setValue(3)

        self.capw_current_spinBox.setMinimum(0)
        self.capw_current_spinBox.setMaximum(12)
        self.capw_current_spinBox.setValue(0.3)

        self.capw_minimum_frequency_spinBox.setMinimum(8)
        self.capw_minimum_frequency_spinBox.setMaximum(150000)
        self.capw_minimum_frequency_spinBox.setValue(180)

        self.capw_maximum_frequency_spinBox.setMinimum(8)
        self.capw_maximum_frequency_spinBox.setMaximum(150000)
        self.capw_maximum_frequency_spinBox.setValue(310)

        self.capw_frequency_step_spinBox.setMinimum(0.05)
        self.capw_frequency_step_spinBox.setMaximum(1000)
        self.capw_frequency_step_spinBox.setValue(1)

        self.capw_minimum_capacitance_spinBox.setMinimum(0)
        self.capw_minimum_capacitance_spinBox.setMaximum(50000)
        self.capw_minimum_capacitance_spinBox.setValue(3300)

        self.capw_maximum_capacitance_spinBox.setMinimum(0)
        self.capw_maximum_capacitance_spinBox.setMaximum(50000)
        self.capw_maximum_capacitance_spinBox.setValue(4000)

        self.capw_frequency_margin_spinBox.setMinimum(0)
        self.capw_frequency_margin_spinBox.setMaximum(1000)
        self.capw_frequency_margin_spinBox.setValue(15)

        self.capw_frequency_settling_time_spinBox.setMinimum(0.01)
        self.capw_frequency_settling_time_spinBox.setMaximum(10)
        self.capw_frequency_settling_time_spinBox.setValue(0.5)

    # -------------------------------------------------------------------- #
    # ------------------------- Global Functions ------------------------- #
    # -------------------------------------------------------------------- #
    def browse_folder(self):
        """
        Open file dialog to browse through directories
        """
        global_variables = cf.read_global_settings()

        self.global_path = QtWidgets.QFileDialog.getExistingDirectory(
            QtWidgets.QFileDialog(),
            "Select a Folder",
            global_variables["default_saving_path"],
            QtWidgets.QFileDialog.ShowDirsOnly,
        )
        print(self.global_path)
        # file_dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)

        # if file_dialog1.exec():
        #     # Set global path to selected path
        #     self.global_path = file_dialog1.selectedFiles()

        #     # Set the according line edit
        self.sw_folder_path_lineEdit.setText(self.global_path + "/")

    def show_settings(self):
        """
        Shows the settings
        """
        self.settings_window = Settings(self)
        # ui = Ui_Settings()
        # ui.setupUi(self.settings_window, parent=self)

        p = (
            self.frameGeometry().center()
            - QtCore.QRect(QtCore.QPoint(), self.settings_window.sizeHint()).center()
        )

        self.settings_window.move(p)

        # self.settings_window.show()

        result = self.settings_window.exec()

    @QtCore.Slot(RigolOscilloscope)
    def init_oscilloscope(self, oscilloscope_object):
        """
        Inits oscilloscope
        """
        self.oscilloscope = oscilloscope_object

    @QtCore.Slot(VoltcraftSource)
    def init_source(self, source_object):
        """
        Receives a source object from the init thread
        """
        self.source = source_object

    @QtCore.Slot(Arduino)
    def init_arduino(self, arduino_object):
        """
        Receives an arduino object from the init thread
        """
        self.arduino = arduino_object

    def open_file(self, path):
        """
        Opens a file on the machine with the standard program
        https://stackoverflow.com/questions/6045679/open-file-with-pyqt
        """
        if sys.platform.startswith("linux"):
            subprocess.call(["xdg-open", path])
        else:
            os.startfile(path)

    def closeEvent(self, event):
        """
        Function that shall allow for save closing of the program
        """

        cf.log_message("Program closed")

        # Kill threads here
        self.setup_thread.kill()
        self.oscilloscope_measurement.kill()

        # Kill Osci
        try:
            self.oscilloscope.close()
        except Exception as e:
            cf.log_message("Oscilloscope thread could not be killed")
            cf.log_message(e)

        # Kill Source
        try:
            self.source.close()
        except Exception as e:
            cf.log_message("I am not yet sure how to close the Rigol source correctly")
            cf.log_message(e)

        # Kill arduino connection
        try:
            self.arduino.close()
        except Exception as e:
            cf.log_message("Arduino connection could not be savely killed")
            cf.log_message(e)

        # if can_exit:
        event.accept()  # let the window close
        # else:
        #     event.ignore()

    def changed_tab_widget(self):
        """
        Function that shall manage the threads that are running when we are
        on a certain tab. For instance the spectrum thread really only must
        run when the user is on the spectrum tab. Otherwise it can be paused.
        This might become important in the future. The best idea is probably
        to just kill all unused threads when we change the tab.
        """

        cf.log_message(
            "Switched to tab widget no. " + str(self.tabWidget.currentIndex())
        )

        return

    # -------------------------------------------------------------------- #
    # --------------------------- Setup Thread --------------------------- #
    # -------------------------------------------------------------------- #
    @QtCore.Slot(float, float)
    def update_display(self, voltage, current):
        """
        Function to update the readings of the LCD panels that serve as an
        overview to yield the current value of voltage, current and frequency
        """
        # self.sw_frequency_lcdNumber.display(frequency)
        self.sw_voltage_lcdNumber.display(voltage)
        self.sw_current_lcdNumber.display(current)

    def voltage_changed(self):
        """
        Function that changes voltage on source when it is changed on spinbox
        """
        if self.t < 2:
            self.t += 1
            return
        else:
            voltage = self.sw_voltage_spinBox.value()
            self.source.set_voltage(voltage)
            self.source.output(True)
            cf.log_message("Source voltage set to " + str(voltage) + " V")

    def current_changed(self):
        """
        Function that changes current on source when it is changed on spinbox
        """
        if self.t < 2:
            self.t += 1
            return
        else:
            current = self.sw_current_spinBox.value()
            self.source.set_current(current)
            cf.log_message("Source current set to " + str(current) + " A")

    def frequency_changed(self):
        """
        Function that changes frequency on arduino when it is changed on spinbox
        """
        frequency = self.sw_frequency_spinBox.value()
        self.arduino.set_frequency(frequency)
        cf.log_message("Arduino frequency set to " + str(frequency) + " kHz")

    def capacity_changed(self):
        """
        Function that changes frequency on arduino when it is changed on spinbox
        """
        capacity = self.sw_capacitance_spinBox.value()
        self.arduino.set_capacitance(capacity)

        self.sw_capacitance_lcdNumber.display(self.arduino.real_capacity)

        cf.log_message("Capacity set to " + str(self.arduino.real_capacity) + " pF")

    def safe_read_setup_parameters(self):
        """
        Read setup parameters and if any important field is missing, return a qmessagebox
        """

        # Read out measurement and setup parameters from GUI
        setup_parameters = self.read_setup_parameters()

        # Check if folder path exists
        if (
            setup_parameters["folder_path"] == ""
            or setup_parameters["batch_name"] == ""
        ):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Please set folder path and batch name first!")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setStyleSheet(
                "background-color: rgb(44, 49, 60);\n"
                "color: rgb(255, 255, 255);\n"
                'font: 63 bold 10pt "Segoe UI";\n'
                ""
            )
            msgBox.exec()

            self.specw_start_measurement_pushButton.setChecked(False)

            cf.log_message("Folder path or batchname not defined")
            raise UserWarning("Please set folder path and batchname first!")

        # Now check if the folder path ends on a / otherwise try to add it
        if not setup_parameters["folder_path"][-1] == "/":
            setup_parameters["folder_path"] = setup_parameters["folder_path"] + "/"
            self.sw_folder_path_lineEdit.setText(setup_parameters["folder_path"])

        # Now check if the read out path is a valid path
        if not os.path.isdir(setup_parameters["folder_path"]):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Please enter a valid folder path")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setStyleSheet(
                "background-color: rgb(44, 49, 60);\n"
                "color: rgb(255, 255, 255);\n"
                'font: 63 bold 10pt "Segoe UI";\n'
                ""
            )
            msgBox.exec()

            self.specw_start_measurement_pushButton.setChecked(False)

            cf.log_message("Folder path not valid")
            raise UserWarning("Please enter a valid folder path!")

        return setup_parameters

    def read_setup_parameters(self):
        """
        Function to read out the current fields entered in the setup tab
        """
        setup_parameters = {
            "folder_path": self.sw_folder_path_lineEdit.text(),
            "batch_name": self.sw_batch_name_lineEdit.text(),
            "device_number": self.sw_device_number_spinBox.value(),
        }

        # Update statusbar
        cf.log_message("Setup parameters read")

        return setup_parameters

    def toggle_source_output(self):
        """
        Function to toggle source output on or off
        """
        # Currently this only works independently of other functions but it
        # checks for the true state of the source
        if self.source.output_state:
            self.source.output(False)
            self.specw_start_measurement_pushButton.setChecked(False)
        else:
            self.source.output(True)
            self.specw_start_measurement_pushButton.setChecked(True)

    # -------------------------------------------------------------------- #
    # -------------------------- Frequency Sweep ------------------------- #
    # -------------------------------------------------------------------- #
    def read_frequency_sweep_parameters(self):
        """
        Function to read out the current fields entered in the frequency sweep tab
        """
        frequency_sweep_parameters = {
            "voltage": self.specw_voltage_spinBox.value(),
            "current_compliance": self.specw_current_spinBox.value(),
            "minimum_frequency": self.specw_minimum_frequency_spinBox.value(),
            "maximum_frequency": self.specw_maximum_frequency_spinBox.value(),
            "frequency_step": self.specw_frequency_step_spinBox.value(),
            "frequency_settling_time": self.specw_frequency_settling_time_spinBox.value(),
            "autoset_capacitance": self.specw_autoset_capacitance_toggleSwitch.isChecked(),
        }

        # Update statusbar
        cf.log_message("Frequency sweep parameters read")

        return frequency_sweep_parameters

    def start_frequency_sweep(self):
        """
        Function that saves the spectrum (probably by doing another
        measurement and shortly turning on the OLED for a background
        measurement and then saving this into a single file)
        """
        if not self.specw_start_measurement_pushButton.isChecked():
            self.frequency_sweep.kill()
            return

        # Load in setup parameters and make sure that the parameters make sense
        setup_parameters = self.safe_read_setup_parameters()
        frequency_sweep_parameters = self.read_frequency_sweep_parameters()

        self.progressBar.show()

        # self.arduino.set_capacitance(False)
        time.sleep(1)

        self.frequency_sweep = FrequencyScan(
            self.arduino,
            self.source,
            self.oscilloscope,
            frequency_sweep_parameters,
            setup_parameters,
            parent=self,
        )

        self.frequency_sweep.start()

    @QtCore.Slot(list, list, list)
    def update_spectrum(self, frequency, current, vpp):
        """
        Function that is continuously evoked when the spectrum is updated by
        the other thread
        """
        # Clear plot
        # self.specw_ax.cla()
        try:
            del self.specw_ax.lines[0]
            del self.specw_ax2.lines[0]
        except IndexError:
            cf.log_message("Oscilloscope line can not be deleted")

        # Set x and y limit
        self.specw_ax.set_xlim([min(frequency), max(frequency)])
        self.specw_ax.set_ylim([min(current) - 0.2, max(current) + 0.2])

        self.specw_ax2.set_ylim([min(vpp) - 0.2, max(vpp) + 0.2])

        # Plot current
        self.specw_ax.plot(
            frequency,
            current,
            color=(68 / 255, 188 / 255, 65 / 255),
            marker="o",
        )

        self.specw_ax2.plot(
            frequency,
            vpp,
            color=(85 / 255, 170 / 255, 255 / 255),
            marker="o",
        )

        self.specw_fig.draw()

    # -------------------------------------------------------------------- #
    # -------------------------- Capacitor Sweep ------------------------- #
    # -------------------------------------------------------------------- #
    def read_capacitance_sweep_parameters(self):
        """
        Function to read out the current fields entered in the capacitance sweep tab
        """
        capacitance_sweep_parameters = {
            "voltage": self.capw_voltage_spinBox.value(),
            "current_compliance": self.capw_current_spinBox.value(),
            "minimum_frequency": self.capw_minimum_frequency_spinBox.value(),
            "maximum_frequency": self.capw_maximum_frequency_spinBox.value(),
            "frequency_step": self.capw_frequency_step_spinBox.value(),
            "minimum_capacitance": self.capw_minimum_capacitance_spinBox.value(),
            "maximum_capacitance": self.capw_maximum_capacitance_spinBox.value(),
            "frequency_margin": self.capw_frequency_margin_spinBox.value(),
            "frequency_settling_time": self.capw_frequency_settling_time_spinBox.value(),
        }

        # Update statusbar
        cf.log_message("Capacitance sweep parameters read")

        return capacitance_sweep_parameters

    def start_capacitance_sweep(self):
        """
        Function that saves the spectrum (probably by doing another
        measurement and shortly turning on the OLED for a background
        measurement and then saving this into a single file)
        """
        if not self.capw_start_measurement_pushButton.isChecked():
            self.capacitance_sweep.kill()
            return

        # Load in setup parameters and make sure that the parameters make sense
        setup_parameters = self.safe_read_setup_parameters()
        capacitance_sweep_parameters = self.read_capacitance_sweep_parameters()

        self.progressBar.show()

        # self.arduino.set_capacitance(False)
        time.sleep(1)

        self.capacitance_sweep = CapacitanceScan(
            self.arduino,
            self.source,
            # self.oscilloscope,
            capacitance_sweep_parameters,
            setup_parameters,
            parent=self,
        )

        self.capacitance_sweep.start()

    @QtCore.Slot(list, list, list, str, bool, str, bool)
    def update_capacitance_spectrum(
        self, frequency, current, limits, label, first_bool, color, fit
    ):
        """
        Function that is continuously evoked when the spectrum is updated by
        the other thread
        """
        # Clear plot
        # self.specw_ax.cla()
        # Always delete the last line except when first_bool = True which is
        # the case, for the first time a new capacitor is introduced
        if not first_bool:
            try:
                lines = self.capw_ax.get_lines()
                lines[-1].remove()
                # del self.specw_ax.lines[0]
            except IndexError:
                cf.log_message("Spectrum line can not be deleted")

        # Set x and y limit
        self.capw_ax.set_xlim([limits[0], limits[1]])
        # self.capw_ax.set_ylim([min(current) - 0.2, max(current) + 0.2])

        # self.specw_ax2.set_ylim([min(vpp) - 0.2, max(vpp) + 0.2])

        # Plot current
        if fit == True:
            self.capw_ax.plot(frequency, current, color=color)
        else:
            # Plot with linewidth zero is chosen instead of scatter to ensure that lines can be deleted correctly
            self.capw_ax.plot(
                frequency, current, marker="o", linewidth=0, color=color, label=label
            )

        # Only regenerate the legend if the line is the first
        if first_bool:
            legend = self.capw_ax.legend()
            legend.set_draggable(True)

        # self.specw_ax2.plot(
        #     frequency,
        #     vpp,
        #     color=(85 / 255, 170 / 255, 255 / 255),
        #     marker="o",
        # )

        self.capw_fig.draw()

    # -------------------------------------------------------------------- #
    # -------------------------- Oscilloscope ---------------------------- #
    # -------------------------------------------------------------------- #
    @QtCore.Slot(list, list, list)
    def plot_oscilloscope(self, time, voltage, measurements):
        """
        Function that plots the oscilloscope image
        """
        # Clear plot
        # self.specw_ax.cla()
        try:
            del self.ow_ax.lines[0]
        except IndexError:
            cf.log_message("Oscilloscope line can not be deleted")

        # Set x and y limit
        self.ow_ax.set_xlim([min(time), max(time)])
        self.ow_ax.set_ylim([min(voltage) - 2, max(voltage) + 5])

        # Plot current
        self.ow_ax.plot(
            time,
            voltage,
            color=(68 / 255, 188 / 255, 65 / 255),
            # marker="o",
        )

        # self.ow_ax.text(
        #     0.2,
        #     0.7,
        #     "VPP: "
        #     + str(measurements[0])
        #     + "\nVmax: "
        #     + str(measurements[1])
        #     + "\nVmin: "
        #     + str(measurements[2])
        #     + "\nFrequency: "
        #     + str(measurements[3]),
        #     verticalalignment="bottom",
        #     horizontalalignment="left",
        #     transform=self.ow_ax.transAxes,
        #     bbox={"facecolor": "white", "alpha": 0.5, "pad": 10},
        # )

        self.ow_fig.draw()

    def stop_osci(self):
        """
        Function to start and stop the oscilloscope
        """

        # Start and stop the oscilloscope
        if self.ow_stop_pushButton.isChecked():
            self.oscilloscope.stop()
            # self.ow_stop_pushButton.setChecked(False)
        else:
            self.oscilloscope.run()
            # self.ow_stop_pushButton.setChecked(True)

    def auto_scale_osci(self):
        """
        Function to call the autoscale function of the oscilloscope
        """
        self.oscilloscope.auto_scale()

    def save_osci(self):
        """
        Save Data that is currently visible on oscilloscope to file
        """
        # Read parameters
        setup_parameters = self.safe_read_setup_parameters()

        # Read data
        time_data, data = self.oscilloscope.get_data()
        df = pd.DataFrame(columns=["time", "voltage"])
        df.time = time_data
        df.voltage = data

        variables = self.oscilloscope.measure()

        # Define Header
        line01 = "VPP:   " + str(variables[0]) + " V \t"
        line02 = "### Measurement data ###"
        line03 = "Time\t Voltage"
        line04 = "s\t V\n"

        header_lines = [
            line01,
            line02,
            line03,
            line04,
        ]

        # Write header lines to file
        file_path = (
            setup_parameters["folder_path"]
            + dt.date.today().strftime("%Y-%m-%d_")
            + setup_parameters["batch_name"]
            + "_d"
            + str(setup_parameters["device_number"])
            + "_osci"
            + ".csv"
        )

        cf.save_file(df, file_path, header_lines)


# Logging
# Prepare file path etc. for logging
LOG_FILENAME = "./usr/log.out"
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format=(
        "%(asctime)s - [%(levelname)s] -"
        " (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    ),
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

# Activate log_rotate to rotate log files after it reached 1 MB size ()
handler = RotatingFileHandler(LOG_FILENAME, maxBytes=1000000)
logging.getLogger("Rotating Log").addHandler(handler)


# ---------------------------------------------------------------------------- #
# -------------------- This is to execute the program ------------------------ #
# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()

    # Icon (see https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105)
    import ctypes

    myappid = u"mycompan.myproduct.subproduct.version"  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app_icon = QtGui.QIcon()
    app_icon.addFile("./icons/program_icon.png", QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)

    ui.show()
    sys.exit(app.exec_())
