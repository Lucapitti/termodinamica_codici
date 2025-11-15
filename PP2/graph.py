import numpy as np
import matplotlib.pyplot as plt

x, y = np.loadtxt("data/temp_acqua_grafico.txt", unpack=True, skiprows=1)

plt.plot(x, y)
plt.xlabel("Tempo [s]")
plt.ylabel("Temperatura [$^oC$]")
plt.title("Raffreddamento del termometro in acqua")
plt.savefig("grafico_acqua.png")
plt.show()

x, y = np.loadtxt("data/temp_aria_grafico.txt", unpack=True, skiprows=1)
plt.plot(x, y)
plt.xlabel("Tempo [s]")
plt.ylabel("Temperatura [$^oC$]")
plt.title("Raffreddamento del termometro in aria")
plt.savefig("grafico_aria.png")
plt.show()