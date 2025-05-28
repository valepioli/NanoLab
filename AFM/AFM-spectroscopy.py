import pandas as pd
import matplotlib.pyplot as plt

file_name = 'h-Amp.txt'

data = pd.read_csv(file_name, skiprows=7, header=None, usecols=[1, 2], sep='\s+')
data.columns = ['Height', 'Amplitude']

plt.figure(figsize=(10, 6))
plt.plot(data['Height'], data['Amplitude'], marker='.', linestyle='-')
plt.title('Oscillation amplitude as a function of height')
plt.xlabel(r'Height ($\mu$m)')
plt.ylabel('Amplitude (nm)')
plt.grid(True)
plt.show()