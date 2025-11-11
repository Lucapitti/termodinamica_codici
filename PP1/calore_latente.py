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
for i in range(0, len(c_sp)):
	print(f" & {c_sp[i]} & {sigma_c_sp[i]} \\\\")
c_mean = np.sum(c_sp / sigma_c_sp**2)/np.sum(1/sigma_c_sp**2)
sigma_mean = np.sqrt(1/np.sum(1/sigma_c_sp**2))
print(test_chi(c_sp, sigma_c_sp))

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
	if (i % 2 == 0):
			print((c_sp[i] - c_sp[i + 1])/np.sqrt(sigma_c_sp[i]**2 + sigma_c_sp[i + 1]**2))
	print(f" & {c_sp[i]} & {sigma_c_sp[i]} \\\\")

# plt.plot(1, (c_sp[0] - 0.094)/sigma_c_sp[0], "o", color="red")
# plt.errorbar(1, (c_sp[0] - 0.094)/sigma_c_sp[0], yerr=1, color="red")
# plt.plot(2, (c_sp[1] - 0.094)/sigma_c_sp[1], "o", color="red")
# plt.errorbar(2, (c_sp[1] - 0.094)/sigma_c_sp[1], yerr=1, color="red")
# plt.show()

# plt.plot(1, (c_sp[2] - 0.091)/sigma_c_sp[2], "o", color="green")
# plt.errorbar(1, (c_sp[2] - 0.091)/sigma_c_sp[2], yerr=1, color="green")
# plt.plot(2, (c_sp[3] - 0.091)/sigma_c_sp[3], "o", color="green")
# plt.errorbar(2, (c_sp[3] - 0.091)/sigma_c_sp[3], yerr=1, color="green")
# plt.show()

# plt.plot(1, (c_sp[4] - 0.091)/sigma_c_sp[4], "o", color="blue")
# plt.errorbar(1, (c_sp[4] - 0.091)/sigma_c_sp[4], yerr=1, color="blue")
# plt.plot(2, (c_sp[5] - 0.091)/sigma_c_sp[5], "o", color="blue")
# plt.errorbar(2, (c_sp[5] - 0.091)/sigma_c_sp[5], yerr=1, color="blue")
# plt.show()

Ma = np.array([200.7, 265])
Mg = np.array([69.7, 72.5])
Ta = np.array([57.9, 58.6])
Tf = np.array([27.4, 34])

c_lat = ((Ma + 25)*(Ta - Tf) - Mg*(Tf - 0))/Mg

inc_Ma = 0.03
inc_Me = 5
inc_Ta = 0.06
inc_Tf = 0.06
inc_Tg = 0.5
inc_Mg = 0.03

inc_c_lat = np.sqrt(((Ta - Tf)/Mg*inc_Ma)**2 + ((Ta - Tf)/Mg*inc_Me)**2 + ((Ma + 25)/Mg*inc_Ta)**2 + ((Ma + 25 + Mg)/Mg*inc_Tf)**2 + (inc_Tg)**2 + ((Ma + 25)*(Ta - Tf)/Mg/Mg*inc_Mg)**2)
print(c_lat, inc_c_lat)
