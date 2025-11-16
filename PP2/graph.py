import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

masse = [15.3, 30.7, 61.5, 99.8, 183.8]

# filenames = [["data/Posizione_1bullone_mod.txt",
# "data/Posizione_2bulloni_mod.txt",
# "data/Posizione_4bulloni_mod.txt",
# "data/Posizione_5bullvite_mod.txt", "data/Posizione_2viti_mod.txt"], ["data/Posizione_cilindro_1bull_mod.txt", "data/Posizione_cilindro_2bull_mod.txt", "data/Posizione_cilindro_4bull_mod.txt", "data/Posizione_cilindro_5bullvite_mod.txt", "data/Posizione_cilindro_2viti_mod.txt"]]
files = ["data/pressione_volume_mod.txt", "data/pressione_volume2_mod.txt"]
count = 0
for file in files:
	x, y = np.loadtxt(file, unpack=True, skiprows=1)
	plt.plot(x, y)
	plt.title("Grafico pressione in funzione del tempo")
	plt.ylabel("$p [kPa]$")
	plt.xlabel("$t [s]$")
	plt.grid()
	plt.savefig(f"img/plot_pressione_vol_{count}.png")
	plt.show()
	count = count + 1