import utils
import scipy.integrate as integrate
from time_calc import qV
from iapws import IAPWS97
import math


def cP_calc():
	tW_start = data['tW_start']
	tW_boil = data['tW_boil']

	interval_len = (tW_boil - tW_start) / 20

	temps = [tW_start + 0.5 * interval_len + i * interval_len for i in range(20)]

	cp = []

	for i in range(20):
		water = IAPWS97(T=temps[i] + 273.0, P=12.7)
		cp.append(water.cp)

	cp = sum(cp) * interval_len / (tW_boil - tW_start) * 1e3

	return cp

def ro_w_calc():
	tW_start = data['tW_start']
	tW_boil = data['tW_boil']

	interval_len = (tW_boil - tW_start) / 20

	temps = [tW_start + 0.5 * interval_len + i * interval_len for i in range(20)]

	ro = []

	for i in range(20):
		water = IAPWS97(T=temps[i] + 273.0, P=12.7)
		ro.append(water.v ** -1)

	ro = sum(ro) * interval_len / (tW_boil - tW_start)

	return ro

data = {}
utils.fill_dict_from_file(data, "input.txt")

if __name__ == "__main__":
	cp = cP_calc()
	ro = ro_w_calc()
	r = 1.0974e+6

	delta_m = ro * data['V_w'] * (1 - 1 / math.e)

	A = cp * delta_m * (data['tW_boil'] - data['tW_start'])
	B = r * delta_m
	E = data['Cp'] * 10000 * data['V_fuel'] * (600 - 420)
	C = A + B

	tau = 0

	while True:
		tau += 0.001
		D = data['V_fuel'] * integrate.quad(qV, 0, tau)[0]
		print("D: {}; C: {}".format(D, C))

		if D >= C:
			break

	print("\ntau = {:.2f}".format(tau))