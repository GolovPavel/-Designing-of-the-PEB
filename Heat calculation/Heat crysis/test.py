from iapws import IAPWS97

water1 = IAPWS97(T = 294.7, P = 12.7)
water2 = IAPWS97(T = 329.04, x = 0)

i = water1.Liquid.h
ish = water2.h
r = water2.Vapor.Hvap
# r = 1.4438e+006

res = (i - ish) / r
print(res)
