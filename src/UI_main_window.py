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

        # Setup widget header
        self.sw_header2_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_header2_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.sw_header2_label.setObjectName("sw_header2_label")
        self.gridLayout_7.addWidget(self.sw_header2_label, 4, 0, 1, 1)

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

        # Setup widget current tester voltage
        self.sw_ct_voltage_spinBox = QtWidgets.QDoubleSpinBox(self.setup_widget)
        self.sw_ct_voltage_spinBox.setObjectName("sw_ct_voltage_spinBox")
        self.gridLayout_7.addWidget(self.sw_ct_voltage_spinBox, 8, 1, 1, 1)
        self.sw_change_voltage_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_change_voltage_label.setObjectName("sw_change_voltage_label")
        self.gridLayout_7.addWidget(self.sw_change_voltage_label, 8, 0, 1, 1)

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

        # Setup widget header 1
        self.sw_header1_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_header1_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.sw_header1_label.setObjectName("sw_header1_label")
        self.gridLayout_7.addWidget(self.sw_header1_label, 0, 0, 1, 1)

        # ------------- Setup widget, Select pixels to test ------------------ #
        self.sw_select_pixel_widget = QtWidgets.QWidget(self.setup_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sw_select_pixel_widget.sizePolicy().hasHeightForWidth()
        )
        self.sw_select_pixel_widget.setSizePolicy(sizePolicy)
        self.sw_select_pixel_widget.setMinimumSize(QtCore.QSize(100, 0))
        self.sw_select_pixel_widget.setMaximumSize(QtCore.QSize(171, 200))
        self.sw_select_pixel_widget.setObjectName("sw_select_pixel_widget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.sw_select_pixel_widget)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.sw_pixel_label = QtWidgets.QLabel(self.sw_select_pixel_widget)
        self.sw_pixel_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.sw_pixel_label.setObjectName("sw_pixel_label")
        self.gridLayout_6.addWidget(self.sw_pixel_label, 1, 0, 1, 1)

        # Activate local mode button
        self.sw_activate_local_mode_pushButton = QtWidgets.QPushButton(
            self.sw_select_pixel_widget
        )
        self.sw_activate_local_mode_pushButton.setObjectName(
            "sw_activate_local_mode_pushButton"
        )
        # self.sw_activate_local_mode_horizontalLayout.addWidget(self.sw_browse_pushButton)
        self.gridLayout_6.addWidget(self.sw_activate_local_mode_pushButton, 0, 0, 1, 2)

        # Pixel 1
        self.sw_pixel1_pushButton = QtWidgets.QPushButton(self.sw_select_pixel_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sw_pixel1_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.sw_pixel1_pushButton.setSizePolicy(sizePolicy)
        self.sw_pixel1_pushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.sw_pixel1_pushButton.setCheckable(True)
        self.sw_pixel1_pushButton.setChecked(False)
        self.sw_pixel1_pushButton.setAutoRepeat(False)
        self.sw_pixel1_pushButton.setObjectName("sw_pixel1_pushButton")
        self.gridLayout_6.addWidget(self.sw_pixel1_pushButton, 2, 0, 1, 1)

        # Pixel 2
        self.sw_pixel2_pushButton = QtWidgets.QPushButton(self.sw_select_pixel_widget)
        self.sw_pixel2_pushButton.setCheckable(True)
        self.sw_pixel2_pushButton.setChecked(False)
        self.sw_pixel2_pushButton.setObjectName("sw_pixel2_pushButton")
        self.gridLayout_6.addWidget(self.sw_pixel2_pushButton, 4, 0, 1, 1)

        # Pixel 3
        self.sw_pixel3_pushButton = QtWidgets.QPushButton(self.sw_select_pixel_widget)
        self.sw_pixel3_pushButton.setCheckable(True)
        self.sw_pixel3_pushButton.setChecked(False)
        self.sw_pixel3_pushButton.setObjectName("sw_pixel3_pushButton")
        self.gridLayout_6.addWidget(self.sw_pixel3_pushButton, 5, 0, 1, 1)

        # Pixel 4
        self.sw_pixel4_pushButton = QtWidgets.QPushButton(self.sw_select_pixel_widget)
        self.sw_pixel4_pushButton.setCheckable(True)
        self.sw_pixel4_pushButton.setChecked(False)
        self.sw_pixel4_pushButton.setObjectName("sw_pixel4_pushButton")
        self.gridLayout_6.addWidget(self.sw_pixel4_pushButton, 6, 0, 1, 1)

        # Pixel 5
        self.sw_pixel5_pushButton = QtWidgets.QPushButton(self.sw_select_pixel_widget)
        self.sw_pixel5_pushButton.setCheckable(True)
        self.sw_pixel5_pushButton.setChecked(False)
        self.sw_pixel5_pushButton.setObjectName("sw_pixel5_pushButton")
        self.gridLayout_6.addWidget(self.sw_pixel5_pushButton, 2, 1, 1, 1)

        # Pixel 6
        self.sw_pixel6_pushButton = QtWidgets.QPushButton(self.sw_select_pixel_widget)
        self.sw_pixel6_pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sw_pixel6_pushButton.setCheckable(True)
        self.sw_pixel6_pushButton.setChecked(False)
        self.sw_pixel6_pushButton.setObjectName("sw_pixel6_pushButton")
        self.gridLayout_6.addWidget(self.sw_pixel6_pushButton, 4, 1, 1, 1)

        # Pixel 7
        self.sw_pixel7_pushButton = QtWidgets.QPushButton(self.sw_select_pixel_widget)
        self.sw_pixel7_pushButton.setCheckable(True)
        self.sw_pixel7_pushButton.setChecked(False)
        self.sw_pixel7_pushButton.setObjectName("sw_pixel7_pushButton")
        self.gridLayout_6.addWidget(self.sw_pixel7_pushButton, 5, 1, 1, 1)

        # Pixel 8
        self.sw_pixel8_pushButton = QtWidgets.QPushButton(self.sw_select_pixel_widget)
        self.sw_pixel8_pushButton.setCheckable(True)
        self.sw_pixel8_pushButton.setChecked(False)
        self.sw_pixel8_pushButton.setObjectName("sw_pixel8_pushButton")
        self.gridLayout_6.addWidget(self.sw_pixel8_pushButton, 6, 1, 1, 1)

        # Select all
        self.sw_select_all_pushButton = QtWidgets.QPushButton(
            self.sw_select_pixel_widget
        )
        self.sw_select_all_pushButton.setObjectName("sw_select_all_pushButton")
        self.gridLayout_6.addWidget(self.sw_select_all_pushButton, 8, 0, 1, 1)

        # Unselect all
        self.sw_unselect_all_push_button = QtWidgets.QPushButton(
            self.sw_select_pixel_widget
        )
        self.sw_unselect_all_push_button.setObjectName("sw_unselect_all_push_button")
        self.gridLayout_6.addWidget(self.sw_unselect_all_push_button, 8, 1, 1, 1)

        # Prebias all
        self.sw_prebias_pushButton = QtWidgets.QPushButton(self.sw_select_pixel_widget)
        self.sw_prebias_pushButton.setObjectName("sw_prebias_pushButton")
        self.gridLayout_6.addWidget(self.sw_prebias_pushButton, 9, 0, 1, 1)

        # Autotest all
        self.sw_auto_test_pushButton = QtWidgets.QPushButton(
            self.sw_select_pixel_widget
        )
        self.sw_auto_test_pushButton.setObjectName("sw_auto_test_pushButton")
        self.gridLayout_6.addWidget(self.sw_auto_test_pushButton, 9, 1, 1, 1)

        self.gridLayout_7.addWidget(self.sw_select_pixel_widget, 5, 0, 1, 1)

        # LCD number widget
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
        self.sw_current_lcdNumber.display("0.0001 A")
        self.gridLayout_7.addWidget(self.sw_current_lcdNumber, 5, 1, 1, 1)

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
        self.specw_ax.set_xlabel("Wavelength (nm)", fontsize=14)
        self.specw_ax.set_ylabel("Intensity (a.u.)", fontsize=14)
        self.specw_ax.set_xlim([350, 830])

        self.specw_ax.axhline(linewidth=1, color="black")
        self.specw_ax.axvline(linewidth=1, color="black")

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

        # ---------------------- Select pixel widget ------------------------- #
        self.specw_select_pixel_widget = QtWidgets.QWidget(
            self.specw_scrollAreaWidgetContents
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.specw_select_pixel_widget.sizePolicy().hasHeightForWidth()
        )
        self.specw_select_pixel_widget.setSizePolicy(sizePolicy)
        self.specw_select_pixel_widget.setMinimumSize(QtCore.QSize(100, 0))
        self.specw_select_pixel_widget.setMaximumSize(QtCore.QSize(150, 124))
        self.specw_select_pixel_widget.setObjectName("specw_select_pixel_widget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.specw_select_pixel_widget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.specw_select_pixel_label = QtWidgets.QLabel(
            self.specw_scrollAreaWidgetContents
        )
        self.specw_select_pixel_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.specw_select_pixel_label.setObjectName("specw_select_pixel_label")
        self.specw_scrollArea_gridLayout.addWidget(
            self.specw_select_pixel_label, 3, 0, 1, 1
        )

        # Pixel 1
        self.specw_pixel1_pushButton = QtWidgets.QPushButton(
            self.specw_select_pixel_widget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.specw_pixel1_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.specw_pixel1_pushButton.setSizePolicy(sizePolicy)
        self.specw_pixel1_pushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.specw_pixel1_pushButton.setCheckable(True)
        self.specw_pixel1_pushButton.setChecked(False)
        self.specw_pixel1_pushButton.setAutoRepeat(False)
        self.specw_pixel1_pushButton.setObjectName("specw_pixel1_pushButton")
        self.gridLayout_4.addWidget(self.specw_pixel1_pushButton, 0, 0, 1, 1)

        # Pixel 2
        self.specw_pixel2_pushButton = QtWidgets.QPushButton(
            self.specw_select_pixel_widget
        )
        self.specw_pixel2_pushButton.setCheckable(True)
        self.specw_pixel2_pushButton.setChecked(False)
        self.specw_pixel2_pushButton.setObjectName("specw_pixel2_pushButton")
        self.gridLayout_4.addWidget(self.specw_pixel2_pushButton, 2, 0, 1, 1)

        # Pixel 3
        self.specw_pixel3_pushButton = QtWidgets.QPushButton(
            self.specw_select_pixel_widget
        )
        self.specw_pixel3_pushButton.setCheckable(True)
        self.specw_pixel3_pushButton.setChecked(False)
        self.specw_pixel3_pushButton.setObjectName("specw_pixel3_pushButton")
        self.gridLayout_4.addWidget(self.specw_pixel3_pushButton, 3, 0, 1, 1)

        # Pixel 4
        self.specw_pixel4_pushButton = QtWidgets.QPushButton(
            self.specw_select_pixel_widget
        )
        self.specw_pixel4_pushButton.setCheckable(True)
        self.specw_pixel4_pushButton.setChecked(False)
        self.specw_pixel4_pushButton.setObjectName("specw_pixel4_pushButton")
        self.gridLayout_4.addWidget(self.specw_pixel4_pushButton, 4, 0, 1, 1)

        # Pixel 5
        self.specw_pixel5_pushButton = QtWidgets.QPushButton(
            self.specw_select_pixel_widget
        )
        self.specw_pixel5_pushButton.setCheckable(True)
        self.specw_pixel5_pushButton.setChecked(False)
        self.specw_pixel5_pushButton.setObjectName("specw_pixel5_pushButton")
        self.gridLayout_4.addWidget(self.specw_pixel5_pushButton, 0, 1, 1, 1)

        # Pixel 6
        self.specw_pixel6_pushButton = QtWidgets.QPushButton(
            self.specw_select_pixel_widget
        )
        self.specw_pixel6_pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.specw_pixel6_pushButton.setCheckable(True)
        self.specw_pixel6_pushButton.setChecked(False)
        self.specw_pixel6_pushButton.setObjectName("specw_pixel6_pushButton")
        self.gridLayout_4.addWidget(self.specw_pixel6_pushButton, 2, 1, 1, 1)

        # Pixel 7
        self.specw_pixel7_pushButton = QtWidgets.QPushButton(
            self.specw_select_pixel_widget
        )
        self.specw_pixel7_pushButton.setCheckable(True)
        self.specw_pixel7_pushButton.setChecked(False)
        self.specw_pixel7_pushButton.setObjectName("specw_pixel7_pushButton")
        self.gridLayout_4.addWidget(self.specw_pixel7_pushButton, 3, 1, 1, 1)

        # Pixel 8
        self.specw_pixel8_pushButton = QtWidgets.QPushButton(
            self.specw_select_pixel_widget
        )
        self.specw_pixel8_pushButton.setCheckable(True)
        self.specw_pixel8_pushButton.setChecked(False)
        self.specw_pixel8_pushButton.setObjectName("specw_pixel8_pushButton")
        self.gridLayout_4.addWidget(self.specw_pixel8_pushButton, 4, 1, 1, 1)

        self.specw_scrollArea_gridLayout.addWidget(
            self.specw_select_pixel_widget, 4, 0, 1, 1, QtCore.Qt.AlignHCenter
        )

        # Save Spectrum button
        self.specw_save_spectrum_pushButton = QtWidgets.QPushButton(
            self.specw_scrollAreaWidgetContents
        )
        self.specw_save_spectrum_pushButton.setObjectName(
            "specw_save_spectrum_pushButton"
        )
        self.specw_scrollArea_gridLayout.addWidget(
            self.specw_save_spectrum_pushButton, 5, 0, 1, 1
        )

        self.tabWidget.addTab(self.spectrum_widget, "")

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
        MainWindow.setWindowTitle(_translate("MainWindow", "OLED Benchmarker"))
        # self.gatherlab_label.setText(
        # _translate("MainWindow", "Gatherlab JVL Measurement")
        # )
        self.sw_header2_label.setText(_translate("MainWindow", "Current Tester"))
        self.sw_browse_pushButton.setText(_translate("MainWindow", "Browse"))
        self.sw_ct_voltage_spinBox.setSuffix(_translate("MainWindow", " V"))
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
        self.sw_header1_label.setText(
            _translate("MainWindow", "Batch Name and File Path")
        )
        self.sw_activate_local_mode_pushButton.setText(
            _translate("MainWindow", "Reset Hardware")
        )
        self.sw_pixel_label.setText(_translate("MainWindow", "Select Pixels"))
        self.sw_pixel2_pushButton.setText(_translate("MainWindow", "2"))
        self.sw_pixel1_pushButton.setText(_translate("MainWindow", "1"))
        self.sw_pixel3_pushButton.setText(_translate("MainWindow", "3"))
        self.sw_select_all_pushButton.setText(_translate("MainWindow", "Select All"))
        self.sw_unselect_all_push_button.setText(
            _translate("MainWindow", "Unselect All")
        )
        self.sw_pixel4_pushButton.setText(_translate("MainWindow", "4"))
        self.sw_prebias_pushButton.setText(_translate("MainWindow", "Pre-Bias All"))
        self.sw_auto_test_pushButton.setText(_translate("MainWindow", "Auto Test All"))
        self.sw_pixel8_pushButton.setText(_translate("MainWindow", "8"))
        self.sw_pixel7_pushButton.setText(_translate("MainWindow", "7"))
        self.sw_pixel6_pushButton.setText(_translate("MainWindow", "6"))
        self.sw_pixel5_pushButton.setText(_translate("MainWindow", "5"))
        self.sw_change_voltage_label.setText(
            _translate("MainWindow", "Change Voltage (V)")
        )
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
        self.specw_pixel2_pushButton.setText(_translate("MainWindow", "2"))
        self.specw_pixel1_pushButton.setText(_translate("MainWindow", "1"))
        self.specw_pixel4_pushButton.setText(_translate("MainWindow", "4"))
        self.specw_pixel3_pushButton.setText(_translate("MainWindow", "3"))
        self.specw_pixel8_pushButton.setText(_translate("MainWindow", "8"))
        self.specw_pixel7_pushButton.setText(_translate("MainWindow", "7"))
        self.specw_pixel6_pushButton.setText(_translate("MainWindow", "6"))
        self.specw_pixel5_pushButton.setText(_translate("MainWindow", "5"))
        # self.specw_max_voltage_label.setText(
        # _translate("MainWindow", "Max Voltage (V)")
        # )
        self.specw_voltage_label.setText(_translate("MainWindow", "Set Voltage (V)"))
        self.specw_voltage_spinBox.setSuffix(_translate("MainWindow", " V"))
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
        self.specw_select_pixel_label.setText(_translate("MainWindow", "Select Pixels"))
        # self.specw_bad_contact_checkBox.setText(
        # _translate("MainWindow", "Check fo Bad Contacts")
        # )
        self.specw_save_spectrum_pushButton.setText(
            _translate("MainWindow", "Save Spectrum")
        )
        self.specw_header1_label.setText(
            _translate("MainWindow", "Measurement Parameters")
        )

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.spectrum_widget),
            _translate("MainWindow", "Spectrum"),
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
