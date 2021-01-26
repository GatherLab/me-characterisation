import pyvisa
import serial

import core_functions as cf

import time
import re
import sys

import numpy as np
import pandas as pd


class RigolOscilloscope:
    """
    Class to control the rigol 1202 Z-E oscilloscope. Using pyvisa's query
    function does not work for the osci. However, writing and reading
    manually seems to work. Basically one has to ask the oscilloscope for an
    information and then read it out afterwards.
    """

    def __init__(self, rigol_source_address):
        """
        Init the oscilloscope
        """
        # Keithley Finding Device
        rm = pyvisa.ResourceManager()
        # The actual addresses for the Keithleys can be accessed via rm.list_resources()
        visa_resources = rm.list_resources()

        # Check if keithley source is present at the given address
        if rigol_source_address not in visa_resources:
            cf.log_message("The Oscilloscope seems to be absent or switched off.")
            # raise IOError("The Oscilloscope seems to be absent or switched off.")

        # Time out is in ms
        self.osci = rm.open_resource(rigol_source_address, timeout=25000)
        time.sleep(2)

        # self.osci.write("*RST")
        # self.osci.write(":KEY:AUTO")
        # time.sleep(2)

        # self.get_data()

    def run(self):
        """
        Runs the oscilloscope
        """
        self.osci.write("RUN")

    def stop(self):
        """
        Stops the oscilloscope
        """
        self.osci.write("STOP")

    def get_data(self):
        """
        Read data from oscilloscope display
        See: https://gist.github.com/pklaus/7e4cbac1009b668eafab
        The entire function needs approximately between 20 and 60 ms to run.
        When omitting stopping and starting of the oscilloscope at the
        beginning it only takes around 5-12 ms. However, I am not sure yet if
        I still need to stop the oscilloscope to get the entire data on the
        screen.
        This obviously limits the number of pictures I can take per time unit.
        """

        # Stop osci so that the data is not altered on the fly
        # self.stop()

        # Get the timescale and offset
        self.osci.write(":TIM:SCAL?")
        timescale = float(self.osci.read())
        self.osci.write(":TIM:OFFS?")
        timeoffset = float(self.osci.read())

        # And the voltage scale and offset
        self.osci.write(":CHAN1:SCAL?")
        voltscale = float(self.osci.read())
        self.osci.write(":CHAN1:OFFS?")
        voltoffset = float(self.osci.read())

        # Sets the mode in which the data is returned
        self.osci.write(":WAV:POIN:MODE RAW")

        # Read data
        self.osci.write(":WAV:DATA? CHAN1")
        raw_data = self.osci.read_raw()[10:]

        # Not exactly sure what this does
        data = np.frombuffer(raw_data, "B")

        # Walk through the data, and map it to actual voltages
        # This mapping is from Cibo Mahto
        # First invert the data
        data = data * -1 + 255

        # Now, we know from experimentation that the scope display range is actually
        # 30-229.  So shift by 130 - the voltage offset in counts, then scale to
        # get the actual voltage.
        data = (data - 130.0 - voltoffset / voltscale * 25) / 25 * voltscale

        # Now, generate a time axis.
        time_data = np.linspace(
            timeoffset - 6 * timescale, timeoffset + 6 * timescale, num=len(data)
        )

        # See if we should use a different time axis
        if time_data[-1] < 1e-3:
            time_data = time_data * 1e6
            tUnit = "uS"
        elif time_data[-1] < 1:
            time_data = time_data * 1e3
            tUnit = "mS"
        else:
            tUnit = "S"

        # Run osci again
        # self.run()

        return time_data, data

    def auto_scale(self):
        """
        I am not yet sure how to do it but this would be an important and
        nice feature. The idea is to mimic the auto scale feature of the
        oscilloscope
        """
        self.osci.write(":KEY:AUTO")
        cf.log_message(self.osci.read())

    def measure(self):
        """
        Measures a bunch of variables of the waveform. The possible commands are
        :MEASure:CLEar
        :MEASure:VPP?
        :MEASure:VMAX?
        :MEASure:VMIN?
        :MEASure:VAMPlitude?
        :MEASure:VTOP?
        :MEASure:VBASe?
        :MEASure:VAVerage?
        :MEASure:VRMS?
        :MEASure:OVERshoot?
        :MEASure:PREShoot?
        :MEASure:FREQuency?
        :MEASure:RISetime?
        :MEASure:FALLtime?
        :MEASure:PERiod?
        :MEASure:PWIDth?
        :MEASure:NWIDth?
        :MEASure:PDUTycycle?
        :MEASure:NDUTycycle?
        :MEASure:PDELay?
        :MEASure:NDELay?
        :MEASure:TOTal
        :MEASure:SOURce
        """
        # Measre VPP
        self.osci.write(":MEAS:VPP? CHAN1")
        vpp = float(self.osci.read())

        # Measure Vmax
        self.osci.write(":MEAS:VMAX? CHAN1")
        vmax = float(self.osci.read())

        # # # Measure Vmin
        self.osci.write(":MEAS:VMIN? CHAN1")
        vmin = float(self.osci.read())

        # # # Measure frequency
        self.osci.write(":MEAS:FREQ? CHAN1")
        frequency = float(self.osci.read())

        # # # Measure rise time
        # self.osci.write(":MEAS:RIS? CHAN1")
        # rise_time = float(self.osci.read())

        # cf.log_message("VPP: " + str(vpp) + " V")

        return [
            vpp,
            vmax,
            vmin,
            frequency,
        ]  # , vmax, vmin, frequency, rise_time]

    def close(self):
        """
        Closes connection to oscilloscope savely
        """
        self.osci.write(":KEY:FORCE")
        self.osci.close()


class VoltcraftSource:
    """
    Class to control the voltcraft PPS-16005 source
    The voltcraft source is controlled via the serial interface
    A usefull source for this is https://github.com/ap--/voltcraft/blob/master/voltcraft/pps.py
    However, the initialisation did not work out of the box for me.
    Furthermore, I wanted to do some further costumisation.
    """

    def __init__(
        self,
        voltcraft_source_address,
    ):
        """
        Initialise voltcraft source
        """
        # Keithley Finding Device
        rm = pyvisa.ResourceManager()
        # The actual addresses for the Keithleys can be accessed via rm.list_resources()
        visa_resources = rm.list_resources()

        # Check if keithley source is present at the given address
        if voltcraft_source_address not in visa_resources:
            cf.log_message("The Voltcraft Source seems to be absent or switched off.")

        # Time out is in ms
        voltcraft_port = "COM" + re.findall(r"\d+", voltcraft_source_address)[0]

        self.source = serial.Serial(voltcraft_port, timeout=1)

        # To see if device is on or not. There is no built-in function for the
        # voltcraft device. This is always true when the software was not used
        # previously. Otherwise the output state will only be the correct one
        # after the first usage of self.output()
        self.output_state = True

        # Now query details about the instrument
        gmax = self.query("GMAX")
        self.maximum_voltage = float(gmax[0:3]) / 10
        self.maximum_current = float(gmax[3:6]) / 10

        self.output(False)
        self.set_voltage(5)
        self.set_current(1)
        cf.log_message("Source successfully initialised")

    def query(self, cmd):
        """
        Basic function that allows querying of the Voltcraft device
        """
        self.source.write((cmd + "\r").encode())
        b = []
        while True:
            b.append(self.source.read(1))
            if b[-1] == "":
                raise serial.SerialTimeoutException()
            if b"".join(b[-3:]) == b"OK\r":
                break
        return (b"".join(b[:-4])).decode()

    def read_values(self):
        """
        Function that returns the display readings of the source in volt and
        ampere. This takes about 20 - 25 ms to run
        """
        # The source will return something liek 119700020 which translates to:
        # U = 11.97 V, I = 0.00 A and it is in C.V. mode (constant voltage)
        raw_data = self.query("GETD")

        # Now disect this string
        voltage = float(raw_data[0:4]) / 100
        current = float(raw_data[4:8]) / 100

        mode = int(raw_data[8:9])
        if mode == 0:
            mode = "CV"
        elif mode == 1:
            # Constant current mode only means that the maximum set current was
            # exceeded and the device now limits the voltage
            mode = "CC"

        return voltage, current, mode

    def set_voltage(self, voltage):
        """
        Function to set the voltage of the device
        """
        # The voltcraft device, however can not deal with floats. Therefore, we
        # have to convert the input first
        voltage_int = int(np.round(voltage, 1) * 10)

        if voltage > self.maximum_voltage:
            cf.log_message(
                "You are attempting to exceed the maximum voltage rating of your device of "
                + str(np.round(self.maximum_voltage, 1) * 10)
                + " V. I set the voltage to this value for you instead."
            )
            voltage_int = int(np.round(self.maximum_voltage, 1) * 10)
        elif voltage < 0:
            cf.log_message(
                "You are attempting to set the voltage to a negative value. This is not possible. I set the voltage to 0 V for you instead"
            )
            voltage_int = 0

        self.query("VOLT%03d" % voltage_int)

    def set_current(self, current):
        """
        Set current of the device
        """
        # The voltcraft device, however can not deal with floats. Therefore, we
        # have to convert the input first
        current_int = int(np.round(current, 1) * 10)

        if current > self.maximum_current:
            cf.log_message(
                "You are attempting to exceed the maximum voltage rating of your device of "
                + str(np.round(self.maximum_current, 1))
                + " V. I set the voltage to this value for you instead."
            )
            current_int = int(np.round(self.maximum_current, 1) * 10)
        elif current < 0:
            cf.log_message(
                "You are attempting to set the voltage to a negative value. This is not possible. I set the voltage to 0 V for you instead"
            )
            current_int = int(0)

        self.query("CURR%03d" % current_int)

    def output(self, state):
        """
        Activate or deactivate output:
        state = True: output on
        state = False: output off
        The device communication fails if the device is already on and one
        asks it to turn on. This possbile error must be checked for first
        (maybe class variable).
        """

        # The logic of the voltcraft source is just the other way around than
        # my logic (true means off)
        self.query("SOUT%d" % int(not state))

        # Set the state variable
        self.output_state = self.output_state


class Arduino:
    """
    Class that manages all functionality of the arduino
    """

    def __init__(self, com_address):

        # Check for devices on the pc
        rm = pyvisa.ResourceManager()
        # The actual addresses for the Keithleys can be accessed via rm.list_resources()
        visa_resources = rm.list_resources()

        # Open COM port to Arduino
        if com_address not in visa_resources:
            cf.log_message(
                "The Arduino seems to be missing. Try to reconnect to computer."
            )

        # Instead of letting the user explicitly define the COM port after he
        # already defined the com_address, search for the number in the
        # com_address to construct the right string
        arduino_port = "COM" + re.findall(r"\d+", com_address)[0]

        # assign name to Arduino and assign short timeout to be able to do things fast
        self.arduino = serial.Serial(arduino_port, timeout=0.01)

        # Try to open the serial connection
        try:
            self.init_serial_connection()
        except serial.SerialException:
            # If the serial connection was already established, close it again and open it again
            try:
                self.arduino.close()
                self.init_serial_connection()
            except IOError:
                cf.log_message(
                    "COM port to Arduino already open. Reconnect arduino manually and try again."
                )
                sys.exit()

        # cf.log_message("Arduino successfully initiated")

    def init_serial_connection(self, wait=1):
        """
        Private function
        Initialise serial connection to com.

        com: func
            specify COM port. Needs to be opened prior to calling this function.
            e.g.:
                > arduino = serial.Serial(2, timeout=0.2)
                > arduino_init(com=arduino)
        wait: flt
            time in seconds to wait before collecting initialisation message.
        """

        # Open serial port
        try:
            self.arduino.open()
        except serial.SerialException:
            # If port was already open, we do not have to open it obviously.
            cf.log_message("Arduino port was already open")

        # Wait for a defined period of time
        time.sleep(wait)

        # Read serial port result
        cf.log_message(
            "Arduino serial port successfully initialised with "
            + str(self.arduino.readall())
        )
        # self.queue.put(com.readall())
        self.serial_connection_open = True

    def close_serial_connection(self):
        """
        Close connection to arduino
        """
        self.arduino.close()
        self.serial_connection_open = False

    def set_frequency(self, frequency):
        """
        Function that allows to set the frequency on the Arduino (by using
        the Serial Connection interface)
        It is set in kHz
        """
        com = self.arduino

        # Check if serial connection was already established
        if self.serial_connection_open == False:
            self.init_serial_connection()

        # Write the frequency to the serial interface
        freq = str.encode(str(frequency * 1000) + "\n")
        com.write(freq)

        # Read answer from Arduino
        cf.log_message(com.readall())

    def read_frequency(self):
        """
        Function that asks the arduino to return the frequency
        """
        com = self.arduino

        # Check if serial connection was already established
        if self.serial_connection_open == False:
            self.init_serial_connection()

        # Write the frequency to the serial interface
        com.write(str.encode("freq\n"))

        # Read answer from Arduino
        frequency = com.readall()
        try:
            frequency = float(frequency)
        except:
            cf.log_message("Could not convert frequency to float")

        cf.log_message("Arduino has the frequency " + str(frequency) + " Hz set.")
        return frequency
