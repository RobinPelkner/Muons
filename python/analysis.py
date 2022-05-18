from ctypes import sizeof
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from  scipy.stats import chisquare

df = pd.read_csv('data/mugr5_4.txt', sep='	',
 names=['chan1', 'chan2', 'chan3', 'chan4', 'chan5', 'chan6', 'chan7', 'chan8',
  'chan9', 'chan10', 'chan11', 'chan12', 'chan13', 'chan14', 'chan15', 'chan16'],
  usecols=['chan3', 'chan4', 'chan5', 'chan6','chan11', 'chan12', 'chan13', 'chan14']) 
print(df.shape)

#sort out empty events
df = df.drop(df[(df['chan3'] ==4095) & (df['chan4'] ==4095)  & (df['chan5'] ==4095) & (df['chan11'] ==4095) & (df['chan12'] ==4095) & (df['chan13'] ==4095)].index)
#print(df.head())
print(df.shape)
#transform into real times
data = np.loadtxt("prelimdata/conv.txt", delimiter=";", skiprows=0, unpack= True) 
conv = data[0]
offset= data[1]
conv = np.append(conv[2:6], conv[10:14])
offset = np.append(offset[2:6], offset[10:14])

def f(x, a, b, tau):
    return a + b * np.exp(- x / tau) 

#P0 Plane

p01 = df.drop(df[(df['chan3'] ==4095)].index)
p01 = p01.drop(p01[(p01['chan4'] !=4095) | (p01['chan5'] !=4095) | (p01['chan11'] !=4095) | (p01['chan12'] !=4095) | (p01['chan13'] !=4095)].index)
p02 = df.drop(df[(df['chan11'] ==4095)].index)
p02 = p02.drop(p02[(p02['chan4'] !=4095) | (p02['chan5'] !=4095) | (p02['chan3'] !=4095) | (p02['chan12'] !=4095) | (p02['chan13'] !=4095)].index)
p02 = p02.sub(offset)
p02 = p02.div(conv)
p02['chan11'] = p02['chan11'] + p02['chan6'] 
p01 = p01.sub(offset)
p01 = p01.div(conv)
#Checking for events in both tdc at the "same" time; there are none
#c = df.drop(df[(df['chan3'] ==4095) | (df['chan11'] ==4095) ].index)
#print(c.head())
range_of_bins = (0, 8700)
number_of_bins = 48
x = p01['chan3']
x = x.append(p02['chan11'])
print(x.shape)
p0, bin_edges, dump = plt.hist(x, bins=number_of_bins, range=range_of_bins, histtype='barstacked', edgecolor='royalblue', color=['lightsteelblue'])
#print('P0', bin_edges)
bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
popt, cov = curve_fit(f, bin_centers[4:], p0[4:], p0=[3, 100, 2000])
print(chisquare(p0[4:], f_exp=f(bin_centers[4:], *popt)))
print('P0')
print(popt[0], np.sqrt(cov[0][0]))
print(popt[1], np.sqrt(cov[1][1]))
print(popt[2], np.sqrt(cov[2][2]))
x_interval_for_fit = np.linspace(bin_edges[4], bin_edges[-1], 10000)
plt.plot(x_interval_for_fit, f(x_interval_for_fit, *popt), label='fit', color='orangered')
plt.errorbar(
    bin_centers,
    p0,
    yerr = np.sqrt(p0),
    fmt='.',
    color='royalblue',
    capsize=3.0
)
plt.savefig('plots/p0.pdf')
plt.clf()

#P1 Plane

p11 = df.drop(df[(df['chan4'] ==4095)].index)
p11 = p11.drop(p11[(p11['chan3'] !=4095) | (p11['chan5'] !=4095) | (p11['chan11'] !=4095) | (p11['chan12'] !=4095) | (p11['chan13'] !=4095)].index)
p12 = df.drop(df[(df['chan12'] ==4095)].index)
p12 = p12.drop(p12[(p12['chan4'] !=4095) | (p12['chan5'] !=4095) | (p12['chan3'] !=4095) | (p12['chan11'] !=4095) | (p12['chan13'] !=4095)].index)
p12 = p12.sub(offset)
p12 = p12.div(conv)
p12['chan12'] = p12['chan12'] + p12['chan6'] 
p11 = p11.sub(offset)
p11 = p11.div(conv)
#Checking for events in both tdc at the "same" time; there are none
#c = df.drop(df[(df['chan3'] ==4095) | (df['chan11'] ==4095) ].index)
#print(c.head())
number_of_bins = 77
x = p11['chan4']
x = x.append(p12['chan12'])
p1, bin_edges, dump = plt.hist(x, bins=number_of_bins, range=range_of_bins, histtype='barstacked', edgecolor='royalblue', color=['lightsteelblue'])
bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
popt, cov = curve_fit(f, bin_centers[2:], p1[2:], p0=[3, 100, 2000])
print(x.shape)
print(chisquare(p1[2:], f_exp=f(bin_centers[2:], *popt)))
print('P1')
print(popt[0], np.sqrt(cov[0][0]))
print(popt[1], np.sqrt(cov[1][1]))
print(popt[2], np.sqrt(cov[2][2]))
x_interval_for_fit = np.linspace(bin_edges[2], bin_edges[-1], 10000)
plt.plot(x_interval_for_fit, f(x_interval_for_fit, *popt), label='fit', color='orangered')
plt.errorbar(
    bin_centers,
    p1,
    yerr = np.sqrt(p1),
    fmt='.',
    color='royalblue',
    capsize=3.0
)
plt.savefig('plots/p1.pdf')
plt.clf()
#P2 Plane

p21 = df.drop(df[(df['chan5'] ==4095)].index)
p21 = p21.drop(p21[(p21['chan3'] !=4095) | (p21['chan4'] !=4095) | (p21['chan11'] !=4095) | (p21['chan12'] !=4095) | (p21['chan13'] !=4095)].index)
p22 = df.drop(df[(df['chan13'] ==4095)].index)
p22 = p22.drop(p22[(p22['chan4'] !=4095) | (p22['chan5'] !=4095) | (p22['chan3'] !=4095) | (p22['chan11'] !=4095) | (p22['chan12'] !=4095)].index)
p22 = p22.sub(offset)
p22 = p22.div(conv)
p22['chan13'] = p22['chan13'] + p22['chan6'] 
p21 = p21.sub(offset)
p21 = p21.div(conv)
#Checking for events in both tdc at the "same" time; there are none
#c = df.drop(df[(df['chan3'] ==4095) | (df['chan11'] ==4095) ].index)
#print(c.head())
number_of_bins =60
x = p21['chan5']
x = x.append(p22['chan13'])
print(x.shape)
p2, bin_edges, dump = plt.hist(x, bins=number_of_bins, range=range_of_bins, histtype='barstacked', edgecolor='royalblue', color=['lightsteelblue'])
bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
popt, cov = curve_fit(f, bin_centers[3:], p2[3:],p0=[3, 100, 2000])
print(chisquare(p2[3:], f_exp=f(bin_centers[3:], *popt)))
print('P2')
print(popt[0], np.sqrt(cov[0][0]))
print(popt[1], np.sqrt(cov[1][1]))
print(popt[2], np.sqrt(cov[2][2]))
x_interval_for_fit = np.linspace(bin_edges[1], bin_edges[-1], 10000)
plt.plot(x_interval_for_fit, f(x_interval_for_fit, *popt), label='fit', color='orangered')
plt.errorbar(
    bin_centers,
    p2,
    yerr = np.sqrt(p2),
    fmt='.',
    color='royalblue',
    capsize=3.0
)
plt.savefig('plots/p2.pdf')
plt.clf()
#P0+P1+P2
range_of_bins = (0, 8700) 
number_of_bins= 44
x = p21['chan5']
x = x.append([p22['chan13'], p11['chan4'], p12['chan12'], p01['chan3'], p02['chan11']]) 
pALL, bin_edges, dump = plt.hist(x, bins=number_of_bins, align='left', range=range_of_bins, histtype='barstacked', edgecolor='royalblue', color=['lightsteelblue'], stacked=True)
bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
popt, cov = curve_fit(f, bin_centers[3:], pALL[3:], p0=[3, 100, 2000])
print(x.shape)
print(chisquare(pALL[3:], f_exp=f(bin_centers[3:], *popt)))
print('PALL')
print(popt[0], np.sqrt(cov[0][0]))
print(popt[1], np.sqrt(cov[1][1]))
print(popt[2], np.sqrt(cov[2][2]))
x_interval_for_fit = np.linspace(bin_edges[3], bin_edges[-1], 10000)
plt.plot(x_interval_for_fit, f(x_interval_for_fit, *popt), label='fit', color='orangered')
plt.errorbar(
    bin_centers,
    pALL,
    yerr = np.sqrt(pALL),
    fmt='.',
    color='royalblue',
    capsize=3.0
)
plt.savefig('plots/pALL.pdf')

plt.clf()

print('Test')
def test(x, a, c, t1, t2):
    return a *( 1.3 * np.exp(-x/t1) +np.exp(-x/t2)) + c 
number_of_bins = 59
range_of_bins=(0, 8700)
ptest, bin_edges, dump = plt.hist(x, bins=number_of_bins, range=range_of_bins, histtype='barstacked', edgecolor='royalblue', color=['lightsteelblue'], stacked=True)
bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
popt, cov = curve_fit(test, bin_centers[2:], ptest[2:], sigma=np.sqrt(ptest[2:]), p0=[300, 30, 2000, 200])
print(chisquare(ptest[2:], f_exp=test(bin_centers[2:], *popt)))
print(popt[0], np.sqrt(cov[0][0]))
print(popt[1], np.sqrt(cov[1][1]))
print(popt[2], np.sqrt(cov[2][2]))
print(popt[3], np.sqrt(cov[3][3]))
x_interval_for_fit = np.linspace(bin_edges[1], bin_edges[-1], 10000)

plt.plot(x_interval_for_fit, test(x_interval_for_fit, *popt), label='Fit', color='orangered')
plt.plot(x_interval_for_fit[1:], f(x_interval_for_fit[1:], a=popt[1], b=popt[0], tau=popt[3]), color='green', label='Fit for bound Muons')
plt.errorbar(
    bin_centers,
    ptest,
    yerr = np.sqrt(ptest),
    fmt='.',
    color='royalblue',
    capsize=3.0
)
plt.legend()
plt.tight_layout()
plt.savefig('plots/ptest.pdf')
#df = df.mul(conv)
#print(df.head())
