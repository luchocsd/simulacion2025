import random

# Pendientes
# 1 - Programar el ingreso de parametros por consola



# Parámetros por consola

quantityToGenerate = 100
generator = "GCL"

seed = 3429813481 #Opcional pero requiere seedSize en su lugar 
seedSizeParam = 4 #Opcional, se usa cuando no hay seed


def startSimulation(quantityToGenerate, generator, seed = None,seedSizeParam = None):

    # Inicializar resultados de las pruebas
    chiCuadrado = False


    if seed is None:
        
        seed = generateSeed(seedSizeParam)

    
    generatedNumbers, normalizedNumbers = generate(quantityToGenerate,generator, seed)

    


    printGraphics(generatedNumbers,normalizedNumbers)

    return 0


def generate(quantityToGenerate,generator, seed):

    if generator == "CUADRADOS":
        numbers, normalizedNumbers = cuadradosGenerator(quantityToGenerate, seed)
    
    elif generator == "GCL":
        numbers, normalizedNumbers = GCLGenerator(quantityToGenerate,seed)

    return numbers, normalizedNumbers


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


def obtainMiddleDigits(number,seedSize):

    num_str = str(number).zfill(2 * seedSize) ## Rellenar de ceros a la izquierda hasta tener un numero de tantos digitos como el doble de la semilla. 
    

    length = len(num_str)
    
    if length <= seedSize:
        return number
    
    initialPosition = (length - seedSize) // 2
    
    # Extraer los N(seedSize) dígitos del medio dando prioridad a la izquierda
    middleDigits = int(num_str[initialPosition:initialPosition + seedSize])
    
    return middleDigits

def printGraphics(generatedNumbers,normalizedNumbers):

    print(generatedNumbers,normalizedNumbers)

    return 0


def generateSeed(seedSizeParam):

    lower_limit = 10**(seedSizeParam-1)  # Primer número con seedSize dígitos
    upper_limit = (10**seedSizeParam) - 1  # Último número con seedSize dígitos
        
    seed = random.randint(lower_limit, upper_limit)
    print(f"Semilla generada automáticamente: {seed}")

    return seed



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


startSimulation(quantityToGenerate,generator,seed)