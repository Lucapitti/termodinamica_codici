import numpy as np
import matplotlib.pyplot as plt
import PP6.my_lib_santanastasio as my

G = 9.80336
R = 8.31446
CP = R * 7 / 2

P0 = 100450 #modifica (Pa)
uP0 = 14 #modifica
vol_str = 64.89 / 1000000
uvol_str = 0.37 / 1000000
S = (32.5/2)**2*np.pi # in (mm^2)
uS = 32.5*np.pi*0.1 # in (mm^2)
vol_pist = 20*S / 1000000000 #modifica
uvol_pist = np.sqrt((0.3*vol_pist/20)**2 + (20*uS)**2) / 1000000000 #modifica
V0 = vol_str + vol_pist
uV0 = np.sqrt(uvol_str**2 + uvol_pist**2)

print(f"vol pistone: {vol_pist} +- {uvol_pist}")

Tf = 19.4 + 273.15 #292.55 #modifica
uTf = 0.06 #modifica
Tc = 59 + 273.15 #332.15 #modifica
uTc = 0.06 #modifica

massa_aggiunta = 0.0689 #modifica (Kg)
um = 0.00003 #modifica


# t, dp, pos, temp= np.loadtxt("data.txt", unpack=True)
t, dp = np.loadtxt("data/pressione_mod.txt", skiprows=1, unpack=True)
t, pos = np.loadtxt("data/posizione_mod.txt", skiprows=1, unpack=True)

plt.plot(t, dp)
plt.title("Pressione relativa vs tempo con massa aggiuntiva")
plt.xlabel("tempo [s]")
plt.ylabel("pressione relativa [kPa]")
plt.grid(True)
plt.savefig("img/pressione_tempo.png")
plt.show()

plt.plot(t, pos)
plt.title("Posizione relativa pistone vs tempo con massa aggiuntiva")
plt.xlabel("tempo [s]")
plt.ylabel("posizione relativa pistone [m]")
plt.grid(True)
plt.savefig("img/posizione_tempo.png")
plt.show()

plt.plot(pos, dp)
plt.title("Pressione relativa vs posizione relativa pistone con massa aggiuntiva")
plt.xlabel("posizione relativa pistone [m]")
plt.ylabel("pressione relativa [kPa]")
plt.grid(True)
plt.savefig("img/pressione_posizione.png")
plt.show()

dp = dp * 1000

intervallo_pos_a = (0, 20) #modifica (0, 20)
intervallo_pos_c =  (45, 54)#modifica (38, 43)  (42.6, 43.2)

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
upos_a = np.sqrt((np.std(pos[i_min_a:i_max_a], ddof=1) / np.sqrt(i_max_a - i_min_a))**2 + 0.00000625**2)
pos_c = pos[i_min_c:i_max_c].mean()
upos_c = np.sqrt((np.std(pos[i_min_c:i_max_c], ddof=1) / np.sqrt(i_max_c - i_min_c))**2 + 0.00000625**2)

Lavoro = massa_aggiunta * G * (pos_c - pos_a)
uLavoro = np.sqrt((massa_aggiunta * G)**2 * (upos_a**2 + upos_c **2) + (um * G * (pos_c - pos_a))**2)
print(f"Lavoro: {Lavoro} J Incertezza: {uLavoro} J")

if False:
    Tf = temp[i_min_a:i_max_a].mean()
    uTf = np.std(temp[i_min_a:i_max_a], ddof=1) / np.sqrt(i_max_a - i_min_a)
    Tc = temp[i_min_c:i_max_c].mean()
    uTc = np.std(temp[i_min_c:i_max_c], ddof=1) / np.sqrt(i_max_c - i_min_c)

dv = (3.25/2)**2 * np.pi * pos / 10000
udv = np.sqrt(((3.25/2)**2 * np.pi * 0.00000625)**2 + (3.25 * np.pi * pos * 0.01)**2) / 10000

dv_a = dv[i_min_a:i_max_a].mean()
udv_a = np.std(dv[i_min_a:i_max_a], ddof=1) / np.sqrt(i_max_a - i_min_a)
dp_a = dp[i_min_a:i_max_a].mean()
udp_a = np.std(dp[i_min_a:i_max_a], ddof=1) / np.sqrt(i_max_a - i_min_a)
temp_a = Tf
utemp_a = uTf

n_mol = (P0 + dp_a)*(V0 + dv_a)/(R*temp_a)
un_mol = np.sqrt((uP0**2 + udp_a**2)*((V0 + dv_a)/(R*temp_a))**2 + (uV0**2 + udv_a**2)*((P0 + dp_a)/(R*temp_a))**2 + (utemp_a*(P0 + dp_a)*(V0 + dv_a)/(R*temp_a*temp_a))**2)

print(f"numero moli = {n_mol} +- {un_mol}")

'''
Tc = 345 #modifica (Kelvin)
uTc = 0.2 #modifica

#PUNTO PIU DELICATO
for i in range(len(t)):
    if (t[i] >= 0.25): #modifica
        break
Tf = (P0 + dp[i]) * (V0 + dv[i]) / (R * n_mol) #discuti trascurabilita correlazioni
uTf = np.sqrt((uP0**2 + (udp_a * np.sqrt(i_max_a - i_min_a))**2)*((uV0 + dv[i])/(R*n_mol))**2 + (V0**2 + (udv_a * np.sqrt(i_max_a - i_min_a))**2)*((P0 + dp[i])/(R*n_mol))**2 + (un_mol*(P0 + dp[i])*(V0 + dv[i])/(R*n_mol*n_mol))**2)
'''

Qass = n_mol * CP * (Tc - Tf)
uQass = np.sqrt((un_mol * CP * (Tc - Tf))**2 + (uTc**2 + uTf**2)*(n_mol * CP)**2)
print(f"altezza iniziale = {pos_a} +- {upos_a}")
print(f"altezza finale = {pos_c} +- {upos_c}")

print(f"Calore: {Qass} Incertezza: {uQass}")

rendimento = Lavoro / Qass
urendimento = np.sqrt((uLavoro / Qass)**2 + (uQass * Lavoro / Qass / Qass)**2) # controlla indipendenti

rend_carnot = 1 - (Tf / Tc)
ucarnot = np.sqrt((Tf))
print(f"Rendimento: {rendimento} Incertezza: {urendimento} Rendimento Carnot: {rend_carnot}")
