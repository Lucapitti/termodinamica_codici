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


filenames = [["data/Posizione_1bullone_mod_cut.txt",
"data/Posizione_2bulloni_mod_cut.txt",
"data/Posizione_4bulloni_mod_cut.txt",
"data/Posizione_5bullvite_mod_cut.txt", "data/Posizione_2viti_mod_cut.txt"], ["data/Posizione_cilindro_1bull_mod_cut.txt", "data/Posizione_cilindro_2bull_mod_cut.txt", "data/Posizione_cilindro_4bull_mod_cut.txt", "data/Posizione_cilindro_5bullvite_mod_cut.txt", "data/Posizione_cilindro_2viti_mod_cut.txt"]]

S = (3.25/2)**2*math.pi
uS = 3.25*math.pi*0.05

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
	print(ualfa/alfa)
	beta = np.array(alfa)*S
	ubeta = np.sqrt((np.array(ualfa)*S)**2 + (uS*np.array(alfa))**2)
	pressione = (np.array([15.3, 30.7, 61.5, 99.8, 183.8]) + 35)*9.81/S/100
	upressione = np.sqrt((9.81/S/100)**2*(0.03**2 + 0.6**2) + (pressione/S*uS)**2)
	print(ubeta/beta)
	print(upressione/pressione)
	m, um, c, uc, cov, rho = my.lin_fit(pressione, beta, ubeta, plot=False, verbose=False)
	m, um, c, uc, cov, rho = my.lin_fit(pressione, beta, np.sqrt(ubeta**2 + (m*upressione)**2), plot=True)
	plt.title("Fit lineare coefficiente di tenuta $\\beta$ in funzione della pressione")
	plt.xlabel("$\\beta [cm^3/min]$")
	plt.ylabel("$presssione [kPa]$")
	plt.grid()
	plt.savefig(f"img/fit_beta_pressione_{count}.png")
	plt.show()

	y_fit = m * pressione + c
	chi2 = np.sum((beta - y_fit)**2 / (ubeta**2 + (m*upressione)**2))
	nu = len(beta) - 2
	chi2_red = chi2 / nu
	print(chi2_red)
	print(nu)

	residuals = beta - y_fit
	res_norm = residuals / np.sqrt(ubeta**2 + (m*upressione)**2)

	plt.axhline(0, color='black', linewidth=0.8)
	plt.errorbar(pressione, res_norm, yerr=np.ones_like(res_norm),
                 fmt='o', markersize=4)
	plt.xlabel("tempo [s]")
	plt.ylabel("residui normalizzati")
	plt.title(f"Residui normalizzati del fit temperatura vs tempo")
	plt.grid(True)
	plt.savefig(f"img/res_beta_pressione_{count}.png")
	plt.show()

	count = count + 1
	w.append((m, um))
print(w)
