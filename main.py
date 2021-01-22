from hardware import RigolOscilloscope, VoltcraftSource

import matplotlib.pylab as plt
import time

# rigol_source_address = "USB0::0x1AB1::0x0517::DS1ZE223304729::INSTR"
# oscilloscope = RigolOscilloscope(rigol_source_address)
#
# start_time = time.time()
# data, time_data = oscilloscope.get_data()
# print("Acquireing data takes " + str(time.time() - start_time) + " s")
# print(time.time())

voltcraft_source_address = "ASRL4::INSTR"
source = VoltcraftSource(voltcraft_source_address)
# source.output(True)
voltage, current, mode = source.read_values()
print(voltage, current)


# plt.close()
# plt.plot(time_data, data)
# plt.show()


# rm = visa.ResourceManager()

# # We are connecting the oscilloscope through USB here.
# # Only one VISA-compatible instrument is connected to our computer,
# # thus the first resource on the list is our oscilloscope.
# # You can see all connected and available local devices calling
# #
# # print(rm.list_resources())
# #
# osc_resource = rm.open_resource(rm.list_resources()[0])

# osc = rigol1000z.Rigol1000z(osc_resource)

# # Change voltage range of channel 1 to 50mV/div.
# osc[1].set_vertical_scale_V(50e-3)

# # Stop the scope.
# osc.stop()

# # Start the oscilloscope
# # osc.run()

# # Autoscale the oscilloscope
# # osc.autoscale()

# # Take a screenshot.
# osc.get_screenshot("screenshot.png", "png")

# # Capture the data sets from channels 1--4 and
# # write the data sets to their own file.
# for c in range(1, 5):
#     osc[c].get_data("raw", "channel%i.dat" % c)
