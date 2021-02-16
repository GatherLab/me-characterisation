# -*- coding: utf-8 -*-

# Initial gui design with QtCreator then translated into python code and adjusted

# from UI_settings_window import Ui_Settings
from UI_toggle_switch import ToggleSwitch

from PySide2 import QtCore, QtGui, QtWidgets

import matplotlib.pylab as plt
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
import matplotlib.backends.backend_qt5

import time


# ---------------------------------------------------------------------------- #
# --------------------------- Define Main Window ----------------------------- #
# ---------------------------------------------------------------------------- #
class Ui_MainWindow(object):
    """
    Class that contains all information about the main window
    """

    def setupUi(self, MainWindow):
        """
        Setup that sets all gui widgets at their place
        """

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(973, 695)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setStyleSheet(
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
            "QScrollArea {\n"
            "            border: 2px solid rgb(61, 70, 86);\n"
            "            border-radius: 5px;\n"
            "}\n"
            "QScrollBar {\n"
            "            border-radius: 5px;\n"
            "            background: rgb(61, 70, 86);\n"
            "}\n"
            "QScrollBar:add-page {\n"
            "            background: rgb(52, 59, 72);\n"
            "}\n"
            "QScrollBar:sub-page {\n"
            "            background: rgb(52, 59, 72);\n"
            "}\n"
        )

        self.center()

        # Define central widget of the MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget.setStyleSheet(
        #     "QLineEdit {\n"
        #     "            border: 2px solid rgb(61, 70, 86);\n"
        #     "            border-radius: 5px;\n"
        #     "            background-color: rgb(52, 59, 72);\n"
        #     "}\n"
        #     "QSpinBox {\n"
        #     "            border: 2px solid rgb(61, 70, 86);\n"
        #     "            border-radius: 5px;\n"
        #     "            background-color: rgb(52, 59, 72);\n"
        #     "}\n"
        #     "QDoubleSpinBox {\n"
        #     "            border: 2px solid rgb(61, 70, 86);\n"
        #     "            border-radius: 5px;\n"
        #     "            background-color: rgb(52, 59, 72);\n"
        #     "}\n"
        #     "QScrollArea {\n"
        #     "            border: 2px solid rgb(61, 70, 86);\n"
        #     "            border-radius: 5px;\n"
        #     "}\n"
        #     "QScrollBar {\n"
        #     # "            border: 2px solid rgb(85, 170, 255);\n"
        #     "            border-radius: 5px;\n"
        #     "            background: rgb(61, 70, 86);\n"
        #     "}\n"
        #     "QScrollBar:add-page {\n"
        #     "            background: rgb(52, 59, 72);\n"
        #     "}\n"
        #     "QScrollBar:sub-page {\n"
        #     "            background: rgb(52, 59, 72);\n"
        #     "}\n"
        # )
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(-1, -1, -1, 6)
        self.gridLayout.setObjectName("gridLayout")

        # This here shall be the logo of the program
        # self.gatherlab_picture = QtWidgets.QWidget(self.centralwidget)
        # self.gatherlab_picture.setObjectName("gatherlab_picture")
        self.gatherlab_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("icons/logo_cropped.jpg")
        self.gatherlab_label.setPixmap(pixmap)
        self.gatherlab_label.setScaledContents(True)
        # self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        # self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # self.gatherlab_picture.setLayout(self.horizontalLayout_2)
        self.gridLayout.addWidget(self.gatherlab_label, 0, 0, 1, 1)

        # Tab widget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setStyleSheet(
            "QTabBar {\n"
            "        font-weight: bold;\n"
            "}\n"
            "QTabBar:tab {\n"
            "            background: rgb(52, 59, 72);\n"
            "}\n"
            "QTabBar:tab:selected {\n"
            "            background: rgb(61, 70, 86);\n"
            "            color: rgb(85, 170, 255);\n"
            "}\n"
            "QTabBar:tab:hover {\n"
            "            color: rgb(85, 170, 255);\n"
            "}\n"
            "QTabWidget:pane {\n"
            "            border: 2px solid rgb(52, 59, 72);\n"
            "}\n"
        )

        # -------------------------------------------------------------------- #
        # --------------------------- Setup widget --------------------------- #
        # -------------------------------------------------------------------- #
        self.setup_widget = QtWidgets.QWidget()
        self.setup_widget.setObjectName("setup_widget")
        # self.gridLayout_5 = QtWidgets.QGridLayout(self.setup_widget)
        # self.gridLayout_5.setObjectName("gridLayout_5")
        # self.setup_sub_widget = QtWidgets.QWidget(self.setup_widget)
        # self.setup_sub_widget.setObjectName("setup_sub_widget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.setup_widget)
        self.gridLayout_7.setObjectName("gridLayout_7")

        # Setup widget header 1
        self.sw_header1_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_header1_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.sw_header1_label.setObjectName("sw_header1_label")
        self.gridLayout_7.addWidget(self.sw_header1_label, 0, 0, 1, 1)

        # Setup widget header
        # self.sw_header2_label = QtWidgets.QLabel(self.setup_widget)
        # self.sw_header2_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        # self.sw_header2_label.setObjectName("sw_header2_label")
        # self.gridLayout_7.addWidget(self.sw_header2_label, 5, 0, 1, 1)

        # Setup widget base folder path
        self.sw_folder_path_horizontalLayout = QtWidgets.QHBoxLayout()
        self.sw_folder_path_horizontalLayout.setObjectName(
            "sw_folder_path_horizontalLayout"
        )
        self.sw_folder_path_lineEdit = QtWidgets.QLineEdit(self.setup_widget)
        self.sw_folder_path_lineEdit.setReadOnly(False)
        self.sw_folder_path_lineEdit.setObjectName("sw_folder_path_lineEdit")
        self.sw_folder_path_horizontalLayout.addWidget(self.sw_folder_path_lineEdit)
        self.sw_browse_pushButton = QtWidgets.QPushButton(self.setup_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sw_browse_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.sw_browse_pushButton.setSizePolicy(sizePolicy)
        self.sw_browse_pushButton.setMinimumSize(QtCore.QSize(60, 0))
        self.sw_browse_pushButton.setObjectName("sw_browse_pushButton")
        self.sw_folder_path_horizontalLayout.addWidget(self.sw_browse_pushButton)
        self.gridLayout_7.addLayout(self.sw_folder_path_horizontalLayout, 1, 1, 1, 1)
        self.sw_folder_path_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_folder_path_label.setObjectName("sw_folder_path_label")
        self.gridLayout_7.addWidget(self.sw_folder_path_label, 1, 0, 1, 1)

        # Setup widget batch name
        self.sw_batch_name_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_batch_name_label.setObjectName("sw_batch_name_label")
        self.gridLayout_7.addWidget(self.sw_batch_name_label, 2, 0, 1, 1)
        self.sw_batch_name_lineEdit = QtWidgets.QLineEdit(self.setup_widget)
        self.sw_batch_name_lineEdit.setObjectName("sw_batch_name_lineEdit")
        self.gridLayout_7.addWidget(self.sw_batch_name_lineEdit, 2, 1, 1, 1)

        # Setup widget device number
        self.sw_device_number_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_device_number_label.setObjectName("sw_device_number_label")
        self.gridLayout_7.addWidget(self.sw_device_number_label, 3, 0, 1, 1)
        self.sw_device_number_spinBox = QtWidgets.QSpinBox(self.setup_widget)
        self.sw_device_number_spinBox.setObjectName("sw_device_number_spinBox")
        self.gridLayout_7.addWidget(self.sw_device_number_spinBox, 3, 1, 1, 1)

        # Setup widget documentation
        # self.sw_documentation_textEdit = QtWidgets.QTextEdit(self.setup_widget)
        # self.sw_documentation_textEdit.setObjectName("sw_documentation_textEdit")
        # self.gridLayout_7.addWidget(self.sw_documentation_textEdit, 12, 1, 1, 1)
        # self.sw_documentation_label = QtWidgets.QLabel(self.setup_widget)
        # self.sw_documentation_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        # self.sw_documentation_label.setObjectName("sw_documentation_label")
        # self.gridLayout_7.addWidget(self.sw_documentation_label, 12, 0, 1, 1)

        # Header 2
        self.sw_header2_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_header2_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.sw_header2_label.setObjectName("sw_header2_label")
        self.gridLayout_7.addWidget(self.sw_header2_label, 5, 0, 1, 1)

        # Current LCD number widget
        self.sw_source_vc_horizonalLayout = QtWidgets.QHBoxLayout()

        self.sw_current_lcdNumber = QtWidgets.QLCDNumber(self.setup_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sw_current_lcdNumber.sizePolicy().hasHeightForWidth()
        )
        self.sw_current_lcdNumber.setSizePolicy(sizePolicy)
        self.sw_current_lcdNumber.setDigitCount(10)
        self.sw_current_lcdNumber.setAutoFillBackground(False)
        self.sw_current_lcdNumber.setSmallDecimalPoint(False)
        self.sw_current_lcdNumber.setObjectName("sw_current_lcdNumber")
        # self.sw_current_lcdNumber.display("2 A")

        # Voltage LCD number widget
        self.sw_voltage_lcdNumber = QtWidgets.QLCDNumber(self.setup_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sw_voltage_lcdNumber.sizePolicy().hasHeightForWidth()
        )
        self.sw_voltage_lcdNumber.setSizePolicy(sizePolicy)
        self.sw_voltage_lcdNumber.setDigitCount(10)
        self.sw_voltage_lcdNumber.setAutoFillBackground(False)
        self.sw_voltage_lcdNumber.setSmallDecimalPoint(False)
        self.sw_voltage_lcdNumber.setObjectName("sw_voltage_lcdNumber")
        # self.sw_voltage_lcdNumber.display("10 U")

        # Frequency LCD number widget
        self.sw_frequency_lcdNumber = QtWidgets.QLCDNumber(self.setup_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sw_frequency_lcdNumber.sizePolicy().hasHeightForWidth()
        )
        self.sw_frequency_lcdNumber.setSizePolicy(sizePolicy)
        self.sw_frequency_lcdNumber.setDigitCount(10)
        self.sw_frequency_lcdNumber.setAutoFillBackground(False)
        self.sw_frequency_lcdNumber.setSmallDecimalPoint(False)
        self.sw_frequency_lcdNumber.setObjectName("sw_frequency_lcdNumber")

        # capacitance LCD number widget
        self.sw_capacitance_lcdNumber = QtWidgets.QLCDNumber(self.setup_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sw_capacitance_lcdNumber.sizePolicy().hasHeightForWidth()
        )
        self.sw_capacitance_lcdNumber.setSizePolicy(sizePolicy)
        self.sw_capacitance_lcdNumber.setDigitCount(10)
        self.sw_capacitance_lcdNumber.setAutoFillBackground(False)
        self.sw_capacitance_lcdNumber.setSmallDecimalPoint(False)
        self.sw_capacitance_lcdNumber.setObjectName("sw_capacitance_lcdNumber")

        self.sw_source_vc_horizonalLayout.addWidget(self.sw_voltage_lcdNumber)
        self.sw_source_vc_horizonalLayout.addWidget(self.sw_current_lcdNumber)
        self.sw_source_vc_horizonalLayout.addWidget(self.sw_frequency_lcdNumber)
        self.sw_source_vc_horizonalLayout.addWidget(self.sw_capacitance_lcdNumber)

        self.gridLayout_7.addLayout(self.sw_source_vc_horizonalLayout, 6, 0, 1, 2)

        # Setup widget current tester voltage
        # self.sw_change_voltage_label = QtWidgets.QLabel(self.setup_widget)
        # self.sw_change_voltage_label.setObjectName("sw_change_voltage_label")
        # self.gridLayout_7.addWidget(self.sw_change_voltage_label, 6, 0, 1, 1)

        self.sw_set_vc_horizontalLayout = QtWidgets.QHBoxLayout()

        self.sw_voltage_spinBox = QtWidgets.QDoubleSpinBox(self.setup_widget)
        self.sw_voltage_spinBox.setObjectName("sw_voltage_spinBox")
        self.sw_set_vc_horizontalLayout.addWidget(self.sw_voltage_spinBox)

        self.sw_current_spinBox = QtWidgets.QDoubleSpinBox(self.setup_widget)
        self.sw_current_spinBox.setObjectName("sw_current_spinBox")
        self.sw_set_vc_horizontalLayout.addWidget(self.sw_current_spinBox)

        self.sw_frequency_spinBox = QtWidgets.QDoubleSpinBox(self.setup_widget)
        self.sw_frequency_spinBox.setObjectName("sw_frequency_spinBox")
        self.sw_set_vc_horizontalLayout.addWidget(self.sw_frequency_spinBox)

        self.sw_capacitance_spinBox = QtWidgets.QDoubleSpinBox(self.setup_widget)
        self.sw_capacitance_spinBox.setObjectName("sw_capacitance_spinBox")
        self.sw_set_vc_horizontalLayout.addWidget(self.sw_capacitance_spinBox)

        self.gridLayout_7.addLayout(self.sw_set_vc_horizontalLayout, 7, 0, 1, 2)

        self.sw_set_buttons_gridLayout = QtWidgets.QGridLayout()

        self.sw_source_output_pushButton = QtWidgets.QPushButton(self.setup_widget)
        self.sw_source_output_pushButton.setObjectName("sw_source_output_pushButton")
        self.gridLayout_7.addWidget(self.sw_source_output_pushButton, 8, 0, 1, 2)

        self.tabWidget.addTab(self.setup_widget, "")

        # -------------------------------------------------------------------- #
        # ---------------------- Define Spectrum Widget ---------------------- #
        # -------------------------------------------------------------------- #
        self.spectrum_widget = QtWidgets.QWidget()
        self.spectrum_widget.setObjectName("spectrum_widget")
        self.spectrum_widget_gridLayout = QtWidgets.QGridLayout(self.spectrum_widget)
        self.spectrum_widget_gridLayout.setObjectName("spectrum_widget_gridLayout")

        # --------------- Central Widget with matplotlib graph --------------- #
        self.specw_graph_widget = QtWidgets.QWidget(self.spectrum_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.specw_graph_widget.sizePolicy().hasHeightForWidth()
        )
        self.specw_graph_widget.setSizePolicy(sizePolicy)
        self.specw_graph_widget.setMinimumSize(QtCore.QSize(0, 442))
        self.specw_graph_widget.setObjectName("specw_graph_widget")
        self.specw_mpl_graph_gridLayout = QtWidgets.QGridLayout(self.specw_graph_widget)
        self.specw_mpl_graph_gridLayout.setObjectName("specw_mpl_graph_gridLayout")
        self.spectrum_widget_gridLayout.addWidget(self.specw_graph_widget, 0, 1, 1, 1)

        # Define figure
        figureSize = (11, 10)
        self.specw_fig = FigureCanvas(Figure(figsize=figureSize))
        self.specw_mpl_graph_gridLayout.addWidget(self.specw_fig)

        self.specw_ax = self.specw_fig.figure.subplots()
        self.specw_ax.set_facecolor("#E0E0E0")
        self.specw_ax.grid(True)
        self.specw_ax.set_xlabel("Frequency (kHz)", fontsize=14)
        self.specw_ax.set_ylabel("Current (A)", fontsize=14)
        self.specw_ax.set_xlim([50, 600])

        self.specw_ax.axhline(linewidth=1, color="black")
        self.specw_ax.axvline(linewidth=1, color="black")

        self.specw_ax2 = self.specw_ax.twinx()
        self.specw_ax2.set_ylabel(
            "VPP (V)",
            fontsize=14,
        )

        self.specw_fig.figure.set_facecolor("#E0E0E0")
        self.specw_mplToolbar = NavigationToolbar(
            self.specw_fig, self.specw_graph_widget
        )
        self.specw_mplToolbar.setStyleSheet("background-color:#E0E0E0;")
        self.specw_mpl_graph_gridLayout.addWidget(self.specw_mplToolbar)

        # ----------------------- Define scroll area ---------------------------
        self.specw_scrollArea = QtWidgets.QScrollArea(self.spectrum_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.specw_scrollArea.sizePolicy().hasHeightForWidth()
        )
        self.specw_scrollArea.setSizePolicy(sizePolicy)
        self.specw_scrollArea.setMinimumSize(QtCore.QSize(200, 0))
        self.specw_scrollArea.setWidgetResizable(True)
        self.specw_scrollArea.setObjectName("specw_scrollArea")
        self.specw_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.specw_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 170, 655))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.specw_scrollAreaWidgetContents.sizePolicy().hasHeightForWidth()
        )
        self.specw_scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.specw_scrollAreaWidgetContents.setObjectName(
            "specw_scrollAreaWidgetContents"
        )
        self.specw_scrollArea_gridLayout = QtWidgets.QGridLayout(
            self.specw_scrollAreaWidgetContents
        )
        self.specw_scrollArea_gridLayout.setObjectName("specw_scrollArea_gridLayout")

        self.specw_header1_label = QtWidgets.QLabel(self.specw_scrollAreaWidgetContents)
        self.specw_header1_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.specw_header1_label.setObjectName("specw_header1_label")
        self.specw_scrollArea_gridLayout.addWidget(self.specw_header1_label, 0, 0, 1, 1)
        self.specw_scrollArea.setWidget(self.specw_scrollAreaWidgetContents)
        self.spectrum_widget_gridLayout.addWidget(self.specw_scrollArea, 0, 3, 1, 1)

        # Set voltage
        self.specw_voltage_label = QtWidgets.QLabel(self.specw_scrollAreaWidgetContents)
        self.specw_voltage_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.specw_voltage_label.setObjectName("specw_voltage_label")
        self.specw_scrollArea_gridLayout.addWidget(self.specw_voltage_label, 1, 0, 1, 1)
        self.specw_voltage_spinBox = QtWidgets.QDoubleSpinBox(
            self.specw_scrollAreaWidgetContents
        )
        self.specw_voltage_spinBox.setObjectName("specw_voltage_spinBox")
        self.specw_scrollArea_gridLayout.addWidget(
            self.specw_voltage_spinBox, 2, 0, 1, 1
        )

        # Set current limit
        self.specw_current_label = QtWidgets.QLabel(self.specw_scrollAreaWidgetContents)
        self.specw_current_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.specw_current_label.setObjectName("specw_current_label")
        self.specw_scrollArea_gridLayout.addWidget(self.specw_current_label, 3, 0, 1, 1)
        self.specw_current_spinBox = QtWidgets.QDoubleSpinBox(
            self.specw_scrollAreaWidgetContents
        )
        self.specw_current_spinBox.setObjectName("specw_current_spinBox")
        self.specw_scrollArea_gridLayout.addWidget(
            self.specw_current_spinBox, 4, 0, 1, 1
        )

        # Set minimum scan frequency
        self.specw_minimum_frequency_label = QtWidgets.QLabel(
            self.specw_scrollAreaWidgetContents
        )
        self.specw_minimum_frequency_label.setStyleSheet(
            'font: 63 bold 10pt "Segoe UI";'
        )
        self.specw_minimum_frequency_label.setObjectName(
            "specw_minimum_frequency_label"
        )
        self.specw_scrollArea_gridLayout.addWidget(
            self.specw_minimum_frequency_label, 5, 0, 1, 1
        )
        self.specw_minimum_frequency_spinBox = QtWidgets.QDoubleSpinBox(
            self.specw_scrollAreaWidgetContents
        )
        self.specw_minimum_frequency_spinBox.setObjectName(
            "specw_minimum_frequency_spinBox"
        )
        self.specw_scrollArea_gridLayout.addWidget(
            self.specw_minimum_frequency_spinBox, 6, 0, 1, 1
        )

        # Set maximum scan frequency
        self.specw_maximum_frequency_label = QtWidgets.QLabel(
            self.specw_scrollAreaWidgetContents
        )
        self.specw_maximum_frequency_label.setStyleSheet(
            'font: 63 bold 10pt "Segoe UI";'
        )
        self.specw_maximum_frequency_label.setObjectName(
            "specw_maximum_frequency_label"
        )
        self.specw_scrollArea_gridLayout.addWidget(
            self.specw_maximum_frequency_label, 7, 0, 1, 1
        )
        self.specw_maximum_frequency_spinBox = QtWidgets.QDoubleSpinBox(
            self.specw_scrollAreaWidgetContents
        )
        self.specw_maximum_frequency_spinBox.setObjectName(
            "specw_maximum_frequency_spinBox"
        )
        self.specw_scrollArea_gridLayout.addWidget(
            self.specw_maximum_frequency_spinBox, 8, 0, 1, 1
        )

        # Set frequency step
        self.specw_frequency_step_label = QtWidgets.QLabel(
            self.specw_scrollAreaWidgetContents
        )
        self.specw_frequency_step_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.specw_frequency_step_label.setObjectName("specw_frequency_step_label")
        self.specw_scrollArea_gridLayout.addWidget(
            self.specw_frequency_step_label, 9, 0, 1, 1
        )
        self.specw_frequency_step_spinBox = QtWidgets.QDoubleSpinBox(
            self.specw_scrollAreaWidgetContents
        )
        self.specw_frequency_step_spinBox.setObjectName("specw_frequency_step_spinBox")
        self.specw_scrollArea_gridLayout.addWidget(
            self.specw_frequency_step_spinBox, 10, 0, 1, 1
        )

        # Save Spectrum button
        self.specw_start_measurement_pushButton = QtWidgets.QPushButton(
            self.specw_scrollAreaWidgetContents
        )
        self.specw_start_measurement_pushButton.setObjectName(
            "specw_start_measurement_pushButton"
        )
        self.specw_scrollArea_gridLayout.addWidget(
            self.specw_start_measurement_pushButton, 11, 0, 1, 1
        )

        self.tabWidget.addTab(self.spectrum_widget, "")

        # -------------------------------------------------------------------- #
        # ------------------- Define capacitance Tester Widget ------------------ #
        # -------------------------------------------------------------------- #
        self.capacitance_tester_widget = QtWidgets.QWidget()
        self.capacitance_tester_widget.setObjectName("capacitance_tester_widget")
        self.capacitance_tester_gridLayout = QtWidgets.QGridLayout(
            self.capacitance_tester_widget
        )
        self.capacitance_tester_gridLayout.setObjectName(
            "capacitance_tester_gridLayout"
        )

        # --------------- Central Widget with matplotlib graph --------------- #
        self.capw_graph_widget = QtWidgets.QWidget(self.capacitance_tester_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.capw_graph_widget.sizePolicy().hasHeightForWidth()
        )
        self.capw_graph_widget.setSizePolicy(sizePolicy)
        self.capw_graph_widget.setMinimumSize(QtCore.QSize(0, 442))
        self.capw_graph_widget.setObjectName("capw_graph_widget")
        self.capw_mpl_graph_gridLayout = QtWidgets.QGridLayout(self.capw_graph_widget)
        self.capw_mpl_graph_gridLayout.setObjectName("capw_mpl_graph_gridLayout")
        self.capacitance_tester_gridLayout.addWidget(self.capw_graph_widget, 0, 1, 1, 1)

        # Define figure
        figureSize = (11, 10)
        self.capw_fig = FigureCanvas(Figure(figsize=figureSize))
        self.capw_mpl_graph_gridLayout.addWidget(self.capw_fig)

        self.capw_ax = self.capw_fig.figure.subplots()
        self.capw_ax.set_facecolor("#E0E0E0")
        self.capw_ax.grid(True)
        self.capw_ax.set_xlabel("Frequency (kHz)", fontsize=14)
        self.capw_ax.set_ylabel("Current (A)", fontsize=14)
        self.capw_ax.set_xlim([50, 600])

        self.capw_ax.axhline(linewidth=1, color="black")
        self.capw_ax.axvline(linewidth=1, color="black")

        self.capw_fig.figure.set_facecolor("#E0E0E0")
        self.capw_mplToolbar = NavigationToolbar(self.capw_fig, self.capw_graph_widget)
        self.capw_mplToolbar.setStyleSheet("background-color:#E0E0E0;")
        self.capw_mpl_graph_gridLayout.addWidget(self.capw_mplToolbar)

        # ----------------------- Define scroll area ---------------------------
        self.capw_scrollArea = QtWidgets.QScrollArea(self.capacitance_tester_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.capw_scrollArea.sizePolicy().hasHeightForWidth()
        )
        self.capw_scrollArea.setSizePolicy(sizePolicy)
        self.capw_scrollArea.setMinimumSize(QtCore.QSize(200, 0))
        self.capw_scrollArea.setWidgetResizable(True)
        self.capw_scrollArea.setObjectName("capw_scrollArea")
        self.capw_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.capw_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 170, 655))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.capw_scrollAreaWidgetContents.sizePolicy().hasHeightForWidth()
        )
        self.capw_scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.capw_scrollAreaWidgetContents.setObjectName(
            "capw_scrollAreaWidgetContents"
        )
        self.capw_scrollArea_gridLayout = QtWidgets.QGridLayout(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_scrollArea_gridLayout.setObjectName("capw_scrollArea_gridLayout")

        self.capw_header1_label = QtWidgets.QLabel(self.capw_scrollAreaWidgetContents)
        self.capw_header1_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.capw_header1_label.setObjectName("capw_header1_label")
        self.capw_scrollArea_gridLayout.addWidget(self.capw_header1_label, 0, 0, 1, 1)
        self.capw_scrollArea.setWidget(self.capw_scrollAreaWidgetContents)
        self.capacitance_tester_gridLayout.addWidget(self.capw_scrollArea, 0, 3, 1, 1)

        # Set voltage
        self.capw_voltage_label = QtWidgets.QLabel(self.capw_scrollAreaWidgetContents)
        self.capw_voltage_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.capw_voltage_label.setObjectName("capw_voltage_label")
        self.capw_scrollArea_gridLayout.addWidget(self.capw_voltage_label, 1, 0, 1, 1)
        self.capw_voltage_spinBox = QtWidgets.QDoubleSpinBox(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_voltage_spinBox.setObjectName("capw_voltage_spinBox")
        self.capw_scrollArea_gridLayout.addWidget(self.capw_voltage_spinBox, 2, 0, 1, 1)

        # Set current limit
        self.capw_current_label = QtWidgets.QLabel(self.capw_scrollAreaWidgetContents)
        self.capw_current_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.capw_current_label.setObjectName("capw_current_label")
        self.capw_scrollArea_gridLayout.addWidget(self.capw_current_label, 3, 0, 1, 1)
        self.capw_current_spinBox = QtWidgets.QDoubleSpinBox(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_current_spinBox.setObjectName("capw_current_spinBox")
        self.capw_scrollArea_gridLayout.addWidget(self.capw_current_spinBox, 4, 0, 1, 1)

        # Set minimum scan frequency
        self.capw_minimum_frequency_label = QtWidgets.QLabel(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_minimum_frequency_label.setStyleSheet(
            'font: 63 bold 10pt "Segoe UI";'
        )
        self.capw_minimum_frequency_label.setObjectName("capw_minimum_frequency_label")
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_minimum_frequency_label, 5, 0, 1, 1
        )
        self.capw_minimum_frequency_spinBox = QtWidgets.QDoubleSpinBox(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_minimum_frequency_spinBox.setObjectName(
            "capw_minimum_frequency_spinBox"
        )
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_minimum_frequency_spinBox, 6, 0, 1, 1
        )

        # Set maximum scan frequency
        self.capw_maximum_frequency_label = QtWidgets.QLabel(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_maximum_frequency_label.setStyleSheet(
            'font: 63 bold 10pt "Segoe UI";'
        )
        self.capw_maximum_frequency_label.setObjectName("capw_maximum_frequency_label")
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_maximum_frequency_label, 7, 0, 1, 1
        )
        self.capw_maximum_frequency_spinBox = QtWidgets.QDoubleSpinBox(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_maximum_frequency_spinBox.setObjectName(
            "capw_maximum_frequency_spinBox"
        )
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_maximum_frequency_spinBox, 8, 0, 1, 1
        )

        # Set frequency step
        self.capw_frequency_step_label = QtWidgets.QLabel(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_frequency_step_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.capw_frequency_step_label.setObjectName("capw_frequency_step_label")
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_frequency_step_label, 9, 0, 1, 1
        )
        self.capw_frequency_step_spinBox = QtWidgets.QDoubleSpinBox(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_frequency_step_spinBox.setObjectName("capw_frequency_step_spinBox")
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_frequency_step_spinBox, 10, 0, 1, 1
        )

        # Set minimum capacitance
        self.capw_minimum_capacitance_label = QtWidgets.QLabel(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_minimum_capacitance_label.setStyleSheet(
            'font: 63 bold 10pt "Segoe UI";'
        )
        self.capw_minimum_capacitance_label.setObjectName(
            "capw_minimum_capacitance_label"
        )
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_minimum_capacitance_label, 11, 0, 1, 1
        )
        self.capw_minimum_capacitance_spinBox = QtWidgets.QDoubleSpinBox(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_minimum_capacitance_spinBox.setObjectName(
            "capw_minimum_capacitance_spinBox"
        )
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_minimum_capacitance_spinBox, 12, 0, 1, 1
        )

        # Set maximum scan capacitance
        self.capw_maximum_capacitance_label = QtWidgets.QLabel(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_maximum_capacitance_label.setStyleSheet(
            'font: 63 bold 10pt "Segoe UI";'
        )
        self.capw_maximum_capacitance_label.setObjectName(
            "capw_maximum_capacitance_label"
        )
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_maximum_capacitance_label, 13, 0, 1, 1
        )
        self.capw_maximum_capacitance_spinBox = QtWidgets.QDoubleSpinBox(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_maximum_capacitance_spinBox.setObjectName(
            "capw_maximum_capacitance_spinBox"
        )
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_maximum_capacitance_spinBox, 14, 0, 1, 1
        )

        # Set Frequency Margin around the resonance frequency
        self.capw_frequency_margin_label = QtWidgets.QLabel(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_frequency_margin_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.capw_frequency_margin_label.setObjectName("capw_frequency_margin_label")
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_frequency_margin_label, 15, 0, 1, 1
        )
        self.capw_frequency_margin_spinBox = QtWidgets.QDoubleSpinBox(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_frequency_margin_spinBox.setObjectName(
            "capw_frequency_margin_spinBox"
        )
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_frequency_margin_spinBox, 16, 0, 1, 1
        )

        # Save Spectrum button
        self.capw_start_measurement_pushButton = QtWidgets.QPushButton(
            self.capw_scrollAreaWidgetContents
        )
        self.capw_start_measurement_pushButton.setObjectName(
            "capw_start_measurement_pushButton"
        )
        self.capw_scrollArea_gridLayout.addWidget(
            self.capw_start_measurement_pushButton, 17, 0, 1, 1
        )

        self.tabWidget.addTab(self.capacitance_tester_widget, "")

        # -------------------------------------------------------------------- #
        # ----------------------- Define Osci Widget-------------------------- #
        # -------------------------------------------------------------------- #
        self.osci_widget = QtWidgets.QWidget()
        self.osci_widget.setObjectName("osci_widget")
        self.osci_widget_gridLayout = QtWidgets.QGridLayout(self.osci_widget)
        self.osci_widget_gridLayout.setObjectName("osci_widget_gridLayout")

        # --------------- Central Widget with matplotlib graph --------------- #
        self.ow_graph_widget = QtWidgets.QWidget(self.osci_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ow_graph_widget.sizePolicy().hasHeightForWidth()
        )
        self.ow_graph_widget.setSizePolicy(sizePolicy)
        self.ow_graph_widget.setMinimumSize(QtCore.QSize(0, 442))
        self.ow_graph_widget.setObjectName("ow_graph_widget")
        self.ow_mpl_graph_gridLayout = QtWidgets.QGridLayout(self.ow_graph_widget)
        self.ow_mpl_graph_gridLayout.setObjectName("ow_mpl_graph_gridLayout")
        self.osci_widget_gridLayout.addWidget(self.ow_graph_widget, 0, 1, 1, 1)

        # Define figure
        figureSize = (11, 10)
        self.ow_fig = FigureCanvas(Figure(figsize=figureSize))
        self.ow_mpl_graph_gridLayout.addWidget(self.ow_fig)

        self.ow_ax = self.ow_fig.figure.subplots()
        self.ow_ax.set_facecolor("#E0E0E0")
        self.ow_ax.grid(True)
        self.ow_ax.set_xlabel("Time (s)", fontsize=14)
        self.ow_ax.set_ylabel("Voltage (V)", fontsize=14)
        self.ow_ax.set_xlim([50, 600])

        self.ow_ax.axhline(linewidth=1, color="black")
        self.ow_ax.axvline(linewidth=1, color="black")

        self.ow_fig.figure.set_facecolor("#E0E0E0")
        self.ow_mplToolbar = NavigationToolbar(self.ow_fig, self.ow_graph_widget)
        self.ow_mplToolbar.setStyleSheet("background-color:#E0E0E0;")
        self.ow_mpl_graph_gridLayout.addWidget(self.ow_mplToolbar)

        # ----------------------- Define scroll area ---------------------------
        self.ow_scrollArea = QtWidgets.QScrollArea(self.osci_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ow_scrollArea.sizePolicy().hasHeightForWidth()
        )
        self.ow_scrollArea.setSizePolicy(sizePolicy)
        self.ow_scrollArea.setMinimumSize(QtCore.QSize(200, 0))
        self.ow_scrollArea.setWidgetResizable(True)
        self.ow_scrollArea.setObjectName("ow_scrollArea")
        self.ow_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.ow_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 170, 655))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ow_scrollAreaWidgetContents.sizePolicy().hasHeightForWidth()
        )
        self.ow_scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.ow_scrollAreaWidgetContents.setObjectName("ow_scrollAreaWidgetContents")
        self.ow_scrollArea_gridLayout = QtWidgets.QGridLayout(
            self.ow_scrollAreaWidgetContents
        )
        self.ow_scrollArea_gridLayout.setObjectName("ow_scrollArea_gridLayout")

        self.ow_header1_label = QtWidgets.QLabel(self.ow_scrollAreaWidgetContents)
        self.ow_header1_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.ow_header1_label.setObjectName("ow_header1_label")
        self.ow_scrollArea_gridLayout.addWidget(self.ow_header1_label, 0, 0, 1, 1)
        self.ow_scrollArea.setWidget(self.ow_scrollAreaWidgetContents)
        self.osci_widget_gridLayout.addWidget(self.ow_scrollArea, 0, 3, 1, 1)

        # Set voltage
        self.ow_voltage_label = QtWidgets.QLabel(self.ow_scrollAreaWidgetContents)
        self.ow_voltage_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.ow_voltage_label.setObjectName("ow_voltage_label")
        self.ow_scrollArea_gridLayout.addWidget(self.ow_voltage_label, 1, 0, 1, 1)
        self.ow_voltage_spinBox = QtWidgets.QDoubleSpinBox(
            self.ow_scrollAreaWidgetContents
        )
        self.ow_voltage_spinBox.setObjectName("ow_voltage_spinBox")
        self.ow_scrollArea_gridLayout.addWidget(self.ow_voltage_spinBox, 2, 0, 1, 1)

        # Set current limit
        self.ow_current_label = QtWidgets.QLabel(self.ow_scrollAreaWidgetContents)
        self.ow_current_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.ow_current_label.setObjectName("ow_current_label")
        self.ow_scrollArea_gridLayout.addWidget(self.ow_current_label, 3, 0, 1, 1)
        self.ow_current_spinBox = QtWidgets.QDoubleSpinBox(
            self.ow_scrollAreaWidgetContents
        )
        self.ow_current_spinBox.setObjectName("ow_current_spinBox")
        self.ow_scrollArea_gridLayout.addWidget(self.ow_current_spinBox, 4, 0, 1, 1)

        # Set minimum scan frequency
        self.ow_minimum_frequency_label = QtWidgets.QLabel(
            self.ow_scrollAreaWidgetContents
        )
        self.ow_minimum_frequency_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.ow_minimum_frequency_label.setObjectName("ow_minimum_frequency_label")
        self.ow_scrollArea_gridLayout.addWidget(
            self.ow_minimum_frequency_label, 5, 0, 1, 1
        )
        self.ow_minimum_frequency_spinBox = QtWidgets.QDoubleSpinBox(
            self.ow_scrollAreaWidgetContents
        )
        self.ow_minimum_frequency_spinBox.setObjectName("ow_minimum_frequency_spinBox")
        self.ow_scrollArea_gridLayout.addWidget(
            self.ow_minimum_frequency_spinBox, 6, 0, 1, 1
        )

        # Set maximum scan frequency
        self.ow_maximum_frequency_label = QtWidgets.QLabel(
            self.ow_scrollAreaWidgetContents
        )
        self.ow_maximum_frequency_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.ow_maximum_frequency_label.setObjectName("ow_maximum_frequency_label")
        self.ow_scrollArea_gridLayout.addWidget(
            self.ow_maximum_frequency_label, 7, 0, 1, 1
        )
        self.ow_maximum_frequency_spinBox = QtWidgets.QDoubleSpinBox(
            self.ow_scrollAreaWidgetContents
        )
        self.ow_maximum_frequency_spinBox.setObjectName("ow_maximum_frequency_spinBox")
        self.ow_scrollArea_gridLayout.addWidget(
            self.ow_maximum_frequency_spinBox, 8, 0, 1, 1
        )

        # Set frequency step
        self.ow_frequency_step_label = QtWidgets.QLabel(
            self.ow_scrollAreaWidgetContents
        )
        self.ow_frequency_step_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.ow_frequency_step_label.setObjectName("ow_frequency_step_label")
        self.ow_scrollArea_gridLayout.addWidget(
            self.ow_frequency_step_label, 9, 0, 1, 1
        )
        self.ow_frequency_step_spinBox = QtWidgets.QDoubleSpinBox(
            self.ow_scrollAreaWidgetContents
        )
        self.ow_frequency_step_spinBox.setObjectName("ow_frequency_step_spinBox")
        self.ow_scrollArea_gridLayout.addWidget(
            self.ow_frequency_step_spinBox, 10, 0, 1, 1
        )

        # Auto Scale
        self.ow_auto_scale_pushButton = QtWidgets.QPushButton(
            self.ow_scrollAreaWidgetContents
        )
        self.ow_auto_scale_pushButton.setObjectName("ow_auto_scale_pushButton")
        self.ow_scrollArea_gridLayout.addWidget(
            self.ow_auto_scale_pushButton, 11, 0, 1, 1
        )

        # Stop
        self.ow_stop_pushButton = QtWidgets.QPushButton(
            self.ow_scrollAreaWidgetContents
        )
        self.ow_stop_pushButton.setObjectName("ow_stop_pushButton")
        self.ow_stop_pushButton.setCheckable(True)
        self.ow_scrollArea_gridLayout.addWidget(self.ow_stop_pushButton, 12, 0, 1, 1)

        # Save osci button
        self.ow_start_measurement_pushButton = QtWidgets.QPushButton(
            self.ow_scrollAreaWidgetContents
        )
        self.ow_start_measurement_pushButton.setObjectName(
            "ow_start_measurement_pushButton"
        )
        self.ow_scrollArea_gridLayout.addWidget(
            self.ow_start_measurement_pushButton, 13, 0, 1, 1
        )

        self.tabWidget.addTab(self.osci_widget, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        # -------------------------------------------------------------------- #
        # ------------------------- Define Menubar --------------------------- #
        # -------------------------------------------------------------------- #

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 973, 31))
        self.menubar.setObjectName("menubar")
        self.menudfg = QtWidgets.QMenu(self.menubar)
        self.menudfg.setObjectName("menudfg")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)

        # Define actions for menubar
        self.actionOpen_Logs = QtWidgets.QAction(MainWindow)
        self.actionOpen_Logs.setObjectName("actionOpen_Logs")
        # self.actionOpen_Logfile_on_Machine = QtWidgets.QAction(MainWindow)
        # self.actionOpen_Logfile_on_Machine.setObjectName(
        # "actionOpen_Logfile_on_Machine"
        # )

        self.actionChange_Path = QtWidgets.QAction(MainWindow)
        self.actionChange_Path.setObjectName("actionChange_Path")

        self.actionOptions = QtWidgets.QAction(MainWindow)
        self.actionOptions.setObjectName("actionOptions")

        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")

        self.actionLoad_Measurement_Parameters = QtWidgets.QAction(MainWindow)
        self.actionLoad_Measurement_Parameters.setObjectName(
            "actionLoad_Measurement_Parameters"
        )
        self.actionSave_Measurement_Parameters = QtWidgets.QAction(MainWindow)
        self.actionSave_Measurement_Parameters.setObjectName(
            "actionSave_Measurement_Parameters"
        )
        self.actionOpen_Log = QtWidgets.QAction(MainWindow)
        self.actionOpen_Log.setObjectName("actionOpen_Log")
        self.menudfg.addAction(self.actionLoad_Measurement_Parameters)
        self.menudfg.addAction(self.actionSave_Measurement_Parameters)
        self.menuSettings.addAction(self.actionOptions)
        self.menuSettings.addAction(self.actionDocumentation)
        self.menuSettings.addAction(self.actionOpen_Log)
        self.menubar.addAction(self.menudfg.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        # -------------------------------------------------------------------- #
        # ----------------------- Define Statusbar --------------------------- #
        # -------------------------------------------------------------------- #

        # Define progress bar in the status bar
        self.progressBar = QtWidgets.QProgressBar()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(150, 15))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet(
            "QProgressBar"
            "{"
            "border-radius: 5px;"
            "background-color: #E0E0E0;"
            "text-align: center;"
            "color: black;"
            'font: 63 bold 10pt "Segoe UI";'
            "}"
            "QProgressBar::chunk "
            "{"
            "background-color: rgb(85, 170, 255);"
            "border-radius: 5px;"
            "}"
        )

        # Define the statusbar itself
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setToolTip("")
        self.statusbar.setStatusTip("")
        self.statusbar.setWhatsThis("")
        self.statusbar.setAccessibleName("")
        self.statusbar.setObjectName("statusbar")
        self.statusbar.addPermanentWidget(self.progressBar)
        self.statusbar.showMessage("Ready", 10000000)

        MainWindow.setStatusBar(self.statusbar)

        # -------------------------------------------------------------------- #
        # --------------------- Some General things -------------------------- #
        # -------------------------------------------------------------------- #
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        This function basicall contains all the text that is visible in the window.
        I think it is good practice to keep this seperate just in case the program
        would be translated to other languages.
        """

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ME Device Benchmarker"))
        # self.gatherlab_label.setText(
        # _translate("MainWindow", "Gatherlab JVL Measurement")
        # )
        # self.sw_header2_label.setText(
        # _translate("MainWindow", "Source Voltage & Current")
        # )
        self.sw_browse_pushButton.setText(_translate("MainWindow", "Browse"))
        self.sw_voltage_spinBox.setSuffix(_translate("MainWindow", " V"))
        self.sw_current_spinBox.setSuffix(_translate("MainWindow", " A"))
        self.sw_frequency_spinBox.setSuffix(_translate("MainWindow", " kHz"))
        self.sw_capacitance_spinBox.setSuffix(_translate("MainWindow", " pF"))
        self.sw_source_output_pushButton.setText(
            _translate("MainWindow", "Output On/Off")
        )
        self.sw_batch_name_label.setText(_translate("MainWindow", "Batch Name"))
        self.sw_device_number_label.setText(_translate("MainWindow", "Device Number"))
        self.sw_header1_label.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>The file name the data is saved in in the end"
                " will be in the format"
                " yyyy-mm-dd_&lt;batch-name&gt;_d&lt;device-number&gt;_p&lt;pixel-number&gt;.csv.</p></body></html>",
            )
        )
        self.sw_header1_label.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Dashboard that shows the current values of the important parameters.</p></body></html>",
            )
        )
        self.sw_header1_label.setText(
            _translate("MainWindow", "Batch Name and File Path")
        )
        self.sw_header2_label.setText(_translate("MainWindow", "Current Parameters"))
        # self.sw_change_voltage_label.setText(
        # _translate("MainWindow", "Change Voltage (V)")
        # )
        # self.sw_documentation_label.setToolTip(
        # _translate(
        # "MainWindow",
        # "<html><head/><body><p>Please write here any comments to the"
        # " measurement of your batch. The comments will be saved as .md file"
        # " within your selected file path. If there are any issues with the"
        # " measurement setup or the software document it in a seperate line"
        # " starting with [!] to ensure easy debugging.</p></body></html>",
        # )
        # )
        # self.sw_documentation_label.setText(_translate("MainWindow", "Documentation"))
        self.sw_folder_path_label.setText(_translate("MainWindow", "Folder Path"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.setup_widget), _translate("MainWindow", "Setup")
        )
        # self.specw_max_voltage_label.setText(
        # _translate("MainWindow", "Max Voltage (V)")
        # )
        self.specw_voltage_label.setText(_translate("MainWindow", "Voltage (V)"))
        self.specw_current_label.setText(
            _translate("MainWindow", "Current Compliance (A)")
        )
        self.specw_minimum_frequency_label.setText(
            _translate("MainWindow", "Min Frequency (kHz)")
        )
        self.specw_maximum_frequency_label.setText(
            _translate("MainWindow", "Max Frequency (kHz)")
        )
        self.specw_frequency_step_label.setText(
            _translate("MainWindow", "Frequency Step (kHz)")
        )
        self.specw_voltage_spinBox.setSuffix(_translate("MainWindow", " V"))
        self.specw_current_spinBox.setSuffix(_translate("MainWindow", " A"))
        self.specw_minimum_frequency_spinBox.setSuffix(_translate("MainWindow", " kHz"))
        self.specw_maximum_frequency_spinBox.setSuffix(_translate("MainWindow", " kHz"))
        self.specw_frequency_step_spinBox.setSuffix(_translate("MainWindow", " kHz"))
        self.specw_start_measurement_pushButton.setText(
            _translate("MainWindow", "Start Measurement")
        )
        self.specw_header1_label.setText(
            _translate("MainWindow", "Measurement Parameters")
        )

        self.capw_voltage_label.setText(_translate("MainWindow", "Voltage (V)"))
        self.capw_current_label.setText(
            _translate("MainWindow", "Current Compliance (A)")
        )
        self.capw_minimum_frequency_label.setText(
            _translate("MainWindow", "Min Frequency (kHz)")
        )
        self.capw_maximum_frequency_label.setText(
            _translate("MainWindow", "Max Frequency (kHz)")
        )
        self.capw_frequency_step_label.setText(
            _translate("MainWindow", "Frequency Step (kHz)")
        )
        self.capw_voltage_spinBox.setSuffix(_translate("MainWindow", " V"))
        self.capw_current_spinBox.setSuffix(_translate("MainWindow", " A"))
        self.capw_minimum_frequency_spinBox.setSuffix(_translate("MainWindow", " kHz"))
        self.capw_maximum_frequency_spinBox.setSuffix(_translate("MainWindow", " kHz"))
        self.capw_frequency_step_spinBox.setSuffix(_translate("MainWindow", " kHz"))
        self.capw_start_measurement_pushButton.setText(
            _translate("MainWindow", "Start Measurement")
        )
        self.capw_header1_label.setText(
            _translate("MainWindow", "Measurement Parameters")
        )
        self.capw_minimum_capacitance_label.setText(
            _translate("MainWindow", "Min Capacitance (pF)")
        )
        self.capw_maximum_capacitance_label.setText(
            _translate("MainWindow", "Max Capacitance (pF)")
        )
        self.capw_frequency_margin_label.setText(
            _translate("MainWindow", "Frequency Margin (kHz)")
        )

        self.ow_voltage_label.setText(_translate("MainWindow", "Voltage (V)"))
        self.ow_current_label.setText(
            _translate("MainWindow", "Current Compliance (A)")
        )
        self.ow_minimum_frequency_label.setText(
            _translate("MainWindow", "Min Frequency (kHz)")
        )
        self.ow_maximum_frequency_label.setText(
            _translate("MainWindow", "Max Frequency (kHz)")
        )
        self.ow_frequency_step_label.setText(
            _translate("MainWindow", "Frequency Step (kHz)")
        )
        self.ow_voltage_spinBox.setSuffix(_translate("MainWindow", " V"))
        self.ow_current_spinBox.setSuffix(_translate("MainWindow", " A"))
        self.ow_minimum_frequency_spinBox.setSuffix(_translate("MainWindow", " kHz"))
        self.ow_maximum_frequency_spinBox.setSuffix(_translate("MainWindow", " kHz"))
        self.ow_frequency_step_spinBox.setSuffix(_translate("MainWindow", " kHz"))

        # self.specw_changeover_voltage_label.setText(
        # _translate("MainWindow", "Changeover Voltage (V)")
        # )
        # self.specw_low_voltage_step_label.setText(
        # _translate("MainWindow", "Low Voltage Step (V)")
        # )
        # self.specw_scan_compliance_label.setText(
        # _translate("MainWindow", "Scan Compliance (A)")
        # )
        # self.specw_pd_saturation_checkBox.setText(
        # _translate("MainWindow", "Check for PD Saturation")
        # )
        # self.specw_select_pixel_label.setText(_translate("MainWindow", "Select Pixels"))
        # self.specw_bad_contact_checkBox.setText(
        # _translate("MainWindow", "Check fo Bad Contacts")
        # )

        self.ow_stop_pushButton.setText(_translate("MainWindow", "Run/Stop"))
        self.ow_auto_scale_pushButton.setText(_translate("MainWindow", "Auto Scale"))
        self.ow_start_measurement_pushButton.setText(
            _translate("MainWindow", "Save Data")
        )
        self.ow_header1_label.setText(_translate("MainWindow", "Osci Parameters"))

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.spectrum_widget),
            _translate("MainWindow", "Frequency Scan"),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.capacitance_tester_widget),
            _translate("MainWindow", "Capacitance Scan"),
        )

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.osci_widget),
            _translate("MainWindow", "Oscilloscope"),
        )

        self.menudfg.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))

        # self.actionOpen_Logs.setText(_translate("MainWindow", "Open Logs"))
        # self.actionOpen_Logfile_on_Machine.setText(
        # _translate("MainWindow", "Open Logfile on Machine")
        # )
        self.actionChange_Path.setText(_translate("MainWindow", "Change Saving Path"))
        self.actionOptions.setText(_translate("MainWindow", "Options"))
        self.actionDocumentation.setText(_translate("MainWindow", "Help"))
        self.actionLoad_Measurement_Parameters.setText(
            _translate("MainWindow", "Load Measurement Parameters")
        )
        self.actionSave_Measurement_Parameters.setText(
            _translate("MainWindow", "Save Measurement Settings")
        )
        self.actionOpen_Log.setText(_translate("MainWindow", "Open Log"))

    # ------------------------------------------------------------------------ #
    # ----------------- User Defined UI related Functions -------------------- #
    # ------------------------------------------------------------------------ #
    def center(self):
        # position and size of main window

        # self.showFullScreen()
        qc = self.frameGeometry()
        # desktopWidget = QtWidgets.QApplication.desktop()
        # PCGeometry = desktopWidget.screenGeometry()
        # self.resize(PCGeometry.height(), PCGeometry.height())
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qc.moveCenter(cp)
        self.move(qc.topLeft())
