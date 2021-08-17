from PySide2 import QtCore
import core_functions as cf
import time

from hardware import (
    KoradSource,
    RigolOscilloscope,
    VoltcraftSource,
    KoradSource,
    Arduino,
)
from tests.tests import MockRigoOscilloscope, MockVoltcraftSource, MockArduino


class InitThread(QtCore.QThread):
    """
    Worker thread that is only meant to do the initialisation, before the program is started
    """

    update_loading_dialog = QtCore.Signal(int, str)
    kill_dialog = QtCore.Signal()
    ask_retry = QtCore.Signal()
    emit_oscilloscope = QtCore.Signal(RigolOscilloscope)
    emit_dc_source = QtCore.Signal(KoradSource)
    emit_hf_source = QtCore.Signal(VoltcraftSource)
    emit_arduino = QtCore.Signal(Arduino)

    def __init__(self, widget=None):
        super(InitThread, self).__init__()

        # Read global settings
        settings = cf.read_global_settings()

        # Connect signals
        self.update_loading_dialog.connect(widget.update_loading_dialog)
        self.kill_dialog.connect(widget.kill_dialog)
        self.ask_retry.connect(widget.ask_retry)
        self.emit_oscilloscope.connect(widget.parent.init_oscilloscope)
        self.emit_hf_source.connect(widget.parent.init_hf_source)
        self.emit_dc_source.connect(widget.parent.init_dc_source)
        self.emit_arduino.connect(widget.parent.init_arduino)

        self.oscilloscope_address = settings["rigol_oscilloscope_address"]
        self.dc_source_address = settings["dc_source_address"]
        self.hf_source_address = settings["hf_source_address"]
        self.arduino_address = settings["arduino_address"]

        # Now set widget
        self.widget = widget

        # Variable that checks if initialisation shall be repeated
        self.repeat = False

    def run(self):
        """
        Function that initialises the parameters before the main program is called
        """
        # self.update_loading_dialog.emit("Test")
        # Read global settings first (what if they are not correct yet?)

        import pydevd

        pydevd.settrace(suspend=False)

        self.update_loading_dialog.emit(0, "Initialising Oscilloscope")

        # Try if Rigol Oscilloscope can be initialised
        try:
            osci = RigolOscilloscope(self.oscilloscope_address)
            cf.log_message("Rigol Oscilloscope successfully initialised")
            oscilloscope_init = True
        except Exception as e:
            osci = MockRigoOscilloscope(self.oscilloscope_address)
            cf.log_message(
                "Rigol Oscilloscope could not be initialised. Please reconnect the device or check its com number in the global settings."
            )
            cf.log_message(e)
            oscilloscope_init = False

        self.emit_oscilloscope.emit(osci)

        time.sleep(0.1)

        self.update_loading_dialog.emit(25, "Initialising DC Source")

        # Try if Voltcraft Source can be initialised
        try:
            try:
                dc_source = KoradSource(self.dc_source_address)
                cf.log_message("Voltcraft Source successfully initialised")
                dc_source_init = True
            except:
                # In the case that there was already a connection established,
                # it could happen that the hf_source does not allow to establish
                # a new one. Therefore, close the old one first.
                self.widget.parent.setup_thread.pause = True
                self.widget.parent.hf_source.close()

                dc_source = KoradSource(self.dc_source_address)
                cf.log_message("Voltcraft Source successfully initialised")
                dc_source_init = True

        except Exception as e:
            dc_source = KoradSource(self.dc_source_address)
            cf.log_message(
                "The Korad hf_source could not be initialised! Please reconnect the device and check the serial number in the settings file!"
            )
            cf.log_message(e)
            dc_source_init = False

        self.emit_dc_source.emit(dc_source)
        time.sleep(0.1)
        self.update_loading_dialog.emit(50, "Initialising HF Source")

        # Try if KORAD Source can be initialised
        # try:
        try:
            hf_source = VoltcraftSource(self.hf_source_address)
            cf.log_message("Korad Source successfully initialised")
            hf_source_init = True
        except:
            # In the case that there was already a connection established,
            # it could happen that the hf_source does not allow to establish
            # a new one. Therefore, close the old one first.
            # self.widget.parent.setup_thread.pause = True
            # self.widget.parent.hf_source.close()

            dc_source = MockVoltcraftSource(self.hf_source_address)
            cf.log_message(
                "The Voltcraft hf_source could not be initialised! Please reconnect the device and check the serial number in the settings file!"
            )
            cf.log_message(e)
            dc_source_init = False

        # except Exception as e:
        #     hf_source = MockKoradSource(self.source_address)
        #     cf.log_message(
        #         "The Koard hf_source could not be initialised! Please reconnect the device and check the serial number in the settings file!"
        #     )
        #     cf.log_message(e)
        #     source_init = False

        self.emit_hf_source.emit(hf_source)
        time.sleep(0.1)
        self.update_loading_dialog.emit(75, "Initialising Arduino")

        # Try if Arduino can be initialised
        try:
            try:
                arduino = Arduino(self.arduino_address)
                cf.log_message("Arduino successfully initialised")
                arduino_init = True
            except:
                # In the case that there was already a connection established,
                # it could happen that the arduino does not allow to establish
                # a new one. Therefore, close the old one first.
                self.widget.parent.arduino.close()

                arduino = Arduino(self.arduino_address)
                cf.log_message("Arduino successfully initialised")
                arduino_init = True

            # motor.move_to(-45)
        except Exception as e:

            arduino = MockArduino(self.arduino_address)
            cf.log_message(
                "The Arduino could not be initialised! Please reconnect the device and check the serial number in the settings file!"
            )
            cf.log_message(e)
            arduino_init = False

        self.emit_arduino.emit(arduino)
        time.sleep(0.1)

        # If one of the devices could not be initialised for whatever reason,
        # ask the user if she wants to retry after reconnecting the devices or
        # continue without some of the devices

        # If one of the devices could not be initialised for whatever reason,
        # ask the user if she wants to retry after reconnecting the devices or
        # continue without some of the devices
        if (
            oscilloscope_init == False
            or dc_source_init == False
            or hf_source_init == False
            or arduino_init == False
        ):
            device_not_loading_message = []
            if oscilloscope_init == False:
                device_not_loading_message.append("Oscilloscope")
            if dc_source_init == False:
                device_not_loading_message.append("DC Source")
            if hf_source_init == False:
                device_not_loading_message.append("HF Source")
            if arduino_init == False:
                device_not_loading_message.append("Arduino")

            if (
                len(device_not_loading_message) > 1
                and len(device_not_loading_message) < 4
            ):
                a = ", ".join(device_not_loading_message[:-1])
                b = a + " and " + device_not_loading_message[-1]
            elif len(device_not_loading_message) == 1:
                b = device_not_loading_message[0]
            elif len(device_not_loading_message) == 4:
                b = "None"

            c = b + " could not be initialised."

            if len(device_not_loading_message) == 4:
                c = "None of the devices could be initialised."

            self.update_loading_dialog.emit(
                100,
                c,
            )
            self.ask_retry.emit()

        else:
            self.update_loading_dialog.emit(100, "One more moment")
            time.sleep(0.5)
            self.kill_dialog.emit()
