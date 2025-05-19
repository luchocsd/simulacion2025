import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kstest, expon, norm, binom, poisson
import argparse


largo_secuencia = 10000
lambda_Exp= 1

def dist_exponencial(lambd, largo_secuencia_exponencial):
    # Generamos la secuencia de números pseudoaleatorios
    secuencia = np.random.uniform(0, 1, largo_secuencia_exponencial)
    # Generación de la distribución exponencial con metodo de inversion
    datos_exponencial = [-math.log(x) / lambd for x in secuencia]
    return datos_exponencial



exponencial_valores = dist_exponencial(lambda_Exp, largo_secuencia)

exponential_valores = np.random.exponential(1, largo_secuencia)
plt.hist(exponencial_valores, bins=50, density=True, alpha=0.6, color='g', label='Datos Exponencial')
x = np.linspace(0, 10, 1000)
plt.plot(x, expon.pdf(x), 'r-', label='Esperado')
plt.title('Distribucion Exponencial')
plt.legend()


plt.tight_layout()
plt.show()
