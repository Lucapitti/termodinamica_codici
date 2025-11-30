import matplotlib.pyplot as plt
import numpy as np
import my_lib_santanastasio as my

pres_max = []
pres_min = []

for i in range(0, 5):
    tempo, pressione = np.loadtxt(f"data/pressione_volume_{i + 1}_mod.txt", unpack=True, skiprows=1)
    pres_max.append(np.max(pressione))
    pres_min.append(np.mean(pressione[-20:]))
    m, um, c, uc, cov, rho = my.lin_fit(tempo[-20:], pressione[-20:], np.repeat(0.0025, 20))
    print(f"z score = {m/um:.20f}")

sigma_dV = 0.3
sigma_dp_max = 0.038 # AGGIORNIAMOLA CON LA SIGMA A DI UNA MISURA RIPETUTA
sigma_dp_min = 0.0014
Delta_volume = np.array([-16, -27, -38, -49, -60])#CONTROLLA VALORI
Delta_pres_max = np.array(pres_max)
Delta_pres_min = np.array(pres_min)

x_list = [Delta_volume, Delta_pres_min, Delta_volume]
y_list = [Delta_pres_max, Delta_pres_max, Delta_pres_min]

u_x_list = [np.repeat(sigma_dV, len(x_list[0])), np.repeat(sigma_dp_max, len(x_list[1])), np.repeat(sigma_dV, len(x_list[2]))]
u_y_list = [np.repeat(sigma_dp_min, len(x_list[0])), np.repeat(sigma_dp_max, len(x_list[1])), np.repeat(sigma_dp_min, len(x_list[2]))]

label_x = ["$\Delta V$", "$\Delta P_T$", "$\Delta V$"]
label_y = ["$\Delta P_S$", "$\Delta P_S$", "$\Delta P_T$"]
unit_x = [" $[cm^3]$", " $[kPa]$", " $[cm^3]$"]


print(Delta_pres_max, Delta_pres_min)

for i in range(0, 3):

    m, um, c, uc, cov, rho = my.lin_fit(x_list[i], y_list[i], u_y_list[i], plot=False, verbose=False)
    u_tot = np.sqrt((m * u_x_list[i])**2 + u_y_list[i]**2)
    m, um, c, uc, cov, rho = my.lin_fit(x_list[i], y_list[i], u_tot, plot=True, verbose=False)
    plt.xlabel(label_x[i] + unit_x[i])
    plt.ylabel(label_y[i] + " $[kPa]$")
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
    plt.xlabel(label_x[i] + unit_x[i])
    plt.ylabel("residui normalizzati")
    plt.title(f"Residui normalizzati del fit {label_y[i]} vs {label_x[i]}")
    plt.grid(True)
    plt.savefig(f"residui_manometro_{label_y[i].strip("$\ /")}_{label_x[i].strip("$\ /")}.png")
    plt.show()

    print(f"${m} \\pm {um}$ e z score = {(m - 1.4)/um}")