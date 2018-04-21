import utils
import scipy.integrate as integrate
from scipy.special import j0, j1
from scipy.optimize import root
import numpy as np

import matplotlib.pyplot as plt


def tetta_calc(tau):
	F0 = at * tau / (data['r1'] ** 2)

	res = 0

	for i in range(1):
		A = 1 / 2 * (1 / Bi0 - 1 / Bi)
		B = 1 / (mu[i] ** 2)
		C = integrate.quad(lambda x: qV(x) / data['qV0'] * np.exp(mu[i] ** 2 * x), 0, F0)[0]

		An = 2 * j1(mu[i]) / (mu[i] * (j0(mu[i]) ** 2 + j1(mu[i]) ** 2))

		D = An * np.exp(-mu[i] ** 2 * F0)
		res = res + (A + B + C) * D
	return res


def Q_big_calc(tau):
	F0 = at * tau / (data['r1'] ** 2)

	res = 0

	for i in range(1):
		A = 1 / 2 * (1 / Bi0 - 1 / Bi)
		B = 1 / (mu[i] ** 2)
		C = integrate.quad(lambda x: qV(x) / data['qV0'] * np.exp(mu[i] ** 2 * x), 0, F0)[0]

		An = 2 * j1(mu[i]) / (mu[i] * (j0(mu[i]) ** 2 + j1(mu[i]) ** 2))

		D = An * mu[i] * j1(mu[i]) * np.exp(-mu[i] ** 2 * F0)
		res = res + (A + B + C) * D
	return res


def t_fuel_calc(tau):
	tetta = tetta_calc(tau)
	result = tetta * data['qV0'] * data['r1'] ** 2 / data['lambdaT'] + data['tW']
	return result


def q_calc(tau):
	Q_big = Q_big_calc(tau)
	result = Q_big * data['qV0'] * data['r1']
	return result


def t_sh_out_calc(tau):
	return data['tW'] + q_calc(tau) / alpha


def t_sh_in_calc(tau):
	return data['tW'] + q_calc(tau) * (1 / alpha + data['delta_sh'] / data['lambda_sh'])


def qV(tau):
	qV = data['qV0'] * (0.99 * (np.exp(-tau / data['tau1'])) ** 2 + (
			0.1 * ((tau + data['tau2']) / data['tau2']) ** (-0.2)) ** 2) ** 0.5
	return qV


def j_fun(x, Bi):
	return j0(x) / j1(x) - x / Bi


def alpha_fun(tau, T):
	return alpha0 * np.exp(-tau / T)


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
	alpha0 = data['alpha0']
	T = data['T']

	tau = []
	t_fuel = []
	t_sh_out = []
	t_sh_in = []
	qv = []

	tau_new = -1

	while True:
		tau_new += 1

		alpha = alpha_fun(tau_new, T)

		qv_new = qv.append(qV(tau_new))

		k0 = 1 / (data['delta_sh'] / data['lambda_sh'] + 1 / alpha0)
		k = 1 / (data['delta_sh'] / data['lambda_sh'] + 1 / alpha)

		Bi0 = k0 * data['r1'] / data['lambdaT']
		Bi = k * data['r1'] / data['lambdaT']

		mu = get_mu(Bi)
		print('tau = {}\nBi = {}.\nMu: {}\n'.format(tau_new, Bi, mu))

		at = data['lambdaT'] / (data['Cp'] * data['ro'])

		t_fuel_new = t_fuel_calc(tau_new)
		t_sh_in_new = t_sh_in_calc(tau_new)
		t_sh_out_new = t_sh_out_calc(tau_new)

		t_fuel.append(t_fuel_new)
		t_sh_in.append(t_sh_in_new)
		t_sh_out.append(t_sh_out_new)
		tau.append(tau_new)

		if t_fuel_new > 600:
			break

	plt.figure(0)
	plt.plot(tau, t_fuel)
	# plt.plot(tau, t_sh_out)
	# plt.plot(tau, t_sh_in)
	plt.xlabel('Время, сек')
	plt.ylabel('Температура топлива, $^\circ$C')
	plt.title('Температура топлива от времени')
	plt.grid(True)


	plt.figure(1)
	plt.plot(tau, qv)
	plt.xlabel('Время, сек')
	plt.ylabel('qV, Вт/(м^3)')
	plt.title('Энерговыделение от времени')
	plt.grid(True)

	plt.show()
