import my_lib_santanastasio as my
import matplotlib.pyplot as plt
import numpy as np

P0 = 101.57 #kPa
uP0 = 0.5

offset = 0.15
uOffset = 0.003

Delta_pressioni = np.array([-89.30, -89.33, -89.53])
Temp_multiple = np.array([50, 50.6, 51.8])
uTemp = np.std(Temp_multiple, ddof=1)
uPress = np.std(Delta_pressioni, ddof=1)
Temp = np.array([np.mean(Temp_multiple), 56, 59.4, 64.8, 69.8, 74.4, 79.6, 84.6, 90.4]) + 273.15
Press = np.array([np.mean(Delta_pressioni), -85.88, -83.39, -78.26, -72.56, -67.59, -59.69, -50.01, -36.88])
Press = (np.array(Press) - offset + P0) *1000
uPress = np.array(uPress)
uTemp = np.array(uTemp)
uPress = np.sqrt(uPress**2 + uOffset**2 + uP0**2)*1000

y = np.log(Press)
x = 1/Temp
uy = uPress/Press
ux = uTemp/Temp**2

print(uPress, uTemp)

m, um, c, uc, cov, rho = my.lin_fit(x, y, uy)
m, um, c, uc, cov, rho = my.lin_fit(x, y, np.sqrt(uy**2 + (m*ux)**2), plot=True)
plt.show()

y_pred = x * m + c
res = y_pred - y
res_norm = res / np.sqrt(uy**2 + (m*ux)**2)

plt.figure()
plt.axhline(0, lw=0.8, color='black')
plt.errorbar(y, res_norm, yerr=np.ones_like(res_norm), fmt='o')
plt.title("Residui normalizzati")
plt.xlabel("$\Delta T / T$")
plt.ylabel("Residui normalizzati")
plt.grid(True)
plt.savefig(f"residui_pres_temp.png")
plt.show()

print(-m*8.314/18)
print(um*8.314/18)