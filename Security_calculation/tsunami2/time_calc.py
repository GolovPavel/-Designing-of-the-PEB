import utils
import math
import scipy.integrate as integrate
from scipy.special import j0, j1
import numpy as np


def tetta_calc(tau):
	F0 = at * tau / (data['r1'] ** 2)

	res = 0

	for i in range(2):
		first = 1 / 2 * (1 / Bi0 - 1 / Bi) + 1 / mu[i] ** 2 + \
		        integrate.quad(lambda x: qV(x) / data['qV0'] * np.exp(mu[i] ** 2 * x), 0, F0)[0]
		An = 2 * j1(mu[i]) / (mu[i] * (j0(mu[i]) ** 2 + j1(mu[i]) ** 2))
		second = An * math.exp(-mu[i] ** 2 * F0)
		res = res + first * second
		# print(first * second)
	return res


def t_calc(tau):
	tetta = tetta_calc(tau)
	result = tetta * data['qV0'] * data['r1'] ** 2 / data['lambdaT'] + data['tW']
	return result


def qV(tau):
	qV = data['qV0'] * (0.99 * (math.exp(-tau / data['tau1'])) ** 2 + (0.1 * ((tau + data['tau2']) / data['tau2']) ** (-0.2)) ** 2) ** 0.5
	return qV


if __name__ == "__main__":
	data = {}
	utils.fill_dict_from_file(data, "input.txt")

	# tau = data['tau']
	alpha = data['alpha0'] * data['alpha/alpha0']

	k0 = 1 / (data['delta_sh'] / data['lambda_sh'] + 1 / data['alpha0'])
	k = 1 / (data['delta_sh'] / data['lambda_sh'] + 1 / alpha)

	Bi0 = k0 * data['r1'] / data['lambdaT']

	print("Calculation for alpha = {} alpha0".format(alpha / data["alpha0"]))
	Bi = k * data['r1'] / data['lambdaT']

	mu = [float(num) for num in input('Bi = {}.\nWrite mu1, mu2, mu3\n'.format(Bi)).split()]

	at = data['lambdaT'] / (data['Cp'] * data['ro'])

	for tau in range(1, 20):
		print('t: {} C   tau: {}'.format(t_calc(tau), tau))