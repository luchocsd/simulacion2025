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
def martingalaRefactor(tiradas,numeroElegido,capitalInicial):
    
    frecuenciasRelativas = []  # evolución de frecuencia relativa
    capitales = []    # evolución del capital
    bancaRotaBandera = False
  
    apuestaActual = 1 # Se empieza apostando 1 unidad monetaria
    frecuenciaAbsolutaActual = 0
    capitalActual = capitalInicial

    print(f"Inicio martingala con capital: {capitalActual}")

    for x in range(0,tiradas):

      bancaRotaBandera =  estoyEnBancarrota(apuestaActual,capitalActual) # Puede pasar que no estas en 0, pero la apuestaActual supera a tu capital. Se entiende que es una banca rota de lo contrario seria una martingala variable.
      if (bancaRotaBandera == False):

        resultadoTirada=random.randint(0,36)
        if (resultadoTirada == numeroElegido):
          capitalActual = capitalActual + (apuestaActual * 36)
          capitales.append(capitalActual)
          frecuenciaAbsolutaActual = frecuenciaAbsolutaActual + 1
          frecuenciasRelativas.append(frecuenciaAbsolutaActual / (x + 1))


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
  if apuestaActual > capitalActual:
    return True
  else: 
    return False



def startSimulation(corridas,tiradas,numeroElegido,estrategia,tipoCapital):
 # Por simplicidad, si hay una bancarrota termina la corrida
 # Pendiente implementar tipoCapital infinito, se trabaja con capital finito actualmente

  bancaRotas = 0
  capitalesCorridas = [] 
  frecuenciasRelativasCoridas = []
  for j in range(0,corridas):

    if estrategia == "m":
      frecuenciasRelativas, capitales, bancaRotaBandera = martingalaRefactor(tiradas,numeroElegido,CAPITAL_CONSTANTE) # Devuelve array evolucionFrecuenciasRelativas, array evolucionCapital, y una bandera de bancarrota.

    if estrategia == "f":
      print("Hola Mundo")

    if estrategia == "d":
      print("Hola mundo")

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