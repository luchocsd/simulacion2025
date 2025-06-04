import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kstest, expon, norm, binom, poisson
import argparse


largo_secuencia = 10000
n = 10
p = 0.5 

def dist_binomial(n, p, largo_secuencia):
  datos_binomial = []
  for i in range(largo_secuencia):
    x = 0
    for i in range(n):
      r = np.random.uniform(0, 1)
      if r <= p:
        x = x + 1
    datos_binomial.append(x)
  return datos_binomial

binomial_valores = dist_binomial(n, p, largo_secuencia)


plt.hist(binomial_valores, bins=np.arange(n+2)-0.5, density=True, alpha=0.7, color='#4F81BD', edgecolor='black',label='Datos Binomial',width=0.8)
x = np.arange(0, n+1)
plt.plot(x, binom.pmf(x, n, p), 'o-', color='#C0504D', label='Esperado', linewidth=2, markersize=7)
plt.title('Distribución Binomial')
plt.xlabel('Número de éxitos')
plt.ylabel('Probabilidad')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)


plt.tight_layout()
plt.show()