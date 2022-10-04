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


class MockKoradSource:
    """
    Mock class for testing
    """

    def __init__(self, com2_address, dummy):
        print(com2_address)
        self.voltage = 5
        self.current = 1
        self.magnetic_field = 1

    def read_values(self):
        return (
            self.voltage,
            self.current,
            self.magnetic_field,
        )

    def set_voltage(self, voltage):
        self.voltage = voltage

    def set_current(self, current):
        self.current = current

    def set_magnetic_field(self, magnetic_field):
        """
        Function that converts a value for a magnetic field to a current that
        can be set on the source
        """
        self.magnetic_field = magnetic_field

    def start_constant_magnetic_field_mode(
        self, pid_parameters, set_point, maximum_voltage
    ):
        """
        Start constant magnetic field mode according to a set value
        """
        print("Magnetic field mode started")

    def adjust_magnetic_field(
        self,
        pickup_coil_windings,
        pickup_coil_radius,
        frequency,
        osci,
        break_if_too_long=False,
    ):
        """
        Does the adjustment to a constant magnetic field according to an input
        magnetic field and measurements using an external device (e.g. osci).
        magnetic field in mT, frequency in kHz
        """
        return 0, 1

    def output(self, state, slow=False):
        """
        Activate or deactivate output:
        state = True: output on
        state = False: output off
        The device communication fails if the device is already on and one
        asks it to turn on. This possbile error must be checked for first
        (maybe class variable).
        """
        print("Korad output triggered")

    def close(self):
        """
        Savely close the source
        """
        print("MockKorad source closed")


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
        )

    def set_voltage(self, voltage):
        self.voltage = voltage

    def set_current(self, current):
        self.current = current

    def output(self, state, slow=False):
        """
        Activate or deactivate output:
        state = True: output on
        state = False: output off
        The device communication fails if the device is already on and one
        asks it to turn on. This possbile error must be checked for first
        (maybe class variable).
        """
        print("Voltcraft output triggered")


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

    def trigger_frequency_generation(self, state):
        print("Frequency generation triggered with " + str(state))
