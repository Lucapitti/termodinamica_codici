import math as m
import numpy as np
import matplotlib.pyplot as plt

def test_chi(list, sigma_list):
	return (np.sum((c_sp - c_mean)**2/(sigma_c_sp**2)))


T1, Ta, Teq = np.loadtxt("dati_all.txt", unpack=True)
masse = 96.4
Ma1 = 209
sigma_Ma = 0.03
sigma_T = 0.06
sigma_M = 0.03
dc_dT1 = (Ma1 + 25)*(Ta - Teq)/(Teq - T1)**2/masse
dc_dta = (Ma1 + 25)/(Teq - T1)/masse
dc_dMa = (Ta - Teq)/(Teq - T1)/masse
dc_dMe = (Ta - Teq)/(Teq - T1)/masse
dc_dTe = (Ma1 + 25)/ masse * (T1 - Ta)/(Teq - T1)**2
dc_dmasse = (Ma1 + 25)*(Ta - Teq)/(Teq - T1)/masse**2

c_sp = (Ma1 + 25)*(Ta - Teq)/(masse*(Teq - T1))
sigma_c_sp = np.sqrt((sigma_Ma * dc_dMa)**2 + (sigma_M * dc_dmasse)**2 + (5 * dc_dMe)**2 +
					 (sigma_T * dc_dT1)**2 + (sigma_T * dc_dta)**2 + (sigma_T * dc_dTe)**2)

# for i in range(0, len(c_sp)):
# 	print(f" & {c_sp[i]} & {sigma_c_sp[i]} \\\\")
c_mean = np.sum(c_sp / sigma_c_sp**2)/np.sum(1/sigma_c_sp**2)
sigma_mean = np.sqrt(1/np.sum(1/sigma_c_sp**2))
# print(test_chi(c_sp, sigma_c_sp))
# Impostazioni per grafico elegante
plt.figure(figsize=(10, 6))

# Plot dei dati
for i in range(len(c_sp)):
    y = c_sp[i]
    yerr = sigma_c_sp[i]
    plt.errorbar(i + 1, y, yerr=yerr, fmt='o', color='#E74C3C', 
                 markersize=8, capsize=5, capthick=2, 
                 elinewidth=2)

# Linea di riferimento per valore atteso (zero)
plt.axhline(y=0.215, color='#2C3E50', linestyle='--', linewidth=1.5, 
            alpha=0.7, label='Valore teorico')

# Etichette e titolo
plt.xlabel('Numero Misura', fontsize=13, fontweight='bold')
plt.ylabel('Calore specifico\n[cal/(g·°C)]', 
              fontsize=13, fontweight='bold')
plt.title('Misure del Calore Specifico dell\'Alluminio', 
          fontsize=16, fontweight='bold', pad=20)

# Griglia e limiti
plt.grid(True, alpha=0.3, linestyle=':', linewidth=1)
plt.xlim(0.5, len(c_sp) + 0.5)

# Aggiungi valore teorico come testo
plt.text(0.02, 0.98, r'$c_{teo} = 0.215$ cal/(g·°C)', 
         transform=plt.gca().transAxes, fontsize=11,
         verticalalignment='top', bbox=dict(boxstyle='round', 
         facecolor='wheat', alpha=0.5))

# Legend
plt.legend(loc='best', fontsize=11, framealpha=0.9)

# Layout pulito
plt.tight_layout()
plt.savefig("Alluminio.png")
plt.show()

T1, Ta, Teq = np.loadtxt("dati.txt", unpack=True)
masse = np.array([194.4, 194.4, 35, 35, 41.3, 41.3])
Ma2 = np.array([209, 203, 209, 203, 209, 203])

dc_dT1 = (Ma2 + 25)*(Ta - Teq)/(Teq - T1)**2/masse
dc_dta = (Ma2 + 25)/(Teq - T1)/masse
dc_dMa = (Ta - Teq)/(Teq - T1)/masse
dc_dMe = (Ta - Teq)/(Teq - T1)/masse
dc_dTe = (Ma2 + 25)/ masse * (T1 - Ta)/(Teq - T1)**2
dc_dmasse = (Ma2 + 25)*(Ta - Teq)/(Teq - T1)/masse**2
c_sp = (Ma1 + 25)*(Ta - Teq)/(masse*(Teq - T1))

sigma_c_sp = np.sqrt((sigma_Ma * dc_dMa)**2 + (sigma_M * dc_dmasse)**2 + (5 * dc_dMe)**2 +
					 (sigma_T * dc_dT1)**2 + (sigma_T * dc_dta)**2 + (sigma_T * dc_dTe)**2)
for i in range(0, len(c_sp)):
	print(f" & {c_sp[i]} & {sigma_c_sp[i]} \\\\")

# Dati per ogni materiale: (indici, valore misurato, colore, nome)
materiali = [
    ([0, 1], 0.094, '#D4AF37', 'Ottone'),      # Oro/bronzo per ottone
    ([2, 3], None, '#808080', 'Granito'),      # Grigio per granito
    ([4, 5], None, '#4A90E2', 'Okite')         # Blu per okite
]

# Crea un grafico separato per ogni materiale
for indici, c_misurato, colore, nome in materiali:
    # Nuova figura per questo materiale
    plt.figure(figsize=(10, 6))
    
    # Plot dei dati per questo materiale
    for j, i in enumerate(indici):
        y = c_sp[i]
        yerr = sigma_c_sp[i]
        print(y, yerr)
        plt.errorbar(j + 1, y, yerr=yerr, fmt='o', color=colore, 
                   markersize=10, capsize=6, capthick=2.5, 
                   elinewidth=2.5, alpha=0.8)
    
    # Linea di riferimento solo se c'è un valore misurato
    if c_misurato is not None:
        plt.axhline(y=c_misurato, color='#2C3E50', linestyle='--', linewidth=1.5, 
                   alpha=0.7, label='Valore teorico')
    
    # Etichette
    plt.xlabel('Numero Misura', fontsize=13, fontweight='bold')
    plt.ylabel('Calore specifico\n[cal/(g·°C)]', 
              fontsize=13, fontweight='bold')
    plt.title(f'Misure del Calore Specifico del {nome}', 
            fontsize=16, fontweight='bold', pad=20)
    
    # Griglia e limiti
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=1)
    plt.xlim(0.5, len(indici) + 0.5)
    plt.xticks(range(1, len(indici) + 1))
    
    # Box informativo solo se c'è un valore misurato
    if c_misurato is not None:
        plt.text(0.02, 0.98, f'$c_{{teo}} = {c_misurato:.3f}$ cal/(g·°C)', 
               transform=plt.gca().transAxes, fontsize=11,
               verticalalignment='top', bbox=dict(boxstyle='round', 
               facecolor='wheat', alpha=0.5))
        plt.legend(loc='best', fontsize=11, framealpha=0.9)
    
    # Layout pulito
    plt.tight_layout()
    plt.savefig(f"{nome}.png")
    plt.show()

ottone_mean = (c_sp[0]/sigma_c_sp[0]**2 + c_sp[1]/sigma_c_sp[1]**2)/(1/sigma_c_sp[0]**2 + 1/sigma_c_sp[1]**2)
sigma_mean = (1/sigma_c_sp[0]**2 + 1/sigma_c_sp[1]**2)**(-1/2)
print(ottone_mean, sigma_mean, (ottone_mean - 0.094)/sigma_mean)
okite_mean = (c_sp[4]/sigma_c_sp[4]**2 + c_sp[5]/sigma_c_sp[5]**2)/(1/sigma_c_sp[4]**2 + 1/sigma_c_sp[5]**2)
okite_sigma_mean = (1/sigma_c_sp[4]**2 + 1/sigma_c_sp[5]**2)**(-1/2)
print(okite_mean, okite_sigma_mean)
granito_mean = (c_sp[2]/sigma_c_sp[2]**2 + c_sp[3]/sigma_c_sp[3]**2)/(1/sigma_c_sp[2]**2 + 1/sigma_c_sp[3]**2)
granito_sigma_mean = (1/sigma_c_sp[2]**2 + 1/sigma_c_sp[3]**2)**(-1/2)
print(granito_mean, granito_sigma_mean)

Ma = np.array([200.7, 265])
Mg = np.array([69.7, 72.5])
Ta = np.array([57.9, 58.6])
Tf = np.array([27.4, 34])

c_lat = ((Ma + 25)*(Ta - Tf) - Mg*(Tf - 0))/Mg

inc_Ma = 0.03
inc_Me = 5
inc_Ta = 0.06
inc_Tf = 0.06
inc_Tg = 0.06
inc_Mg = 0.03

inc_c_lat = np.sqrt(((Ta - Tf)/Mg*inc_Ma)**2 + ((Ta - Tf)/Mg*inc_Me)**2 + 
					((Ma + 25)/Mg*inc_Ta)**2 + ((Ma + 25 + Mg)/Mg*inc_Tf)**2 + 
					(inc_Tg)**2 + ((Ma + 25)*(Ta - Tf)/Mg/Mg*inc_Mg)**2)
ghiaccio = (c_lat[0]/inc_c_lat[0]**2 + c_lat[1]/inc_c_lat[1]**2)/(1/inc_c_lat[0]**2 + 1/inc_c_lat[1]**2)
digma_ghiaccio = (1/inc_c_lat[0]**2 + 1/inc_c_lat[1]**2)**(-1/2)
print(ghiaccio, digma_ghiaccio)

print(c_lat, inc_c_lat)