import matplotlib.pyplot as plt

# Dati da IVtransfer.txt (Vin e Corrente)
vin_values = [-0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.1, 0.2, 0.3,
    0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3
]

current_values = [
    -0.0000260000,
    -0.0000200000,
    -0.0000080000,
    -0.0000009000,
    -0.0000004000,
    -0.0000001500,
    -0.0000000330,
    -0.0000000026,
     0.0000000005,
     0.0000000005,
     0.0000000005,
    0.0000000006,
    0.00000000067,
    0.00000000061,
    0.00000000060,
    0.00000000060,
    0.00000000061,
    0.00000000063,
    0.00000000064,
    0.00000000065,
    0.00000000068
]

# Creazione del grafico
plt.figure(figsize=(8, 5))
plt.plot(vin_values, current_values, marker='o', linestyle='-', color='blue')
plt.xlabel("Vin (V)", fontsize=14)
plt.ylabel("Current (A)", fontsize=14)
plt.title("IV characteristics of diode", fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()
