import matplotlib.pyplot as plt

import numpy
from numpy import sqrt,floor

import numpy as np
import pandas as pd
import random
import math

# libreria locale
import my_lib_santanastasio as my
##NOTA IMPORTANTE: se cambi qualcosa in my_lib_santanastasio 
# devi fare Kernel --> Restart prima di rigirare il codice
# altrimenti i cambiamenti non saranno applicati.

from scipy import stats
import scipy.integrate as integrate
from scipy import optimize

random_Gseed = 1112
np.random.seed(random_Gseed)

# change "virgola" (comma) with "punto" (point) in the file
alfa = []
ualfa = []

filenames = ["data/Posizione_1bullone_mod.txt",
"data/Posizione_2bulloni_mod.txt",
"data/Posizione_4bulloni_mod.txt",
"data/Posizione_5bullvite_mod.txt"]

for file in filenames:
	t_temp, pos_temp = np.loadtxt(file, unpack=True, skiprows=1)
	uh = np.repeat(0.001,len(pos_temp))
	m, um, c, uc, cov ,rho = my.lin_fit(t_temp, pos_temp, uh)
	print(m)
	alfa.append(m)
	ualfa.append(um)
	# filemod = file.replace(".txt", "_cut.txt")

	# reading_file = open(file, "r", encoding="utf8", errors='ignore')

	# new_file_content = ""
	# for i, line in enumerate(reading_file):
	# 	#print (i, line)
	# 	stripped_line = line.strip()
	# 	split_line = stripped_line.split()
	# 	if (float(split_line[0]) >= 17 and float(split_line[0]) <= 99):
	# 		new_file_content += stripped_line + "\n"
	# reading_file.close()

	# writing_file = open(filemod, "w")
	# writing_file.write(new_file_content)
	# writing_file.close()
S = 32.5**2*math.pi
uS = 2*32.5*math.pi*0.1
beta = np.array(alfa)*S
pressione = np.array([15.3, 30.7, 61.5, 183.8])*9.81/S
upressione = np.sqrt((9.81/S*0.03)**2 + (pressione*9.81/S**2*uS)**2)
ubeta = np.sqrt((np.array(ualfa)*S)**2 + (uS*np.array(alfa))**2)
m, um, c, uc, cov, rho = my.lin_fit(pressione, beta, ubeta, plot=False, verbose=False)
m, um, c, uc, cov, rho = my.lin_fit(pressione, beta, np.sqrt(ubeta**2 + (m*upressione)**2), plot=True)
plt.show()