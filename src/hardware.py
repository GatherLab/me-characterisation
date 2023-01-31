import pyvisa
import serial

from PySide2 import QtCore
from serial.serialutil import SerialException, SerialTimeoutException

import core_functions as cf
import physics_functions as pf
from physics_functions import calculate_resonance_frequency

import time
import re
import sys

from simple_pid import PID

import math
import copy
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
        self.mutex = QtCore.QMutex(QtCore.QMutex.Recursive)

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

        # Change scale of both channels so that they are well defined
        # make sure that the scales are not random but follow some logic
        self.available_scales = np.array(
            [10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]
        )

        self.scales = np.repeat(2.0, 2)
        # self.change_scale(1, 2)
        # self.change_scale(2, 2)

        # Also set both to zero
        self.osci.write(":CHAN1:OFFSET 0")
        self.osci.write(":CHAN2:OFFSET 0")

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

    def change_scale(self, channel, scale):
        """
        Function that allows the easy change of scale of a channel on the oscilloscope
        """
        self.mutex.lock()
        if int(channel) not in [1, 2]:
            cf.log_message("Channel does not exist on this oscilloscope.")
            return
        if scale > 10:
            cf.log_message("Scale can not be set higher than 10 V")
            return
        elif scale < 0.001:
            cf.log_message("Scale can not be set below 1 mV")
            return

        # Choose closest available scale
        available_scales_smaller = self.available_scales[self.available_scales <= scale]
        scale_to_set = available_scales_smaller[
            (np.abs(available_scales_smaller - scale)).argmin()
        ]

        # Set scale
        self.osci.write(":CHAN" + str(channel) + ":SCALE " + str(scale_to_set))

        # Change the value of the scale in the array
        self.scales[int(channel - 1)] = scale_to_set
        time.sleep(0.2)

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

    def auto_scale(self, channel):
        """
        I am not yet sure how to do it but this would be an important and
        nice feature. The idea is to mimic the auto scale feature of the
        oscilloscope
        """
        self.mutex.lock()
        vmax = 0
        # Check if the oscillscope has to be rescaled
        while True:
            # Measure Vmax
            self.osci.write(":MEAS:VMAX? CHAN" + str(channel))
            vmax = self.osci.read()

            index_scale = np.where(
                self.available_scales == self.scales[int(channel) - 1]
            )[0][0]

            # Now check if the next scale is already the smallest or largest available
            if index_scale + 1 == np.size(self.available_scales):
                next_smaller_scale = np.min(self.available_scales)
                next_larger_scale = self.available_scales[index_scale - 1]
            elif index_scale == 0:
                next_larger_scale = np.max(self.available_scales)
                next_smaller_scale = self.available_scales[index_scale + 1]
            else:
                next_smaller_scale = self.available_scales[index_scale + 1]
                next_larger_scale = self.available_scales[index_scale - 1]

            if float(vmax) > 10000:
                self.change_scale(channel, next_larger_scale)
                time.sleep(0.5)
            elif float(vmax) < 4 * next_smaller_scale and float(vmax) >= 0.01:
                self.change_scale(channel, next_smaller_scale)
            else:
                break
            print(self.scales)

        self.mutex.unlock()
        return vmax

        # cf.log_message(self.osci.read())

    def measure(self, channel=1):
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

        # # Measure Vmax
        # self.osci.write(":MEAS:VMAX? CHAN" + str(channel))
        # vmax = self.osci.read()
        vmax = self.auto_scale(channel)

        # Measre VPP
        self.osci.write(":MEAS:VPP? CHAN" + str(channel))
        vpp = self.osci.read()

        # # # Measure Vmin
        self.osci.write(":MEAS:VMIN? CHAN" + str(channel))
        vmin = self.osci.read()

        # # # Measure frequency
        self.osci.write(":MEAS:FREQ? CHAN" + str(channel))
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

    def measure_vmax(self, channel=1):
        """
        Measure Vavg only
        """
        self.mutex.lock()

        vmax = self.auto_scale(channel)
        # # Measre vavg
        # self.osci.write(":MEAS:VMAX? " + channel)

        # vmax = self.osci.read()

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
        self.set_voltage(1)
        self.set_current(0.1)

        cf.log_message("Voltcraft Source successfully initialised")

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

        # Mode is not returned since this function is never used
        return voltage, current

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
        elif voltage < 0.8:
            cf.log_message(
                "You are attempting to set the voltage below the capabilities of the power supply. This is not possible."
            )
            return

        self.query("VOLT%03d" % voltage_int)
        cf.log_message("Source voltage set to " + str(voltage))
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

    def start_constant_magnetic_field_mode(
        self, pid_parameters, set_point, maximum_voltage
    ):
        """
        Start constant magnetic field mode according to a set value
        """
        try:
            del self.pid
        except:
            print("PID did not yet exist")

        self.pid = PID(
            pid_parameters[0],
            pid_parameters[1],
            pid_parameters[2],
            setpoint=set_point,
        )
        # Minimum of one volt is required by the voltcraft source
        self.pid.output_limits = (1, maximum_voltage)

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
        self.mutex.lock()
        a = 0
        start_time = time.time()
        while True:
            # Calculate the magnetic field using a pickup coil
            magnetic_field = (
                pf.calculate_magnetic_field_from_Vind(
                    pickup_coil_windings,
                    pickup_coil_radius * 1e-3,
                    float(osci.measure_vmax(1)),
                    frequency * 1e3,
                )
                * 1e3
            )

            # ask for optimum value of pid
            pid_voltage = self.pid(magnetic_field)

            # Set the voltage to that value (rounded to the accuracy of the
            # source)
            self.set_voltage(round(pid_voltage, 1))

            # Wait for a bit so that the hardware can react
            time.sleep(0.05)

            # If the magnetic field and the setpoint deviate by less than 0.02,
            # increase a else set it back to zero
            if math.isclose(self.pid.setpoint, magnetic_field, rel_tol=0.03):
                a += 1
            else:
                a = 0

            # Only break if this is the case for several iterations
            if a >= 5:
                break

            # Measure the elapsed time to keep track of how long the adjustment
            # takes. If it already took longer than 10 s, break
            elapsed_time = time.time() - start_time
            if break_if_too_long:
                if elapsed_time >= 6:
                    break

        print(elapsed_time)

        self.mutex.unlock()
        return pid_voltage, elapsed_time

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
        import pydevd

        pydevd.settrace(suspend=False)

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

        # Frequency in kHz
        self.frequency = 1000
        self.frequency_on = True

        self.resistor_on = False

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
        temp_combinations_df = (
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
            .drop_duplicates(subset=["sum"], keep="first", ignore_index=True)
        )

        # Add additional column with resonance frequency

        temp_combinations_df["resonance_frequency"] = np.empty(
            len(temp_combinations_df)
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
        for index, capacitance in temp_combinations_df["sum"].items():
            temp_combinations_df.loc[index, "resonance_frequency"] = (
                calculate_resonance_frequency(
                    capacitance * 1e-12, global_settings["coil_inductance"] * 1e-3
                )
                / 1e3
            )

        # Thin out the resonances to only obtain those close to a digit number
        # min_frequency = int(round(temp_combinations_df["resonance_frequency"].min(), 0))
        # max_frequency = int(round(temp_combinations_df["resonance_frequency"].max(), 0))

        # for freq in np.arange(min_frequency, max_frequency + 1, 1):
        #     temp_series = pd.Series(
        #         temp_combinations_df.iloc[
        #             (temp_combinations_df.resonance_frequency - freq)
        #             .abs()
        #             .argsort()[:1]
        #         ].values[0],
        #         index=["constituents", "arduino_pins", "sum", "resonance_frequency"],
        #     )
        #     self.combinations_df = self.combinations_df.append(
        #         temp_series, ignore_index=True
        #     )

        # Now drop duplicates
        temp_combinations_df = temp_combinations_df.drop_duplicates(
            "resonance_frequency", ignore_index=True
        )

        self.all_capacitances_df = copy.copy(temp_combinations_df)

        # Now replace those values that do exist in the calibration file with these resonance frequencies
        for index, capacitance in temp_combinations_df["sum"].items():
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
                temp_combinations_df.loc[
                    index, "resonance_frequency"
                ] = calibration.loc[
                    calibration["capacitance"] == capacitance, "resonance_frequency"
                ].to_list()[
                    0
                ]
            else:
                cf.log_message(
                    "Capacitance "
                    + str(capacitance)
                    + " pF not found in calibration file"
                )

        # Now cut out all entries that are not present in the calibration file
        # but are within its frequency range
        self.combinations_df = temp_combinations_df.drop(
            temp_combinations_df.loc[
                np.logical_and(
                    np.logical_and(
                        temp_combinations_df["sum"] >= calibration["capacitance"].min(),
                        temp_combinations_df["sum"] <= calibration["capacitance"].max(),
                    ),
                    ~temp_combinations_df["sum"].isin(calibration["capacitance"]),
                )
            ].index
        ).reset_index(drop=True)

        # self.combinations_df = pd.DataFrame(
        # columns=["constituents", "arduino_pins", "sum", "resonance_frequency"]
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
        freq = str.encode("freq_" + str(frequency * 1000) + "\n")
        com.write(freq)
        time.sleep(0.1)

        # Read answer from Arduino
        cf.log_message(com.readall())

        if set_capacitance:
            closest_resonance_frequency, idx = cf.find_nearest(
                self.combinations_df["resonance_frequency"].to_numpy(), frequency
            )

            closest_capacitance = self.combinations_df.at[idx, "sum"]
            self.set_capacitance(closest_capacitance)

        # Set capacitance accordingly
        # self.set_capacitance(frequency)
        self.frequency = frequency

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

    def read_cap_states(self):
        """
        Function that asks the arduino to return the frequency
        """
        self.mutex.lock()
        com = self.arduino

        # Check if serial connection was already established
        if self.serial_connection_open == False:
            self.init_serial_connection()

        # Write the frequency to the serial interface
        com.write(str.encode("cap\n"))
        time.sleep(0.3)

        # Read answer from Arduino
        try:
            cap_states = np.array(list(str(com.readall()))[2:-3], dtype=int) == 1
        except:
            cf.log_message("Could not convert capacitor states to array")

        # This is no universal ordering yet, I have to do this later on
        self.cap_states = cap_states[self.arduino_pins - 1]
        print(self.cap_states)
        self.mutex.unlock()

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
            com.write(str.encode("cap_" + str(cap_no) + "\n"))

            # print(com.readall())
            # time.sleep(0.5)
            self.cap_states[np.where(np.array(self.arduino_pins) == cap_no)] = state
        # else:
        # print("Cap " + str(cap_no) + " was already in state " + str(state))

        self.mutex.unlock()

    def set_capacitance(self, capacitance):
        """
        Sets right capacitance according to the capacitance set
        """
        self.mutex.lock()

        # Check the real capacitor states
        self.read_cap_states()

        # Now convert resonance frequency to capacitance and find nearest in combinations array
        # resonance_capacitance = resonance_frequency_to_capacitance(frequency)
        # resonance_capacitance = frequency

        # Find closest capacitor available and convert again to resonance frequency
        self.real_capacitance, idx = cf.find_nearest(
            self.combinations_df["sum"], capacitance
        )

        # Turn off all pins that are not in the above array
        for arduino_port in self.arduino_pins[
            ~np.isin(self.arduino_pins, self.combinations_df["arduino_pins"].iloc[idx])
        ]:
            self.switch_cap(arduino_port, False)
            # print("Turned off pin " + str(arduino_port))
            # time.sleep(0.1)

        # Turn on all pins that are in the above array
        for arduino_port in self.combinations_df["arduino_pins"].iloc[idx]:
            self.switch_cap(arduino_port, True)
            # print("Turned on pin " + str(arduino_port))
            # time.sleep(0.1)

        cf.log_message("Capacitance set to " + str(capacitance) + " pF")
        self.mutex.unlock()

    def set_resistance(self, resistance):
        """
        Function that allows to set the resistance on the Arduino (by using
        the Serial Connection interface)
        """
        self.mutex.lock()
        com = self.arduino

        # Check if serial connection was already established
        if self.serial_connection_open == False:
            self.init_serial_connection()

        # Write the resistance to the serial interface
        freq = str.encode("res_" + str(int(resistance)) + "\n")
        com.write(freq)

        # Read answer from Arduino
        cf.log_message(com.readall())
        # cf.log_message("Resistance set to " + str(resistance) + " pF")

        self.mutex.unlock()

    def read_resistance(self):
        """
        Function that asks the arduino to return the set resistance
        """
        self.mutex.lock()
        com = self.arduino

        # Check if serial connection was already established
        if self.serial_connection_open == False:
            self.init_serial_connection()

        # Write the frequency to the serial interface
        com.write(str.encode("res\n"))

        # Read answer from Arduino
        resistance = com.readall()
        try:
            resistance = int(resistance)
        except:
            cf.log_message("Could not convert resistance to float")

        # cf.log_message("Arduino has the frequency " + str(frequency) + " Hz set.")
        self.mutex.unlock()
        return resistance

    def turn_resistor_on(self):
        """
        Function that turns on relays allowing to work with the variable resistor
        """
        self.mutex.lock()
        com = self.arduino
        # Check if serial connection was already established
        if self.serial_connection_open == False:
            self.init_serial_connection()

        # Write the command to turn on/off the resistor
        if not self.resistor_on:
            com.write(str.encode("reson\n"))
            self.resistor_on = True
        else:
            cf.log_message("Resistor is already on")

        self.mutex.unlock()

    def turn_resistor_off(self):
        """
        Function that turns on relays allowing to work with the variable resistor
        """
        self.mutex.lock()
        com = self.arduino
        # Check if serial connection was already established
        if self.serial_connection_open == False:
            self.init_serial_connection()

        # Write the command to turn on/off the resistor
        if self.resistor_on:
            com.write(str.encode("reson\n"))
            self.resistor_on = False
        else:
            cf.log_message("Resistor is already off")

        self.mutex.unlock()

    def trigger_frequency_generation(self, state):
        """
        Function that turns on the frequency generator SI5351A
        """
        self.mutex.lock()
        com = self.arduino
        # Check if serial connection was already established
        if self.serial_connection_open == False:
            self.init_serial_connection()

        # Write the command to turn on/off the frequency generation (true to enable, false to disable)
        com.write(str.encode("trig_" + str(int(state)) + "\n"))

        self.frequency_on = state

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


class KoradSource:
    """
    Class to control the KORAD KA3005P source
    The korad source is controlled via the serial interface
    A usefull source for this is
    https://github.com/vb0/korad/blob/master/kcontrol.py and
    https://sigrok.org/wiki/Korad_KAxxxxP_series#Protocol
    """

    def __init__(self, source_address, dc_field_conversion_factor):
        """
        Initialise KORAD source
        """
        import pydevd

        pydevd.settrace(suspend=False)
        self.mutex = QtCore.QMutex(QtCore.QMutex.Recursive)

        rm = pyvisa.ResourceManager()
        # The actual addresses for the devices can be accessed via rm.list_resources()
        visa_resources = rm.list_resources()

        # Check if source is present at the given address
        if source_address not in visa_resources:
            cf.log_message("The Korad Source seems to be absent or switched off.")

        # Time out is in ms
        source_port = "COM" + re.findall(r"\d+", source_address)[0]

        self.source = serial.Serial(source_port, timeout=1)

        # To see if device is on or not. There is no built-in function for the
        # voltcraft device. This is always true when the software was not used
        # previously. Otherwise the output state will only be the correct one
        # after the first usage of self.output()
        self.output_state = True

        self.dc_field_conversion_factor = dc_field_conversion_factor

        # # Now query details about the instrument
        # gmax = self.query("GMAX")
        self.maximum_voltage = 30
        self.maximum_current = 5

        self.output(False)
        self.set_voltage(20)
        self.current_voltage_value = 20
        self.set_current(0.05)

        cf.log_message("Korad Source successfully initialised")

    def read_values(self):
        """
        Function that returns the display readings of the source in volt and
        ampere. This takes about 20 - 25 ms to run
        """
        self.mutex.lock()
        # The source will return something liek 119700020 which translates to:
        # U = 11.97 V, I = 0.00 A and it is in C.V. mode (constant voltage)
        self.source.write(b"VOUT1?")
        raw_voltage = self.source.read(5).decode()
        try:
            voltage = float(raw_voltage)
        except:
            cf.log_message("Couldn't read out voltage")
            voltage = 0

        time.sleep(0.2)
        self.source.write(b"IOUT1?")
        raw_current = self.source.read(5).decode()
        try:
            current = float(raw_current)
        except:
            cf.log_message("Couldn't read out current")
            current = 0

        magnetic_field = current * self.dc_field_conversion_factor

        time.sleep(0.2)
        # Now disect this string

        self.mutex.unlock()
        return voltage, current, magnetic_field

    def set_voltage(self, voltage):
        """
        Function to set the voltage of the device
        """
        # self.mutex.lock()
        # The voltcraft device, however can not deal with floats. Therefore, we
        # have to convert the input first
        voltage = np.round(voltage, 2)

        if voltage > self.maximum_voltage:
            cf.log_message(
                "You are attempting to exceed the maximum voltage rating of your device of "
                + str(np.round(self.maximum_voltage, 2))
                + " V. I set the voltage to this value for you instead."
            )
            voltage = np.round(self.maximum_voltage, 2)
        elif voltage < 0:
            cf.log_message(
                "You are attempting to set the voltage to a negative value. This is not possible. I set the voltage to 0 V for you instead"
            )
            voltage = 0

        try:
            self.source.write(str.encode("VSET1:" + str(voltage)))
        except SerialTimeoutException as err:
            cf.log_message(err)
            time.sleep(0.2)
            self.source.write(str.encode("VSET1:" + str(voltage)))

        time.sleep(0.2)
        # self.mutex.unlock()

    def set_current(self, current):
        """
        Set current of the device
        """
        # self.mutex.lock()
        # The voltcraft device, however can not deal with floats. Therefore, we
        # have to convert the input first
        current = np.round(current, 3)

        if current > self.maximum_current:
            cf.log_message(
                "You are attempting to exceed the maximum voltage rating of your device of "
                + str(np.round(self.maximum_current, 1))
                + " V. I set the voltage to this value for you instead."
            )
            current = np.round(self.maximum_current, 1)
        elif current < 0:
            cf.log_message(
                "You are attempting to set the voltage to a negative value. This is not possible. I set the voltage to 0 V for you instead"
            )
            current = 0

        self.source.write(str.encode("ISET1:" + str(current)))
        time.sleep(0.2)
        # self.mutex.unlock()

    def set_magnetic_field(self, magnetic_field):
        """
        Function that converts a value for a magnetic field to a current that
        can be set on the source
        """
        current = magnetic_field / self.dc_field_conversion_factor

        self.set_current(current)

    def start_constant_magnetic_field_mode(
        self, pid_parameters, set_point, maximum_voltage
    ):
        """
        Start constant magnetic field mode according to a set value
        """
        try:
            del self.pid
        except:
            print("PID did not yet exist")

        self.pid = PID(
            pid_parameters[0],
            pid_parameters[1],
            pid_parameters[2],
            setpoint=set_point,
        )
        # Minimum of one volt is required by the voltcraft source
        self.pid.output_limits = (1, maximum_voltage)

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
        self.mutex.lock()
        a = 0
        start_time = time.time()
        while True:
            # Calculate the magnetic field using a pickup coil
            magnetic_field = (
                pf.calculate_magnetic_field_from_Vind(
                    pickup_coil_windings,
                    pickup_coil_radius * 1e-3,
                    float(osci.measure_vmax(1)),
                    frequency * 1e3,
                )
                * 1e3
            )

            # ask for optimum value of pid
            pid_voltage = self.pid(magnetic_field)

            # Set the voltage to that value (rounded to the accuracy of the
            # source)
            self.set_voltage(round(pid_voltage, 2))

            # Wait for a bit so that the hardware can react
            time.sleep(0.05)

            # If the magnetic field and the setpoint deviate by less than 0.02,
            # increase a else set it back to zero
            if math.isclose(self.pid.setpoint, magnetic_field, rel_tol=0.03):
                a += 1
            else:
                a = 0

            # Only break if this is the case for several iterations
            if a >= 5:
                break

            # Measure the elapsed time to keep track of how long the adjustment
            # takes. If it already took longer than 10 s, break
            elapsed_time = time.time() - start_time
            if break_if_too_long:
                if elapsed_time >= 6:
                    break

        print(elapsed_time)

        self.mutex.unlock()
        return pid_voltage, elapsed_time

    def output(self, state, slow=False):
        """
        Activate or deactivate output:
        state = True: output on
        state = False: output off
        The device communication fails if the device is already on and one
        asks it to turn on. This possbile error must be checked for first
        (maybe class variable).
        """
        # self.mutex.lock()
        # The logic of the voltcraft source is just the other way around than
        # my logic (true means off)
        if slow:
            voltage, current = self.read_values()
            self.set_voltage(round(voltage / 4, 2))

            self.source.write(str.encode("OUT" + str(int(state))))
            time.sleep(1)

            self.set_voltage(round(voltage / 2, 2))
            time.sleep(0.2)
            self.set_voltage(round(voltage, 2))
            time.sleep(0.2)
        else:
            try:
                self.source.write(str.encode("OUT" + str(int(state))))

            except SerialTimeoutException as err:
                cf.log_message(err)
                time.sleep(0.2)
                self.source.write(str.encode("OUT" + str(int(state))))

            # Wait shortly because the source needs a bit until the final voltage is reached
            time.sleep(1)

        # Set the state variable
        self.output_state = state

        # self.mutex.unlock()

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
