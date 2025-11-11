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

# set global random seed
random_Gseed = 1112
np.random.seed(random_Gseed)

time, temp = np.loadtxt("data/temp_acqua_mod.txt", unpack=True, skiprows=1)

time = time - time[0]
print(temp[-1])
temp = temp - temp[-1]


temp = np.delete(temp, -1)
utemp = np.repeat(0.2,len(temp))
time = np.delete(time, -1)

m, sm, c, sc, cov, rho = my.lin_fit(time, np.log(temp), utemp, plot=True)
plt.show()
print(-1/m)