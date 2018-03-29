import utils
import scipy.integrate as integrate
from scipy.special import j0, j1
from scipy.optimize import root
import numpy as np

import matplotlib.pyplot as plt


def tetta_calc(tau):
	F0 = at * tau / (data['r1'] ** 2)

	res = 0

	for i in range(2):
		A = 1 / 2 * (1 / Bi0 - 1 / Bi)
		B = 1 / (mu[i] ** 2)
		C = integrate.quad(lambda x: qV(x) / data['qV0'] * np.exp(mu[i] ** 2 * x), 0, F0)[0]

		An = 2 * j1(mu[i]) / (mu[i] * (j0(mu[i]) ** 2 + j1(mu[i]) ** 2))

		D = An * np.exp(-mu[i] ** 2 * F0)
		res = res + (A + B + C) * D
	return res


def t_calc(tau):
	tetta = tetta_calc(tau)
	result = tetta * data['qV0'] * data['r1'] ** 2 / data['lambdaT'] + data['tW']
	return result


def qV(tau):
	qV = data['qV0'] * (0.99 * (np.exp(-tau / data['tau1'])) ** 2 + (
				0.1 * ((tau + data['tau2']) / data['tau2']) ** (-0.2)) ** 2) ** 0.5
	return qV


def j_fun(x, Bi):
	return j0(x) / j1(x) - x / Bi


def get_mu(Bi):
	start = 0.01

	mu1 = root(j_fun, start, args=(Bi,)).x

	while True:
		start += 0.1
		mu2 = root(j_fun, start, args=(Bi,)).x
		if mu2[0] - mu1[0] < 1e-4:
			continue
		else:
			break

	while True:
		start += 0.1
		mu3 = root(j_fun, start, args=(Bi,)).x
		if mu3[0] - mu2[0] < 1e-4:
			continue
		else:
			break

	return [mu1[0], mu2[0], mu3[0]]


data = {}
utils.fill_dict_from_file(data, "input.txt")

if __name__ == "__main__":
	alpha = data['alpha0'] * data['alpha/alpha0']

	k0 = 1 / (data['delta_sh'] / data['lambda_sh'] + 1 / data['alpha0'])
	k = 1 / (data['delta_sh'] / data['lambda_sh'] + 1 / alpha)

	Bi0 = k0 * data['r1'] / data['lambdaT']
	Bi = k * data['r1'] / data['lambdaT']

	print("Calculation for alpha = {} alpha0".format(alpha / data["alpha0"]))

	mu = get_mu(Bi)
	print('Bi = {}.\nMu: {}\n'.format(Bi, mu))

	at = data['lambdaT'] / (data['Cp'] * data['ro'])

	tau = []
	t_fuel = []

	for i in range(1, 301):
		tau_new = i * 0.1
		t_fuel_new = t_calc(tau_new)

		t_fuel.append(t_fuel_new)
		tau.append(tau_new)

		print('t: {:.2f} C   tau: {} sec'.format(t_fuel_new, tau_new))

	plt.plot(tau, t_fuel)
	plt.xlabel('Время, сек')
	plt.ylabel('Температура топлива, $^\circ$C')
	plt.title(r'$\alpha/\alpha_0={}; \tau_1={} сек; \tau_2={} сек$'.format(
		data['alpha/alpha0'],
		data['tau1'],
		data['tau2'],
	))
	plt.grid(True)
	plt.show()
