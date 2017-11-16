from iapws import IAPWS97

water1 = IAPWS97(T = 294.7 + 273, P = 12.7)
water2 = IAPWS97(P = 12.7, x = 0.0)

i = water1.h
print(i)
ish = water2.h
print(ish)
r = 1.1504e+006

res = (i - ish) / r * 1e3
print(res)

print((1.3111e+006 - 1.5195e+006) / 1.1504e+006)
