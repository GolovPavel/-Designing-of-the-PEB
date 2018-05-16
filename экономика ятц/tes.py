Nel = 70
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
Tcl = 50
Kut = 1.38

def tes_calc(RZ):
    W = Nel * 8760 * fi * (1 - Kcn)
    Gx = Nel * 8760 * fi * mud * Kut * 1e-3 / 1e5
    Gxtot = Gx * (Tcl - trez)

    Ca = Aren * Kud / (8760 * fi)
    Cz = nud * Fz / (8760 * fi * 1000)

    Ce = RZ - En * Kud / (8760 * fi)
    Ct = Ce / 1.25 - (2.5 * Ca + 1.5 * Cz)
    Zt = Ct / (mud * 1e-6 * Kut)

    print('\n-----Расчет ТЭС---------')
    print('W = {:.2f}*10^5  Мвт*час/год'.format(W / 1e5))
    print('Gx: {:.2f}*10^5  т/год'.format(Gx))
    print('Gxtot: {:.2f} *10^5'.format(Gxtot))
    print('Аморт. сост. Ca: {:.3f} $/КВт*час'.format(Ca))
    print('Сост. зарплаты Cz: {:.5f} $/КВт*час'.format(Cz))

    print('Себестоимость отпущ. энергии: {:.3f} $/КВт*час'.format(Ce))
    print('Себ. топлива: {:.3f} $/КВт*час'.format(Ct))
    print('Цт: {:.2f} $/т'.format(Zt))
