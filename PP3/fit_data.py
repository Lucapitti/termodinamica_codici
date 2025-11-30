import my_lib_santanastasio as my
import numpy as np
import matplotlib.pyplot as plt

# def fit_lin_posteriori_se_serve(x, y, uy, ux, count):
# 	m, um, c, uc, cov, rho = my.lin_fit(x, y, uy, plot=False, verbose=False)
# 	u_comb = np.sqrt(uy**2 + (m*ux)**2)
# 	m, um, c, uc, cov, rho = my.lin_fit(x, y, u_comb, plot=True, verbose=True)

# 	y_fit = m * x + c
# 	res = (y - y_fit)/u_comb

# 	chi2_red = np.sum(res**2) / (len(y)-2)
# 	if (chi2_red > 5):
# 		sigma_post = np.sqrt(np.sum(res**2)/(len(y)-2))
# 		u_post = np.full_like(y, sigma_post)
# 		m, um, c, uc, cov, rho = my.lin_fit(x, y, u_post, plot=True, verbose=False)
# 		plt.title("Fit $\\Delta p/p_0$ vs $\\Delta T/T_0$")
# 		plt.xlabel("$\\Delta T/T_0 \\,[K]$")
# 		plt.ylabel("$\\Delta p / p_0\\,[kPa]$")
# 		plt.grid()
# 		plt.legend()
# 		plt.savefig(f"img/fit_y_x_{count}.png")
# 		plt.show()

# 		res_norm = res / sigma_post
# 		plt.figure()
# 		plt.axhline(0, lw=0.8, color='black')
# 		plt.errorbar(x, res_norm, yerr=np.ones_like(res_norm), fmt='o')
# 		plt.title("Residui normalizzati")
# 		plt.xlabel("x [kPa]")
# 		plt.ylabel("Residui normalizzati")
# 		plt.grid(True)
# 		plt.savefig(f"img/res_y_x_{count}.png")
# 		plt.show()

# 		chi2_red = np.sum(res_norm**2) / (len(y)-2)

# 	return m, um, c, uc, chi2_red, sigma_post
for i in range (1, 4):
	temperatura, pressione = np.loadtxt(f"data/temp_pressione_{i}_mod.txt", skiprows=1, unpack=True)

	T_min = 32
	T_max = 36

	i_min = -1
	i_max = -1

	T0 = temperatura[0] + 273.15
	pressione = pressione
	# plt.plot(temperatura, pressione, label=f"presa dati $n^o$ {i}")


	for j in range(len(temperatura)):
		if (temperatura[j] > T_min and i_min == -1):
			i_min = j
		if (temperatura[j] > T_max and i_max == -1):
			i_max = j

	temperatura = temperatura[i_min:i_max]
	pressione = pressione[i_min:i_max]

	temperatura += 273.15

	uT0 = 0.014
	P0 = 100.300
	uP0 = 0.003

	P0 = 100.300

	up = 0.038
	udpsup = np.sqrt((up/P0)**2 + (pressione/P0**2*uP0)**2)
	# print(udpsup/(pressione/P0))


	udt = 0.02
	udtsut = np.sqrt((udt/T0)**2 + (temperatura/T0**2*uT0)**2)
	# print(udtsut/((temperatura -T0)/T0))

	# print(pressione[-1], temperatura[-1], T0, P0)
	x = (temperatura - T0)/T0
	y = pressione/P0
	m, um, c, uc, cov, rho = my.lin_fit(x, y, udpsup, plot=False, verbose=False)
	ucomb = np.sqrt(udpsup**2 + (m*udtsut)**2)
	m, um, c, uc, cov, rho = my.lin_fit(x, y, ucomb, plot=True, verbose=False)
	plt.title("Fit $\\Delta p/p_0$ vs $\\Delta T/T_0$")
	plt.xlabel("$\\Delta T/T_0$")
	plt.ylabel("$\\Delta p / p_0$")
	plt.grid()
	plt.legend()
	plt.savefig(f"img/fit_lin_dp_dt_{i}.png")
	plt.show()
	print(f"{i}\t& {m}\t& {um}\t& {c}\t& {uc}\t& {cov}\t& {rho}\\\\")
	res = (y - (m*x + c))/ucomb
	chi2_red = np.sum(res**2) / (len(y)-2)
	# print(chi2_red)
	plt.errorbar(x, res, yerr=1, fmt='o')
	plt.title("Residui normalizzati")
	plt.xlabel("$\\Delta T/T_0$")
	plt.ylabel("Residui normalizzati")
	plt.grid(True)
	plt.savefig(f"img/res_norm_dp_dt_{i}.png")
	plt.show()


plt.axvspan(T_min, T_max, color='orange', alpha=0.3, label='intervallo per fit lineare')
plt.xlabel("$T [^oC]$")
plt.ylabel("$\Delta p [kPa]$")
plt.grid()
plt.title("Grafico $\\Delta p$ vs $T$")
plt.legend()
plt.savefig(f"img/grafico_pressione_temp.png")
plt.show()