import psutil
import numpy as np


class MockRigoOscilloscope:
    """
    Mock class for testing
    """

    def __init__(self, com2_address):
        print(com2_address)


class MockVoltcraftSource:
    """
    Mock class for testing
    """

    def __init__(self, com2_address):
        print(com2_address)

    def read_values(self):
        return (
            float(psutil.cpu_percent() / 100),
            float(psutil.cpu_percent() / 100),
            float(psutil.cpu_percent() / 100),
        )


class MockArduino:
    """
    Mock class for testing
    """

    def __init__(self, com2_address):
        print(com2_address)
