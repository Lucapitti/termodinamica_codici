import numpy as np

x, y = np.loadtxt("data/temp_acqua_mod.txt", unpack=True, skiprows=1)

x = x[100:340]
y = y[100:340]

count = 0
for i in range(0, len(x)):
	if i%30==0:
		f = open(f"data/fit_acqua/temp_acqua{count}.txt", "w")
		count += 1
	f.write(f"{x[i]}\t{y[i]}\n")
f.close()