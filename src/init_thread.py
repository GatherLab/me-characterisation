from PySide2 import QtCore
import core_functions as cf
import time

from hardware import RigolOscilloscope, VoltcraftSource, Arduino
from tests.tests import MockRigoOscilloscope, MockVoltcraftSource, MockArduino


class InitThread(QtCore.QThread):
    """
    Worker thread that is only meant to do the initialisation, before the program is started
    """

    update_loading_dialog = QtCore.Signal(int, str)
    kill_dialog = QtCore.Signal()
    ask_retry = QtCore.Signal()
    emit_oscilloscope = QtCore.Signal(RigolOscilloscope)
    emit_source = QtCore.Signal(VoltcraftSource)
    emit_arduino = QtCore.Signal(Arduino)

    def __init__(
        self, oscilloscope_address, source_address, arduino_address, widget=None
    ):
        super(InitThread, self).__init__()

        # Connect signals
        self.update_loading_dialog.connect(widget.update_loading_dialog)
        self.kill_dialog.connect(widget.kill_dialog)
        self.ask_retry.connect(widget.ask_retry)
        self.emit_oscilloscope.connect(widget.parent.init_oscilloscope)
        self.emit_source.connect(widget.parent.init_source)
        self.emit_arduino.connect(widget.parent.init_arduino)

        self.oscilloscope_address = oscilloscope_address
        self.source_address = source_address
        self.arduino_address = arduino_address

        # Variable that checks if initialisation shall be repeated
        self.repeat = False

    def run(self):
        """
        Function that initialises the parameters before the main program is called
        """
        # self.update_loading_dialog.emit("Test")
        # Read global settings first (what if they are not correct yet?)

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

        self.update_loading_dialog.emit(33, "Initialising Source")

        # Try if Voltcraft Source can be initialised
        try:
            source = VoltcraftSource(self.source_address)
            cf.log_message("Voltcraft Source successfully initialised")
            source_init = True
        except Exception as e:
            source = MockVoltcraftSource(self.source_address)
            cf.log_message(
                "The Voltcraft source could not be initialised! Please reconnect the device and check the serial number in the settings file!"
            )
            cf.log_message(e)
            source_init = False

        self.emit_source.emit(source)
        time.sleep(0.1)
        self.update_loading_dialog.emit(66, "Initialising Arduino")

        # Try if Arduino can be initialised
        try:
            arduino = Arduino(self.arduino_address)
            cf.log_message("Arduino successfully initialised")
            arduino_init = True
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
        if oscilloscope_init == False or source_init == False:
            self.update_loading_dialog.emit(
                100,
                "Some of the devices could not be initialised.",
            )
            self.ask_retry.emit()

        else:
            self.update_loading_dialog.emit(100, "One more moment")
            time.sleep(0.5)
            self.kill_dialog.emit()
