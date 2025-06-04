import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2
from generarEmpirica import P_EMPIRICA, VALORES 

def generar_rechazo(n_muestras, p=P_EMPIRICA):
    muestras = []
    q = 1 / len(p)
    c = max(p) / q
    while len(muestras) < n_muestras:
        x = random.randint(1, 10)
        u = random.random()
        if u < p[x - 1] / (c * q):
            muestras.append(x)
    return muestras

def test_chi_cuadrado(muestras, p=P_EMPIRICA, alpha=0.05):
    observado = [muestras.count(i) for i in VALORES]
    esperado = [len(muestras) * pi for pi in p]
    chi_obtenido = sum(((obs - esp) ** 2) / esp for obs, esp in zip(observado, esperado))
    chi_critico = round(chi2.ppf(1 - alpha, df=len(p) - 1), 2)

    print("Test Chi Cuadrado")
    print("---------------------------")
    print(f"Valor Chi² obtenido: {chi_obtenido:.4f}")
    print(f"Valor crítico (gl={len(p)-1}, α={alpha}): {chi_critico}")
    print("Resultado:", "✅ Pasa el test" if chi_obtenido < chi_critico else "❌ No pasa el test")
    print()
    print("Valor\tObservado\tEsperado")
    for i in range(10):
        print(f"{i+1}\t{observado[i]}\t\t{esperado[i]:.2f}")

def graficar_comparacion(muestras, p_teorica):
    frecuencias = [muestras.count(i) / len(muestras) for i in VALORES]

    plt.figure(figsize=(10, 5))
    plt.bar(VALORES, frecuencias, label='Empírica (rechazo)', alpha=0.7, color='cornflowerblue')
    plt.plot(VALORES, p_teorica, marker='o', color='red', linestyle='--', label='Probabilidad Teórica')
    plt.xlabel("Valor")
    plt.ylabel("Probabilidad")
    plt.title("Distribución generada por Rechazo")
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
    muestras = generar_rechazo(1000)
    graficar_comparacion(muestras, P_EMPIRICA)
    graficar_histograma(muestras)
    test_chi_cuadrado(muestras)
