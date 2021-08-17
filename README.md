# Magnetoelectric Device Characterisation

Software that interfaces several hardware components (listed below) to determine
the performance of magnetoelectric thin films. The software allows for
calibration of the devices, and control of a pair of DC Helmholtz coils as well
as a high-frequency AC coil.

Self-built electronics are interfaced with an Arduino.

## Setup
### First Setup

1. Install the python packages provided by requirements.txt best in a new virtual environment
2. Install Ultra Sigma from the rigol website (https://www.rigolna.com/download/), takes ages to download and install
3. Install Ultra Scope from rigol website
4. Connect oscilloscope
5. I couldn't make Ultra sigma work but the oscilloscope is now recognized by windows
6. Download Voltcraft PPS-16005 software (https://www.conrad.de/de/p/voltcraft-pps-16005-labornetzgeraet-einstellbar-1-36-v-dc-0-10-a-360-w-usb-remote-programmierbar-anzahl-ausgaenge-2-513914.html?refresh=true#productDownloads)
7. Against all intuition the voltcraft pps-16005 must be set to normal mode when controlled remotly by the pc and not to "Remote Control" on the rear side of the device.
8. Connect KORAD 3005P and install the software

### Development
- Python formatter: black

## Hardware

| Item         | Brand     | Model Number              |
| ------------ | --------- | ------------------------- |
| Oscilloscope | Rigol     | DS1202 Z-E (1000Z Series) |
| DC Source    | Korad     | KA3005P                   |
| RF Source    | Voltcraft | PPS-16005                 |

## User Journey
### Setup
#### Loading Window

To start the program execute main.py in your virtual environment setup as
described above. The start screen that appears should look something like this.
It will guide you through the initialisation of all different hardware
components.

In case everything went well and all hardware could be initialised the screen
will directly disappear. However, if the program had a problem initialising any
of the component it will indicate that in the following dialog. You can either
select to continue anyways if the device that could not be initialised is not
necessary for your measurements or you can troubleshoot your device and retry
the initialisation again. In case the device address is not correct, either
continue and modify it in the settings as described below or directly modify it
in the /usr/global_settings.json file.

In case everything went well or the user decided to continue anyways she will
end up with the following window.

This main window gives you several options that can be selected from the top tabs and are

- Setup
- Oscilloscope
- Resonance Frequency
- Bias Field
- Power
- Capacitance Calibration
- PID Tuning

Additionally, the user can select Settings from the top menubar. The different
tabs as well as the settings are described in more detail in the following.

#### Setup

Here the user has to define the saving path, batch name, device number and the
size of the device. These quantities are used during measurement and are saved
in the measurement file for future reference.

Furthermore, the user has the option to manually adjust all hardware parameters
for a quick test of the device and the equipment. The LCD numbers directly yield
the current value that is set at the equipment itself.

#### Oscilloscope 

Direct interface to the attached Rigol Oscilloscope allowing the user to
permanently read out the oscilloscope output and easily stop it and save it.
There is a latency of about 1 s between the updates of the oscilloscope due to a
lag in communication between computer and oscilloscope.

### Measurement

An ME device can be characterized by its resonance frequency, the bias field
necessary to obtain the maximum resonance voltage and the power that can be
generated from the device. In order to do one full characterization a device has
to be measured in this three different tabs. In case the resonance frequency is
already roughly known this should take less than 5-10 min per device.

#### Resonance Frequency
The resonance frequency tab allows the user to sweep over a broad frequency
range (depending on coil capacitance configuration) to identify the resonance
frequency of the investigated ME device. For this the user enters all relevant
parameters for the measurement and can decide on some automatization options.


#### Bias Field
#### Power 

### Calibration
#### Capacitance Calibration
#### PID Tuning 