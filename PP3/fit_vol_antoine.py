import my_lib_santanastasio as my
import numpy as np
import matplotlib.pyplot as plt

for j in range (1,3):
	temperatura, altezza = np.loadtxt(f"data/temp_altezza_{j}_mod.txt", skiprows=1, unpack=True)
	delta_volume = (3.25/2)**2 * np.pi * (altezza * 100)
	udv = np.sqrt(((3.25/2)**2 * np.pi * 0.00625 / np.sqrt(12))**2 + ((3.25/2) * np.pi * altezza * 100 * 0.01)**2)
	ut = np.repeat(0.014, temperatura.size)

	T_min = 32
	T_max = 36

	i_min = -1
	i_max = -1

	vol_cil = (1.895**2)*np.pi*(8.81 - 0.23 -3.27)
	vol_tubi = (0.16)**2*np.pi*52
	volume_aggiuntivo = vol_cil + vol_tubi
	uvol_aggiuntivo = np.sqrt((2*vol_cil/1.895 * 0.005)**2 + (vol_cil/(8.81 - 0.23 -3.27) * 0.0087)**2 + (2*vol_tubi/0.16 * 0.0025)**2 + ((0.16)**2*np.pi * 0.03)**2)

	T0 = temperatura[0] + 273.15
	uT0 = 0.014
	V0 = volume_aggiuntivo + delta_volume[0]
	uV0 = np.sqrt(udv[0]**2 + uvol_aggiuntivo**2)

	for i in range(len(temperatura)):
		if (temperatura[i] > T_min and i_min == -1):
			i_min = i
		if (temperatura[i] > T_max and i_max == -1):
			i_max = i

	temperatura = temperatura[i_min:i_max]
	delta_volume = delta_volume[i_min:i_max]
	udv = udv[i_min:i_max]
	ut = ut[i_min:i_max]
	temperatura += 273.15

	if True: # set false if you want P0 and V0 to be set at the start
		T0 = temperatura[0]
		V0 = volume_aggiuntivo + delta_volume[0]
		uV0 = np.sqrt(udv[0]**2 + uvol_aggiuntivo**2)

	P0 = 100.300
	uP0 = 0.003

	print(f"V0: {V0} variazione V iniziale: {delta_volume[0]}, V aggiuntivo: {volume_aggiuntivo}")

	temperatura = ((temperatura * volume_aggiuntivo) + ((26 + 273.15) * delta_volume)) / (volume_aggiuntivo + delta_volume)
	ut = np.sqrt(((volume_aggiuntivo / (volume_aggiuntivo + delta_volume))**2 * ut**2) + (((delta_volume * (temperatura - (26 + 273.15))) / ((volume_aggiuntivo + delta_volume)**2))**2 * uvol_aggiuntivo**2) + (((volume_aggiuntivo * ((26 + 273.15) - temperatura)) / ((volume_aggiuntivo + delta_volume)**2))**2 * udv**2))

	#Legge di Antoine
	
	pressioni_vapore = np.exp(23.1964 - (3816.44/(temperatura - 46.13))) / 1000
	print(f"Le pressioni vapore vanno da {pressioni_vapore[0]} a {pressioni_vapore[-1]}")
	p_aria = np.repeat(P0, pressioni_vapore.size) - pressioni_vapore
	print(f"Le pressioni dell' aria vanno da {p_aria[0]} a {p_aria[-1]}")

	n_aria = p_aria * (volume_aggiuntivo + delta_volume) / (8.314 * temperatura)
	plt.plot(volume_aggiuntivo + delta_volume, n_aria)
	plt.title("moli di aria in funzione della temperatura")
	plt.xlabel("temperatura")
	plt.ylabel("$n_{aria}$")
	plt.grid(True)
	plt.savefig(f"new_moli_aria_temperatura_{j}")

	m, um, c, uc, cov, rho = my.lin_fit(temperatura, n_aria, np.sqrt((p_aria * udv/ (8.314 * temperatura))**2 + (ut * p_aria * (volume_aggiuntivo + delta_volume) / (8.314 * temperatura**2))**2), plot=True)
	plt.title("moli di aria in funzione della temperatura")
	plt.xlabel("temperatura")
	plt.ylabel("$n_{aria}$")
	plt.grid(True)
	plt.savefig(f"fit_moli_aria_temperatura_{j}")
	plt.show()
	print(f"coefficente: {m}, incertezza: {um}")

	vol_dry = (n_aria * 8.314 * temperatura) / P0

	dvsuv = (vol_dry - vol_dry[0]) / vol_dry[0]
	dtsut = (temperatura - T0) / T0
	udvsuv = np.sqrt((udv/V0)**2 + (delta_volume/V0**2*uV0)**2)
	udtsut = np.sqrt((ut/T0)**2 + (temperatura/T0**2*uT0)**2)


	m, um, c, uc, cov, rho = my.lin_fit(dtsut, dvsuv, udvsuv, plot=False)
	m, um, c, uc, cov, rho = my.lin_fit(dtsut, dvsuv, np.sqrt(udvsuv**2 + (m*udtsut)**2), plot=True)
	plt.title("Fit $\Delta V / V$ vs $\Delta T / T$")
	plt.xlabel("$\Delta T / T$")
	plt.ylabel("$\Delta V / V$")
	plt.grid(True)
	plt.savefig(f"fit_volume_temperatura_corretti_{j}")
	plt.show()

	y_pred = dtsut * m + c
	res = y_pred - dvsuv
	res_norm = res / np.sqrt(udvsuv**2 + (m*udtsut)**2)
	
	plt.figure()
	plt.axhline(0, lw=0.8, color='black')
	plt.errorbar(dtsut, res_norm, yerr=np.ones_like(res_norm), fmt='o')
	plt.title("Residui normalizzati")
	plt.xlabel("$\Delta T / T$")
	plt.ylabel("Residui normalizzati")
	plt.grid(True)
	plt.savefig(f"residui_volume_temperatura_corretti_{j}")
	plt.show()