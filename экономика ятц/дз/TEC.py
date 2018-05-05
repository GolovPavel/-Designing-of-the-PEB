import math

Nel = 1000
brutto = 0.4
Kcn = 0.05
mud = 330
fi = 0.85
Aren = 4 * 1e-2
Kud = 1000
nud = 0.7
Fz = 14000
En = 0.11
trez = 0.25
Kut = 0.86
Tcl = 60
Zt = 88.33
K = 52609.76 / 1e3


W = Nel * 8760 * fi * (1 - Kcn) / 1e6
Gx = Nel * 1e3 * 8760 * 0.00011 * fi * mud * 1e-6 * Kud / 1e6
Gxtot = Gx * Tcl
Ca = Aren * Kud / (8760 * fi)
Cz = nud * Fz / (8760 * fi * 1000)
Ct = mud * 1e-6 * Kut * Zt
Ce = 1.25 * (Ct + 2.5 * Ca + 1.5 * Cz)
RZ = Ce + En * K /(8760 * fi)


print('W = {:.2f}*10^6  Мвт*час/год'.format(W))
print('Gx: {:.2f}*10^6  т/год'.format(Gx))
print('Gxtot: {:.2f} *10^6'.format(Gxtot))
print('Аморт. сост. Ca: {:.3f} $/КВт*час'.format(Ca))
print('Сост. зарплаты Cz: {:.5f} $/КВт*час'.format(Cz))
print('Себ. топлива: {:.3f} $/КВт*час'.format(Ct))
print('Себестоимость отпущ. энергии: {:.3f} $/КВт*час'.format(Ce))
print('RZ: {:.2f} $/КВт*час'.format(RZ))
