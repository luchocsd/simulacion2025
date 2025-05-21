import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, nbinom
import os

# Parámetros
lambda_poisson = 3
cantidad = 10000

# Preparar carpetas
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_graficas = os.path.join(directorio_actual, 'graficas/')
os.makedirs(ruta_graficas, exist_ok=True)

# Generador con método de rechazo
def generar_poisson_rechazo(lambd, cantidad_a_generar):
    numeros_generados = []

    # Distribución propuesta: Pascal
    r = lambd
    p = r / (r + 1)

    # Rango razonable para buscar C
    rango = np.arange(0, int(3 * lambd) + 1)
    f = poisson.pmf(rango, lambd)
    g = nbinom.pmf(rango, r, p)

    indices_validos = g > 1e-10
    cocientes = np.zeros_like(f)
    cocientes[indices_validos] = f[indices_validos] / g[indices_validos]
    C = np.max(cocientes) * 1.01  # Margen

    print(f"Constante C = {C:.4f}")

    aceptados = 0
    intentos = 0

    while len(numeros_generados) < cantidad_a_generar:
        intentos += 1
        x = np.random.negative_binomial(r, p)
        f_x = poisson.pmf(x, lambd)
        g_x = nbinom.pmf(x, r, p)

        if g_x < 1e-10:
            continue

        u = np.random.uniform()
        if u <= f_x / (C * g_x):
            numeros_generados.append(x)
            aceptados += 1

        if intentos % 1000 == 0:
            print(f"Intentos: {intentos}, Aceptados: {aceptados}, Tasa: {aceptados / intentos:.4f}")

    print(f"Tasa de aceptación final: {aceptados / intentos:.4f}")
    return numeros_generados

# Gráfico comparativo
def graficar_comparacion(datos, lambd, nombre="Poisson-Rechazo"):
    ruta_archivo = os.path.join(ruta_graficas, f'histograma_{nombre}.png')
    plt.figure(figsize=(10, 6))

    x_vals = np.arange(0, max(datos) + 1)
    bins = np.arange(0, max(datos) + 2) - 0.5
    frec_rel = [datos.count(x) / len(datos) for x in x_vals]
    pmf_teo = poisson.pmf(x_vals, lambd)

    plt.bar(x_vals - 0.2, frec_rel, width=0.4, label='Simulación', alpha=0.7, color='royalblue')
    plt.bar(x_vals + 0.2, pmf_teo, width=0.4, label='Poisson Teórica', alpha=0.7, color='orange')
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia relativa / Probabilidad")
    plt.title(f'Comparación: Método de Rechazo para Poisson(λ={lambd})')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Estadísticas
    media_sim = np.mean(datos)
    var_sim = np.var(datos)
    texto = f"Media simulada: {media_sim:.2f}\nVarianza simulada: {var_sim:.2f}\nMedia teórica: {lambd}\nVarianza teórica: {lambd}"
    plt.figtext(0.15, 0.15, texto, bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()
    plt.savefig(ruta_archivo)
    plt.close()

# Main
datos = generar_poisson_rechazo(lambda_poisson, cantidad)
graficar_comparacion(datos, lambda_poisson)
