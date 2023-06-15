# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtGui, QtWidgets

import json
import os
import core_functions as cf
from pathlib import Path

from loading_window import LoadingWindow
from UI_settings_window import Ui_Settings


class Settings(QtWidgets.QDialog, Ui_Settings):
    """
    Settings window
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

        self.parent = parent

        # Load from file to fill the lines
        default_settings = cf.read_global_settings()

        self.dc_source_address_lineEdit.setText(default_settings["dc_source_address"])
        self.hf_source_address_lineEdit.setText(default_settings["hf_source_address"])
        self.rigol_oscilloscope_address_lineEdit.setText(
            default_settings["rigol_oscilloscope_address"]
        )
        self.arduino_com_address_lineEdit.setText(default_settings["arduino_address"])
        self.default_saving_path_lineEdit.setText(
            default_settings["default_saving_path"]
        )
        self.pid_parameters_lineEdit.setText(default_settings["pid_parameters"])
        self.luminance_mode_toggleSwitch.setChecked(
            bool(default_settings["luminance_mode"])
        )
        # isChecked()
        self.base_capacitance_lineEdit.setText(
            str(default_settings["base_capacitance"])
        )
        self.capacitances_lineEdit.setText(str(default_settings["capacitances"]))
        self.coil_inductance_lineEdit.setText(str(default_settings["coil_inductance"]))
        self.coil_windings_lineEdit.setText(str(default_settings["coil_windings"]))
        self.pickup_coil_windings_lineEdit.setText(
            str(default_settings["pickup_coil_windings"])
        )
        self.pickup_coil_radius_lineEdit.setText(
            str(default_settings["pickup_coil_radius"])
        )
        self.coil_radius_lineEdit.setText(str(default_settings["coil_radius"]))
        self.circuit_resistance_lineEdit.setText(
            str(default_settings["circuit_resistance"])
        )
        self.arduino_pins_lineEdit.setText(str(default_settings["arduino_pins"]))
        self.resonance_frequency_calibration_path_lineEdit.setText(
            str(default_settings["calibration_file_path"])
        )
        self.dc_field_conversion_lineEdit.setText(
            str(default_settings["dc_field_conversion_factor"])
        )

        self.load_rlc_settings_pushButton.clicked.connect(self.load_rlc_settings)

        # Connect buttons to functions
        self.load_defaults_pushButton.clicked.connect(self.load_defaults)
        self.save_settings_pushButton.clicked.connect(self.save_settings)

    def load_rlc_settings(self):
        """
        Load RLC settings
        """
        global_variables = cf.read_global_settings()

        path = QtWidgets.QFileDialog.getOpenFileName(
            QtWidgets.QFileDialog(),
            "Select a RLC Parameter File",
            global_variables["default_saving_path"],
            # QtWidgets.QFileDialog.ShowDirsOnly,
        )[0]
        # Load the rlc specs from file
        with open(path) as json_file:
            rlc_settings = json.load(json_file)

        # Now set the right fields
        self.base_capacitance_lineEdit.setText(rlc_settings["base_capacitance"])
        self.coil_inductance_lineEdit.setText(rlc_settings["coil_inductance"])
        self.coil_windings_lineEdit.setText(rlc_settings["coil_windings"])
        self.coil_radius_lineEdit.setText(rlc_settings["coil_radius"])
        self.capacitances_lineEdit.setText(rlc_settings["capacitances"])
        self.circuit_resistance_lineEdit.setText(rlc_settings["circuit_resistance"])
        self.arduino_pins_lineEdit.setText(rlc_settings["arduino_pins"])
        self.resonance_frequency_calibration_path_lineEdit.setText(
            rlc_settings["calibration_file_path"]
        )

    def save_settings(self):
        """
        Save the settings the user just entered
        """

        # Gather the new settings
        settings_data = {}
        settings_data["overwrite"] = []
        settings_data["overwrite"].append(
            {
                "dc_source_address": self.dc_source_address_lineEdit.text(),
                "hf_source_address": self.hf_source_address_lineEdit.text(),
                "rigol_oscilloscope_address": self.rigol_oscilloscope_address_lineEdit.text(),
                "arduino_address": self.arduino_com_address_lineEdit.text(),
                "default_saving_path": self.default_saving_path_lineEdit.text(),
                "pid_parameters": self.pid_parameters_lineEdit.text(),
                "luminance_mode": self.luminance_mode_toggleSwitch.isChecked(),
                "base_capacitance": self.base_capacitance_lineEdit.text(),
                "coil_inductance": self.coil_inductance_lineEdit.text(),
                "coil_windings": self.coil_windings_lineEdit.text(),
                "coil_radius": self.coil_radius_lineEdit.text(),
                "pickup_coil_windings": self.pickup_coil_windings_lineEdit.text(),
                "pickup_coil_radius": self.pickup_coil_radius_lineEdit.text(),
                "circuit_resistance": self.circuit_resistance_lineEdit.text(),
                "capacitances": self.capacitances_lineEdit.text(),
                "arduino_pins": self.arduino_pins_lineEdit.text(),
                "calibration_file_path": self.resonance_frequency_calibration_path_lineEdit.text(),
                "dc_field_conversion_factor": self.dc_field_conversion_lineEdit.text(),
            }
        )

        # Load the default parameter settings
        with open(
            os.path.join(Path(__file__).parent.parent, "usr", "global_settings.json")
        ) as json_file:
            data = json.load(json_file)

        # Add the default parameters to the new settings json
        settings_data["default"] = []
        settings_data["default"] = data["default"]

        # Save the entire thing again to the settings.json file
        with open(
            os.path.join(Path(__file__).parent.parent, "usr", "global_settings.json"),
            "w",
        ) as json_file:
            json.dump(settings_data, json_file, indent=4)

        cf.log_message("Settings saved")

        # Close window on accepting
        self.accept()

        # Before closing the window, reinstanciate the devices with the new
        # parameters
        reload_window_comparison = {
            k: settings_data["overwrite"][0][k]
            for k in data["overwrite"][0]
            if k in settings_data["overwrite"][0]
            and data["overwrite"][0][k] != settings_data["overwrite"][0][k]
        }
        # If any of the parameters that require a reinitialisation has been changed, then do one
        if any(
            key in reload_window_comparison.keys()
            for key in [
                "dc_source_address",
                "hf_source_address",
                "arduino_com_address",
                "rigol_oscilloscope_address",
            ]
        ):
            loading_window = LoadingWindow(self.parent)

            # Execute loading dialog
            loading_window.exec()
        elif any(
            key in reload_window_comparison.keys()
            for key in [
                "coil_inductance",
                "dc_field_conversion_factor",
                "capacitances",
                "base_capacitance",
                "arduino_pins",
                "calibration_file_path",
            ]
        ):
            # Only reinit caps and dc field conversion factor
            self.parent.arduino.init_caps()
            self.parent.dc_source.dc_field_conversion_factor = float(
                settings_data["overwrite"][0]["dc_field_conversion_factor"]
            )

    def load_defaults(self):
        """
        Load default settings (in case the user messed up the own settings)
        """

        with open(
            os.path.join(Path(__file__).parent.parent, "usr", "global_settings.json")
        ) as json_file:
            data = json.load(json_file)

        default_settings = data["default"][0]
        self.dc_source_address_lineEdit.setText(default_settings["dc_source_address"])
        self.hf_source_address_lineEdit.setText(default_settings["hf_source_address"])
        self.rigol_oscilloscope_address_lineEdit.setText(
            default_settings["rigol_oscilloscope_address"]
        )
        self.arduino_com_address_lineEdit.setText(default_settings["arduino_address"])

        self.default_saving_path_lineEdit.setText(
            default_settings["default_saving_path"]
        )
        self.pid_parameters_lineEdit.setText(default_settings["pid_parameters"])
        self.luminance_mode_toggleSwitch.setChecked(
            bool(default_settings["luminance_mode"])
        )
        # isChecked()
        self.base_capacitance_lineEdit.setText(
            str(default_settings["base_capacitance"])
        )
        self.capacitances_lineEdit.setText(str(default_settings["capacitances"]))
        self.coil_inductance_lineEdit.setText(str(default_settings["coil_inductance"]))
        self.coil_windings_lineEdit.setText(str(default_settings["coil_windings"]))
        self.pickup_coil_windings_lineEdit.setText(
            str(default_settings["pickup_coil_windings"])
        )
        self.pickup_coil_radius_lineEdit.setText(
            str(default_settings["pickup_coil_radius"])
        )
        self.coil_radius_lineEdit.setText(str(default_settings["coil_radius"]))
        self.circuit_resistance_lineEdit.setText(
            str(default_settings["circuit_resistance"])
        )
        self.arduino_pins_lineEdit.setText(str(default_settings["arduino_pins"]))
        self.resonance_frequency_calibration_path_lineEdit.setText(
            str(default_settings["calibration_file_path"])
        )
        self.dc_field_conversion_lineEdit.setText(
            str(default_settings["dc_field_conversion_factor"])
        )

        self.load_rlc_settings_pushButton.clicked.connect(self.load_rlc_settings)

        # Connect buttons to functions
        self.load_defaults_pushButton.clicked.connect(self.load_defaults)
        self.save_settings_pushButton.clicked.connect(self.save_settings)

        self.base_capacitance_lineEdit.setText(default_settings["base_capacitance"])

        self.capacitances_lineEdit.setText(default_settings["capacitances"])

        self.coil_inductance_lineEdit.setText(default_settings["coil_inductance"])
        self.coil_windings_lineEdit.setText(default_settings["coil_windings"])
        self.pickup_coil_windings_lineEdit.setText(
            default_settings["pickup_coil_windings"]
        )
        self.pickup_coil_radius_lineEdit.setText(default_settings["pickup_coil_radius"])
        self.coil_radius_lineEdit.setText(default_settings["coil_radius"])
        self.circuit_resistance_lineEdit.setText(default_settings["circuit_resistance"])
        self.arduino_pins_lineEdit.setText(default_settings["arduino_pins"])
        self.resonance_frequency_calibration_path_lineEdit.setText(
            default_settings["calibration_file_path"]
        )
        self.dc_field_conversion_lineEdit.setText(
            default_settings["dc_field_conversion_factor"]
        )
