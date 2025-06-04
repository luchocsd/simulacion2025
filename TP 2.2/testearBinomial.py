import math
import numpy as np
import matplotlib.pyplot as plt
import argparse



parser = argparse.ArgumentParser(description="Simulador de ruleta")
parser.add_argument("-n", default=10000, type=int, help="Número de pruebas")
args = parser.parse_args()
largo_secuencia = args.n
n = 10
p = 0.5

if largo_secuencia < 1:
    print("El número de pruebas debe ser mayor a 0")
    exit()
if largo_secuencia <= 5000:
    size_puntos_graficos = 15
if largo_secuencia > 5000 and largo_secuencia <= 20000:
    size_puntos_graficos = 10
if largo_secuencia > 20000:
    size_puntos_graficos = 3




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




def graficar_histograma(datos, nombre=""):
    plt.figure(figsize=(14, 8))  
    bins = 40
    color = 'royalblue'
    if "Numpy" in nombre:
      color = 'limegreen'
    if "comparacion" in nombre: 
      color = ['limegreen', 'royalblue']
    plt.hist(datos, bins=bins, edgecolor='black', color=color)
    plt.title(f'Histograma de Frecuencias: {nombre}. N={largo_secuencia}')
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.show()

def graficar_dispersion(datos, nombre=""):
    if "Numpy" in nombre:
      color = 'limegreen'
    else:
      color = 'royalblue'
    plt.figure(figsize=(14, 8))
    plt.scatter(range(len(datos)), datos, label=nombre, color=color, s=size_puntos_graficos)
    plt.xlabel('Índice')
    plt.ylabel('Número Pseudoaleatorio')
    plt.title(f'Gráfico de Dispersión de Números Pseudoaleatorios: {nombre}. N={largo_secuencia}')
    plt.tight_layout()
    plt.show()

def binomial():
  sec_e = np.random.binomial(n, p, largo_secuencia) 
  binomial_valores = dist_binomial(n, p, largo_secuencia) 
  # Graficamos la distribución binomial
  graficar_histograma(binomial_valores, "Binomial")
  graficar_dispersion(binomial_valores, "Binomial")
  graficar_histograma(sec_e, "Numpy-Binomial")
  graficar_dispersion(sec_e, "Numpy-Binomial")
  graficar_histograma([sec_e, binomial_valores], "Binomial-comparacion")



binomial()