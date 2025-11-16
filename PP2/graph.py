import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

filenames = [["data/Posizione_1bullone_mod.txt",
"data/Posizione_2bulloni_mod.txt",
"data/Posizione_4bulloni_mod.txt",
"data/Posizione_5bullvite_mod.txt", "data/Posizione_2viti_mod.txt"], ["data/Posizione_cilindro_1bull_mod.txt", "data/Posizione_cilindro_2bull_mod.txt", "data/Posizione_cilindro_4bull_mod.txt", "data/Posizione_cilindro_5bullvite_mod.txt", "data/Posizione_cilindro_2viti_mod.txt"]]
count = 0
for files in filenames:
	for file in files:
		x, y = np.loadtxt(file, unpack=True, skiprows=1)
		plt.plot(x, y)
	plt.title("Altezza in funzione della posizione")
	plt.xlabel("$h [m]$")
	plt.ylabel("$t [s]$")
	plt.grid()
	plt.savefig(f"img/plot_altezza_tempo_{count}.png")
	plt.show()
	count = count + 1