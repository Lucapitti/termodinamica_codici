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
time, temp = np.loadtxt("../PP2/data/temp_acqua_mod.txt", unpack=True, skiprows=1)
temp = temp[-20:]
utemp_a = np.sqrt(np.sum((temp - np.mean(temp))**2)/(len(temp)- 1))
print(utemp_a)

for i in range (1, 4):
	temperatura, pressione = np.loadtxt(f"data/temp_pressione_{i}_mod.txt", skiprows=1, unpack=True)

	T_min = 30
	T_max = 37

	i_min = -1
	i_max = -1


	T0 = temperatura[0] + 273.15
	pressione = pressione


	for i in range(len(temperatura)):
		if (temperatura[i] > T_min and i_min == -1):
			i_min = i
		if (temperatura[i] > T_max and i_max == -1):
			i_max = i

	temperatura = temperatura[i_min:i_max]
	pressione = pressione[i_min:i_max]

	temperatura = temperatura*2 - 26

	# plt.plot(temperatura, pressione, label="Pressione", color="red")
	# plt.grid(True)
	# plt.show()

	temperatura += 273.15
	uT0 = 0.014
	P0 = 100.300
	uP0 = 0.003

	P0 = 100.300

	up = 0.038
	udpsup = np.sqrt((up/P0)**2 + (pressione/P0**2*uP0)**2)
	# print(udpsup/(pressione/P0))


	udt = 2*np.sqrt(0.014**2 + 0.03**2)
	udtsut = np.sqrt((udt/T0)**2 + (temperatura/T0**2*uT0)**2)
	# print(udtsut/((temperatura -T0)/T0))

	# print(pressione[-1], temperatura[-1], T0, P0)
	m, um, c, uc, cov, rho = my.lin_fit((temperatura - T0)/T0, pressione/P0, udpsup, plot=True, verbose=False)
	plt.show()
	m, um, c, uc, cov, rho = my.lin_fit((temperatura - T0)/T0, pressione/P0, np.sqrt(udpsup**2 + (m*udtsut)**2), plot=True)
	plt.show()
	print((m - 1)/um)

