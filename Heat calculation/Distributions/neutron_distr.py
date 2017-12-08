import numpy as np
import matplotlib.pyplot as plt
import utils
from iapws import IAPWS97
from scipy.interpolate import interp1d

k = [0.7, 0.9659, 1.4674, 1.7507, 1.7729, 1.5234, 0.9626, 0.6583, 0.4465, 0.2889, 0.1633]
kr = 1.164
kv = [kr * i for i in k]
z = [0, 0.13, 0.26, 0.39, 0.52, 0.65, 0.78, 0.91, 1.04, 1.17, 1.30]

q = np.zeros(len(z))
t_water = np.zeros(len(z))
t_sh_outer = np.zeros(len(z))
t_sh_inner = np.zeros(len(z))
t_fuel35 = np.zeros(len(z))
t_fuel14 = np.zeros(len(z))

def plot_spline(x, y, xlabel, ylabel):
    f = interp1d(x, y, kind='cubic')
    x = np.linspace(x[0], x[len(x) - 1], num=40, endpoint=True)
    plt.plot(x, f(x))
    plt.grid(True)
    plt.xlabel(xlabel, fontsize=14, fontweight='bold')
    plt.ylabel(ylabel, fontsize=14, fontweight='bold')
    plt.show()

def q_distribution_over_the_height_calc(isPlot):
    global q

    q = [data["qSr"] * i for i in kv]
    plot_spline(z, q, r'z, $м$', r'q, $МВт/м^2$')

def temp_distribution_of_water_calc(isPlot):
    global t_water

    for i in range(len(z)):
        t_water[i] = data["tVhR"] + data["kG"] * data["Pt"] / (data["kQ"] * data["kR"] * data["Gtn"] * data["Cp"]) * np.trapz(q[0: (i + 1)], z[0: (i + 1)]) * 1e6

    if isPlot:
        plt.plot(z, t_water, label=r'$t_в$')
        # plt.plot(z, ts, 'r--',  label=r'$t_s$')
        plt.grid(True)
        plt.xlabel(r'z, $м$', fontsize=14, fontweight='bold')
        plt.ylabel(r't, $^oC$', fontsize=14, fontweight='bold')
        plt.legend()
        # plt.ylim(290, 340)
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

        # if (t_sh_outer[i] > ts[0]):
        #     aBoil = 4.32 * (data["P1c"] ** 0.14 + 1.28 * 10 ** -2 * data["P1c"] ** 2) * q[i] ** 0.7
        #     RaBoil = 1 / aBoil
        #     t_surf_boil = ts[0] + q[i] * RaBoil
        #     print(np.abs(t_sh_outer[i] - t_surf_boil))


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

def calculate_temp_distributions(isPlot):
    temp_distribution_of_water_calc(isPlot)
    # temp_distribution_of_outer_shell(isPlot)
    # temp_distribution_of_inner_shell(isPlot)
    # temp_distribution_of_fuel(isPlot)


def main_characteristics_TVSM():

    qVMax = data["qV"] * data["kR"]
    qlAvgMax = data["qlAvg"] * data["kR"]
    Qtvsm = data["Qtvs"] * data["kR"]
    qMax = max(q) * 1e-6
    qAvg = sum(q) / len(q) * 1e-6
    roW = data["roH2O"] * Wtvsm
    t_sh_outer_max = max(t_sh_outer)
    t_sh_inner_max = max(t_sh_inner)
    t_fuel35_max = max(t_fuel35)
    t_fuel14_max = max(t_fuel14)

    upper_ts = []
    for i in range(0, len(z)):
        if t_sh_outer[i] >= ts[0]:
            upper_ts.append(i)
            break
    for i in range(len(z) - 1, -1, -1):
        if t_sh_outer[i] >= ts[0]:
            upper_ts.append(i)
            break
    LBoil = z[upper_ts[1]] - z[upper_ts[0]]


    out.write(("qVMax: %.3f MVt/m^3\nqlAvgMax: %.3f Vt/cm\nQtvsm: %.3f MVt\nqMax: %.3f MVt/m^2\nqAvg: %.3f MVt/m^2\n" +\
        "Gtvsm: %.3f kg/s\nWtvsm: %.3f kg/s\nroWtvsm: %.3f kg/(m^2*s)\n" +\
        "tOutShMax: %.3f C\ntInShMax: %.3f C\n" +\
        "tFuel35Max:  %.3f C\ntFuel14Max:  %.3f C\nLBoil: %.3f m\n")
        % (qVMax, qlAvgMax, Qtvsm, qMax, qAvg, Gtvsm, Wtvsm, roW, t_sh_outer_max, t_sh_inner_max, t_fuel35_max, t_fuel14_max, LBoil))

data = {}
utils.fill_dict_from_file(data, "..\\Distributions\\neutron_distr.txt")
kV = data["kR"] * data["kZ"]



# out = open("..\\Distributions\\distributionOut.txt", "w")

#Constants calculation
# Gtvsm = data["Gtn"] * data["kR"]
# Wtvsm = data["w"] * data["kR"]
# water=IAPWS97(P = data["P1c"], x = 0)
# ts = list(map(lambda x: water.T - 273, np.zeros(z.size)))

q_distribution_over_the_height_calc(True)
if __name__ == "__main__":
    calculate_temp_distributions(True)
#     main_characteristics_TVSM()
#
# out.write("deltaZ: %.3f m\n" % deltaZ)
# out.write("deltaR: %.3f m\n" % deltaR)
# out.write("kV: %.3f\n" % kV)
#
# out.close()
