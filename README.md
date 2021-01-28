# Magnetoelectric Device Measurement and Readout

Coil driver control and read out of oscilloscope for benchmarking and automatised control of ME devices.

## Hardware

- Rigol DS1202 Z-E (1000Z Series), python api: https://github.com/jeanyvesb9/Rigol1000z
- Voltcraft PPS-16005, python api: https://github.com/ap--/voltcraft
- PCB with electric components
- Cupper Coil
- Various Capacitors of different capacity

## First Installation

- Install the python packages provided by requirements.txt best in a new virtual environment
  <!-- - Install NI IVI Compliance Package (ICP) and IVI Shared Components (https://www.ni.com/de-de/support/downloads/drivers/download.ivi-compliance-package.html#346218) -->
  <!-- - Install DS1000Z Drivers from rigol website (https://www.rigolna.com/download/) -->
- Install Ultra Sigma from the rigol website (https://www.rigolna.com/download/), takes ages to download and install
- Install Ultra Scope from rigol website
- Connect oscilloscope
- I couldn't make Ultra sigma work but the oscilloscope is now recognized by windows
- Download Voltcraft PPS-16005 software (https://www.conrad.de/de/p/voltcraft-pps-16005-labornetzgeraet-einstellbar-1-36-v-dc-0-10-a-360-w-usb-remote-programmierbar-anzahl-ausgaenge-2-513914.html?refresh=true#productDownloads)
- Against all intuition the voltcraft pps-16005 must be set to normal mode when controlled remotly by the pc and not to "Remote Control" on the rear side of the device.
  <!-- - Start Ultra Sigma -->
  <!-- - Start Ultra Scope -->

## Comments on API

- The rigol oscilloscope can be controlled with SCPI interface with the commands listed here: https://www.batronix.com/pdf/Rigol/ProgrammingGuide/DS1000DE_ProgrammingGuide_EN.pdf

## User Journey

- User should be able to set the frequency of the frequency generator to a set value
- User should be able to do a frequency sweep from one frequency to another one and also set the steps for this sweep
- User should be able to set the voltage and maximum allowed current of the power source
- The user should see a diagram with the current voltage and current reading of the power source.
- When sweeping over a frequency range a diagram with the current drawn by the coil from the source should be visible to characterise quality factor and maximum drawn current. It should build up from low frequency to high frequency and remain there until a new measurement is started.
- The user should be able to save the raw data of this graph to a data file where wavelength, voltage and current are stored.
- Additionally, to characterise the ME film, the maximum voltage on the oscilloscope should be read out and also plotted in the very same diagram (second y-axis). I am not sure yet how to measure the power output on the ME device but I am probably still a little bit away (an easy way would be to simply attach a consumer to it, otherwise a current-meter must be used somehow). The ME film voltage should be optional and even without the oscilloscope the drawn current should be visible.
- I am not sure yet but it could also come handy to simply replicate the oscilloscope image on the PC so that it would be easy to save an oscilloscope image (e.g. when measureing the frequency of a magnetic field or showing the time delay between magnetic field and stimulation signal).

## Future Features

- Button on the setup page that allows to turn on and off the source output
- There should be another widget where the user enters the capacitance of the capacitor used and the inductance of the inductor used that automatically transforms this into a resonance frequency and tells the user where that one is.
- Automatically fit the coil resonance and return q-factor, maximum and its frequency (With automatically I probably mean after setting a range and pressing the fit button)
- Fill settings with life (last priority)

## Design Choices

- To remain consist with my previous software for this group, I think a center graph with a scrollable side panel would be good, where all the parameters can be changed.
- I also want to design this with a tab widget although for now, I only have one tab in mind. However, at a later point I might want to add tabs (e.g. with oscilloscope reading etc.).
