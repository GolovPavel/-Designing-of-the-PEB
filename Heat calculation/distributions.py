import numpy as np
import matplotlib.pyplot as plt
import utils
import sympy as sp

step = 0.05
z = np.arange(0, 1.3 + step, step)

def q_distribution_over_the_height_calc(data):
    qMax = data["kV"] * data["qSr"]
    q = qMax * np.cos(np.pi / 2 * (data["Haz"] - 2 * z) / (data["Haz"] + 2 * data["deltaZ"])) * 1e6

    plt.plot(z, q)
    plt.grid(True)
    plt.title("фыв")
    plt.xlabel(r'z, $м$', fontsize=14, fontweight='bold')
    plt.ylabel(r'q, $Вт/м^2$', fontsize=14, fontweight='bold')
    plt.show()

def temp_distribution_of_water_over_the_height_calc(data):
    qMax = data["kV"] * data["qSr"] * 1e6

    f0 = -1 / np.pi * (data["Haz"] + 2 * data["deltaZ"]) * np.sin(np.pi / 2 * ((data["Haz"]) / (data["Haz"] + 2 * data["deltaZ"])))
    f = -1 / np.pi * (data["Haz"] + 2 * data["deltaZ"]) * np.sin(np.pi / 2 * ((data["Haz"] - 2 * z) / (data["Haz"] + 2 * data["deltaZ"]))) - f0

    t_water = data["tVhR"] + (data["kG"] * data["Pt"] * qMax) / (data["kQ"] * data["kR"] * data["Gtn"] * data["Cp"]) * f

    plt.plot(z, t_water)
    plt.grid(True)
    plt.xlabel(r'z, $м$', fontsize=14, fontweight='bold')
    plt.ylabel(r't, $^oC$', fontsize=14, fontweight='bold')
    plt.show()



data = {}
utils.fill_dict_from_file(data, "distributionsInput.txt")
q_distribution_over_the_height_calc(data)
temp_distribution_of_water_over_the_height_calc(data)
