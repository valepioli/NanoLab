import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Prova con 'Qt5Agg' se 'TkAgg' non funziona
import matplotlib.pyplot as plt

files = ["FFT_220.9kohm_noise_filter.txt", "FFT_149.9kohm_noise_filter.txt", "FFT_100.2kohm_noise_filter.txt",
         "FFT_55.67kohm_noise_filter.txt", "FFT_9.99kohm_noise_filter.txt", "FFT_0.998kohm_noise_filter.txt"]

r_values = ["220.9 kOhm", "149.9 kOhm", "100.2 kOhm", "55.67 kOhm", "9.99 kOhm", "0.99 kOhm"]

def compute_power_spectrum(v, N, dt):
    """ Compute the power spectrum of the signal """
    fft_vals = np.fft.rfft(v)  # Compute the FFT (only positive frequencies)
    power_spectrum = (np.abs(fft_vals) ** 2) / (N * dt)  # Correct normalization
    return power_spectrum

# Create a large figure window
fig = plt.figure(figsize=(20, 10))

rows, cols = 2, 3  # Arrange the plots in 2 rows and 3 columns

for idx, (file, r) in enumerate(zip(files, r_values)):
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
    t_max = time[-1]
    power = compute_power_spectrum(v_rms, N_points, dt)

    # Compute frequency values correctly
    freq = np.fft.rfftfreq(N_points, dt)

    # Apply the mask for frequencies between 1000 Hz and 9000 Hz
    mask = (freq >= 1000) & (freq <= 9000)
    freq_masked = freq[mask]
    power_masked = power[mask]

    plt.subplot(rows, cols, idx + 1)  # Place the plot in the grid
    plt.plot(freq_masked, power_masked)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Density (V^2/Hz)")
    plt.title(f"Noise Power Spectrum - {r}")
    plt.grid()

plt.tight_layout()  # Optimize spacing between plots
plt.show()
