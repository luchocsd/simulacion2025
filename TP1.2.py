import random
import sys
import matplotlib.pyplot as plt
import numpy as np

# PENDIENTES
# desarrollar las 4 estrategias (D'Alambert, Fibonacci y otra estrategia a elección del grupo)
# codificar alguna manera mas entendible para analizar los resultados y bancarrotas POR CONSOLA
# generar los graficos de cada estrategia y compararlos entre si



#Ejemplo para usar el programa (20 tiradas, 5 corridas y numero elegido 22, estrategia martingala, capital finito):
#   python TP1.2.py -c 20 -n 5 -e 22 -s m -a f
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

CAPITAL_CONSTANTE = 200


""""
#Array bidimensional, con todos los resultados de cada ruleta, de cada corrida
resultados = [[0 for i in range(tiradas)] for j in range(corridas)]

#Array con la cantidad de veces por ciclo que aparece el numero elegido
frecuencias = [0 for i in range(corridas)]

print("Tiradas: ", tiradas)
print("Corridas: ", corridas)
print("Número elegido: ", numeroElegido)
"""
""""
# calcula la frecuencia relativa del numero elegido despues de cada girada de ruleta y lo appendea
def f_rel_por_tirada(numeroElegido,resultados):
  frecuencia_absoluta = 0
  numero_tirada = 0
  frecuencias_relativas_por_tirada = []
  for numero in resultados:
      numero_tirada += 1
      if numeroElegido == numero:
          frecuencia_absoluta += 1
      frecuencia_relativa = frecuencia_absoluta / numero_tirada
      frecuencias_relativas_por_tirada.append(frecuencia_relativa)  
  return frecuencias_relativas_por_tirada

#estrategia martingala
def martingala(resultadoTirada, capital, tipoCapital):
  if tipoCapital == "f":
    if resultadoTirada == numeroElegido:
      capital += 36 
    else:
      capital -= 1
      multiplo = multiplo + 1 
  elif tipoCapital == "i":
    if resultadoTirada == numeroElegido:
      capital += 36
    else:
      capital -= 1
  return capital
"""
def martingalaStrategy(tiradas,numeroElegido,capitalInicial):
    
    frecuenciasRelativas = []  # evolución de frecuencia relativa
    capitales = []    # evolución del capital
    bancaRotaBandera = False
  
    apuestaActual = 1 # Se empieza apostando 1 unidad monetaria
    frecuenciaAbsolutaActual = 0
    capitalActual = capitalInicial


    for x in range(0,tiradas):

      bancaRotaBandera =  estoyEnBancarrota(apuestaActual,capitalActual) # Puede pasar que no estas en 0, pero la apuestaActual supera a tu capital. Se entiende que es una banca rota de lo contrario seria una martingala variable.
      if (bancaRotaBandera == False):

        resultadoTirada=random.randint(0,36)
        if (resultadoTirada == numeroElegido):
          capitalActual = capitalActual + (apuestaActual * 36)
          frecuenciaAbsolutaActual = frecuenciaAbsolutaActual + 1
          apuestaActual = 1 # Se reinicia la apuesta despues de ganar

        else:
          capitalActual = capitalActual - apuestaActual
          apuestaActual = apuestaActual * 2

        capitales.append(capitalActual)
        frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))
      
      else:
        return frecuenciasRelativas, capitales, bancaRotaBandera # Es innecesario este else, podria usarse el return de afuera.

    return frecuenciasRelativas, capitales, bancaRotaBandera

def estoyEnBancarrota(apuestaActual, capitalActual):

  return apuestaActual > capitalActual

def dalembertStrategy(tiradas,numeroElegido,capitalInicial):
    
  frecuenciasRelativas = []  
  capitales = []   
  bancaRotaBandera = False

  apuestaActual = 1 # Se empieza apostando 1 unidad monetaria
  frecuenciaAbsolutaActual = 0
  capitalActual = capitalInicial

  for x in range(0,tiradas):

    bancaRotaBandera =  estoyEnBancarrota(apuestaActual,capitalActual) 
    if (bancaRotaBandera == False):

      resultadoTirada=random.randint(0,36)
      if (resultadoTirada == numeroElegido):
        capitalActual = capitalActual + (apuestaActual * 36)
        frecuenciaAbsolutaActual = frecuenciaAbsolutaActual + 1

        if(apuestaActual != 1):
          apuestaActual = apuestaActual - 1
        ## En la dalembert se baja 1 UM si se gano. Si ya estamos apostando lo minimo, 1 UM no bajamos. 

      else:
        capitalActual = capitalActual - apuestaActual
        apuestaActual = apuestaActual + 1
 

      capitales.append(capitalActual)
      frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))

    else:
     return frecuenciasRelativas, capitales, bancaRotaBandera # Es innecesario este else, podria usarse el return de afuera.
    
  return frecuenciasRelativas, capitales, bancaRotaBandera


def fibonacciStrategy(tiradas,numeroElegido,capitalInicial):
  frecuenciasRelativas = []  
  capitales = []   
  bancaRotaBandera = False

  frecuenciaAbsolutaActual = 0
  capitalActual = capitalInicial

  ## Propio de fibonacci
  ## Construimos la secuencia de fibonacci de forma dinamica 
  secuencia = [1, 1]
  indice = 0

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

        indice = max(indice - 2, 0) # Usar max evita tener que usar if. Se retrocede 2 numeros en la secuencia, o se vuelve a la primer posición si se llegase a una posicion inexistente (-1)

      else:
        capitalActual = capitalActual - apuestaActual
        indice = indice + 1
 

      capitales.append(capitalActual)
      frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))



  return frecuenciasRelativas, capitales, bancaRotaBandera

def martingalaCustomStrategy(tiradas,color,capitalInicial):
  frecuenciasRelativas = []  
  capitales = []   
  bancaRotaBandera = False

  apuestaActual = 1 # Se empieza apostando 1 unidad monetaria
  frecuenciaAbsolutaActual = 0
  capitalActual = capitalInicial

 ## Constantes de la martingalaCustom. podrian pedirse como parámetro.

  if color == "ROJO":
      colorApuesta = 0
  elif color == "NEGRO":
      colorApuesta = 1

  cantidadEsperas = 3

  ## Inicialización 
  cantidadColorNoDeseado = 0
  jugarEstaTirada = False

  for x in range(0,tiradas):

    jugarEstaTirada = (cantidadColorNoDeseado == cantidadEsperas) # Si ya esperaste que saliera 3 veces el color no jugado, se juega el color jugado.
    bancaRotaBandera =  estoyEnBancarrota(apuestaActual,capitalActual) 
    
    if (bancaRotaBandera == False):

      resultadoTirada=random.randint(0,36)
      colorTirada = getColor(resultadoTirada)

      if colorTirada == colorApuesta and jugarEstaTirada == True: ## Ganar
         
        capitalActual = capitalActual + (apuestaActual * 2)
        frecuenciaAbsolutaActual = frecuenciaAbsolutaActual + 1
        apuestaActual = 1
        cantidadColorNoDeseado = 0
      
      if colorTirada == colorApuesta and jugarEstaTirada == False: ## Se corta la racha de espera
         
        frecuenciaAbsolutaActual = frecuenciaAbsolutaActual + 1
        cantidadColorNoDeseado = 0

      if colorTirada != colorApuesta and jugarEstaTirada == True: ## Perder 
         
        capitalActual = capitalActual - apuestaActual
        apuestaActual = apuestaActual * 2
        cantidadColorNoDeseado = 0
       
      if colorTirada != colorApuesta and jugarEstaTirada == False: ## Racha de espera 
         
         cantidadColorNoDeseado = cantidadColorNoDeseado + 1
         
      if colorTirada == 2: ## Se corta la racha de espera por 0
         
         cantidadColorNoDeseado = 0 # Si sale 0 se reinicia el contador porque es imposible que sea el color desado.

      capitales.append(capitalActual)
      frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))

    
    else:
      return frecuenciasRelativas, capitales, bancaRotaBandera # Es innecesario este else, podria usarse el return de afuera.

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




def startSimulation(corridas,tiradas,numeroElegido,estrategia,tipoCapital):
 # Por simplicidad, si hay una bancarrota termina la corrida
 # Pendiente implementar tipoCapital infinito, se trabaja con capital finito actualmente

  bancaRotas = 0
  capitalesCorridas = [] 
  frecuenciasRelativasCoridas = []
  for j in range(0,corridas):

    if estrategia == "m":
      frecuenciasRelativas, capitales, bancaRotaBandera = martingalaStrategy(tiradas,numeroElegido,CAPITAL_CONSTANTE) # Devuelve array evolucionFrecuenciasRelativas, array evolucionCapital, y una bandera de bancarrota.

    if estrategia == "d":
      frecuenciasRelativas, capitales, bancaRotaBandera = dalembertStrategy(tiradas,numeroElegido,CAPITAL_CONSTANTE)

    if estrategia == "f":
      frecuenciasRelativas, capitales, bancaRotaBandera = fibonacciStrategy(tiradas,numeroElegido,CAPITAL_CONSTANTE)

    if estrategia == "c":
       frecuenciasRelativas, capitales, bancaRotaBandera = martingalaCustomStrategy(tiradas,"NEGRO",CAPITAL_CONSTANTE)

  # Codigo independiente a la estrategia

    # Las bancarotas son visuales en el sentido de que se interrumpe la linea de la corrida.
    if (bancaRotaBandera == True):
        bancaRotas = bancaRotas + 1
        bancaRotaBandera = False

    capitalesCorridas.append(capitales)
    frecuenciasRelativasCoridas.append(frecuenciasRelativas)


  # Imprimimos estadísticas
  print(f"Cantidad de bancas rotas: {bancaRotas} de {corridas}")
  print(f"Evolucion de capital en cada corrida:{capitalesCorridas}")
  print(f"Evolucion de frecuencia relativa en cada corrida:{frecuenciasRelativasCoridas}")

    
  # Gráficos


  return 0

## PROGRAMA PRINCIPAL

startSimulation(corridas,tiradas,numeroElegido,estrategia,tipoCapital)



"""""
# calculo de resultados, promedios y frecuencia de aparicion de nuestro numero elegido 
for j in range(0, corridas):
  frecuencia = 0
  bancaRota = 0
  for i in range(0, tiradas):
    resultadoTirada=random.randint(0,36)
    print("Capital: ", capital)
    if estrategia == "m":
      capital=martingala(resultadoTirada, capital, tipoCapital)
    # elif estrategia == "d":
    #   d_alambert(resultadoTirada, capital, tipoCapital)
    # elif estrategia == "f":
    #   fibonacci(resultadoTirada, capital, tipoCapital)
    # elif estrategia == "o":
    #   otra_estrategia(resultadoTirada, capital, tipoCapital)
    if capital == 0:
      capital = 10
      bancaRota += 1
    resultados[j][i] = resultadoTirada
    if(resultados[j][i] == numeroElegido):
      frecuencia +=1
  print("Banca rota en corrida ",[j],": ", bancaRota)
  frecuencias[j] = frecuencia
  capital = 10

print("Resultados: ", resultados)
print("Frecuencia absoluta de num elegido por corrida: ", frecuencias)
"""

# x1= list(range(1,tiradas+1))
# cmap = plt.cm.get_cmap("hsv",corridas)
# figura, lista_graficos = plt.subplots(nrows=2, ncols=2, figsize=(18, 6))
# lista_graficos[0,0].plot(x1,label='Frecuencia relativa teórica',linestyle='--',color='blue')
# lista_graficos[0,1].plot(x1,label='Promedio teórico',linestyle='--',color='blue')
# lista_graficos[1,0].plot(x1,label='Desviación estándar teórica',linestyle='--',color='blue')
# lista_graficos[1,1].plot(x1,label='Varianza teórica',linestyle='--',color='blue')
# for i in range(corridas):
#   color = list(np.random.choice(range(256), size=3)) 
#   #grafico de frecuencia relativa
#   lista_graficos[0,0].plot(x1, f_rel_por_tirada(numeroElegido,resultados[i]), color=cmap(i))
#   lista_graficos[0,0].set_xlabel('Número de tirada')
#   lista_graficos[0,0].set_ylabel('Frecuencia relativa')
#   lista_graficos[0,0].set_title('Frecuencia relativa por tiradas')
#   lista_graficos[0,0].set_yticks(np.linspace(0, 1, 11))
#   lista_graficos[0,0].legend()
#   lista_graficos[0,0].grid(True)
#   #grafico de promedio por tiradas
#   lista_graficos[0,1].plot(x1, color=cmap(i))
#   lista_graficos[0,1].set_xlabel('Número de tirada')
#   lista_graficos[0,1].set_ylabel('Número')
#   lista_graficos[0,1].set_title('Promedio por tiradas')
#   lista_graficos[0,1].legend()
#   lista_graficos[0,1].grid(True)
#   #grafico de desviacion estandar por tiradas
#   lista_graficos[1,0].plot(x1, color=cmap(i))
#   lista_graficos[1,0].set_xlabel('Número de tirada')
#   lista_graficos[1,0].set_ylabel('Número')
#   lista_graficos[1,0].set_title('Desviación estandar por tiradas')
#   lista_graficos[1,0].legend()
#   lista_graficos[1,0].grid(True)
#   #grafico de varianza calculada por tiradas
#   lista_graficos[1, 1].plot(x1,color=cmap(i))
#   lista_graficos[1,1].set_xlabel('Número de tirada')
#   lista_graficos[1, 1].set_ylabel('Valor de varianza')
#   lista_graficos[1, 1].set_title('Varianza por tiradas')
#   lista_graficos[1, 1].legend()
#   lista_graficos[1, 1].grid(True)

# plt.tight_layout()
# plt.show()

