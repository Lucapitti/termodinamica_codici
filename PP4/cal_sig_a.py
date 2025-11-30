import numpy as np

press_max = []
for i in range(0, 5):
	time, pressione = np.loadtxt(f"data/sigma_{i + 1}_mod.txt", unpack=True, skiprows=1)
	press_max.append(np.max(pressione))

chi2 = np.sum(((press_max - np.mean(press_max)) / 0.0025)**2)
nu = len(press_max) - 1
chi2_red = chi2 / nu

print(np.sqrt(np.sum((press_max - np.mean(press_max))**2)/(len(press_max)- 1)))