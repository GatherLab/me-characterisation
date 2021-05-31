# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtGui, QtWidgets

import json
import core_functions as cf

from loading_window import LoadingWindow


class Ui_Settings(object):
    def setupUi(self, Settings, parent=None):
        # Note: this is not how it should be done but currently I don't know
        # how to do it differently. This is only needed to be able to emit
        # signals to the main window
        self.parent = parent

        Settings.setObjectName("Settings")
        Settings.resize(509, 317)
        Settings.setStyleSheet(
            "QWidget {\n"
            "            background-color: rgb(44, 49, 60);\n"
            "            color: rgb(255, 255, 255);\n"
            '            font: 63 10pt "Segoe UI";\n'
            "}\n"
            "QPushButton {\n"
            "            border: 2px solid rgb(52, 59, 72);\n"
            "            border-radius: 5px;\n"
            "            background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:hover {\n"
            "            background-color: rgb(57, 65, 80);\n"
            "            border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {\n"
            "            background-color: rgb(35, 40, 49);\n"
            "            border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QPushButton:checked {\n"
            "            background-color: rgb(35, 40, 49);\n"
            "            border: 2px solid rgb(85, 170, 255);\n"
            "}"
            "QLineEdit {\n"
            "            border: 2px solid rgb(61, 70, 86);\n"
            "            border-radius: 5px;\n"
            "            background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QSpinBox {\n"
            "            border: 2px solid rgb(61, 70, 86);\n"
            "            border-radius: 5px;\n"
            "            background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QDoubleSpinBox {\n"
            "            border: 2px solid rgb(61, 70, 86);\n"
            "            border-radius: 5px;\n"
            "            background-color: rgb(52, 59, 72);\n"
            "}\n"
        )
        self.gridLayout = QtWidgets.QGridLayout(Settings)
        self.gridLayout.setContentsMargins(25, 10, 25, 10)
        self.gridLayout.setObjectName("gridLayout")

        # Device settings
        self.device_settings_header_label = QtWidgets.QLabel(Settings)
        self.device_settings_header_label.setMinimumSize(QtCore.QSize(0, 20))
        self.device_settings_header_label.setStyleSheet(
            'font: 75 bold 10pt "Segoe UI";'
        )
        self.device_settings_header_label.setObjectName("device_settings_header_label")
        self.gridLayout.addWidget(self.device_settings_header_label, 0, 0, 1, 2)

        self.header_line_1 = QtWidgets.QFrame()
        self.header_line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.header_line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.header_line_1, 1, 0, 1, 2)
        self.header_line_1.setStyleSheet(
            "QFrame {\n" "            border: 2px solid rgb(52, 59, 72);\n" "}\n"
        )

        # Source address
        self.source_address_label = QtWidgets.QLabel(Settings)
        self.source_address_label.setObjectName("source_address_label")
        self.gridLayout.addWidget(self.source_address_label, 2, 0, 1, 1)
        self.source_address_lineEdit = QtWidgets.QLineEdit(Settings)
        self.source_address_lineEdit.setObjectName("source_address_lineEdit")
        self.source_address_lineEdit.setMinimumSize(QtCore.QSize(270, 0))
        # self.source_address_lineEdit.setText(
        # u"USB0::0x05E6::0x2450::04102170::INSTR"
        # )
        self.gridLayout.addWidget(self.source_address_lineEdit, 2, 1, 1, 1)

        # Keithley multimeter address
        self.rigol_oscilloscope_address_label = QtWidgets.QLabel(Settings)
        self.rigol_oscilloscope_address_label.setObjectName(
            "rigol_oscilloscope_address_label"
        )
        self.gridLayout.addWidget(self.rigol_oscilloscope_address_label, 3, 0, 1, 1)
        self.rigol_oscilloscope_address_lineEdit = QtWidgets.QLineEdit(Settings)
        self.rigol_oscilloscope_address_lineEdit.setObjectName(
            "rigol_oscilloscope_address_lineEdit"
        )
        # self.rigol_oscilloscope_address_lineEdit.setText(
        # u"USB0::0x05E6::0x2100::8003430::INSTR"
        # )
        self.gridLayout.addWidget(self.rigol_oscilloscope_address_lineEdit, 3, 1, 1, 1)

        # Arduino COM address
        self.arduino_com_address_label = QtWidgets.QLabel(Settings)
        self.arduino_com_address_label.setObjectName("arduino_com_address_label")
        self.gridLayout.addWidget(self.arduino_com_address_label, 4, 0, 1, 1)
        self.arduino_com_address_lineEdit = QtWidgets.QLineEdit(Settings)
        self.arduino_com_address_lineEdit.setObjectName("arduino_com_address_lineEdit")
        self.gridLayout.addWidget(self.arduino_com_address_lineEdit, 4, 1, 1, 1)

        # Global Software Settings
        self.software_settings_header_label = QtWidgets.QLabel(Settings)
        self.software_settings_header_label.setMinimumSize(QtCore.QSize(0, 20))
        self.software_settings_header_label.setStyleSheet(
            'font: 75 bold 10pt "Segoe UI";'
        )
        self.software_settings_header_label.setObjectName(
            "software_settings_header_label"
        )
        self.gridLayout.addWidget(self.software_settings_header_label, 5, 0, 1, 2)

        self.header_line_3 = QtWidgets.QFrame()
        self.header_line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.header_line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.header_line_3, 6, 0, 1, 2)
        self.header_line_3.setStyleSheet(
            "QFrame {\n" "            border: 2px solid rgb(52, 59, 72);\n" "}\n"
        )

        # Standard Saving Path
        self.default_saving_path_label = QtWidgets.QLabel(Settings)
        self.default_saving_path_label.setObjectName("default_saving_path_label")
        self.gridLayout.addWidget(self.default_saving_path_label, 7, 0, 1, 1)
        self.default_saving_path_lineEdit = QtWidgets.QLineEdit(Settings)
        self.default_saving_path_lineEdit.setObjectName("default_saving_path_lineEdit")
        self.gridLayout.addWidget(self.default_saving_path_lineEdit, 7, 1, 1, 1)

        self.pid_parameters_label = QtWidgets.QLabel(Settings)
        self.pid_parameters_label.setObjectName("pid_parameters_label")
        self.gridLayout.addWidget(self.pid_parameters_label, 8, 0, 1, 1)
        self.pid_parameters_lineEdit = QtWidgets.QLineEdit(Settings)
        self.pid_parameters_lineEdit.setObjectName("pid_parameters_lineEdit")
        self.gridLayout.addWidget(self.pid_parameters_lineEdit, 8, 1, 1, 1)

        # Data Evaluation Settings
        self.lcr_header_label = QtWidgets.QLabel(Settings)
        self.lcr_header_label.setMinimumSize(QtCore.QSize(0, 20))
        self.lcr_header_label.setStyleSheet('font: 75 bold 10pt "Segoe UI";')
        self.lcr_header_label.setObjectName("lcr_header_label")
        self.gridLayout.addWidget(self.lcr_header_label, 9, 0, 1, 2)

        self.load_rlc_settings_pushButton = QtWidgets.QPushButton(Settings)
        self.load_rlc_settings_pushButton.setObjectName("load_rlc_settings_pushButton")
        self.gridLayout.addWidget(self.load_rlc_settings_pushButton, 9, 1, 1, 2)

        self.header_line_2 = QtWidgets.QFrame()
        self.header_line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.header_line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.header_line_2, 10, 0, 1, 2)
        self.header_line_2.setStyleSheet(
            "QFrame {\n" "            border: 2px solid rgb(52, 59, 72);\n" "}\n"
        )

        # Coil inductance
        self.coil_inductance_label = QtWidgets.QLabel(Settings)
        self.coil_inductance_label.setObjectName("coil_inductance_label")
        self.gridLayout.addWidget(self.coil_inductance_label, 11, 0, 1, 1)
        self.coil_inductance_lineEdit = QtWidgets.QLineEdit(Settings)
        self.coil_inductance_lineEdit.setObjectName("coil_inductance_lineEdit")
        self.gridLayout.addWidget(self.coil_inductance_lineEdit, 11, 1, 1, 1)

        # Coil windings
        self.coil_windings_label = QtWidgets.QLabel(Settings)
        self.coil_windings_label.setObjectName("coil_windings_label")
        self.gridLayout.addWidget(self.coil_windings_label, 12, 0, 1, 1)
        self.coil_windings_lineEdit = QtWidgets.QLineEdit(Settings)
        self.coil_windings_lineEdit.setObjectName("coil_windings_lineEdit")
        self.gridLayout.addWidget(self.coil_windings_lineEdit, 12, 1, 1, 1)

        # Coil radius
        self.coil_radius_label = QtWidgets.QLabel(Settings)
        self.coil_radius_label.setObjectName("coil_radius_label")
        self.gridLayout.addWidget(self.coil_radius_label, 13, 0, 1, 1)
        self.coil_radius_lineEdit = QtWidgets.QLineEdit(Settings)
        self.coil_radius_lineEdit.setObjectName("coil_radius_lineEdit")
        self.gridLayout.addWidget(self.coil_radius_lineEdit, 13, 1, 1, 1)

        # Circuit Resistance
        self.circuit_resistance_label = QtWidgets.QLabel(Settings)
        self.circuit_resistance_label.setObjectName("circuit_resistance_label")
        self.gridLayout.addWidget(self.circuit_resistance_label, 14, 0, 1, 1)
        self.circuit_resistance_lineEdit = QtWidgets.QLineEdit(Settings)
        self.circuit_resistance_lineEdit.setObjectName("circuit_resistance_lineEdit")
        self.gridLayout.addWidget(self.circuit_resistance_lineEdit, 14, 1, 1, 1)

        # Base capacitance
        self.base_capacitance_label = QtWidgets.QLabel(Settings)
        self.base_capacitance_label.setObjectName("base_capacitance_label")
        self.gridLayout.addWidget(self.base_capacitance_label, 15, 0, 1, 1)
        self.base_capacitance_lineEdit = QtWidgets.QLineEdit(Settings)
        self.base_capacitance_lineEdit.setObjectName("base_capacitance_lineEdit")
        self.gridLayout.addWidget(self.base_capacitance_lineEdit, 15, 1, 1, 1)

        # Capacitances
        self.capacitances_label = QtWidgets.QLabel(Settings)
        self.capacitances_label.setObjectName("capacitances_label")
        self.gridLayout.addWidget(self.capacitances_label, 16, 0, 1, 1)
        self.capacitances_lineEdit = QtWidgets.QLineEdit(Settings)
        self.capacitances_lineEdit.setObjectName("capacitances_lineEdit")
        self.gridLayout.addWidget(self.capacitances_lineEdit, 16, 1, 1, 1)

        # Arduino Pins (matching the capacitances)
        self.arduino_pins_label = QtWidgets.QLabel(Settings)
        self.arduino_pins_label.setObjectName("arduino_pins_label")
        self.gridLayout.addWidget(self.arduino_pins_label, 17, 0, 1, 1)
        self.arduino_pins_lineEdit = QtWidgets.QLineEdit(Settings)
        self.arduino_pins_lineEdit.setObjectName("arduino_pins_lineEdit")
        self.gridLayout.addWidget(self.arduino_pins_lineEdit, 17, 1, 1, 1)

        # Resonance Frequency calibration file
        self.resonance_frequency_calibration_path_label = QtWidgets.QLabel(Settings)
        self.resonance_frequency_calibration_path_label.setObjectName(
            "resonance_frequency_calibration_path_label"
        )
        self.gridLayout.addWidget(
            self.resonance_frequency_calibration_path_label, 18, 0, 1, 1
        )
        self.resonance_frequency_calibration_path_lineEdit = QtWidgets.QLineEdit(
            Settings
        )
        self.resonance_frequency_calibration_path_lineEdit.setObjectName(
            "resonance_frequency_calibration_path_lineEdit"
        )
        self.gridLayout.addWidget(
            self.resonance_frequency_calibration_path_lineEdit, 18, 1, 1, 1
        )

        # Magnetic field measurement settings
        self.magnetic_field_measurement_label = QtWidgets.QLabel(Settings)
        self.magnetic_field_measurement_label.setMinimumSize(QtCore.QSize(0, 20))
        self.magnetic_field_measurement_label.setStyleSheet(
            'font: 75 bold 10pt "Segoe UI";'
        )
        self.magnetic_field_measurement_label.setObjectName(
            "magnetic_field_measurement_label"
        )
        self.gridLayout.addWidget(self.magnetic_field_measurement_label, 19, 0, 1, 2)

        self.header_line_3 = QtWidgets.QFrame()
        self.header_line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.header_line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.header_line_3, 20, 0, 1, 2)
        self.header_line_3.setStyleSheet(
            "QFrame {\n" "            border: 2px solid rgb(52, 59, 72);\n" "}\n"
        )

        # Coil windings
        self.pickup_coil_windings_label = QtWidgets.QLabel(Settings)
        self.pickup_coil_windings_label.setObjectName("pickup_coil_windings_label")
        self.gridLayout.addWidget(self.pickup_coil_windings_label, 21, 0, 1, 1)
        self.pickup_coil_windings_lineEdit = QtWidgets.QLineEdit(Settings)
        self.pickup_coil_windings_lineEdit.setObjectName(
            "pickup_coil_windings_lineEdit"
        )
        self.gridLayout.addWidget(self.pickup_coil_windings_lineEdit, 21, 1, 1, 1)

        # Coil radius (in mm)
        self.pickup_coil_radius_label = QtWidgets.QLabel(Settings)
        self.pickup_coil_radius_label.setObjectName("pickup_coil_radius_label")
        self.gridLayout.addWidget(self.pickup_coil_radius_label, 22, 0, 1, 1)
        self.pickup_coil_radius_lineEdit = QtWidgets.QLineEdit(Settings)
        self.pickup_coil_radius_lineEdit.setObjectName("pickup_coil_radius_lineEdit")
        self.gridLayout.addWidget(self.pickup_coil_radius_lineEdit, 22, 1, 1, 1)

        # # Transimpedance Amplifier Resistance
        # self.amplifier_resistance_label = QtWidgets.QLabel(Settings)
        # self.amplifier_resistance_label.setObjectName("amplifier_resistance_label")
        # self.gridLayout.addWidget(self.amplifier_resistance_label, 17, 0, 1, 1)
        # self.amplifier_resistance_lineEdit = QtWidgets.QLineEdit(Settings)
        # self.amplifier_resistance_lineEdit.setObjectName(
        #     "amplifier_resistance_lineEdit"
        # )
        # self.gridLayout.addWidget(self.amplifier_resistance_lineEdit, 17, 1, 1, 1)

        # # Active OLED area
        # self.oled_area_label = QtWidgets.QLabel(Settings)
        # self.oled_area_label.setObjectName("oled_area_label")
        # self.gridLayout.addWidget(self.oled_area_label, 18, 0, 1, 1)
        # self.oled_area_lineEdit = QtWidgets.QLineEdit(Settings)
        # self.oled_area_lineEdit.setObjectName("oled_area_lineEdit")
        # self.gridLayout.addWidget(self.oled_area_lineEdit, 18, 1, 1, 1)

        # # Distance photodiode, OLED
        # self.distance_photodiode_oled_label = QtWidgets.QLabel(Settings)
        # self.distance_photodiode_oled_label.setObjectName(
        #     "distance_photodiode_oled_label"
        # )
        # self.gridLayout.addWidget(self.distance_photodiode_oled_label, 19, 0, 1, 1)
        # self.distance_photodiode_oled_lineEdit = QtWidgets.QLineEdit(Settings)
        # self.distance_photodiode_oled_lineEdit.setObjectName(
        #     "distance_photodiode_oled_lineEdit"
        # )
        # self.gridLayout.addWidget(self.distance_photodiode_oled_lineEdit, 19, 1, 1, 1)

        # Push Buttons
        self.buttons_HBoxLayout = QtWidgets.QHBoxLayout()
        self.load_defaults_pushButton = QtWidgets.QPushButton(Settings)
        self.load_defaults_pushButton.setObjectName("load_defaults_pushButton")
        self.buttons_HBoxLayout.addWidget(self.load_defaults_pushButton)

        self.save_settings_pushButton = QtWidgets.QPushButton(Settings)
        self.save_settings_pushButton.setObjectName("save_settings_pushButton")
        self.buttons_HBoxLayout.addWidget(self.save_settings_pushButton)

        self.gridLayout.addLayout(self.buttons_HBoxLayout, 23, 0, 1, 2)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Options"))
        self.device_settings_header_label.setText(
            _translate("Settings", "Device Settings")
        )
        self.source_address_label.setText(
            _translate("Settings", "Voltcraft Source Address")
        )
        self.rigol_oscilloscope_address_label.setText(
            _translate("Settings", "Rigol Oscilloscope Address")
        )
        self.arduino_com_address_label.setText(
            _translate("Settings", "Arduino Com Address")
        )

        self.software_settings_header_label.setText(
            _translate("Settings", "Software Settings")
        )

        self.default_saving_path_label.setText(
            _translate("Settings", "Default Saving Path")
        )
        self.pid_parameters_label.setText(
            _translate("Settings", "Magnetic Field PID Parameters")
        )

        self.lcr_header_label.setText(_translate("Settings", "LCR Settings"))
        self.magnetic_field_measurement_label.setText(
            _translate("Settings", "Magnetic Field Measurement Settings")
        )
        self.base_capacitance_label.setText(
            _translate("Settings", "Base Capacitance (pF)")
        )

        self.capacitances_label.setText(
            _translate("Settings", "Capacitances (pF seperated by ,)")
        )
        self.arduino_pins_label.setText(
            _translate("Settings", "Arduino Pins (same order seperated by ,)")
        )
        self.coil_inductance_label.setText(
            _translate("Settings", "Coil Inductance (mH)")
        )
        self.pickup_coil_windings_label.setText(
            _translate("Settings", "Pickup Coil Windings")
        )

        self.pickup_coil_radius_label.setText(
            _translate("Settings", "Pickup Coil Radius (mm)")
        )
        self.coil_windings_label.setText(_translate("Settings", "Coil Windings"))
        self.coil_radius_label.setText(_translate("Settings", "Coil Radius (mm)"))
        self.circuit_resistance_label.setText(
            _translate("Settings", "Circuit Resistance (Ohm)")
        )
        self.resonance_frequency_calibration_path_label.setText(
            _translate("Settings", "Calibration File Path")
        )
        # self.amplifier_resistance_label.setText(
        #     _translate("Settings", "Transimpedance Amplifier Resistance (Ohm)")
        # )
        # self.oled_area_label.setText(_translate("Settings", "Active OLED Area (mm^2)"))
        # self.distance_photodiode_oled_label.setText(
        #     _translate("Settings", "Distance Photodiode-OLED (mm)")
        # )

        self.save_settings_pushButton.setText(_translate("Settings", "Save Settings"))
        self.load_defaults_pushButton.setText(_translate("Settings", "Load Defaults"))
        self.load_rlc_settings_pushButton.setText(
            _translate("Settings", "Load RLC Settings")
        )
