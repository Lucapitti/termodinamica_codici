import numpy as np
import matplotlib.pyplot as plt

x, y = np.loadtxt("data/temp_acqua_mod.txt", unpack=True, skiprows=1)

plt.plot(x, y)
plt.show()