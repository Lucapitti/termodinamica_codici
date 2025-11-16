import matplotlib.pyplot as plt
import numpy
from numpy import sqrt,floor
import numpy as np
import pandas as pd
import random
import math
import my_lib_santanastasio as my
from scipy import stats
import scipy.integrate as integrate
from scipy import optimize

random_Gseed = 1112
np.random.seed(random_Gseed)

import numpy as np
import matplotlib.pyplot as plt

def fit_con_posteriori(pressione, beta, ubeta, upressione, count):
	# Primo fit con incertezze combinate
	m, um, c, uc, cov, rho = my.lin_fit(pressione, beta, ubeta, plot=False, verbose=False)
	u_comb = np.sqrt(ubeta**2 + (m*upressione)**2)
	m, um, c, uc, cov, rho = my.lin_fit(pressione, beta, u_comb, plot=False, verbose=False)

	# Calcolo chi2 e incertezze a posteriori
	y_fit = m * pressione + c
	res = beta - y_fit
	sigma_post = np.sqrt(np.sum(res**2)/(len(beta)-2))
	u_post = np.full_like(beta, sigma_post)

	# Fit finale con incertezze posteriori
	mf, umf, cf, ucf, covf, rhof = my.lin_fit(pressione, beta, u_post, plot=True, verbose=False)

	plt.title("Fit $\\beta$ vs pressione")
	plt.xlabel("pressione [kPa]")
	plt.ylabel("$\\beta\\text{ }[cm^3/min]$")
	plt.grid()
	plt.legend()
	plt.savefig(f"img/fit_beta_pressione_{count}.png")
	plt.show()

	# Plot residui normalizzati
	res_norm = res / sigma_post
	plt.figure()
	plt.axhline(0, lw=0.8, color='black')
	plt.errorbar(pressione, res_norm, yerr=np.ones_like(res_norm), fmt='o')
	plt.title("Residui normalizzati")
	plt.xlabel("pressione [kPa]")
	plt.ylabel("Residui normalizzati")
	plt.grid(True)
	plt.savefig(f"img/res_beta_pressione_{count}.png")
	plt.show()

	# Reduced chi² finale
	chi2_red = np.sum(res_norm**2) / (len(beta)-2)

	return mf, umf, cf, ucf, chi2_red, sigma_post


filenames = [["data/Posizione_1bullone_mod_cut.txt",
"data/Posizione_2bulloni_mod_cut.txt",
"data/Posizione_4bulloni_mod_cut.txt",
"data/Posizione_5bullvite_mod_cut.txt", "data/Posizione_2viti_mod_cut.txt"], ["data/Posizione_cilindro_1bull_mod_cut.txt", "data/Posizione_cilindro_2bull_mod_cut.txt", "data/Posizione_cilindro_4bull_mod_cut.txt", "data/Posizione_cilindro_5bullvite_mod_cut.txt", "data/Posizione_cilindro_2viti_mod_cut.txt"]]

S = (3.25/2)**2*math.pi
uS = 3.25*math.pi*0.01

w = []
count = 0

for files in filenames:
	alfa = []
	ualfa = [] 
	for file in files:
		t_temp, pos_temp = np.loadtxt(file, unpack=True, skiprows=1)
		t_temp = t_temp/60
		pos_temp = pos_temp*100
		uh = np.repeat(0.0018,len(pos_temp))
		m, um, c, uc, cov ,rho = my.lin_fit(t_temp, pos_temp, uh, verbose=False, plot=False)
		alfa.append(m)
		ualfa.append(um)

	ualfa = np.array(ualfa)
	alfa = np.array(alfa)
	beta = alfa*S
	ubeta = np.sqrt((ualfa*S)**2 + (uS*alfa)**2)
	print("\n")
	for i in range(0, len(alfa)):
		print(f"{i + 1}\t& {alfa[i]}\t& {ualfa[i]}\t& {beta[i]}\t& {ubeta[i]} \\\\")
	pressione = (np.array([15.3, 30.7, 61.5, 99.8, 183.8]) + 35)*9.81/S/100
	upressione = np.sqrt((9.81/S/100)**2*(0.03**2 + 0.6**2) + (pressione/S*uS)**2)
	m, um, c, uc, cov, rho = fit_con_posteriori(pressione, beta, ubeta, upressione, count)
	count = count + 1
	w.append((m, um))
w = np.array(w)
print(w)