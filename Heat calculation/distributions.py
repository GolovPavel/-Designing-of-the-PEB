import numpy as np
import matplotlib.pyplot as plt
import utils
import sympy as sp
from iapws import IAPWS97

step = 0.01
z = np.arange(0, 1.3 + step, step)
q = np.zeros(z.size)
t_water = np.zeros(z.size)
t_sh_outer = np.zeros(z.size)
t_sh_inner = np.zeros(z.size)
t_fuel35 = np.zeros(z.size)
t_fuel14 = np.zeros(z.size)

def q_distribution_over_the_height_calc(isPlot):
    global q

    qMax = data["kV"] * data["qSr"]
    q = qMax * np.cos(np.pi / 2 * (data["Haz"] - 2 * z) / (data["Haz"] + 2 * data["deltaZ"])) * 1e6

    if isPlot:
        plt.plot(z, q / 1e6)
        plt.grid(True)
        plt.xlabel(r'z, $м$', fontsize=14, fontweight='bold')
        plt.ylabel(r'q, $МВт/м^2$', fontsize=14, fontweight='bold')
        plt.show()

def temp_distribution_of_water_calc(isPlot):
    global t_water

    qMax = data["kV"] * data["qSr"] *1e6

    f0 = -1 / np.pi * (data["Haz"] + 2 * data["deltaZ"]) * np.sin(np.pi / 2 * ((data["Haz"]) / (data["Haz"] + 2 * data["deltaZ"])))
    f = -1 / np.pi * (data["Haz"] + 2 * data["deltaZ"]) * np.sin(np.pi / 2 * ((data["Haz"] - 2 * z) / (data["Haz"] + 2 * data["deltaZ"]))) - f0

    t_water = data["tVhR"] + (data["kG"] * data["Pt"] * qMax) / (data["kQ"] * data["kR"] * Gtvsm * data["Cp"]) * f

    if isPlot:
        plt.plot(z, t_water, label=r'$t_в$')
        plt.plot(z, ts, 'r--',  label=r'$t_s$')
        plt.grid(True)
        plt.xlabel(r'z, $м$', fontsize=14, fontweight='bold')
        plt.ylabel(r't, $^oC$', fontsize=14, fontweight='bold')
        plt.legend()
        plt.ylim(290, 340)
        plt.show()


def temp_distribution_of_outer_shell(isPlot):
    global t_sh_outer

    for i in range(z.size):
        water = IAPWS97(T = t_water[i] + 273.0, P = data["P1c"])
        nu = water.Liquid.nu
        mu = water.Liquid.mu
        Pr = water.Liquid.Prandt
        lambda_water = water.Liquid.k

        Re = Wtvsm * data["d"] / nu
        Nu = 0.023 * Re ** 0.8 * Pr ** 0.4
        a = Nu * lambda_water / data["d"]
        Ra = 1 / a
        t_sh_outer[i] = t_water[i] + q[i] * Ra

    if isPlot:
        plt.plot(z, t_sh_outer, label=r'$t_{об.н}$')
        plt.plot(z, ts, 'r--',  label=r'$t_s$')
        plt.grid(True)
        plt.xlabel(r'z, $м$', fontsize=14, fontweight='bold')
        plt.ylabel(r't, $^oC$', fontsize=14, fontweight='bold')
        plt.legend()
        plt.show()

def temp_distribution_of_inner_shell(isPlot):
    global t_sh_inner
    RShell = data["deltaShell"] / data["lambdaShell"]
    t_sh_inner = t_sh_outer + q * RShell

    if isPlot:
        plt.plot(z, t_sh_inner)
        plt.grid(True)
        plt.xlabel(r'z, $м$', fontsize=14, fontweight='bold')
        plt.ylabel(r't, $^oC$', fontsize=14, fontweight='bold')
        plt.show()


def temp_distribution_of_fuel(isPlot):
    global t_fuel35, t_fuel14
    RFuel35 = data["d"] / (4 * data["lambdaFuel35"])
    RFuel14 = data["d"] / (4 * data["lambdaFuel14"])
    t_fuel35 = t_sh_inner + q * RFuel35
    t_fuel14 = t_sh_inner + q * RFuel14

    if isPlot:
        plt.figure(1)
        plt.plot(z, t_fuel35)
        plt.grid(True)
        plt.xlabel(r'z, $м$', fontsize=14, fontweight='bold')
        plt.ylabel(r't, $^oC$', fontsize=14, fontweight='bold')
        plt.figure(2)
        plt.plot(z, t_fuel14)
        plt.grid(True)
        plt.xlabel(r'z, $м$', fontsize=14, fontweight='bold')
        plt.ylabel(r't, $^oC$', fontsize=14, fontweight='bold')
        plt.show()

def calculate_distributions(isPlot):
    q_distribution_over_the_height_calc(isPlot)
    temp_distribution_of_water_calc(isPlot)
    temp_distribution_of_outer_shell(isPlot)
    temp_distribution_of_inner_shell(isPlot)
    temp_distribution_of_fuel(isPlot)

def main_characteristics_TVSM():
    out = open("distributionOut.txt", "w")

    Qtvsm = data["Qtvs"] * data["kR"]
    qMax = max(q) * 1e-6
    qAvg = sum(q) / len(q) * 1e-6
    t_sh_outer_max = max(t_sh_outer)
    t_sh_inner_max = max(t_sh_inner)
    t_fuel35_max = max(t_fuel35)
    t_fuel14_max = max(t_fuel14)
    print(max(q) / data["Haz"])


    out.write(("Qtvsm: %.3f MVt\nqMax: %.3f MVt/m^2\nqAvg: %.3f MVt/m^2\n" +\
        "Gtvsm: %.3f kg/s\nWtvsm: %.3f kg/s\n" +\
        "tOutShMax: %.3f C\ntInShMax: %.3f C\n" +\
        "tFuel35Max:  %.3f C\ntFuel14Max:  %.3f C")
        % (Qtvsm, qMax, qAvg, Gtvsm, Wtvsm, t_sh_outer_max, t_sh_inner_max, t_fuel35_max, t_fuel14_max))
    out.close()


data = {}
utils.fill_dict_from_file(data, "distributionsInput.txt")

#Constants calculation
Gtvsm = data["Gtn"] * data["kR"]
Wtvsm = data["w"] * data["kR"]
water=IAPWS97(P=data["P1c"], x = 0)
ts = list(map(lambda x: water.T - 273, np.zeros(z.size)))

calculate_distributions(False)
main_characteristics_TVSM()
