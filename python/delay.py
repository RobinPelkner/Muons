import numpy as np 
import matplotlib.pyplot as plt 

data = np.loadtxt("prelimdata/delay.csv", delimiter=";", skiprows=1, unpack= True) 
plt.scatter(data[0], data[1])
plt.errorbar(data[0], data[1], yerr=np.sqrt(data[1]), fmt='o', capsize=4.0)

plt.xlabel(r'Delay / ns')
plt.ylabel(r'Number of coincidences')
plt.tight_layout()
plt.grid(alpha=0.5)
plt.savefig('plots/delay.pdf')
