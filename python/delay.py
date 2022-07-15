import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
import uncertainties.unumpy as unp
def linear(x, a, b):
    return a*x +b


data = np.loadtxt("prelimdata/delay.csv", delimiter=";", skiprows=1, unpack= True) 
data = data[ :, data[0].argsort()]
print(data)
plt.scatter(data[0], data[1])
plt.errorbar(data[0], data[1], yerr=np.sqrt(data[1]), fmt='o', capsize=4.0)
plt.fill_between(np.arange(-31, 34), 296, 390,  color='orange', hatch='//', alpha=0.4)
max_count = np.sum(data[1][(-25 <= data[0]) & (32 >= data[0])]) / np.count_nonzero(
    (-25 <= data[0]) & (32 >= data[0]))
print("Gemittelte maximale Anzahl an Counts", max_count, np.sqrt(max_count))
params, covariance_matrix = curve_fit(linear, data[0][4:11], data[1][4:11])
print(params, np.sqrt(np.diag(covariance_matrix)))
#plt.plot(data[0][4:11], linear(data[0][4:11], *params), "r-", label='Linear Fit')
err = unp.uarray(params, np.sqrt(np.diag(covariance_matrix)))
t_half_left = (max_count / 2 - err[1]) / err[0]
print("Fit-Parameter linke Flanke: ", params, "\n Werte half maximum links: ", t_half_left)


params, covariance_matrix = curve_fit(linear, data[0][-9:], data[1][-9:])
print(params, np.sqrt(np.diag(covariance_matrix)))
#plt.plot(data[0][-9:], linear(data[0][-9:], *params), "r-", label='Linear Fit')
err = unp.uarray(params, np.sqrt(np.diag(covariance_matrix)))
t_half_right = (max_count / 2 - err[1]) / err[0]
print("Fit-Parameter rechte Flanke: ", params, "\n Werte half maximum rechts: ", t_half_right)

print('FWHM ', -t_half_left + t_half_right)

plt.xlabel(r'Delay $\Delta t$ / ns')
plt.ylabel(r'Number of coincidences $N$')
plt.tight_layout()
plt.grid(alpha=0.5)
plt.savefig('plots/delay.pdf')
