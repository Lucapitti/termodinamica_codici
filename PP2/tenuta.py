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
"data/Posizione_5bullvite_mod_cut.txt"], ["data/Posizione_cilindro_1bull_mod_cut.txt", "data/Posizione_cilindro_2bull_mod_cut.txt", "data/Posizione_cilindro_4bull_mod_cut.txt", "data/Posizione_cilindro_5bullvite_mod_cut.txt"]]

S = (3.25/2)**2*math.pi
uS = 3.25*math.pi*0.05

w = []

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
		# filemod = file.replace(".txt", "_cut.txt")

		# reading_file = open(file, "r", encoding="utf8", errors='ignore')

		# new_file_content = ""
		# for i, line in enumerate(reading_file):
		# 	#print (i, line)
		# 	stripped_line = line.strip()
		# 	split_line = stripped_line.split()
		# 	if (float(split_line[0]) >= 17 and float(split_line[0]) <= 80):
		# 		new_file_content += stripped_line + "\n"
		# reading_file.close()

		# writing_file = open(filemod, "w")
		# writing_file.write(new_file_content)
		# writing_file.close()

	print(alfa, ualfa)
	beta = np.array(alfa)*S
	ubeta = np.sqrt((np.array(ualfa)*S)**2 + (uS*np.array(alfa))**2)
	pressione = (np.array([15.3, 30.7, 61.5, 183.8]) + 35)*9.81/S/100
	upressione = np.sqrt((9.81/S)**2*(0.03**2 + 0.6**2) + (pressione/S*uS)**2)
	print(pressione, upressione)
	print(beta, ubeta)



	m, um, c, uc, cov, rho = my.lin_fit(pressione, beta, ubeta, plot=False, verbose=False)
	m, um, c, uc, cov, rho = my.lin_fit(pressione, beta, np.sqrt(ubeta**2 + (m*upressione)**2), plot=True)
	plt.show()
	w.append((m, um))
print(w)
