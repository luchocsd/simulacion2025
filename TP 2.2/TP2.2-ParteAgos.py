import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import hypergeom, binom

# N = Tamaño población
# K = Número de individuos con la caracteristica deseada
# n = Tamaño de la muestra que se observara
# Cuando se calcula la probabilidad de X = x, estas calculando la probabilidad de que en la muestra se obtengan x individuos con la caracteristica deseada

def generar_hipergeometrica(N, K, n, quantityToGenerate):
    generatedNumbers = []
    
    # Parámetro de la binomial
    p = K/N
    
    # Cálculo de la constante C óptima

    c = max([hypergeom.pmf(k, N, K, n) / binom.pmf(k, n, p) for k in range(max(0, n+K-N), min(K, n)+1)])
    
    generatedQuantity = 0
    while generatedQuantity < quantityToGenerate:
        # Generar candidato de la distribución binomial
        x = np.random.binomial(n, p)
        
        # Calcular probabilidad de aceptación
        p_hypergeom = hypergeom.pmf(x, N, K, n) # Evalua la variable aleatoria generada en la función de densidad de la hipergeometrica
        p_binom = binom.pmf(x, n, p) # Evalua la variable aleatoria generada en la función de densidad de la binomial
        p_accept = p_hypergeom / (c * p_binom) # Calcula la condicion de rechazo
        
        # Decidir si aceptar o rechazar
        if np.random.uniform() <= p_accept:
            generatedNumbers.append(x)
            generatedQuantity += 1
    
    return generatedNumbers


def generateHistogramComparison(numeros, N, K, n):
    plt.figure(figsize=(10, 6))

    # Valores posibles de éxitos en la muestra
    x_values = np.arange(max(0, n + K - N), min(K, n) + 1)

    # Frecuencia relativa de los datos simulados
    sim_counts = [numeros.count(x) / len(numeros) for x in x_values]

    # Distribución teórica (PMF)
    pmf_values = [hypergeom.pmf(x, N, K, n) for x in x_values]

    # Dibujar barras comparativas
    plt.bar(x_values - 0.2, sim_counts, width=0.4, label='Simulación', alpha=0.7, color='blue')
    plt.bar(x_values + 0.2, pmf_values, width=0.4, label='Distribución teórica', alpha=0.7, color='red')

    # Etiquetas y leyenda
    plt.title(f'Distribución Hipergeométrica: N={N}, K={K}, n={n}')
    plt.xlabel('Número de éxitos en la muestra')
    plt.ylabel('Probabilidad')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Estadísticas
    mean_simulated = np.mean(numeros)
    mean_theoretical = n * (K / N)
    var_simulated = np.var(numeros)
    var_theoretical = n * (K / N) * (1 - K / N) * ((N - n) / (N - 1))

    stats_text = (
        f'Media simulada: {mean_simulated:.4f}\n'
        f'Media teórica: {mean_theoretical:.4f}\n'
        f'Varianza simulada: {var_simulated:.4f}\n'
        f'Varianza teórica: {var_theoretical:.4f}'
    )
    plt.figtext(0.15, 0.15, stats_text, bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()
    plt.show()

    return 0


## Programa principal
N = 1000
K = 90
n = 20
quantityToGenerate = 10000

numeros = generar_hipergeometrica(N,K,n,quantityToGenerate)
print(numeros)
generateHistogramComparison(numeros,N,K,n)

