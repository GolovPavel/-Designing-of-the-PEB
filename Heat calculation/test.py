from iapws import IAPWS97

water=IAPWS97(T=300,P=10)
print(water.Liquid.mu)
