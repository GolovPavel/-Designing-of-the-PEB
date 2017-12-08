import matplotlib.pyplot as plt

x = [0, 0.13, 0.26, 0.39, 0.52, 0.65, 0.78, 0.91, 1.04, 1.17, 1.30]
y = [1.042, 1.042, 1.041, 1.040, 1.038, 1.034, 1.027, 1.018, 1.008, 1.002, 1.00]

plt.plot(x, y)
plt.grid(True)
plt.xlabel(r'z,$м$', fontsize=14, fontweight='bold')
plt.ylabel(r'$k_{eff}$', fontsize=14, fontweight='bold')
plt.show()
