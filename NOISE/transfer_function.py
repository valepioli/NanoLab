import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Make all text bigger
plt.rcParams.update({
    'font.size': 16,         # default text size
    'axes.labelsize': 18,    # x and y labels
    'axes.titlesize': 20,    # title
    'legend.fontsize': 16,   # legend
    'xtick.labelsize': 14,   # x ticks
    'ytick.labelsize': 14    # y ticks
})

# Definition of the transfer function (low pass filter)
def gain_function(f, G0, fb):
    return G0 / np.sqrt(1 + (f / fb)**2)

# Load data
data = np.loadtxt("gain_vs_freq.txt", skiprows=2)
frequencies = data[:, 1]
gains = data[:, 0]

# Sort data by frequency
sorted_indices = np.argsort(frequencies)
frequencies = frequencies[sorted_indices]
gains = gains[sorted_indices]

# Fit data
popt, pcov = curve_fit(gain_function, frequencies, gains, p0=[1000, 10000])
G0_fit, fb_fit = popt
G0_err, fb_err = np.sqrt(np.diag(pcov))

# Generate fitted curve
f_fit = np.logspace(np.log10(min(frequencies)), np.log10(max(frequencies)), 500)
gain_fit = gain_function(f_fit, *popt)

# Plot
plt.figure(figsize=(9, 6))
plt.plot(frequencies, gains, 'o', label='Experimental data')
plt.plot(f_fit, gain_fit, '-',
         label=fr'Fit: $G_0$ = {G0_fit:.1f}±{G0_err:.1f}, $f_b$ = {fb_fit/1000:.2f}±{fb_err/1000:.2f} kHz')
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')
plt.title('Transfer Function and Fit')
plt.grid(True, which="both", linestyle="--", linewidth=0.6)
plt.legend()
plt.tight_layout()
plt.show()
