import matplotlib.pyplot as plt
import numpy as np
import my_lib_santanastasio as my

tempo, pressione = np.loadtxt("data/pressione_volume_mod.txt", unpack=True, skiprows=1)

pres_max = []
pres_min = []

intervalli = [
    (),
    (),
    (),
    (),
    (),
]

for (tmin, tmax) in intervalli:
    mask = (tempo >= tmin) & (tempo <= tmax)
    pres_max.append(np.max(pressione[mask]))
    pres_min.append(np.min(pressione[mask]))

data = []

P0 = 101.26 #CONTROLLA VALORI
UP0 = ? #CONTROLLA VALORE
V0 = 1112.77 + 54 #CONTROLLA VALORI
UV0 = 5 #CONTROLLA VALORE
sigma_dV = 0.3
sigma_dp = 0.0014
Delta_volume = np.array([])#CONTROLLA VALORI
Delta_pres_max = np.array(pres_max)
Delta_pres_min = np.array(pres_min)
udp_max = np.sqrt((Delta_pres_max/P0**2 * UP0)**2 + (1/P0 * sigma_dp)**2)
udp_min = np.sqrt((Delta_pres_min/P0**2 * UP0)**2 + (1/P0 * sigma_dp)**2)
uVol = np.sqrt((Delta_volume/V0**2 * UV0)**2 + (1/V0 * sigma_dV)**2)

x_list = [Delta_volume/V0, Delta_pres_max/P0, Delta_volume/V0]
y_list = [Delta_pres_max/P0, Delta_pres_min/P0, Delta_pres_min/P0]

u_x_list = [uVol, udp_max, uVol]
u_y_list = [udp_max, udp_min, udp_min]

label_x = ["$\Delta V/V_0$", "$\Delta P_S/P_0$", "$\Delta V/V_0$"]
label_y = ["$\Delta P_S/P_0$", "$\Delta P_T/P_0$", "$\Delta P_T/P_0$"]


for i in range(0, 3):

    m, um, c, uc, cov, rho = my.lin_fit(x_list[i], y_list[i], u_y_list[i], plot=False, verbose=False)
    u_tot = np.sqrt((m * u_x_list[i])**2 + u_y_list[i]**2)
    m, um, c, uc, cov, rho = my.lin_fit(x_list[i], y_list[i], u_tot, plot=False, verbose=False)
    plt.xlabel(label_x[i])
    plt.ylabel(label_y[i])
    plt.title(f"Fit {label_y[i]} vs {label_x[i]}")
    plt.savefig(f"fit_{label_y[i].strip("$\ /")}_{label_x[i].strip("$\ /")}.png")
    plt.show()

    y_fit = m * x_list[i] + c
    chi2 = np.sum(((y_list[i] - y_fit) / u_tot)**2)
    nu = len(x_list[i]) - 2
    chi2_red = chi2 / nu

    residuals = y_list[i] - y_fit
    res_norm = residuals / u_tot

    plt.axhline(0, color='black', linewidth=0.8)
    plt.errorbar(x_list[i], res_norm, yerr=np.ones_like(res_norm), fmt='o', markersize=4)
    plt.xlabel(label_x[i])
    plt.ylabel("residui normalizzati")
    plt.title(f"Residui normalizzati del fit {label_y[i]} vs {label_x[i]}")
    plt.grid(True)
    plt.savefig(f"residui_manometro_{label_y[i].strip("$\ /")}_{label_x[i].strip("$\ /")}.png")
    plt.show()