import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from scipy.optimize import curve_fit

data = pd.read_csv(
    "C:\\Users\\GatherLab-Julian\\Documents\\Nextcloud\\01-Studium\\03-Promotion\\02-Data\ME-Devices\\2021-02-10_Capacitance-Sweep\\2021-02-10_test_d0_3300.0pF_03.csv",
    sep="\t",
    skiprows=5,
    names=["frequency", "voltage", "current"],
)

calibration = pd.read_csv(
    "C:/Users/GatherLab-Julian/Documents/Nextcloud/01-Studium/03-Promotion/02-Data/ME-Devices/2021-02-16_Capacitance-calibration/2021-02-16_settling-time-01-freq-step-02_resonances_02.csv",
    sep="\t",
    skiprows=6,
    names=[
        "capacitance",
        "resonance_frequency",
        "quality_factor",
        "maximum_current",
    ],
)


class ResonanceFit:
    """
    Class that wraps the fitting of a resonance
    """

    def __init__(self, resistance, voltage):
        self.v0 = voltage
        self.R = resistance

    def func(self, w, w0, Q):
        """
        Inverse square
        """
        # Set initial voltage and resistance
        return self.v0 / np.sqrt(
            self.R ** 2
            + Q ** 2
            * self.R ** 2
            / (w0 * 2 * np.pi * 1e5) ** 2
            / (w * 2 * np.pi * 1e5) ** 2
            * (((w * 2 * np.pi * 1e5) ** 2 - (w0 * 2 * np.pi * 1e5) ** 2)) ** 2
        )

    def fit(self, x, y):
        """
        Does the actual fitting
        """

        # Get the frequency at the curve maximum as initial parameter
        freq_at_max = x[np.where(y == np.max(y))][0]

        # Do the fit using initial parameters and bounds on the parameters
        popt, pcov = curve_fit(
            self.func,
            x,
            y,
            p0=[freq_at_max, 120],
            bounds=([50, 0], [1000, 1000]),
        )
        return popt, pcov


fit_class = ResonanceFit(resistance=12, voltage=5)
popt, pcov = fit_class.fit(data["frequency"].to_numpy(), data["current"].to_numpy())


# Print optimised parameters
print(popt)

# Plot graphs
plt.close()

# Plot the initial data
plt.scatter(data["frequency"], data["current"])
# plt.plot(data["frequency"], func(data["frequency"], *popt))

# Extend the plotted range
x_fit = np.linspace(data["frequency"].min(), data["frequency"].max(), 500)
plt.plot(x_fit, fit_class.func(x_fit, *popt), color="orange")
plt.show()