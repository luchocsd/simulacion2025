import random
import secrets
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats


# Parámetros 

quantityToGenerate = 10000
generator = "CUADRADOS"

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
    runsTestResult = runs_test(normalizedNumbers)
    printRunsTest(runsTestResult)

    meanVarianceResult = mean_variance_test(normalizedNumbers)

    print("El resultado de la prueba de media y varianza es:", meanVarianceResult)

    return 0

## Funciones auxiliares

def generate(quantityToGenerate,generator, seed):

    if generator == "CUADRADOS":
        numbers, normalizedNumbers = cuadradosGenerator(quantityToGenerate, seed)
    
    elif generator == "GCL":
        numbers, normalizedNumbers = GCLGenerator(quantityToGenerate,seed)

    elif generator == "PYTHON":
        numbers,normalizedNumbers = randomPythonGenerator(quantityToGenerate)
    
    elif generator == "PYTHON_SECRETS":
        numbers,normalizedNumbers = randomPythonGeneratorWithSecrets(quantityToGenerate)

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
def mean_variance_test(normalizedNumbers, mean_tol=0.01, var_tol=0.005):
    """
    Verifica si el promedio y la varianza están dentro de un rango razonable
    de los valores esperados para una distribución uniforme en [0,1].
    No utiliza chi-cuadrado.
    """
    sample_mean = np.mean(normalizedNumbers)
    sample_var = np.var(normalizedNumbers)  # Por defecto, ddof=0: población

    expected_mean = 0.5
    expected_var = 1/12

    mean_passed = abs(sample_mean - expected_mean) <= mean_tol
    var_passed = abs(sample_var - expected_var) <= var_tol

    return {
        'mean': sample_mean,
        'expected_mean': expected_mean,
        'mean_tol': mean_tol,
        'mean_passed': mean_passed,
        'variance': sample_var,
        'expected_variance': expected_var,
        'var_tol': var_tol,
        'var_passed': var_passed,
        'passed': mean_passed and var_passed
    }


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

def runs_test(normalizedNumbers):
    """
    Realiza el test de corridas para verificar la aleatoriedad de una secuencia.
    Basado en la cantidad de veces que los números cruzan por encima y por debajo de la media.
    """

    median = 0.5  # Usamos 0.5 porque los números deberían ser uniformemente distribuidos

    # Convertimos la secuencia a una lista de signos: + si >= 0.5, - si < 0.5
    signs = ['+' if x >= median else '-' for x in normalizedNumbers]

    # Contar el número de corridas: una corrida es una secuencia de signos iguales
    runs = 1  # Siempre hay al menos una corrida
    for i in range(1, len(signs)):
        if signs[i] != signs[i - 1]:
            runs += 1

    n1 = signs.count('+')
    n2 = signs.count('-')

    # Verificaciones para evitar división por cero
    if n1 == 0 or n2 == 0:
        return {
            'runs': runs,
            'expected': None,
            'std_dev': None,
            'z_score': None,
            'p_value': 0.0,
            'passed': False
        }

    # Cálculo del valor esperado y desviación estándar bajo la hipótesis nula
    expected_runs = (2 * n1 * n2) / (n1 + n2) + 1
    std_dev_runs = np.sqrt((2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) /
                           (((n1 + n2) ** 2) * (n1 + n2 - 1)))

    # Estadístico Z
    z = (runs - expected_runs) / std_dev_runs
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))  # Prueba bilateral
    passed = p_value > 0.05

    return {
        'runs': runs,
        'expected': expected_runs,
        'std_dev': std_dev_runs,
        'z_score': z,
        'p_value': p_value,
        'passed': passed
    }

def printRunsTest(runsTestResult):
    print("\nResultados del Test de Corridas (Runs Test):")
    print("--------------------------------------------")
    print(f"Cantidad de corridas observadas: {runsTestResult['runs']}")
    print(f"Cantidad esperada de corridas: {runsTestResult['expected']:.2f}")
    print(f"Desviación estándar esperada: {runsTestResult['std_dev']:.2f}")
    print(f"Z-score: {runsTestResult['z_score']:.4f}")
    print(f"Valor p: {runsTestResult['p_value']:.4f}")
    print(f"Resultado: {'Aceptado' if runsTestResult['passed'] else 'Rechazado'} (α=0.05)")


## Generadores a comparar

def randomPythonGenerator(quantityToGenerate):
    numbers = []
    normalizedNumbers = []

    for _ in range(quantityToGenerate):
    
        x = random.uniform(0, 1)
        
        numbers.append(x)
        normalizedNumbers.append(x)
    
    return numbers, normalizedNumbers ## Devolvemos los 2 simplemente por consistencia 


def randomPythonGeneratorWithSecrets(quantityToGenerate):
    numbers = []
    normalizedNumbers = []

    for _ in range(quantityToGenerate):
        # Generamos un número aleatorio entre 0 y 1 utilizando secrets
        x = secrets.randbelow(2**32)  # Genera un número aleatorio en el rango [0, 2^32)
        
        # Normalizamos el número a [0, 1]
        normalized_x = x / float(2**32)
        
        numbers.append(x)
        normalizedNumbers.append(normalized_x)
    
    return numbers, normalizedNumbers



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
    
    # Crear etiquetas para los ejes con intervalos reales
    interval_labels = [f"{i/k:.1f}-{(i+1)/k:.1f}" for i in range(k)]
    
    plt.figure(figsize=(10, 8))
    
    # Crear el heatmap con etiquetas mejoradas
    ax = sns.heatmap(observed, annot=True, fmt='d', cmap='Blues',
                     xticklabels=interval_labels, 
                     yticklabels=interval_labels)
    
    # Invertir el eje Y para que la visualización sea más intuitiva (0 arriba)
    plt.gca().invert_yaxis()
    
    # Mejorar el etiquetado
    plt.title('Prueba de Series: Distribución de Pares Consecutivos', fontsize=14)
    plt.xlabel('Valor del número X_{i+1} (segundo en el par)', fontsize=12)
    plt.ylabel('Valor del número X_i (primero en el par)', fontsize=12)
    
    
    plt.tight_layout()
    plt.show()
    


## Ejecución programa principal

startSimulation(quantityToGenerate,generator,seed)