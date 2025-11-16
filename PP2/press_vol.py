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

intervalli2 = [
    (0, 4.8),
    (25, 50),
    (80, 110),
    (145, 175),
    (205, 235),
    (260, 290)
]

medie_pressione = []
for (tmin, tmax) in intervalli:
    mask = (tempo >= tmin) & (tempo <= tmax)
    media = np.mean(pressione[mask])
    medie_pressione.append(media)

for i, (tmin, tmax) in enumerate(intervalli):
    print(f"${medie_pressione[i]:.3f} \\pm {0.0014/np.sqrt((tmax - tmin)*100)}$ per $t \in ({tmin}, {tmax})$\t& ")
P0 = 101.26
V0 = 1112.77 + 54
sigma_deltaV = 0.41
Delta_volume = np.array([0, -11, -22, -34, -45, -54])
Delta_pressioni = np.array(medie_pressione)
upressioni = np.repeat(0.001, len(Delta_pressioni))
uVol = np.sqrt((Delta_volume/V0**2 * 5)**2 + (1/V0 * sigma_deltaV)**2)
m, um, c, uc, cov, rho = my.lin_fit(Delta_pressioni/P0, Delta_volume/V0, uVol, plot=True)
plt.xlabel("$\Delta p/p_0$")
plt.ylabel("$\Delta V/V_0$")
plt.title("Fit calibrazione manometro")
plt.legend()
#plt.savefig("fit_manometro2.png")
plt.show()

# residui e chi quadro
y_fit = m * Delta_pressioni/P0 + c
chi2 = np.sum(((Delta_volume/V0 - y_fit) / uVol)**2)
nu = len(Delta_pressioni/P0) - 2
chi2_red = chi2 / nu

residuals = Delta_volume/V0 - y_fit
res_norm = residuals / uVol

plt.axhline(0, color='black', linewidth=0.8)
plt.errorbar(Delta_pressioni/P0, res_norm, yerr=np.ones_like(res_norm),
                fmt='o', markersize=4)
plt.xlabel("$\Delta p/p_0$")
plt.ylabel("residui normalizzati")
plt.title(f"Residui normalizzati del fit $\Delta V/V_0$ vs $\Delta p/p_0$")
plt.grid(True)
#plt.savefig("residui_manometro2.png")
plt.show()

print(Delta_volume/V0, Delta_pressioni/P0)
print(1/(len(Delta_volume) - 2) * np.sum(((Delta_volume/V0 - (Delta_pressioni/P0*m + c))/uVol)**2))