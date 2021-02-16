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

        self.source_address_lineEdit.setText(default_settings["source_address"])
        self.rigol_oscilloscope_address_lineEdit.setText(
            default_settings["rigol_oscilloscope_address"]
        )
        self.arduino_com_address_lineEdit.setText(default_settings["arduino_address"])
        self.default_saving_path_lineEdit.setText(
            default_settings["default_saving_path"]
        )
        self.base_capacitance_lineEdit.setText(default_settings["base_capacitance"])
        self.capacitances_lineEdit.setText(default_settings["capacitances"])
        self.coil_inductance_lineEdit.setText(default_settings["coil_inductance"])
        self.circuit_resistance_lineEdit.setText(default_settings["circuit_resistance"])
        self.arduino_pins_lineEdit.setText(default_settings["arduino_pins"])

        # Connect buttons to functions
        self.load_defaults_pushButton.clicked.connect(self.load_defaults)
        self.save_settings_pushButton.clicked.connect(self.save_settings)

    def save_settings(self):
        """
        Save the settings the user just entered
        """

        # Gather the new settings
        settings_data = {}
        settings_data["overwrite"] = []
        settings_data["overwrite"].append(
            {
                "source_address": self.source_address_lineEdit.text(),
                "rigol_oscilloscope_address": self.rigol_oscilloscope_address_lineEdit.text(),
                "arduino_address": self.arduino_com_address_lineEdit.text(),
                "default_saving_path": self.default_saving_path_lineEdit.text(),
                "base_capacitance": self.base_capacitance_lineEdit.text(),
                "coil_inductance": self.coil_inductance_lineEdit.text(),
                "circuit_resistance": self.circuit_resistance_lineEdit.text(),
                "capacitances": self.capacitances_lineEdit.text(),
                "arduino_pins": self.arduino_pins_lineEdit.text(),
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
        print(settings_data)

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
        loading_window = LoadingWindow(self.parent)

        # Execute loading dialog
        loading_window.exec()

    def load_defaults(self):
        """
        Load default settings (in case the user messed up the own settings)
        """

        with open(
            os.path.join(Path(__file__).parent.parent, "usr", "global_settings.json")
        ) as json_file:
            data = json.load(json_file)

        default_settings = data["default"][0]
        self.source_address_lineEdit.setText(default_settings["source_address"])
        self.rigol_oscilloscope_address_lineEdit.setText(
            default_settings["rigol_oscilloscope_address"]
        )
        self.arduino_com_address_lineEdit.setText(default_settings["arduino_address"])

        self.default_saving_path_lineEdit.setText(
            default_settings["default_saving_path"]
        )
        self.base_capacitance_lineEdit.setText(default_settings["base_capacitance"])

        self.capacitances_lineEdit.setText(default_settings["capacitances"])

        self.coil_inductance_lineEdit.setText(default_settings["coil_inductance"])
        self.circuit_resistance_lineEdit.setText(default_settings["circuit_resistance"])
        self.arduino_pins_lineEdit.setText(default_settings["arduino_pins"])
