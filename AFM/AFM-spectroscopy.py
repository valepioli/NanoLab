import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import cumtrapz
from scipy.optimize import curve_fit

file_name = 'h-Amp.txt'

data = pd.read_csv(file_name, skiprows=8, header=None, usecols=[1, 2], sep='\s+')
data.columns = ['Height', 'Amplitude']

data['Height'] = pd.to_numeric(data['Height'])
data['Amplitude'] = pd.to_numeric(data['Amplitude'])
data.dropna(inplace=True)

min_height_idx = data['Height'].idxmin()

forward_sweep_data = data.iloc[:min_height_idx + 1].copy()
backward_sweep_data = data.iloc[min_height_idx:].copy()
is_two_sweeps = True

A0_height_min = -2.6884
A0_height_max = -2.6800
A0_data = data[(data['Height'] >= A0_height_min) & (data['Height'] <= A0_height_max)].copy()
A0 = A0_data['Amplitude'].mean()

k_cantilever = 42.0 # N/m

data['Height_m'] = data['Height'] * 1e-6 # µm to m
data['Amplitude_m'] = data['Amplitude'] * 1e-9 # nm to m
A0_m = A0 * 1e-9 # nm to m

data['F_prime_z'] = -2 * k_cantilever / (A0_m**2) * (A0_m - data['Amplitude_m'])
data['F'] = cumtrapz(data['F_prime_z'], data['Height_m'], initial=0)
data['F_nN'] = data['F'] * 1e9 # Convert to nN

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.set_xlabel(r'Height ($\mu$m)')
ax1.set_ylabel('Amplitude (nm)')
if is_two_sweeps:
    ax1.plot(forward_sweep_data['Height'], forward_sweep_data['Amplitude'], marker='.', linestyle='-', color='skyblue', label='Approach Sweep')
    ax1.plot(backward_sweep_data['Height'], backward_sweep_data['Amplitude'], marker='.', linestyle='-', color='steelblue', label='Retract Sweep')
else:
    ax1.plot(data['Height'], data['Amplitude'], marker='.', linestyle='-', color='skyblue', label='Single Sweep')
ax1.tick_params(axis='y')
ax1.grid(True)

ax2 = ax1.twinx()
ax2.set_ylabel(r"$F'_z$ (N/m$^2$)")
if is_two_sweeps:
    ax2.plot(forward_sweep_data['Height'], data['F_prime_z'].loc[forward_sweep_data.index], marker='.', linestyle='-', color='skyblue')
    ax2.plot(backward_sweep_data['Height'], data['F_prime_z'].loc[backward_sweep_data.index], marker='.', linestyle='-', color='steelblue')
else:
    ax2.plot(data['Height'], data['F_prime_z'], marker='.', linestyle='-', color='skyblue')
ax2.tick_params(axis='y')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines, labels, loc='best')

plt.title(r"Amplitude and Force Gradient as a function of Height")
plt.show()

plt.figure(figsize=(10, 6))
if is_two_sweeps:
    plt.plot(forward_sweep_data['Height'], data['F_nN'].loc[forward_sweep_data.index], marker='.', linestyle='-', color='skyblue', label="Approach (Forward) Sweep")
    plt.plot(backward_sweep_data['Height'], data['F_nN'].loc[backward_sweep_data.index], marker='.', linestyle='-', color='steelblue', label="Retract (Backward) Sweep")
else:
    plt.plot(data['Height'], data['F_nN'], marker='.', linestyle='-', color='skyblue', label="Single Sweep")

plt.title(r"Force as a function of Height")
plt.xlabel(r'Height ($\mu$m)')
plt.ylabel(r"$F$ (nN)")
plt.grid(True)

def inverse_power_shifted_force(z, A, z0, n):
    term = z - z0
    return A / (term)**n

fit_height_data = data['Height_m'].loc[forward_sweep_data.index]
fit_force_data = data['F_nN'].loc[forward_sweep_data.index]

z_raw_for_fit = fit_height_data

popt, pcov = curve_fit(inverse_power_shifted_force, z_raw_for_fit, fit_force_data)
param_A, param_z0, param_n = popt

plot_z_values_m = np.linspace(z_raw_for_fit.min(), z_raw_for_fit.max(), 500)

F_fitted_curve = inverse_power_shifted_force(plot_z_values_m, param_A, param_z0, param_n)
height_for_plot = plot_z_values_m * 1e6

plt.plot(height_for_plot, F_fitted_curve, linestyle='--', color='red',
         label=f'Fit $F = A/(z-z_0)^n$\n(A={param_A:.2e}, $z_0$={param_z0*1e6:.2f} µm, n={param_n:.2f})')

plt.legend()
plt.show()
