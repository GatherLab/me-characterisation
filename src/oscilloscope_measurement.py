from PySide2 import QtCore

from hardware import RigolOscilloscope, VoltcraftSource

import time


class OscilloscopeThread(QtCore.QThread):
    """
    Class thread that manages the constant read out of current, voltage and frequency
    """

    # Define costum signals
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
    # With pyside2 https://wiki.qt.io/Qt_for_Python_Signals_and_Slots
    update_oscilloscope = QtCore.Signal(list, list, list, list, list)

    def __init__(self, osci, parent=None):
        super(OscilloscopeThread, self).__init__()
        # Variable to kill thread
        self.is_killed = False
        self.pause = False

        # Assign hardware and reset
        self.osci = osci
        # self.oscilloscope = oscilloscope

        # Connect signal to the updater from the parent class
        self.update_oscilloscope.connect(parent.plot_oscilloscope)

    def run(self):
        """
        Class that continuously measures the spectrum
        """
        import pydevd

        pydevd.settrace(suspend=False)

        while True:
            # Measure
            time_data, data = self.osci.get_data("CHAN1")
            time_data2, data2 = self.osci.get_data("CHAN2")
            variables = self.osci.measure()

            self.update_oscilloscope.emit(time_data, data, time_data2, data2, variables)

            # The sleep time here is very important because if it is chosen to
            # short, the program may crash. Currently 1 s seems to be save (one can at least go down to 0.5s)
            time.sleep(1)

            if self.pause:
                while True:
                    time.sleep(0.5)

                    if not self.pause:
                        break

            if self.is_killed:
                self.quit()
                break

    def kill(self):
        """
        Kill this thread by stopping the loop
        """
        self.osci.close()

        # Trigger interruption of run sequence
        self.is_killed = True
