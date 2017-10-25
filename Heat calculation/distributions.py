import numpy as np
import matplotlib.pyplot as plt
import utils

def temp_distribution_over_the_height_calculation(data):
    qMax = data["kV"] * data["qSr"]
    step = 0.05
    z = np.arange(0, 1.3 + step, step)
    q = qMax * np.cos(np.pi / 2 * (data["Haz"] * 1e-3 - 2 * z) / (data["Haz"] * 1e-3 + 2 * data["deltaZ"])) * 1e6
    plt.plot(z, q)
    plt.grid(True)
    plt.xlabel(r'z, $м$', fontsize=14, fontweight='bold')
    plt.ylabel(r'q, $Вт/м^2$', fontsize=14, fontweight='bold')
    plt.show()

data = {}
utils.fill_dict_from_file(data, "distributionsInput.txt")
temp_distribution_over_the_height_calculation(data)
