import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import cumtrapz

file_name = 'h-Amp.txt'

# Read the data
data = pd.read_csv(file_name, skiprows=8, header=None, usecols=[1, 2], sep='\s+')
data.columns = ['Height', 'Amplitude']

# Convert columns to numeric and drop NaNs
data['Height'] = pd.to_numeric(data['Height'], errors='coerce')
data['Amplitude'] = pd.to_numeric(data['Amplitude'], errors='coerce')
data.dropna(inplace=True)

# --- Identify and separate forward and backward sweeps ---
# Find the index of the minimum height, which indicates the turning point
min_height_idx = data['Height'].idxmin()

forward_sweep_data = pd.DataFrame()
backward_sweep_data = pd.DataFrame()
is_two_sweeps = False

# Check if a clear turning point exists (not at the beginning or end)
if min_height_idx > 0 and min_height_idx < len(data) - 1:
    forward_sweep_data = data.iloc[:min_height_idx + 1].copy()
    backward_sweep_data = data.iloc[min_height_idx:].copy()
    is_two_sweeps = True
    print("Detected both forward (approach) and backward (retract) sweeps.")
elif data['Height'].is_monotonic_decreasing:
    forward_sweep_data = data.copy()
    print("Detected a single sweep (likely approach), as Height is monotonically decreasing.")
elif data['Height'].is_monotonic_increasing:
    backward_sweep_data = data.copy()
    print("Detected a single sweep (likely retract), as Height is monotonically increasing.")
else:
    # If not monotonic and no clear turning point, assume single sweep for calculations but plot all data
    forward_sweep_data = data.copy()
    print("Could not clearly determine forward/backward sweeps. Processing as a single sweep.")


# Define the height range for determining A0 (the "flat part" where no interaction occurs)
# User specified this range: -2.6884 to -2.6800
A0_height_min = -2.6884
A0_height_max = -2.6800

# Filter the data for A0 calculation using the entire dataset
A0_data = data[(data['Height'] >= A0_height_min) & (data['Height'] <= A0_height_max)].copy()

# Determine A0 (free oscillation amplitude) by taking the mean of amplitude in this "flat" region
if len(A0_data) > 0:
    A0 = A0_data['Amplitude'].mean()
    print(f"A0 (Free oscillation amplitude, calculated as mean in range [{A0_height_min}, {A0_height_max}]): {A0:.2f} nm")
else:
    raise ValueError(f"Not enough data points in the specified A0 range ({A0_height_min} to {A0_height_max}) to determine A0.")

# Set the cantilever spring constant (k)
k_cantilever = 42.0  # N/m

# --- Unit conversion to SI units for calculations ---
# Convert Height from micrometers to meters
data['Height_m'] = data['Height'] * 1e-6 # µm to m
# Convert Amplitude from nanometers to meters
data['Amplitude_m'] = data['Amplitude'] * 1e-9 # nm to m
A0_m = A0 * 1e-9 # nm to m

# --- Calculate F'z using Equation (7) for the entire data range ---
# F'z = -2k / A0^2 * (A0 - A)
# Reminder: Based on units, F'z will be in N/m^2 if k is N/m and A0, A are in m.
data['F_prime_z'] = -2 * k_cantilever / (A0_m**2) * (A0_m - data['Amplitude_m'])

# --- Integrate F'z to get F for the entire data range ---
# F = integral(F'z dz)
# Since data is sorted by Height in decreasing order (furthest to closest),
# we integrate directly using cumtrapz.
# Assume F = 0 at the furthest point (first data point in the sorted array)
# cumtrapz computes the cumulative integral using the trapezoidal rule.
# The result will be in N/m (N/m^2 * m = N/m)
# For the first point, cumtrapz returns 0, so we fill it with 0 if initial was not specified.
data['F'] = cumtrapz(data['F_prime_z'], data['Height_m'], initial=0)


# --- Plotting the original data with forward/backward sweeps using similar colors ---
plt.figure(figsize=(10, 6))
if is_two_sweeps:
    plt.plot(forward_sweep_data['Height'], forward_sweep_data['Amplitude'], marker='.', linestyle='-', color='skyblue', label='Approach (Forward) Sweep')
    plt.plot(backward_sweep_data['Height'], backward_sweep_data['Amplitude'], marker='.', linestyle='-', color='steelblue', label='Retract (Backward) Sweep')
else:
    plt.plot(data['Height'], data['Amplitude'], marker='.', linestyle='-', color='skyblue', label='Single Sweep')

plt.title('Oscillation amplitude as a function of height')
plt.xlabel(r'Height ($\mu$m)')
plt.ylabel('Amplitude (nm)')
plt.grid(True)
plt.legend()
plt.show()


# --- Plotting F'z with forward/backward sweeps using similar colors ---
plt.figure(figsize=(10, 6))
if is_two_sweeps:
    plt.plot(forward_sweep_data['Height'], data['F_prime_z'].loc[forward_sweep_data.index], marker='.', linestyle='-', color='skyblue', label="Approach (Forward) Sweep")
    plt.plot(backward_sweep_data['Height'], data['F_prime_z'].loc[backward_sweep_data.index], marker='.', linestyle='-', color='steelblue', label="Retract (Backward) Sweep")
else:
    plt.plot(data['Height'], data['F_prime_z'], marker='.', linestyle='-', color='skyblue', label="Single Sweep")

plt.title(r"Derivative of Force ($F'_z$) as a function of Height (using Eq. 7)")
plt.xlabel(r'Height ($\mu$m)')
plt.ylabel(r"$F'_z$ (N/m$^2$)") # Units noted based on formula dimensions
plt.grid(True)
plt.legend()
plt.show()

# --- Plotting F with forward/backward sweeps in the same style as other graphs ---
plt.figure(figsize=(10, 6))
if is_two_sweeps:
    plt.plot(forward_sweep_data['Height'], data['F'].loc[forward_sweep_data.index], marker='.', linestyle='-', color='skyblue', label="Approach (Forward) Sweep")
    plt.plot(backward_sweep_data['Height'], data['F'].loc[backward_sweep_data.index], marker='.', linestyle='-', color='steelblue', label="Retract (Backward) Sweep")
else:
    plt.plot(data['Height'], data['F'], marker='.', linestyle='-', color='skyblue', label="Single Sweep")

plt.title(r"Force ($F$) as a function of Height (Integrated from $F'_z$)")
plt.xlabel(r'Height ($\mu$m)')
plt.ylabel(r"$F$ (N/m)") # Units noted based on formula dimensions
plt.grid(True)
plt.legend()
plt.show()

print("\nCalculations complete. Please review the plots and the unit considerations mentioned above.")