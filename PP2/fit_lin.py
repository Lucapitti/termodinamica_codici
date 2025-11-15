import numpy as np
import matplotlib.pyplot as plt
import my_lib_santanastasio as my

m_list = []
um_list = []
Tf = 16.81588

for i in range(0, 8):
    file = f"data/fit_acqua/temp_acqua{i}.txt"
    time, Temp = np.loadtxt(file, unpack=True)
    time = time - time[0]

    # errore su T (assunto costante)
    uTemp = np.repeat(0.014, len(Temp))

    # seleziona solo punti con Temp > Tf
    mask = (Temp - Tf) > 0
    time_v = time[mask]
    Temp_v = Temp[mask]
    uTemp_v = uTemp[mask]

    if len(time_v) < 3:
        print(f"file {i}: troppi pochi punti validi dopo il masking; salto")
        continue

    # variabile per il fit lineare
    y = np.log(Temp_v - Tf)
    sigma_y = uTemp_v / (Temp_v - Tf)   # propagazione

    # esegui il fit (usa la tua funzione my.lin_fit)
    # signature attesa: lin_fit(x, y, sigma_y, plot=True/False, verbose=...)
    m1, sm1, c1, sc1, cov1, rho1 = my.lin_fit(time_v, y, sigma_y, plot=True, verbose=False)

    # residui e chi quadro
    y_fit = m1 * time_v + c1
    chi2 = np.sum(((y - y_fit) / sigma_y)**2)
    nu = len(time_v) - 2
    chi2_red = chi2 / nu

    residuals = y - y_fit
    res_norm = residuals / sigma_y

    # costante di tempo
    tau = -1.0 / m1
    u_tau = sm1 / (m1**2)
    print(f"{m1} & {sm1} & {tau} & {u_tau} \\\\")

    # print(f"file {i}: m = {m1:.6g} ± {sm1:.6g}, c = {c1:.6g} ± {sc1:.6g}")
    # print(f"         chi2 = {chi2:.3f}, nu = {nu}, chi2_red = {chi2_red:.3f}")
    # print(f"         tau = {tau:.6g} ± {u_tau:.6g}")

    m_list.append(tau)
    um_list.append(u_tau)
    plt.xlabel("$t [s[$")
    plt.ylabel("$In(T - T_f)$")
    plt.grid()
    plt.title("Fit lineare tempo caratteristico")
    plt.savefig(f"fit_lin_acqua{i}.png")
    plt.show()


    plt.axhline(0, color='black', linewidth=0.8)
    plt.errorbar(time_v, res_norm, yerr=np.ones_like(res_norm),
                 fmt='o', markersize=4)
    plt.xlabel("tempo [s]")
    plt.ylabel("residui normalizzati")
    plt.title(f"Residui normalizzati del fit temperatura vs tempo")
    plt.grid(True)
    plt.savefig(f"fit_lin_acqua_res{i}.png")
    plt.show()

m_array = np.array(m_list)
um_array = np.array(um_list)
print("tau per file:", m_array, "incertezze m:", um_array)
