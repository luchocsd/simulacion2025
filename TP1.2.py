import random
import sys
import matplotlib.pyplot as plt
import numpy as np



#Ejemplo para usar el programa (20 tiradas, 5 corridas y numero elegido 22, estrategia martingala, capital finito):
#   python TP1.2.py -c 50 -n 5 -e 10 -s m -a f
if len(sys.argv) != 11 or sys.argv[1] != "-c" or sys.argv[3] != "-n" or sys.argv[5] != "-e" or sys.argv[7] != "-s" or sys.argv[9] != "-a":
  print("Uso: python TP1.2.py -c XXX -n YYY -e ZZ -s WW -a XX (cantidad de tiradas, corridas, número elegido, estrategia y capital)")
  sys.exit(1)

# Cantidad de veces que gira la ruleta en una corrida
tiradas = int(sys.argv[2])

# Cantidad de veces que se repite el ciclo de tiradas
corridas = int(sys.argv[4])

# Numero que se busca en el ciclo de tiradas
numeroElegido = int(sys.argv[6])

# Estrategia elegida m (martingala), d (D’Alambert), f (Fibonacci) y o (otra estrategia a elección del grupo)
estrategia = sys.argv[8]

# Tipo de capital, finito f o infinito i
tipoCapital = sys.argv[10]

# Capital  inicial CONSTANTE no ingresada por el usuario
CAPITAL_CONSTANTE = 500

def estoyEnBancarrota(apuestaActual, capitalActual):
  if tipoCapital == "f":
    return apuestaActual > capitalActual 
  else: 
    return False # Si el capital es infinito, nunca se considera en bancarrota.

def estrategiaMartingala(tiradas,numeroElegido,capitalInicial):
  # La estrategia de la martingala consiste en duplicar la apuesta cada vez que se pierde, 
  # y volver a la apuesta inicial cuando se gana.
  frecuenciasRelativas = []  # evolución de frecuencia relativa
  capitales = []    # evolución del capital
  bancaRotaBandera = False
  apuestaActual = 1 # Se empieza apostando 1 unidad monetaria
  frecuenciaAbsolutaActual = 0
  capitalActual = capitalInicial

  capitales.append(capitalActual)
  for x in range(0,tiradas):
    bancaRotaBandera =  estoyEnBancarrota(apuestaActual,capitalActual) 
    # Puede pasar que no estas en 0, pero la apuestaActual supera a tu capital. 
    # Se entiende que es una banca rota de lo contrario seria una martingala variable.
    if (bancaRotaBandera == False):
      resultadoTirada=random.randint(0,36)

      if (resultadoTirada == numeroElegido):
        capitalActual = capitalActual + (apuestaActual * 36)
        frecuenciaAbsolutaActual = frecuenciaAbsolutaActual + 1
        apuestaActual = 1 # Se reinicia la apuesta despues de ganar

      else:
        capitalActual = capitalActual - apuestaActual
        apuestaActual = apuestaActual * 2

    else:
      capitales.append(capitalActual-apuestaActual)
      frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))
      return frecuenciasRelativas, capitales, bancaRotaBandera # Para evitar repeticiones innecesarias
    
    capitales.append(capitalActual)
    frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))
  return frecuenciasRelativas, capitales, bancaRotaBandera

def estrategiaDalembert(tiradas,numeroElegido,capitalInicial):
  # La estrategia de D'Alembert consiste en aumentar la apuesta en 1 unidad monetaria cuando se pierde
  #  y disminuirla en 1 unidad monetaria cuando se gana.
  frecuenciasRelativas = []  
  capitales = []   
  bancaRotaBandera = False
  apuestaActual = 1 # Se empieza apostando 1 unidad monetaria
  frecuenciaAbsolutaActual = 0
  capitalActual = capitalInicial

  capitales.append(capitalActual)
  for x in range(0,tiradas):
    bancaRotaBandera =  estoyEnBancarrota(apuestaActual,capitalActual) 
    
    if (bancaRotaBandera == False):
      resultadoTirada=random.randint(0,36)

      if (resultadoTirada == numeroElegido):
        capitalActual = capitalActual + (apuestaActual * 36)
        frecuenciaAbsolutaActual = frecuenciaAbsolutaActual + 1

        if(apuestaActual != 1):
          apuestaActual = apuestaActual - 1
        # si ya estamos apostando lo minimo, 1 UM no bajamos. 

      else:
        capitalActual = capitalActual - apuestaActual
        apuestaActual = apuestaActual + 1

    else:
      capitales.append(capitalActual-apuestaActual)
      frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))
      return frecuenciasRelativas, capitales, bancaRotaBandera # Para evitar repeticiones innecesarias

    capitales.append(capitalActual)
    frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))
  return frecuenciasRelativas, capitales, bancaRotaBandera

def estrategiaFibonacci(tiradas,numeroElegido,capitalInicial):
  # La estrategia de Fibonacci consiste en aumentar la apuesta siguiendo la secuencia de Fibonacci
  #  y retroceder dos posiciones en la secuencia cuando se gana.
  frecuenciasRelativas = []  
  capitales = []   
  bancaRotaBandera = False
  frecuenciaAbsolutaActual = 0
  capitalActual = capitalInicial

  # Propio de fibonacci
  # Construimos la secuencia de fibonacci de forma dinamica 
  secuencia = [1, 1]
  indice = 0

  capitales.append(capitalActual)
  for x in range(0,tiradas):
    if indice + 1 >= len(secuencia):
      nuevoTermino = secuencia[-1] + secuencia[-2]
      secuencia.append(nuevoTermino) 

    apuestaActual = secuencia[indice] 
    bancaRotaBandera =  estoyEnBancarrota(apuestaActual,capitalActual) 

    if (bancaRotaBandera == False):
      resultadoTirada=random.randint(0,36)

      if (resultadoTirada == numeroElegido):
        capitalActual = capitalActual + (apuestaActual * 36)
        frecuenciaAbsolutaActual = frecuenciaAbsolutaActual + 1
        indice = max(indice - 2, 0) 
        # Se retrocede 2 numeros en la secuencia, o se vuelve a la primer posición si se llegase a una posicion inexistente (-1)

      else:
        capitalActual = capitalActual - apuestaActual
        indice = indice + 1

    else:
      capitales.append(capitalActual-apuestaActual)
      frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))
      return frecuenciasRelativas, capitales, bancaRotaBandera # Para evitar repeticiones innecesarias

    capitales.append(capitalActual)
    frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))
  return frecuenciasRelativas, capitales, bancaRotaBandera

def estrategiaMartingalaPersonalizada(tiradas,color,capitalInicial):
  frecuenciasRelativas = []  
  capitales = []   
  bancaRotaBandera = False
  apuestaActual = 1 # Se empieza apostando 1 unidad monetaria
  frecuenciaAbsolutaActual = 0
  capitalActual = capitalInicial

  # Constantes de la martingalaPersonalizada
  if color == "ROJO":
    colorApuesta = 0

  elif color == "NEGRO":
    colorApuesta = 1

  cantidadEsperas = 3
  # Inicialización 
  cantidadColorNoDeseado = 0
  jugarEstaTirada = False

  capitales.append(capitalActual)
  for x in range(0,tiradas):
    jugarEstaTirada = (cantidadColorNoDeseado == cantidadEsperas) 
    # Si ya esperaste que saliera 3 veces el color no jugado, se juega el color jugado.
    bancaRotaBandera =  estoyEnBancarrota(apuestaActual,capitalActual) 
    if (bancaRotaBandera == False):
      resultadoTirada=random.randint(0,36)
      colorTirada = getColor(resultadoTirada)

      if colorTirada == colorApuesta and jugarEstaTirada == True: # Ganar
        capitalActual = capitalActual + (apuestaActual * 2)
        frecuenciaAbsolutaActual = frecuenciaAbsolutaActual + 1
        apuestaActual = 1
        cantidadColorNoDeseado = 0
      
      if colorTirada == colorApuesta and jugarEstaTirada == False: # Se corta la racha de espera
        frecuenciaAbsolutaActual = frecuenciaAbsolutaActual + 1
        cantidadColorNoDeseado = 0

      if colorTirada != colorApuesta and jugarEstaTirada == True: # Perder 
        capitalActual = capitalActual - apuestaActual
        apuestaActual = apuestaActual * 2
        cantidadColorNoDeseado = 0

      if colorTirada != colorApuesta and jugarEstaTirada == False: # Racha de espera 
        cantidadColorNoDeseado = cantidadColorNoDeseado + 1

      if colorTirada == 2: # Se corta la racha de espera por 0
        cantidadColorNoDeseado = 0 # Si sale 0 se reinicia el contador porque es imposible que sea el color desado.

    else:
      capitales.append(capitalActual-apuestaActual)
      frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))
      return frecuenciasRelativas, capitales, bancaRotaBandera # Para evitar repeticiones innecesarias

    capitales.append(capitalActual)
    frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))
  return frecuenciasRelativas, capitales, bancaRotaBandera

def getColor(numero):
  rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
  negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

  if numero == 0:
    return 2  # Verde
  elif numero in rojos:
    return 0  # Rojo
  elif numero in negros:
    return 1  # Negro

def printGraphics(frecuenciasRelativas, capitales, capitalInicial, corridas, tipoCapital):
  cmap = plt.cm.get_cmap("hsv", (corridas+1))
  figura, lista_graficos = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

  if tipoCapital != "i":
    lista_graficos[1].axhline(y=capitalInicial, color='black', linestyle='--',label='Capital inicial')

  for x in range(corridas):
    # Usar la longitud real de cada corrida. No usar el numero de tiradas para iterar porque puede haber corridas mas cortas por bancarrota.
    # y daria error
    longitud_real_capitales = len(capitales[x])
    longitud_real_frecuencias = len(frecuenciasRelativas[x])
    ejeX_corrida_capitales = list(range(longitud_real_capitales))
    ejeX_corrida_frecuencias = list(range(1, longitud_real_frecuencias+1))

    lista_graficos[0].plot(ejeX_corrida_frecuencias, frecuenciasRelativas[x], color=cmap(x), label=f'Corrida {x}')
    lista_graficos[1].plot(ejeX_corrida_capitales, capitales[x], color=cmap(x), label=f'Corrida {x}')

  lista_graficos[0].set_xlabel('Número de tirada')
  lista_graficos[0].set_ylabel('Frecuencia relativa')
  lista_graficos[0].set_title('Frecuencia relativa')
  lista_graficos[0].set_yticks(np.linspace(0, 1, 11))
  lista_graficos[0].set_xticks(range(1,tiradas+1,100))
  lista_graficos[0].legend()
  lista_graficos[0].grid(True)
  
  lista_graficos[1].set_xlabel('Número de tirada')
  lista_graficos[1].set_ylabel('Capital actual')
  lista_graficos[1].set_title('Flujo de caja')
  lista_graficos[1].legend()
  lista_graficos[1].grid(True)
  
  plt.tight_layout()
  plt.show()
  return 0

def startSimulation(corridas,tiradas,numeroElegido,estrategia,tipoCapital):
  # Por simplicidad, si hay una bancarrota termina la corrida
  global CAPITAL_CONSTANTE
  bancaRotas = 0
  capitalesCorridas = [] 
  frecuenciasRelativasCorridas = []
# if tipoCapital == "i":
#    CAPITAL_CONSTANTE = 100000000000000000

  for j in range(0,corridas):
    if estrategia == "m":
      frecuenciasRelativas, capitales, bancaRotaBandera = estrategiaMartingala(tiradas,numeroElegido,CAPITAL_CONSTANTE)

    if estrategia == "d":
      frecuenciasRelativas, capitales, bancaRotaBandera = estrategiaDalembert(tiradas,numeroElegido,CAPITAL_CONSTANTE)

    if estrategia == "f":
      frecuenciasRelativas, capitales, bancaRotaBandera = estrategiaFibonacci(tiradas,numeroElegido,CAPITAL_CONSTANTE)

    if estrategia == "c":
      frecuenciasRelativas, capitales, bancaRotaBandera = estrategiaMartingalaPersonalizada(tiradas,"NEGRO",CAPITAL_CONSTANTE)

    # Codigo independiente a la estrategia
    # Las bancarotas son visuales en el sentido de que se interrumpe la linea de la corrida.
    if (bancaRotaBandera == True):
      bancaRotas = bancaRotas + 1
      bancaRotaBandera = False

    capitalesCorridas.append(capitales)
    frecuenciasRelativasCorridas.append(frecuenciasRelativas)

  # Imprimimos estadísticas
  print(f"Cantidad de corridas: {corridas}")
  print(f"Cantidad de tiradas: {tiradas}")
  print(f"Numero elegido: {numeroElegido}")
  print(f"Estrategia elegida: {estrategia}")
  print(f"Tipo de capital: {tipoCapital}")
  print(f"Capital inicial: {CAPITAL_CONSTANTE}")
  print(f"Cantidad de bancas rotas: {bancaRotas} de {corridas}")
  print(f"Evolucion de capital en cada corrida:{capitalesCorridas}")
  print(f"Evolucion de frecuencia relativa en cada corrida:{frecuenciasRelativasCorridas}")
  with open("simulation_results.txt", "w") as file:
    file.write(f"Cantidad de corridas: {corridas}\n")
    file.write(f"Cantidad de tiradas: {tiradas}\n")
    file.write(f"Numero elegido: {numeroElegido}\n")
    file.write(f"Estrategia elegida: {estrategia}\n")
    file.write(f"Tipo de capital: {tipoCapital}\n")
    file.write(f"Capital inicial: {CAPITAL_CONSTANTE}\n")
    file.write(f"Cantidad de bancas rotas: {bancaRotas} de {corridas}\n")
    file.write(f"Evolucion de capital en cada corrida: {capitalesCorridas}\n")
    file.write(f"Evolucion de frecuencia relativa en cada corrida: {frecuenciasRelativasCorridas}\n")

  # Gráficos
  printGraphics(frecuenciasRelativasCorridas,capitalesCorridas,CAPITAL_CONSTANTE,corridas,tipoCapital)
  return 0

startSimulation(corridas,tiradas,numeroElegido,estrategia,tipoCapital)
