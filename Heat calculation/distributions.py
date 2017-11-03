import numpy as np
import matplotlib.pyplot as plt
import utils
import sympy as sp
from iapws import IAPWS97

step = 0.05
z = np.arange(0, 1.3 + step, step)
q = np.zeros(z.size)
t_water = np.zeros(z.size)
t_sh_outer = np.zeros(z.size)

def q_distribution_over_the_height_calc(data):
    global q

    qMax = data["kV"] * data["qSr"]
    q = qMax * np.cos(np.pi / 2 * (data["Haz"] - 2 * z) / (data["Haz"] + 2 * data["deltaZ"])) * 1e6

    plt.plot(z, q)
    plt.grid(True)
    plt.xlabel(r'z, $м$', fontsize=14, fontweight='bold')
    plt.ylabel(r'q, $Вт/м^2$', fontsize=14, fontweight='bold')
    plt.show()

def temp_distribution_of_water_calc(data):
    global t_water

    qMax = data["kV"] * data["qSr"] * 1e6

    f0 = -1 / np.pi * (data["Haz"] + 2 * data["deltaZ"]) * np.sin(np.pi / 2 * ((data["Haz"]) / (data["Haz"] + 2 * data["deltaZ"])))
    f = -1 / np.pi * (data["Haz"] + 2 * data["deltaZ"]) * np.sin(np.pi / 2 * ((data["Haz"] - 2 * z) / (data["Haz"] + 2 * data["deltaZ"]))) - f0

    t_water = data["tVhR"] + (data["kG"] * data["Pt"] * qMax) / (data["kQ"] * data["kR"] * data["Gtn"] * data["Cp"]) * f

    plt.plot(z, t_water)
    plt.grid(True)
    plt.xlabel(r'z, $м$', fontsize=14, fontweight='bold')
    plt.ylabel(r't, $^oC$', fontsize=14, fontweight='bold')
    plt.show()


def temp_distribution_of_outer_shell(data):
    global t_sh_outer

    for i in range(z.size):
        water = IAPWS97(T = t_water[i] + 273.0, P = data["P1c"])
        nu = water.Liquid.nu
        mu = water.Liquid.mu
        alfa = water.Liquid.alfa
        lambda_water = water.Liquid.k

        Re = data["w"] * data["d"] / nu
        Pr = nu / alfa
        Nu = (0.0165 + 0.02 * (1 - 0.91 / data["x"] ** 2) * data["x"] ** 0.15) * Re ** 0.8 * Pr ** 0.4
        a = Nu * lambda_water / data["d"]
        Ra = 1 / a
        t_sh_outer[i] = t_water[i] + q[i] * Ra

        #TODO поверхностное кипение

    plt.plot(z, t_sh_outer)
    plt.show()

data = {}
utils.fill_dict_from_file(data, "distributionsInput.txt")
q_distribution_over_the_height_calc(data)
temp_distribution_of_water_calc(data)
temp_distribution_of_outer_shell(data)
