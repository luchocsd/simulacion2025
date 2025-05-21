import numpy as np
from scipy.stats import nbinom, geom
import matplotlib.pyplot as plt


def generar_pascal(r, p, quantityToGenerate):
    """
    Genera números aleatorios con distribución Pascal usando el método de aceptación-rechazo
    con una mejor selección de la constante C y la distribución propuesta.
    
    Args:
        r (float): Parámetro r de la distribución Pascal
        p (float): Parámetro p de la distribución Pascal
        quantityToGenerate (int): Cantidad de números a generar
        
    Returns:
        list: Lista de números generados
    """
    generatedNumbers = []
    q = 1 - p
    
    # Usamos una distribución Poisson con lambda = r*(1-p)/p como propuesta
    # Esta se asemeja más a la forma de la binomial negativa
    lambda_poisson = r * (1-p) / p
    
    # Calculamos C en un rango razonable
    x_range = np.arange(0, int(lambda_poisson * 3) + 1)
    
    # Función de densidad de probabilidad de la binomial negativa
    f_x_values = nbinom.pmf(x_range, r, p)
    
    # Función de densidad de probabilidad de la Poisson
    from scipy.stats import poisson
    g_x_values = poisson.pmf(x_range, lambda_poisson)
    
    # Calculamos las razones donde g_x != 0
    valid_indices = g_x_values > 1e-10
    ratios = np.zeros_like(f_x_values)
    ratios[valid_indices] = f_x_values[valid_indices] / g_x_values[valid_indices]
    
    c = np.max(ratios) * 1.01  # Margen de seguridad
    print(f"Constante C calculada: {c}")
    
    # Para depuración
    aceptados = 0
    intentos = 0
    
    while len(generatedNumbers) < quantityToGenerate:
        intentos += 1
        # Generamos una variable aleatoria Poisson
        x = np.random.poisson(lambda_poisson)
        
        # Calculamos las densidades
        f_x = nbinom.pmf(x, r, p)
        g_x = poisson.pmf(x, lambda_poisson)
        
        # Evitamos división por cero
        if g_x < 1e-10:
            continue
            
        p_accept = f_x / (c * g_x)
        
        if np.random.uniform() < p_accept:
            generatedNumbers.append(x)
            aceptados += 1
            
        # Imprimimos estadísticas cada 1000 intentos
        if intentos % 1000 == 0:
            print(f"Intentos: {intentos}, Aceptados: {aceptados}, Tasa de aceptación: {aceptados/intentos:.4f}")
            
    print(f"Tasa de aceptación final: {aceptados/intentos:.4f}")
    return generatedNumbers

def generateHistogramComparison(numeros_generados, r, p):

    plt.figure(figsize=(12, 7))


    max_obs = 0
    if numeros_generados: # Comprobar si la lista no está vacía
        max_obs = np.max(numeros_generados)

    lim_sup_teorico = nbinom.ppf(0.999, r, p)
    x_max_val = int(max(max_obs, lim_sup_teorico, r + 5)) # Asegurar que r está bien representado
    if x_max_val < 10: # Si el rango es muy pequeño, extenderlo un poco
        x_max_val = 15
    
    x_values = np.arange(0, x_max_val + 1)

    # Frecuencia relativa de los datos simulados
    # np.histogram es más eficiente para esto que list.count
    counts, bin_edges = np.histogram(numeros_generados, bins=np.arange(0, x_max_val + 2) - 0.5, density=True)
    sim_freq = counts

    # Distribución teórica (PMF) de la Binomial Negativa
    # nbinom.pmf(k, n, p) donde k es el número de fracasos, n es el número de éxitos (r)
    pmf_values = [nbinom.pmf(x, r, p) for x in x_values]

    # Dibujar barras comparativas
    plt.bar(x_values - 0.2, sim_freq, width=0.4, label='Simulación (Frec. Relativa)', alpha=0.7, color='deepskyblue')
    plt.bar(x_values + 0.2, pmf_values, width=0.4, label='PMF Teórica (Pascal)', alpha=0.7, color='salmon')

    # Etiquetas y leyenda
    plt.title(f'Comparación: Simulación Pascal vs. PMF Teórica (r={r}, p={p})', fontsize=15)
    plt.xlabel('Número de fracasos antes del r-ésimo éxito (x)', fontsize=12)
    plt.ylabel('Probabilidad / Frecuencia Relativa', fontsize=12)
    plt.xticks(x_values[::max(1, len(x_values)//20)]) # Mostrar xticks de forma más espaciada si hay muchos
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=10)

    # Estadísticas
    mean_simulated = np.mean(numeros_generados)
    var_simulated = np.var(numeros_generados)
    
    # La media teórica de N(r,p) contando fracasos es r*(1-p)/p
    mean_theoretical = nbinom.mean(r, p)
    # La varianza teórica de N(r,p) contando fracasos es r*(1-p)/(p^2)
    var_theoretical = nbinom.var(r, p)

    stats_text = (
        f'Resultados de la Simulación ({len(numeros_generados)} muestras):\n'
        f'  Media simulada: {mean_simulated:.4f}\n'
        f'  Varianza simulada: {var_simulated:.4f}\n\n'
        f'Valores Teóricos (Pascal con r={r}, p={p}):\n'
        f'  Media teórica: {mean_theoretical:.4f}\n'
        f'  Varianza teórica: {var_theoretical:.4f}'
    )
    
    # Añadir el texto de estadísticas al gráfico
    # Ajustar la posición y el tamaño del cuadro de texto para mejor visualización
    plt.figtext(0.5, -0.1, stats_text, ha="center", fontsize=10,
                bbox={"facecolor":"whitesmoke", "alpha":0.7, "pad":5},
                transform=plt.gca().transAxes) # Posicionar relativo a los ejes

    plt.tight_layout(rect=[0, 0.05, 1, 0.95]) # Ajustar layout para que el título y figtext no se solapen
    plt.show()

    return 0



#Programa principal
r = 5
p = 0.5
quantityToGenerate = 1000

numeros = generar_pascal(r,p,quantityToGenerate)
print("SE GENERARON")
generateHistogramComparison(numeros,r,p)