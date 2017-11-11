import utils
import numpy as np

def calculate_K():
    K1 = ((data["dT"]) / 9.36) ** (-1 / 3)
    K2 = 0.2 + 0.57 * data["x"]
    K3 = 1 + 0.6 * np.exp(-0.01 * data["Haz"] / data["dT"])
    A = 1.5 * data["ksiDr"] ** 0.5 * (data["roWtvsm"] / 1000) ** 0.2
    #TODO wrong K4 calculating
    K4 = 1 + A * np.exp(-0.01 * data["Z"] / (data["dT"] * 1e-3))


    out = open("heat_crisisOutput.txt", "w")
    out.write("K1: %.3f\nK2: %.3f\nK3: %.3f\nK4: %.3f\n" % (K1, K2, K3, K4))
    out.close()

data = {}
utils.fill_dict_from_file(data, "heat_crisisInput.txt")
calculate_K()
