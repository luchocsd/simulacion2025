import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats
# Pendientes
# 1 - Programar el ingreso de parametros por consola



# Parámetros por consola

quantityToGenerate = 10000
generator = "GCL"

seed = 1234 #Opcional pero requiere seedSize en su lugar 
seedSizeParam = 4 #Opcional, se usa cuando no hay seed

## Funcion principal

def startSimulation(quantityToGenerate, generator, seed = None,seedSizeParam = None):


    if seed is None:
        
        seed = generateSeed(seedSizeParam)

    
    generatedNumbers, normalizedNumbers = generate(quantityToGenerate,generator, seed)

    chiSquareResult = chi_square_test(normalizedNumbers)
    seriesResult = series_test(normalizedNumbers)

    printGraphics(normalizedNumbers,chiSquareResult)
    printSeriesHeatmap(seriesResult)

    return 0

## Funciones auxiliares

def generate(quantityToGenerate,generator, seed):

    if generator == "CUADRADOS":
        numbers, normalizedNumbers = cuadradosGenerator(quantityToGenerate, seed)
    
    elif generator == "GCL":
        numbers, normalizedNumbers = GCLGenerator(quantityToGenerate,seed)

    return numbers, normalizedNumbers



def obtainMiddleDigits(number,seedSize):

    num_str = str(number).zfill(2 * seedSize) ## Rellenar de ceros a la izquierda hasta tener un numero de tantos digitos como el doble de la semilla. 
    

    length = len(num_str)
    
    if length <= seedSize:
        return number
    
    initialPosition = (length - seedSize) // 2
    
    # Extraer los N(seedSize) dígitos del medio dando prioridad a la izquierda
    middleDigits = int(num_str[initialPosition:initialPosition + seedSize])
    
    return middleDigits


def generateSeed(seedSizeParam):

    lower_limit = 10**(seedSizeParam-1)  # Primer número con seedSize dígitos
    upper_limit = (10**seedSizeParam) - 1  # Último número con seedSize dígitos
        
    seed = random.randint(lower_limit, upper_limit)
    print(f"Semilla generada automáticamente: {seed}")

    return seed

## Generadores

def cuadradosGenerator(quantityToGenerate,seed):

    numbers = []
    normalizedNumbers = []

    seedSize = len(str(seed))
    maxVal = 10**seedSize - 1

    x = seed

    for _ in range (0,quantityToGenerate):

        x = obtainMiddleDigits(x**2,seedSize)

        normalizedNumbers.append(x / maxVal)
        numbers.append(x)
     

    return numbers, normalizedNumbers


def GCLGenerator(quantityToGenerate, seed):
    numbers = []
    normalizedNumbers = []
    # Valores recomendados según Hull-Dobell Theorem para un buen periodo
    # Estos son valores comunes utilizados en implementaciones reales

    multiplicador = 1664525
    incremento = 1013904223
    modulo = 2**32  # Usar potencia de 2 para eficiencia
    
    if seed > modulo:
        return [0], [0]  # Asegurar que la semilla esté en el rango correcto (teoricamente debe ser menor al modulo)
    
    x = seed
    
    for _ in range(quantityToGenerate):
        x = (multiplicador * x + incremento) % modulo

        numbers.append(x)

        # Normaliza entre 0 y 1
        normalizedNumbers.append(x / modulo)
    
    return numbers, normalizedNumbers

## Testeos

def chi_square_test(normalizedNumbers, bins=100):
    """
    Realiza una prueba chi-cuadrado para comprobar la uniformidad de los números generados
    utilizando scipy.stats.chisquare.
    """
    # Clasificar los números en los bins
    observed, bin_edges = np.histogram(normalizedNumbers, bins=bins, range=(0, 1))
    
    # Valor esperado para cada bin (distribución uniforme)
    expected = len(normalizedNumbers) / bins
    
    # Realizar la prueba chi-cuadrado usando scipy
    chi_square_stat, p_value = stats.chisquare(observed, f_exp=[expected]*bins)
    
    # Resultado de la prueba (nivel de significancia típico: 0.05)
    passed = p_value > 0.05
    
    result = {
        'chi_square': chi_square_stat,
        'p_value': p_value,
        'dof': bins - 1,
        'passed': passed,
        'observed': observed,
        'expected': expected
    }
    
    return result

def series_test(normalizedNumbers, grid_size=10):
    observed = np.zeros((grid_size, grid_size), dtype=int)
    n_pairs = len(normalizedNumbers) - 1
    for i in range(n_pairs):
        x = int(normalizedNumbers[i] * grid_size)
        y = int(normalizedNumbers[i + 1] * grid_size)
        if x == grid_size: x -= 1
        if y == grid_size: y -= 1
        observed[x][y] += 1

    expected = n_pairs / (grid_size ** 2)
    chi2 = ((observed - expected) ** 2 / expected).sum()
    dof = grid_size ** 2 - 1
    p_value = 1 - stats.chi2.cdf(chi2, dof)
    passed = p_value > 0.05

    return {
        'observed': observed,
        'expected': expected,
        'chi_square': chi2,
        'p_value': p_value,
        'dof': dof,
        'passed': passed,
        'grid_size': grid_size
    }
## Funciones graficadoras

def printGraphics(normalizedNumbers, chiSquareResult):
    """
    Muestra un único gráfico de histograma con los resultados de la prueba chi-cuadrado.
    """
    import matplotlib.pyplot as plt

    bins = 100 # Aca esta la cantidad de intervalos que usas para la prueba chi cuadrado. Tiene que ser coincidente con el numero usado
    expected = len(normalizedNumbers) / bins

    fig, ax = plt.subplots(figsize=(10, 6))

    # Histograma
    ax.hist(normalizedNumbers, bins=bins, edgecolor='black', alpha=0.7)
    ax.set_title('Histograma de Números Aleatorios Normalizados')
    ax.set_xlabel('Valor')
    ax.set_ylabel('Frecuencia')
    
    # Línea de frecuencia esperada
    ax.axhline(y=expected, color='r', linestyle='-', label=f'Esperado: {expected:.1f}')
    
    # Cuadro con resultado de la prueba chi-cuadrado
    chi_text = f"Chi²: {chiSquareResult['chi_square']:.4f}\np-value: {chiSquareResult['p_value']:.4f}\n"
    chi_text += "Uniformidad: " + ("ACEPTADA" if chiSquareResult['passed'] else "RECHAZADA")
    ax.text(0.05, 0.95, chi_text, transform=ax.transAxes,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.legend()
    plt.tight_layout()
    plt.show()

    # Resultados detallados por consola
    print(f"Resultados del Test Chi-Cuadrado:")
    print(f"Estadístico Chi²: {chiSquareResult['chi_square']:.4f}")
    print(f"Valor p: {chiSquareResult['p_value']:.4f}")
    print(f"Grados de libertad: {chiSquareResult['dof']}")
    print(f"Resultado: {'Aceptado' if chiSquareResult['passed'] else 'Rechazado'} (α=0.05)")
    
    print("\nFrecuencias por intervalo:")
    print("-------------------------")
    print("Intervalo | Observado | Esperado")
    for i, (obs, exp) in enumerate(zip(chiSquareResult['observed'], [expected] * len(chiSquareResult['observed']))):
        print(f"{i/bins:.2f}-{(i+1)/bins:.2f}  | {obs:9d} | {exp:8.1f}")

    return 0

def printSeriesHeatmap(series_result):
    k = series_result['grid_size']
    observed = np.array(series_result['observed']).reshape((k, k))

    plt.figure(figsize=(8, 6))
    sns.heatmap(observed, annot=True, fmt='d', cmap='Blues')
    plt.title('Heatmap de Frecuencias Observadas en la Prueba de Series')
    plt.xlabel('Índice Y (X_{i+1})')
    plt.ylabel('Índice X (X_i)')
    plt.tight_layout()
    plt.show()

## Ejecución programa principal

startSimulation(quantityToGenerate,generator,seed)