import my_lib_santanastasio as my
import matplotlib.pyplot as plt
import numpy as np

P0 = 101.57 #kPa
uP0 = 0.5

offset = 0.15
uOffset = 0.003

Delta_pressioni = np.array([-89.79, -90.08, -90.20, -89.53])
Temp_multiple = np.array([49, 50, 50.6, 51.8])
uTemp = np.std(Temp_multiple, ddof=1)
uPress = np.std(Delta_pressioni, ddof=1)
Temp = np.array([np.mean(Temp_multiple), 56, 59.4, 64.8, 69.8, 74.4, 79.6, 84.6, 90.4]) + 273.15
Press = np.array([np.mean(Delta_pressioni), -86.41, -83.39, -78.26, -72.56, -67.90, -59.69, -50.61, -36.73])
Press = (np.array(Press) - offset + P0) *1000
uPress = np.array(uPress)
uTemp = np.array(uTemp)
uPress = np.sqrt(uPress**2 + uOffset**2 + uP0**2)*1000

y = np.log(Press)
x = 1/Temp
uy = uPress/Press
ux = uTemp/Temp**2

m, um, c, uc, cov, rho = my.lin_fit(x, y, uy)
m, um, c, uc, cov, rho = my.lin_fit(x, y, np.sqrt(uy**2 + (m*ux)**2), plot=True)
plt.show()

print(-m*8.314/18)
print(um*8.314/18)