import math
import numpy as np
import matplotlib.pyplot as plt
import argparse



parser = argparse.ArgumentParser(description="Simulador de ruleta")
parser.add_argument("-n", default=10000, type=int, help="Número de pruebas")
args = parser.parse_args()
largo_secuencia = args.n

if largo_secuencia < 1:
    print("El número de pruebas debe ser mayor a 0")
    exit()
if largo_secuencia <= 5000:
    size_puntos_graficos = 15
if largo_secuencia > 5000 and largo_secuencia <= 20000:
    size_puntos_graficos = 10
if largo_secuencia > 20000:
    size_puntos_graficos = 3




def dist_exponencial(lambd, largo_secuencia_exponencial):
    # Generamos la secuencia de números pseudoaleatorios
    secuencia = np.random.uniform(0, 1, largo_secuencia_exponencial)
    # Generación de la distribución exponencial con metodo de inversion
    datos_exponencial = [-math.log(x) / lambd for x in secuencia]
    return datos_exponencial




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


def exponencial():
  sec_e = np.random.exponential(0.5, largo_secuencia)  #Lambda de numpy es 1/ parametro (con 0.5 seria un lambda de 2)
  datos_exponencial = dist_exponencial(2, largo_secuencia)  
  # Graficamos la distribución exponencial
  graficar_histograma(datos_exponencial, "Exponencial")
  graficar_dispersion(datos_exponencial, "Exponencial")
  graficar_histograma(sec_e, "Numpy-Exponencial")
  graficar_dispersion(sec_e, "Numpy-Exponencial")
  graficar_histograma([sec_e, datos_exponencial], "Exponencial-comparacion")

exponencial()
