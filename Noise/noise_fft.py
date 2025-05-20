""" 
Take as input the noise datafiles.
Return plots of power spectra for each resistance.
Return plots of mean power vs resistance.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import re

files = ["FFT_220.9kohm_noise_filter.txt", "FFT_149.9kohm_noise_filter.txt", "FFT_100.2kohm_noise_filter.txt",
         "FFT_55.67kohm_noise_filter.txt", "FFT_9.99kohm_noise_filter.txt", "FFT_0.998kohm_noise_filter.txt"]

# Define numerical resistance values in kOhm
r_values_kohm = np.array([220.9, 149.9, 100.2, 55.67, 9.99, 0.99])

def compute_power_spectrum(v, N, dt):
    """ Compute the power spectrum of the signal """
    fft_vals = np.fft.rfft(v)  # Compute the FFT (only positive frequencies)
    power_spectrum = (np.abs(fft_vals) ** 2) / (N * dt)  # Normalized power
    return power_spectrum

# Create the first figure for the individual power spectra
fig1 = plt.figure(figsize=(20, 10))
rows_fig1, cols_fig1 = 2, 3  # Arrange the plots in 2 rows and 3 columns

# Lists to store computed values for the second figure's plots
V_rms_2_list = []
area_list = []

# Loop through files and resistance values
for idx, file in enumerate(files):
    r_kohm = r_values_kohm[idx] # Get the current resistance in kOhm

    with open(file, 'r') as f:
        lines = f.readlines()[2:]  # Skip the first two header lines

    time = []
    v_rms = []

    for line in lines:
        values = line.strip().split()
        time.append(float(values[0]))  # First value = time
        v_rms.append(float(values[1])) # Second value = v_rms

    time = np.array(time) - time[0]  # Normalize time starting at zero
    v_rms = np.array(v_rms)

    N_points = len(time)
    dt = time[1] - time[0]  # Time step
    power = compute_power_spectrum(v_rms, N_points, dt)

    # Compute frequency values (positive only)
    freq = np.fft.rfftfreq(N_points, dt)

    # Apply the mask for frequencies between 1000 Hz and 9000 Hz
    mask = (freq >= 1000) & (freq <= 9000)
    freq_masked = freq[mask]
    power_masked = power[mask]

    # Compute V_rms^2 and Area for the second set of plots
    V_rms_2 = np.std(v_rms)**2
    Area = np.trapz(power_masked, freq_masked)

    V_rms_2_list.append(V_rms_2)
    area_list.append(Area)

    # Plotting for the first figure
    plt.figure(fig1.number) # Set current figure to fig1 explicitly
    plt.subplot(rows_fig1, cols_fig1, idx + 1)  # Place the plot in the grid
    plt.plot(freq_masked, power_masked)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Density (V$^2$/Hz)")
    plt.title(f"Noise Power Spectrum - {r_kohm} kOhm") # Added kOhm to title
    plt.grid()

fig1.tight_layout() 

# Create a new figure for V_rms^2 vs R and Area vs R
fig2, axes = plt.subplots(1, 2, figsize=(14, 6)) # Using 'axes' for cleaner subplot handling

# Plot V_rms**2 vs R on the first subplot of fig2
axes[0].plot(r_values_kohm, V_rms_2_list, 'o-', label='$V_{rms}^2$') # Plot R directly in kOhm
axes[0].set_xlabel("Resistance (kOhm)")
axes[0].set_ylabel("$V_{rms}^2$")
axes[0].set_title("$V_{rms}^2$ vs Resistance")
axes[0].grid(True)

# Plot Area vs R on the second subplot of fig2
axes[1].plot(r_values_kohm, area_list, 'x-', label='Area') # Plot R directly in kOhm
axes[1].set_xlabel("Resistance (kOhm)")
axes[1].set_ylabel("Area (V$^2$)") # Units for area would be V^2/Hz * Hz = V^2
axes[1].set_title("Area (Integrated Power) vs Resistance")
axes[1].grid(True)

fig2.tight_layout() 

plt.show() # Display both figures
