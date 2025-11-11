import matplotlib.pyplot as plt
import numpy as np
import my_lib_santanastasio as my

tempo, pressione = np.loadtxt("data/pressione_volume_mod.txt", unpack=True, skiprows=1)
intervalli = [
    (0, 4.5),
    (15.5, 55.6),
    (75, 116),
    (140, 175),
    (200, 230),
    (260, 290)
]

medie_pressione = []
for (tmin, tmax) in intervalli:
    mask = (tempo >= tmin) & (tempo <= tmax)
    media = np.mean(pressione[mask])
    medie_pressione.append(media)

for i, (tmin, tmax) in enumerate(intervalli):
    print(f"Intervallo {i+1}: {tmin}-{tmax} s --> media pressione = {medie_pressione[i]:.3f}")
P0 = 101.26
V0 = 1112.77 + 54
Delta_volume = np.array([0, -11, -22, -34, -45, -54])
Delta_pressioni = np.array(medie_pressione)
upressioni = np.repeat(0.001, len(Delta_pressioni))
my.lin_fit(Delta_volume/V0, Delta_pressioni/P0, upressioni, plot=True)
plt.show()