import numpy as np
import matplotlib.pyplot as plt
import my_lib_santanastasio as my

G = 9.80336
R = 8.31446
CP = R * 7 / 2

P0 = 100300 #modifica (Pa)
uP0 = 0.3 #modifica
vol_str = 64.09 / 1000000
uvol_str = 0.36 / 1000000
vol_pist = 20 / 1000000 #modifica
uvol_pist = 0.03 / 1000000 #modifica
V0 = vol_str + vol_pist
uV0 = np.sqrt(uvol_str**2 + uvol_pist**2)

massa_aggiunta = 0.07 #modifica (Kg)
um = 0.00003 #modifica


t, dp, pos, temp= np.loadtxt("data.txt", unpack=True)

plt.plot(t, dp)
plt.title("Pressione relativa vs tempo")
plt.xlabel("tempo [s]")
plt.ylabel("pressione relativa [kPa]")
plt.grid(True)
plt.savefig("pressione_tempo.png")
plt.show()

plt.plot(t, pos)
plt.title("Posizione relativa pistone vs tempo")
plt.xlabel("tempo [s]")
plt.ylabel("posizione relativa pistone [m]")
plt.grid(True)
plt.savefig("posizione_tempo.png")
plt.show()

plt.plot(pos, dp)
plt.title("Pressione relativa vs posizione relativa pistone")
plt.xlabel("posizione relativa pistone [m]")
plt.ylabel("pressione relativa [kPa]")
plt.grid(True)
plt.savefig("pressione_posizione.png")
plt.show()

dp = dp * 1000

intervallo_pos_a = (0, 0.05) #modifica
intervallo_pos_c = (0.5, 0.55) #modifica

for i in range(len(t)):
    if (t[i] <= intervallo_pos_a[0]):
        i_min_a = i
    if (t[i] <= intervallo_pos_a[1]):
        i_max_a = i
    if (t[i] <= intervallo_pos_c[0]):
        i_min_c = i
    if (t[i] <= intervallo_pos_c[1]):
        i_max_c = i

pos_a = pos[i_min_a:i_max_a].mean()
upos_a = np.std(pos[i_min_a:i_max_a], ddof=1) / np.sqrt(i_max_a - i_min_a)
pos_c = pos[i_min_c:i_max_c].mean()
upos_c = np.std(pos[i_min_c:i_max_c], ddof=1) / np.sqrt(i_max_c - i_min_c)

Lavoro = massa_aggiunta * G * (pos_c - pos_a)
uLavoro = np.sqrt((massa_aggiunta * G)**2 * (upos_a**2 + upos_c **2) + (um * G * (pos_c - pos_a))**2)
print(f"Lavoro: {Lavoro} Incertezza: {uLavoro}")

dv = (3.25/2)**2 * np.pi * pos / 10000
udv = np.sqrt(((3.25/2)**2 * np.pi * 0.00625 / np.sqrt(12))**2 + ((3.25/2) * np.pi * pos * 0.01)**2) / 10000

dv_a = dv[i_min_a:i_max_a].mean()
udv_a = np.std(dv[i_min_a:i_max_a], ddof=1) / np.sqrt(i_max_a - i_min_a)
dp_a = dp[i_min_a:i_max_a].mean()
udp_a = np.std(dp[i_min_a:i_max_a], ddof=1) / np.sqrt(i_max_a - i_min_a)
temp_a = temp[i_min_a:i_max_a].mean()
utemp_a = np.std(temp[i_min_a:i_max_a], ddof=1) / np.sqrt(i_max_a - i_min_a)

n_mol = (P0 + dp_a)*(V0 + dv_a)/(R*temp_a)
un_mol = np.sqrt((uP0**2 + udp_a**2)*((V0 + dv_a)/(R*temp_a))**2 + (uV0**2 + udv_a**2)*((P0 + dp_a)/(R*temp_a))**2 + (utemp_a*(P0 + dp_a)*(V0 + dv_a)/(R*temp_a*temp_a))**2)
Tc = 345 #modifica (Kelvin)
uTc = 0.2 #modifica

#PUNTO PIU DELICATO
for i in range(len(t)):
    if (t[i] >= 0.25): #modifica
        break
Tf = (P0 + dp[i]) * (V0 + dv[i]) / (R * n_mol) #discuti trascurabilita correlazioni
uTf = np.sqrt((uP0**2 + (udp_a * np.sqrt(i_max_a - i_min_a))**2)*((uV0 + dv[i])/(R*n_mol))**2 + (V0**2 + (udv_a * np.sqrt(i_max_a - i_min_a))**2)*((P0 + dp[i])/(R*n_mol))**2 + (un_mol*(P0 + dp[i])*(V0 + dv[i])/(R*n_mol*n_mol))**2)

Qass = n_mol * CP * (Tc - Tf)
uQass = np.sqrt((un_mol * CP * (Tc - Tf))**2 + (uTc**2 + uTf**2)*(n_mol * CP)**2)
print(f"Calore: {Qass} Incertezza: {uQass}")

rendimento = Lavoro / Qass
urendimento = np.sqrt((uLavoro / Qass)**2 + (uQass * Lavoro / Qass / Qass)**2) # controlla indipendenti

rend_carnot = 1 - (Tf / Tc)
print(f"Rendimento: {rendimento} Incertezza: {urendimento} Rendimento Carnot: {rend_carnot}")
