import psutil
import numpy as np


class MockRigoOscilloscope:
    """
    Mock class for testing
    """

    def __init__(self, com2_address):
        print(com2_address)

    def get_data(self, osci_name):
        time = np.arange(0, 100, 0.1)
        return time, np.sin(time)

    def measure(self):
        return 1, 2, 3, 4


class MockVoltcraftSource:
    """
    Mock class for testing
    """

    def __init__(self, com2_address):
        print(com2_address)
        self.voltage = 5
        self.current = 1

    def read_values(self):
        return (
            self.voltage,
            self.current,
            float(psutil.cpu_percent() / 100),
        )

    def set_voltage(self, voltage):
        self.voltage = voltage

    def set_current(self, current):
        self.current = current


class MockArduino:
    """
    Mock class for testing
    """

    def __init__(self, com2_address):
        print(com2_address)
        self.frequency = 10000

    def init_serial_connection(self):
        print("Serial connection initialised")

    def read_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
