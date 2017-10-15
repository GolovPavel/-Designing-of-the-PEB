import utils
import math

Na = 6.002e23


def calc_nuclear_concentrations_and_write_to_file(data):
    out = open('NCOut.txt', 'w')

    N0Zr = data['roZr'] * Na / data['MZr']

    # UO2+PuO2 - MOX fuel
    Stv = math.pi * data['dTop'] ** 2 / 4
    STop = math.pi * (data['dTop'] - 2 * data['deltaTop']) ** 2 / 4
    SOb = math.pi * (data['dTop'] ** 2 - (data['dTop'] - 2 * data['deltaTop']) ** 2) / 4
    NUO2 = data["N0UO2"] * (STop / Stv)
    NZrTop = N0Zr * SOb / Stv
    NOtop = 2 * NUO2
    NPuO2 = NUO2 * data["%PuO2"] / 100
    NUO2 = NUO2 * (1 - data["%PuO2"] / 100)
    N1U235 = NUO2 * data["%1richU5"] / 100
    N1U238 = NUO2 * (1 - data["%1richU5"]) / 100
    N1Pu239 = NPuO2 * data["%1richPu9"] / 100
    N1Pu240 = NPuO2 * (1 - data["%1richPu9"]) / 100
    N2U235 = NUO2 * data["%2richU5"] / 100
    N2U238 = NUO2 * (1 - data["%2richU5"]) / 100
    N2Pu239 = NPuO2 * data["%2richPu9"] / 100
    N2Pu240 = NPuO2 * (1 - data["%2richPu9"]) / 100
    out.write("=============================\n")
    out.write("Fuel: UO2 + PuO2")
    out.write("\nN1U235: %.3e\nN1U238: %.3e\nN1Pu239: %.3e\nN1Pu240: %.3e\nN2U235: %.3e\nN2U238: %.3e\nN2Pu239: %.3e\nN2Pu240: %.3e\nNO: %.3e\nNZr: %.3e"
              % (N1U235, N1U238, N1Pu239, N1Pu240, N2U235, N2U238, N2Pu239, N2Pu240, NOtop, NZrTop))
    out.write("\n=============================\n")

    # H2O - moderator
    N0H2O = data['roH2O'] * Na / data['MH2O']
    NH = 2 * N0H2O
    NOmod = N0H2O
    out.write("Moderator: H2O\n")
    out.write("NH: %.3e\nNO: %.3e\n" % (NH, NOmod))
    out.write("=============================\n")

    # B4C - absorber
    Stv = math.pi * data['dP'] ** 2 / 4
    SP = math.pi * (data['dP'] - 2 * data['deltaP']) ** 2 / 4
    SOb = math.pi * (data['dP'] ** 2 - (data['dP'] - 2 * data['deltaP']) ** 2) / 4
    N0B4C = data['roB4C'] * Na / data['MB4C']
    NB4C = N0B4C * SP / Stv
    NB = 4 * NB4C
    NC = NB4C
    NZrP = N0Zr * SOb / Stv
    out.write("Absorber: B4C\n")
    out.write("NB: %.3e\nNC: %.3e\nNZr: %.3e\n" % (NB, NC, NZrP))
    out.write("=============================\n")

    # Gd2O3 - burnout absorber, d1
    Stv = math.pi * data['dSVP1'] ** 2 / 4
    Ssvp = math.pi * (data['dSVP1'] - 2 * data['deltaSVP']) ** 2 / 4
    SOb = math.pi * (data['dSVP1'] ** 2 - (data['dSVP1'] - 2 * data['deltaSVP']) ** 2) / 4
    N0Gd2O3 = data['roGd2O3'] * Na / data['MGd2O3']
    NGd2O3 = N0Gd2O3 * Ssvp / Stv
    NGd1 = NGd2O3 * 2
    NOsvp1 = NGd2O3 * 3
    NZrSVP1 = N0Zr * SOb / Stv
    out.write("Burnout absorber d1: Gd2O3\n")
    out.write("NGd: %.3e\nNO: %.3e\nNZr: %.3e\n" % (NGd1, NOsvp1, NZrSVP1))
    out.write("=============================\n")

    # Gd2O3 - burnout absorber, d2
    Stv = math.pi * data['dSVP2'] ** 2 / 4
    Ssvp = math.pi * (data['dSVP2'] - 2 * data['deltaSVP']) ** 2 / 4
    SOb = math.pi * (data['dSVP2'] ** 2 - (data['dSVP2'] - 2 * data['deltaSVP']) ** 2) / 4
    N0Gd2O3 = data['roGd2O3'] * Na / data['MGd2O3']
    NGd2O3 = N0Gd2O3 * Ssvp / Stv
    NGd2 = NGd2O3 * 2
    NOsvp2 = NGd2O3 * 3
    NZrSVP2 = N0Zr * SOb / Stv
    out.write("Burnout absorber d2: Gd2O3\n")
    out.write("NGd: %.3e\nNO: %.3e\nNZr: %.3e\n" % (NGd2, NOsvp2, NZrSVP2))
    out.write("=============================\n")

    out.close()

data = {}
utils.fill_dict_from_file(data, 'NCInput.txt')
calc_nuclear_concentrations_and_write_to_file(data)