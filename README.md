# Magnetoelectric Device Measurement and Readout

Software to control DC and RF coil to characterize ME devices.

## Setup
### First Setup

- Install the python packages provided by requirements.txt best in a new virtual environment
- Install Ultra Sigma from the rigol website (https://www.rigolna.com/download/), takes ages to download and install
- Install Ultra Scope from rigol website
- Connect oscilloscope
- I couldn't make Ultra sigma work but the oscilloscope is now recognized by windows
- Download Voltcraft PPS-16005 software (https://www.conrad.de/de/p/voltcraft-pps-16005-labornetzgeraet-einstellbar-1-36-v-dc-0-10-a-360-w-usb-remote-programmierbar-anzahl-ausgaenge-2-513914.html?refresh=true#productDownloads)
- Against all intuition the voltcraft pps-16005 must be set to normal mode when controlled remotly by the pc and not to "Remote Control" on the rear side of the device.
- Connect KORAD 3005P and install the software

### Development
- Python formatter: black

## Hardware

| Item         | Brand     | Model Number              |
| ------------ | --------- | ------------------------- |
| Oscilloscope | Rigol     | DS1202 Z-E (1000Z Series) |
| DC Source    | Korad     | KA3005P                   |
| RF Source    | Voltcraft | PPS-16005                 |

## User Journey
###

- User should be able to set the frequency of the frequency generator to a set value
- User should be able to do a frequency sweep from one frequency to another one and also set the steps for this sweep
- User should be able to set the voltage and maximum allowed current of the power hf_source
- The user should see a diagram with the current voltage and current reading of the power hf_source.
- When sweeping over a frequency range a diagram with the current drawn by the coil from the hf_source should be visible to characterise quality factor and maximum drawn current. It should build up from low frequency to high frequency and remain there until a new measurement is started.
- The user should be able to save the raw data of this graph to a data file where wavelength, voltage and current are stored.
- Additionally, to characterise the ME film, the maximum voltage on the oscilloscope should be read out and also plotted in the very same diagram (second y-axis). I am not sure yet how to measure the power output on the ME device but I am probably still a little bit away (an easy way would be to simply attach a consumer to it, otherwise a current-meter must be used somehow). The ME film voltage should be optional and even without the oscilloscope the drawn current should be visible.
- I am not sure yet but it could also come handy to simply replicate the oscilloscope image on the PC so that it would be easy to save an oscilloscope image (e.g. when measureing the frequency of a magnetic field or showing the time delay between magnetic field and stimulation signal).
