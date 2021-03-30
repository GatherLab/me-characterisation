import pyvisa
import serial

from PySide2 import QtCore

import core_functions as cf
from physics_functions import calculate_resonance_frequency

import time
import re
import sys

import numpy as np
import pandas as pd
from itertools import chain, combinations
import debugpy

debugpy.debug_this_thread()


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
        # Define a mutex
        self.mutex = QtCore.QMutex(QtCore.QMutex.NonRecursive)

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
        self.mutex.lock()
        self.osci.write("RUN")
        self.mutex.unlock()

    def stop(self):
        """
        Stops the oscilloscope
        """
        self.mutex.lock()
        self.osci.write("STOP")
        self.mutex.unlock()

    def get_data(self, channel="CHAN1"):
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

        self.mutex.lock()
        # Stop osci so that the data is not altered on the fly
        # self.stop()

        # Get the timescale and offset
        self.osci.write(":TIM:SCAL?")
        timescale = float(self.osci.read())
        self.osci.write(":TIM:OFFS?")
        timeoffset = float(self.osci.read())

        # Measure Vmax
        self.osci.write(":MEAS:VMAX? " + channel)
        vmax = float(self.osci.read())

        # # # Measure Vmin
        self.osci.write(":MEAS:VMIN? " + channel)
        vmin = float(self.osci.read())

        # And the voltage scale and offset
        self.osci.write(":" + channel + ":SCAL?")
        voltscale = float(self.osci.read())
        self.osci.write(":" + channel + ":OFFS?")
        voltoffset = float(self.osci.read())

        # Set channel source
        self.osci.write("WAV:SOUR " + channel)

        # Sets the mode in which the data is returned
        self.osci.write(":WAV:POIN:MODE RAW")

        # Read data
        self.osci.write(":WAV:DATA?")
        raw_data = self.osci.read_raw()[10:]

        # Not exactly sure what this does
        data = np.frombuffer(raw_data, "B")
        # data = data * 1

        # Walk through the data, and map it to actual voltages
        # This mapping is from Cibo Mahto
        # First invert the data
        # data = data * -1 + 255

        # Now, we know from experimentation that the scope display range is actually
        # 30-229.  So shift by 130 - the voltage offset in counts, then scale to
        # get the actual voltage.
        # data_interp = (data[:-2] - 130.0 - voltoffset / voltscale * 25) / 25 * voltscale
        # Measure Vmax
        # self.osci.write(":MEAS:VMAX? CHAN1")
        # vmax = self.osci.read()
        #
        # # Measure Vmin
        # self.osci.write(":MEAS:VMIN? CHAN1")
        # vmin = self.osci.read()
        #
        # data_interpolated = np.interp(
        # data,
        # [np.min(data), np.max(data)],
        # [vmin, vmax],
        # )
        data_mapped = np.interp(
            data[1:-2],
            [np.min(data[1:-2]), np.max(data[1:-2])],
            [float(vmin), float(vmax)],
        )

        # Now, generate a time axis.
        time_data = np.linspace(
            timeoffset - 6 * timescale, timeoffset + 6 * timescale, num=len(data_mapped)
        )

        # See if we should use a different time axis
        # if time_data[-1] < 1e-3:
        #     time_data = time_data * 1e6
        #     tUnit = "uS"
        # elif time_data[-1] < 1:
        #     time_data = time_data * 1e3
        #     tUnit = "mS"
        # else:
        #     tUnit = "S"

        # Run osci again
        # self.run()
        self.mutex.unlock()

        return time_data, data_mapped

    def auto_scale(self):
        """
        I am not yet sure how to do it but this would be an important and
        nice feature. The idea is to mimic the auto scale feature of the
        oscilloscope
        """
        self.mutex.lock()
        self.osci.write(":KEY:AUTO")
        # cf.log_message(self.osci.read())
        self.mutex.unlock()

    def measure(self, channel="CHAN1"):
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
        self.mutex.lock()
        # Measre VPP
        self.osci.write(":MEAS:VPP? " + channel)
        vpp = self.osci.read()

        # Measure Vmax
        self.osci.write(":MEAS:VMAX? " + channel)
        vmax = self.osci.read()

        # # # Measure Vmin
        self.osci.write(":MEAS:VMIN? " + channel)
        vmin = self.osci.read()

        # # # Measure frequency
        self.osci.write(":MEAS:FREQ? " + channel)
        frequency = self.osci.read()

        # # # Measure rise time
        # self.osci.write(":MEAS:RIS? CHAN1")
        # rise_time = float(self.osci.read())

        # cf.log_message("VPP: " + str(vpp) + " V")
        self.mutex.unlock()

        return [
            vpp,
            vmax,
            vmin,
            frequency,
        ]  # , vmax, vmin, frequency, rise_time]

    def measure_vpp(self, channel="CHAN1"):
        """
        Measure VPP only
        """
        self.mutex.lock()

        # Measre VPP
        self.osci.write(":MEAS:VPP? " + channel)
        vpp = self.osci.read()

        self.mutex.unlock()
        return vpp

    def measure_vmax(self, channel="CHAN1"):
        """
        Measure Vavg only
        """
        self.mutex.lock()

        # Measre vavg
        self.osci.write(":MEAS:VMAX? " + channel)

        vmax = self.osci.read()

        self.mutex.unlock()
        return vmax

    def close(self):
        """
        Closes connection to oscilloscope savely
        """
        self.mutex.lock()
        self.osci.write(":KEY:FORCE")
        self.osci.close()
        self.mutex.unlock()


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
        self.mutex = QtCore.QMutex(QtCore.QMutex.Recursive)

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
        self.mutex.lock()

        self.source.write((cmd + "\r").encode())
        b = []
        while True:
            b.append(self.source.read(1))
            if b[-1] == "":
                raise serial.SerialTimeoutException()
            if b"".join(b[-3:]) == b"OK\r":
                break
        self.mutex.unlock()
        return (b"".join(b[:-4])).decode()

    def read_values(self):
        """
        Function that returns the display readings of the source in volt and
        ampere. This takes about 20 - 25 ms to run
        """
        self.mutex.lock()
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

        self.mutex.unlock()
        return voltage, current, mode

    def set_voltage(self, voltage):
        """
        Function to set the voltage of the device
        """
        self.mutex.lock()
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
        self.mutex.unlock()

    def set_current(self, current):
        """
        Set current of the device
        """
        self.mutex.lock()
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
        self.mutex.unlock()

    def output(self, state):
        """
        Activate or deactivate output:
        state = True: output on
        state = False: output off
        The device communication fails if the device is already on and one
        asks it to turn on. This possbile error must be checked for first
        (maybe class variable).
        """
        self.mutex.lock()

        # The logic of the voltcraft source is just the other way around than
        # my logic (true means off)
        self.query("SOUT%d" % int(not state))

        # Set the state variable
        self.output_state = state

        # Wait shortly because the source needs a bit until the final voltage is reached
        time.sleep(2)

        self.mutex.unlock()

    def close(self):
        """
        Savely close the source
        """
        self.mutex.lock()

        # Deactivate output
        self.output(False)

        # Close serial connection
        self.source.close()

        # Wait shortly to make sure the connection is closed
        time.sleep(1)

        self.mutex.unlock()


class Arduino:
    """
    Class that manages all functionality of the arduino
    """

    def __init__(self, com_address):
        """
        Init arduino
        """

        # Define a mutex
        self.mutex = QtCore.QMutex(QtCore.QMutex.Recursive)

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

        self.init_caps()

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

    def init_caps(self):
        """
        Function to initialise caps
        """
        # Read in global settings
        global_settings = cf.read_global_settings()

        # Capacitances in pF
        self.base_capacitance = float(global_settings["base_capacitance"])
        # self.base_capacitance = 3300
        self.capacitances = np.array(
            global_settings["capacitances"].split(","), dtype=float
        )
        # capacitances = [150, 330, 680, 1000, 2200, 3300]
        # self.arduino_pins = np.array([7, 6, 5, 4, 3, 2])
        self.arduino_pins = np.array(
            global_settings["arduino_pins"].split(","), dtype=int
        )
        self.cap_states = np.repeat(False, np.size(self.arduino_pins))

        def powerset(iterable):
            "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
            s = list(iterable)
            return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

        combinations_list = list(powerset(self.capacitances))
        combinations_pins = list(powerset(self.arduino_pins))

        # Define pandas dataframe that contains the capacitance constituents, the corresponding arduino pins and the sum of the capacitances
        # Drop if there exists more than one
        self.combinations_df = (
            pd.DataFrame(
                np.array(
                    [
                        [list(elem) for elem in combinations_list],
                        [list(elem) for elem in combinations_pins],
                        np.array([np.sum(list(elem)) for elem in combinations_list])
                        + self.base_capacitance,
                    ],
                    dtype=object,
                ).T,
                columns=["constituents", "arduino_pins", "sum"],
            )
            .sort_values("sum", ignore_index=True)
            .drop_duplicates(subset=["sum"], keep="first")
        )

        # Add additional column with resonance frequency

        self.combinations_df["resonance_frequency"] = np.empty(
            len(self.combinations_df)
        )

        # try:
        # Read in capacitor calibration file
        try:
            calibration = pd.read_csv(
                global_settings["calibration_file_path"],
                sep="\t",
                skiprows=5,
                names=[
                    "capacitance",
                    "resonance_frequency",
                    "quality_factor",
                    "maximum_current",
                ],
            )
        except:
            calibration = pd.DataFrame(
                columns=[
                    "capacitance",
                    "resonance_frequency",
                    "quality_factor",
                    "maximum_current",
                ],
            )

        # If capacitance exists in calibration file, set it to that resonance
        # frequency. Otherwise, estimate resonance frequency from coil
        # inductance given in settings.
        for index, capacitance in self.combinations_df["sum"].items():
            # Check if there is an entry in the calibration list
            if (
                len(
                    calibration.loc[
                        calibration["capacitance"] == capacitance, "capacitance"
                    ].to_numpy()
                )
                == 1
            ):
                # print(self.combinations_df.loc[index, "resonance_frequency"])
                self.combinations_df.loc[
                    index, "resonance_frequency"
                ] = calibration.loc[
                    calibration["capacitance"] == capacitance, "resonance_frequency"
                ].to_list()[
                    0
                ]

            # If not, calculate the resonance frequency by ourselfs
            elif (
                len(
                    calibration.loc[
                        calibration["capacitance"] == capacitance, "capacitance"
                    ].to_numpy()
                )
                == 0
            ):
                cf.log_message(
                    "Capacitance "
                    + str(capacitance)
                    + " pF not found in calibration file"
                )
                self.combinations_df.loc[index, "resonance_frequency"] = (
                    calculate_resonance_frequency(
                        capacitance * 1e-12, global_settings["coil_inductance"] * 1e-3
                    )
                    / 1e3
                )
            # Else, something is wrong
            else:
                cf.log_message("Could not calculate the resonance frequency")

        # self.combinations_df[
        # "resonance_frequency"
        # ] = self.capacitance_to_resonance_frequency(
        # self.combinations_df["sum"].astype(np.float64).to_numpy()
        # )

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

        self.mutex.lock()

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
        self.mutex.unlock()

    def close_serial_connection(self):
        """
        Close connection to arduino
        """
        self.mutex.lock()
        self.arduino.close()
        self.serial_connection_open = False
        self.mutex.unlock()

    def set_frequency(self, frequency, set_capacitance=False):
        """
        Function that allows to set the frequency on the Arduino (by using
        the Serial Connection interface)
        It is set in kHz
        """
        self.mutex.lock()
        com = self.arduino

        # Check if serial connection was already established
        if self.serial_connection_open == False:
            self.init_serial_connection()

        # Write the frequency to the serial interface
        freq = str.encode(str(frequency * 1000) + "\n")
        com.write(freq)

        # Read answer from Arduino
        cf.log_message(com.readall())

        if set_capacitance:
            closest_resonance_frequency, idx = cf.find_nearest(
                self.combinations_df["resonance_frequency"].to_numpy(), frequency
            )

            closest_capacitance = self.combinations_df.at[idx, "sum"]
            self.set_capacitance(closest_capacitance)

        # Set capacity accordingly
        # self.set_capacitance(frequency)

        self.mutex.unlock()

    def read_frequency(self):
        """
        Function that asks the arduino to return the frequency
        """
        self.mutex.lock()
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

        # cf.log_message("Arduino has the frequency " + str(frequency) + " Hz set.")
        self.mutex.unlock()
        return frequency

    def switch_cap(self, cap_no, state):
        """
        Function that shall allow to set the capacitance of the LCR circuit
        """
        self.mutex.lock()
        com = self.arduino

        # Check if serial connection was already established
        if self.serial_connection_open == False:
            self.init_serial_connection()

        if (
            self.cap_states[np.where(np.array(self.arduino_pins) == cap_no)[0]][0]
            != state
        ):
            # Write the capacitance to the arduino
            com.write(str.encode("cap" + str(cap_no) + "\n"))

            # print(com.readall())
            # time.sleep(0.5)
            self.cap_states[np.where(np.array(self.arduino_pins) == cap_no)] = state
        else:
            print("Cap " + str(cap_no) + " was already in state " + str(state))

        self.mutex.unlock()

    def set_capacitance(self, capacitance):
        """
        Sets right capacitance according to the capacitance set
        """
        self.mutex.lock()

        # Now convert resonance frequency to capacitance and find nearest in combinations array
        # resonance_capacitance = resonance_frequency_to_capacitance(frequency)
        # resonance_capacitance = frequency

        # Find closest capacitor available and convert again to resonance frequency
        self.real_capacity, idx = cf.find_nearest(
            self.combinations_df["sum"], capacitance
        )

        # Turn off all pins that are not in the above array
        for arduino_port in self.arduino_pins[
            ~np.isin(self.arduino_pins, self.combinations_df["arduino_pins"].iloc[idx])
        ]:
            self.switch_cap(arduino_port, False)

        # Turn on all pins that are in the above array
        for arduino_port in self.combinations_df["arduino_pins"].iloc[idx]:
            self.switch_cap(arduino_port, True)

        cf.log_message("Capacitance set to " + str(capacitance) + " pF")
        self.mutex.unlock()

    # The capacitances can now be matched to resonance frequencies using a fit of capacitance over resonance frequency
    # def capacitance_to_resonance_frequency(self, capacitance):
    # """
    # Function that calculates for a given capacitance the resonance frequency (current coil with 41 windings etc.)
    # Input value in pF, output value in kHz
    # """
    # A = 7.50279e-9
    # return 1 / np.sqrt(capacitance * A)

    # def resonance_frequency_to_capacitance(self, frequency):
    # """
    # Convert frequency to capacitance
    # """
    # A = 7.50279e-9
    # return 1 / (frequency ** 2 * A)

    def close(self):
        """
        Function that is called before program is closed to make sure that
        all relays are closed
        """
        self.mutex.lock()
        self.close_serial_connection()
        self.mutex.unlock()