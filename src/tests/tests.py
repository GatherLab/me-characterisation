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

    def measure_vmax(self, channel):
        return 1


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
        self.frequency = 1000
        self.real_capacitance = 1000

    def init_serial_connection(self):
        print("Serial connection initialised")

    def read_frequency(self):
        return self.frequency

    def set_frequency(self, frequency, set_capacitance=True):
        self.frequency = frequency

    def set_resistance(self, resistance):
        self.resistance = resistance

    def set_capacitance(self, capacitance):
        self.real_capacitance = capacitance
