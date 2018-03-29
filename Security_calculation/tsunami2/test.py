from scipy.optimize import minimize
from scipy.special import j0, j1, jv
from scipy.optimize import root


# def opt_fun(x, c):
#     return (np.tan(x) - 1/x)**2

# def opt_fun(x, Bi):
# 	return (j0(x) / j1(x) - x / Bi) ** 2
#
# const = 1.2
# res = minimize(lambda x: opt_fun(x, const), x0=0.001)

# Check if the optimization was successful
# print(res.success)
# print(res.x)
# print(j0(1), jv(0, 1))

def opt_fun(x, Bi):
	return j0(x) / j1(x) - x / Bi

start = 0.01

mu1 = root(opt_fun, start, args=(1.2, )).x
print(mu1[0])

while(True):
	start += 0.5
	mu2 = root(opt_fun, start, args=(1.2,)).x
	if mu2[0] - mu1[0] < 1e-4:
		continue
	else:
		print(mu2[0])
		break

while(True):
	start += 0.5
	mu3 = root(opt_fun, start, args=(1.2,)).x
	if mu3[0] - mu2[0] < 1e-4:
		continue
	else:
		print(mu3[0])
		break
