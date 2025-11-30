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

filenames = ["data/pressione_volume_5.txt", "data/pressione_volume_4.txt",  "data/pressione_volume_3.txt", "data/pressione_volume_2.txt","data/pressione_volume_1.txt", "data/temp.txt"] 
# filenames = ["data/sigma_5.txt", "data/sigma_4.txt",  "data/sigma_3.txt", "data/sigma_2.txt","data/sigma_1.txt", "data/temp.txt"] 

for myfilename in filenames:
	myfilenamemod = myfilename.replace(".txt", "_mod.txt")

	reading_file = open(myfilename, "r", encoding="utf8", errors='ignore')

	new_file_content = ""
	for i, line in enumerate(reading_file):
		#print (i, line)
		stripped_line = line.strip()
		new_line = stripped_line.replace(",", ".")
		if i!=0: # drop first line of file
			new_file_content += new_line +"\n"
	reading_file.close()

	writing_file = open(myfilenamemod, "w")
	writing_file.write(new_file_content)
	writing_file.close()