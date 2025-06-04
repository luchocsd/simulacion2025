import random
import matplotlib.pyplot as plt
import numpy as np

# Probabilidades fijas
P_EMPIRICA = [0.273, 0.037, 0.195, 0.009, 0.124, 0.058, 0.062, 0.151, 0.047, 0.044]
VALORES = list(range(1, 11))

def generar_empirica(n=1000, p=P_EMPIRICA):
    resultados = []
    for _ in range(n):
        r = random.random()
        acumulado = 0
        valor = 1
        for prob in p:
            acumulado += prob
            if r <= acumulado:
                break
            valor += 1
        resultados.append(valor)
    return resultados

def graficar_distribucion(muestras, p_teorica):
    observados = [muestras.count(i) for i in VALORES]
    probabilidades = [obs / len(muestras) for obs in observados]

    plt.figure(figsize=(10, 5))
    plt.bar(VALORES, probabilidades, color='mediumslateblue', alpha=0.8, label='Probabilidad Empírica')
    plt.plot(VALORES, p_teorica, marker='o', color='red', linestyle='--', label='Probabilidad Teórica')
    plt.xlabel("Valor")
    plt.ylabel("Probabilidad")
    plt.title("Distribución Empírica")
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def graficar_histograma(muestras):
    plt.figure(figsize=(8, 4))
    plt.hist(muestras, bins=np.arange(1, 12) - 0.5, color='orchid', edgecolor='black', rwidth=0.9)
    plt.title("Histograma de Frecuencia")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    plt.xticks(VALORES)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    muestras = generar_empirica()
    graficar_distribucion(muestras, P_EMPIRICA)
    graficar_histograma(muestras)