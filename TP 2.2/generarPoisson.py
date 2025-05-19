import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import poisson

# main
largo_secuencia = 10000

directorio_actual = os.path.dirname(os.path.abspath(__file__))

ruta_graficas = os.path.join(directorio_actual, 'graficas/')
if not os.path.exists(ruta_graficas):
    os.makedirs(ruta_graficas)

ruta_generadas = os.path.join(ruta_graficas, 'generadas/')
if not os.path.exists(ruta_generadas):
    os.makedirs(ruta_generadas)

ruta_graficas_numpy = os.path.join(ruta_graficas, 'numpy/')
if not os.path.exists(ruta_graficas_numpy):
    os.makedirs(ruta_graficas_numpy)

ruta_graficas_comparacion = os.path.join(ruta_graficas, 'comparacion/')
if not os.path.exists(ruta_graficas_comparacion):
    os.makedirs(ruta_graficas_comparacion)

def dist_poisson(p, size):
    # Lista para almacenar los valores generados con distribución de Poisson
    datos_poisson = []
    # Repetimos el proceso 'size' veces para generar 'size' números aleatorios
    for i in range(size):
        x = 0  # Contador de eventos
        b = np.exp(-p)  # Calcula e^(-p), parte de la fórmula de Poisson
        tr = 1  # Inicializa el producto acumulativo de números aleatorios
        # Genera un número aleatorio hasta que el producto sea menor que b
        while True:
            r = np.random.uniform(0, 1)  # Número aleatorio entre 0 y 1
            tr = tr * r  # Actualiza el producto acumulativo
            if tr < b:   # Si el producto es menor que b, termina el ciclo
                break
            x = x + 1  # Cuenta cuántas veces ocurre esto antes de romper el ciclo
        datos_poisson.append(x)  # Agrega el resultado a la lista
    return datos_poisson  # Devuelve la lista de números generados

def graficar_histograma(datos, nombre=""):
    plt.figure(figsize=(14, 8))  
    bins = 40
    color = 'royalblue'
    histograma = os.path.join(ruta_generadas, f'histograma_{nombre}.png')
    if "Numpy" in nombre:
      histograma = os.path.join(ruta_graficas_numpy, f'histograma_{nombre}.png')
      color = 'limegreen'
    if "comparacion" in nombre: 
      histograma = os.path.join(ruta_graficas_comparacion, f'histograma_{nombre}.png')
      color = ['limegreen', 'royalblue']
    if ("Pascal" or "Binomial" or "Hipergeometrica" or "Poisson" or "Empirica_Discreta" ) in nombre: 
      bins = np.arange(0, 21) - 0.5

    plt.hist(datos, bins=bins, edgecolor='black', color=color)
    plt.title(f'Histograma de Frecuencias: {nombre}. N={largo_secuencia}')
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    plt.savefig(histograma)
    plt.close()

def graficar_dispersion(datos, nombre=""):
    if "Numpy" in nombre:
      dispersion = os.path.join(ruta_graficas_numpy, f'dispersion_{nombre}.png')
      color = 'limegreen'
    else:
      dispersion = os.path.join(ruta_generadas, f'dispersion_{nombre}.png')
      color = 'royalblue'
    plt.figure(figsize=(14, 8))
    plt.scatter(range(len(datos)), datos, label=nombre, color=color, s=10)
    plt.xlabel('Índice')
    plt.ylabel('Número Pseudoaleatorio')
    plt.title(f'Gráfico de Dispersión de Números Pseudoaleatorios: {nombre}. N={largo_secuencia}')
    plt.savefig(dispersion)
    plt.close()

def poisson2():
  sec_po = np.random.poisson(5, largo_secuencia)
  datos_poisson = dist_poisson(5, largo_secuencia)
  graficar_histograma(datos_poisson, "Poisson")
  graficar_dispersion(datos_poisson, "Poisson")
  # Graficamos la distribución binomial
  graficar_histograma(sec_po, "Numpy-Poisson")
  graficar_dispersion(sec_po, "Numpy-Poisson")
  graficar_histograma([sec_po, datos_poisson], "Poisson-comparacion")

poisson2()

#test 

# Histograma para la distribución Poisson

tam = 10000
valor_lambda = 5

poisson_valores = np.random.poisson(valor_lambda, tam)

plt.figure(figsize=(8, 6))
plt.hist(poisson_valores, bins=np.arange(0, np.max(poisson_valores)+2) - 0.5, density=True, alpha=0.6, color='g', label='Datos Poisson')
x = np.arange(0, np.max(poisson_valores)+1)
plt.plot(x, poisson.pmf(x, valor_lambda), 'r-', label='Esperado')
plt.title('Distribución Poisson')
plt.legend()
plt.xlabel('Valor')
plt.ylabel('Densidad')
plt.tight_layout()
plt.show()
