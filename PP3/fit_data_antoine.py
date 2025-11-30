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


m_list = []
um_list = []

for i in range (1, 4):
	temperatura, pressione = np.loadtxt(f"data/temp_pressione_{i}_mod.txt", skiprows=1, unpack=True)

	T_min = 32
	T_max = 36

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

	#temperatura = temperatura*2 - 26

	# plt.plot(temperatura, pressione, label="Pressione", color="red")
	# plt.grid(True)
	# plt.show()

	temperatura += 273.15
	pressioni_vapore = np.exp(23.1964 - (3816.44/(temperatura - 46.13))) / 1000
	pressione = (pressione - pressioni_vapore)*0.965
	print(pressioni_vapore[-1])
	uT0 = 0.014
	P0 = 100.300
	uP0 = 0.003

	P0 = 100.300

	up = 0.038
	udpsup = np.sqrt((up*0.965/P0)**2 + (pressione/P0**2*uP0)**2 + (pressione/0.965/P0*0.009)**2)
	# print(udpsup/(pressione/P0))


	udt = 2*np.sqrt(0.014**2 + 0.03**2)
	udtsut = np.sqrt((udt/T0)**2 + (temperatura/T0**2*uT0)**2)
	# print(udtsut/((temperatura -T0)/T0))

	# print(pressione[-1], temperatura[-1], T0, P0)
	m, um, c, uc, cov, rho = my.lin_fit((temperatura - T0)/T0, pressione/P0, udpsup, plot=True, verbose=False)
	plt.show()
	m, um, c, uc, cov, rho = my.lin_fit((temperatura - T0)/T0, pressione/P0, np.sqrt(udpsup**2 + (m*udtsut)**2), plot=True)
	plt.show()
	m_list.append(m)
	um_list.append(um)
	print(f"{i}\t& {m}\t& {um}\t& {c}\t& {uc}\t& {cov}\t& {rho}\\\\")
	
	y_pred = (temperatura - T0)/T0* m + c
	res = y_pred - pressione/P0

	res_norm = res / np.sqrt(udpsup**2 + (m*udtsut)**2)

	plt.figure()
	plt.axhline(0, lw=0.8, color='black')
	plt.errorbar((temperatura - T0)/T0, res_norm, yerr=np.ones_like(res_norm), fmt='o')
	plt.title("Residui normalizzati")
	plt.xlabel("$\Delta p / p_0$")
	plt.ylabel("Residui normalizzati")
	plt.grid(True)
	plt.savefig(f"img/res_norm_antoine_{i}.png")
	plt.show()

print(np.mean(m_list))
sigma_a = np.sqrt(np.sum((m_list - np.mean(m_list))**2/(len(m_list) - 1)))/np.sqrt(len(m_list))
sigma_tot = np.sqrt( (um_list[0]/len(m_list))**2 + (um_list[1]/len(m_list))**2 + (um_list[2]/len(m_list))**2 + sigma_a**2)
print(sigma_tot)
