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

uPress = np.repeat(uPress, len(Press))
uTemp = np.repeat(uTemp, len(Press))

uPress[0] /= 2
uTemp[0] /= 2

y = np.log(Press)
x = 1/Temp
uy = uPress/Press
ux = uTemp/Temp**2

print(uPress, uTemp)

m, um, c, uc, cov, rho = my.lin_fit(x, y, uy)
m, um, c, uc, cov, rho = my.lin_fit(x, y, np.sqrt(uy**2 + (m*ux)**2), plot=True)
plt.title("Fit Lineare ln(p) vs $\\frac{1}{T}$")
plt.xlabel("$\\frac{1}{T} [K^{-1}]$")
plt.ylabel("ln(p)")
plt.grid(True)
plt.savefig(f"fit_pres_temp.png")
plt.show()

y_pred = x * m + c
res = y_pred - y
res_norm = res / np.sqrt(uy**2 + (m*ux)**2)

chi = np.sum((res*res)/(uy**2 + (m*ux)**2))/(y.size - 2)
print(f"chi quadro: {chi}")

plt.figure()
plt.axhline(0, lw=0.8, color='black')
plt.errorbar(y, res_norm, yerr=np.ones_like(res_norm), fmt='o')
plt.title("Residui normalizzati")
plt.xlabel("$\\frac{1}{T} [K^{-1}]$")
plt.ylabel("Residui normalizzati")
plt.grid(True)
plt.savefig(f"residui_pres_temp.png")
plt.show()

sigma_post = np.repeat(np.sqrt(np.sum((y_pred[1:] - y[1:])**2)/(y.size - 3)), y.size)
sigma_post[0] = uy[0]
print(sigma_post)

m, um, c, uc, cov, rho = my.lin_fit(x, y, sigma_post, plot=True)
plt.title("Fit Lineare ln(p) vs $\\frac{1}{T}$")
plt.xlabel("$\\frac{1}{T} [K^{-1}]$")
plt.ylabel("ln(p)")
plt.grid(True)
plt.savefig(f"fit_pres_temp_post.png")
plt.show()

y_pred = x * m + c
res = y_pred - y
res_norm = res / sigma_post

plt.figure()
plt.axhline(0, lw=0.8, color='black')
plt.errorbar(y, res_norm, yerr=np.ones_like(res_norm), fmt='o')
plt.title("Residui normalizzati")
plt.xlabel("$\\frac{1}{T} [K^{-1}]$")
plt.ylabel("Residui normalizzati")
plt.grid(True)
plt.savefig(f"residui_pres_temp_post.png")
plt.show()

print(-m*8.314/18)
print(um*8.314/18)