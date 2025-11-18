import numpy as np
import my_lib_santanastasio as my
import matplotlib.pyplot as plt

Tau = np.array([3.696, 4.594, 5.898, 7.235, 8.17])
uTau = np.array([0.011, 0.021, 0.056, 0.099, 0.2])
Temp = []
for i in range(1, 6):
	t, temp = np.loadtxt(f"data/fit_acqua/temp_acqua{i}.txt", unpack=True)
	temp_mean = 0
	for t in temp:
		temp_mean = temp_mean + t
	temp_mean = temp_mean/len(temp)
	Temp.append(temp_mean - 16.81588)
Temp = np.array(Temp)
for i in range(0, len(Tau)):
	for j in range(i + 1, len(Tau)):
		print("\n******************\n")
		print(f"i = {i}, j = {j}, DT = {Temp[j]} / {Temp[i]} e Tau = {Tau[i]} / {Tau[j]}")
		if abs(Tau[i]/Tau[j] - (Temp[j]/Temp[i])**(1/4)) > abs(Tau[i]/Tau[j] - (Temp[j]/Temp[i])**(1/3)):
			print("migliore 1/4")
		else:
			print("migliore 1/3")
		# print(f"verifica andamento n = 1/4: {Tau[i]/Tau[j] - (Temp[j]/Temp[i])**(1/4)}")
		# print(f"verifica andamento n = 1/3: {Tau[i]/Tau[j] - (Temp[j]/Temp[i])**(1/3)}")
y = np.log(Tau)
x = np.log(Temp)
uy = uTau/Tau
m, um, c, uc, cov, rho = my.lin_fit(x, y, uy, plot=True)
plt.show()
res = y - (m*x + c)
print(np.sum((res / uy)**2) / (y.size - 2))
sigmy_post = np.sqrt(np.sum((res / uy)**2) / (Temp.size - 2))
uy_post = np.full_like(y, sigmy_post)/100
print(uy_post)
print(np.log(Tau))
print(np.log(Temp))
m, um, c, uc, cov, rho = my.lin_fit(x, y, uy_post, plot=True)
plt.show()
print(np.sum((res / uy_post)**2) / (y.size - 2))
print((-m - 1/3)/um)


Tau_aria = np.array([108.41, 100.37, 100.35, 96.47, 108.45])
uTau = np.array([0.16, 0.13, 0.15, 0.28, 0.31])
Temp_aria = []
temp_mean = 0
for i in range(0, 5):
	t, temp = np.loadtxt(f"data/fit_aria/temp_aria{i}.txt", unpack=True)
	for t in temp:
		temp_mean = temp_mean + t
	temp_mean = temp_mean/len(temp)
	Temp_aria.append(temp_mean - 16.81588)
Temp_aria = np.array(Temp_aria)
for i in range(0, len(Tau_aria)):
	for j in range(i + 1, len(Tau_aria)):
		print("\n******************\n")
		print(f"i = {i}, j = {j}, DT (j/i) = {Temp_aria[j]} / {Temp_aria[i]} e Tau = (i/j) {Tau_aria[i]} / {Tau_aria[j]}")
		if abs(Tau_aria[i]/Tau_aria[j] - (Temp_aria[j]/Temp_aria[i])**(1/4)) > abs(Tau_aria[i]/Tau_aria[j] - (Temp_aria[j]/Temp_aria[i])**(1/3)):
			print("migliore 1/4")
		else:
			print("migliore 1/3")
		# print(f"verifica andamento n = 1/4: {Tau_aria[i]/Tau_aria[j] - (Temp_aria[j]/Temp_aria[i])**(1/4)}")
		# print(f"verifica andamento n = 1/3: {Tau_aria[i]/Tau_aria[j] - (Temp_aria[j]/Temp_aria[i])**(1/3)}")
coeff = np.polyfit(np.log(Temp_aria), np.log(Tau_aria), 1)
my.lin_fit(np.log(Temp_aria), np.log(Tau_aria), uTau/Tau_aria, plot=True)
plt.show()
n_global = -coeff[0]
K_global = np.exp(coeff[1])
print(f"\nEsponente globale stimato n = {n_global:.4f}, K = {K_global:.4f}")
