#Ejemplo para usar el programa (20 tiradas, 5 corridas y numero elegido 22):  python TP1.1.py -c 20 -n 5 -e 22

#IMPORTANTE!! Funciona con una version mas vieja de matpolib, la 3.7.3 (pip install matplotlib==3.7.3)

import random
import sys
import matplotlib.pyplot as plt
import numpy as np

VALORES_BASES = list(range(37))  #Todos los posibles valores de la ruleta


def calcular_numero_promedio_por_tirada(valoresAleatorios):
    numeroDeTirada = 0
    suma = 0
    promedios = []
    for numero in valoresAleatorios:
        numeroDeTirada += 1
        suma = suma + numero
        promedio = int(suma / numeroDeTirada)
        promedios.append(promedio)
    return promedios


def calcular_promedio_esperado(numeroDeTiradas):
    suma = 0
    promedio_esperado_recta = []
    for valor in range(37):
        suma += valor
    promedio_esperado = suma / 37
    for _ in range(numeroDeTiradas):
        promedio_esperado_recta.append(promedio_esperado)
    return promedio_esperado_recta


def calcular_frecuencia_relativa_esperada(numeroDeTiradas):
    frecuencia_relativa_esperada = 1 / 37
    frecuencias_relativa_recta = []
    for _ in range(numeroDeTiradas):
        frecuencias_relativa_recta.append(frecuencia_relativa_esperada)
    return frecuencias_relativa_recta


def calcular_frecuencias_relativas_por_tiradas(numeroElegido,valoresAleatorios):
    frecuencia_absoluta = 0
    numero_tirada = 0
    frecuencias_relativas_por_tirada = []
    for numero in valoresAleatorios:
        numero_tirada += 1
        if numeroElegido == numero:
            frecuencia_absoluta += 1
        frecuencia_relativa = frecuencia_absoluta / numero_tirada
        frecuencias_relativas_por_tirada.append(frecuencia_relativa)  
    return frecuencias_relativas_por_tirada


def calcular_desviacion_estandar_por_tirada(valoresAleatorios, numeroElegido):
    desviaciones_por_tirada = []
    for i in range(1, len(valoresAleatorios) + 1):
        valores_tirada = np.array(valoresAleatorios[:i])
        desviacion = np.std(valores_tirada)
        desviaciones_por_tirada.append(desviacion)
    return desviaciones_por_tirada


def calcular_desviacion_estandar_esperada(tiradas):
    desviacion_estandar_esperada = ((((VALORES_BASES[-1] - VALORES_BASES[0] + 1)**2) - 1) / 12)**0.5
    desviacion_estandar_recta = []
    for _ in range(tiradas):
        desviacion_estandar_recta.append(desviacion_estandar_esperada)
    return desviacion_estandar_recta


def calcular_varianza_esperada(tiradas):
    varianza_esperada = (((VALORES_BASES[-1] - VALORES_BASES[0] + 1)**2) - 1) / 12
    varianza_recta = []
    for _ in range(tiradas):
        varianza_recta.append(varianza_esperada)
    return varianza_recta


def calcular_varianza_calculada( valoresAleatorios, numeroDeTiradas):
    promedio = calcular_promedio_esperado(numeroDeTiradas)
    valores_aleatorios = np.array(valoresAleatorios)
    varianzas_calculadas = []
    for i in range(1, numeroDeTiradas + 1):
        diferencias_cuadradas = (valores_aleatorios[:i] - promedio[-1]) ** 2
        varianza_calculada = np.mean(diferencias_cuadradas)
        varianzas_calculadas.append(varianza_calculada)
    return varianzas_calculadas


if len(sys.argv) != 7 or sys.argv[1] != "-c" or sys.argv[3] != "-n" or sys.argv[5] != "-e":
  print("Uso: python TP1.1.py -c XXX -n YYY -e ZZ (cantidad de tiradas, corridas y número elegido)")
  sys.exit(1)

# Cantidad de veces que gira la ruleta en una corrida
tiradas = int(sys.argv[2])

# Cantidad de veces que se repite el ciclo de tiradas
corridas = int(sys.argv[4])

# Numero que se busca en el ciclo de tiradas
numeroElegido = int(sys.argv[6])

#Array bidimensional, con todos los resultados de cada ruleta, de cada corrida
resultados = [[0 for i in range(tiradas)] for j in range(corridas)]

#Array con los promedios de cada ciclo 
promedios = [0 for i in range(corridas)]

#Array con la cantidad de veces por ciclo que aparece el numero elegido
frecuencias = [0 for i in range(corridas)]

print("Tiradas: ", tiradas)
print("Corridas: ", corridas)
print("Número elegido: ", numeroElegido)

for j in range(0, corridas):
    suma = 0
    frecuencia = 0
    for i in range(0, tiradas):
      resultados[j][i] = random.randint(0,36)
      suma+= resultados[j][i]
      if(resultados[j][i] == numeroElegido):
        frecuencia +=1
    promedios[j]= suma/tiradas
    frecuencias[j] = frecuencia

print("Resultados: ", resultados)
print("Frecuencias: ", frecuencias)
print("Promedios: ",promedios)


x1= list(range(1,tiradas+1))
cmap = plt.cm.get_cmap("hsv",corridas)
figura, lista_graficos = plt.subplots(nrows=2, ncols=2, figsize=(18, 6))
lista_graficos[0,0].plot(x1,calcular_frecuencia_relativa_esperada(tiradas),label='Frecuencia relativa esperada',linestyle='--',color='blue')
lista_graficos[0,1].plot(x1,calcular_promedio_esperado(tiradas),label='Promedio esperado',linestyle='--',color='blue')
lista_graficos[1,0].plot(x1,calcular_desviacion_estandar_esperada(tiradas),label='Desviación estándar esperada',linestyle='--',color='blue')
lista_graficos[1,1].plot(x1,calcular_varianza_esperada(tiradas),label='Varianza esperada',linestyle='--',color='blue')
for i in range(corridas):
        color = list(np.random.choice(range(256), size=3)) 
        
        lista_graficos[0,0].plot(x1, calcular_frecuencias_relativas_por_tiradas(numeroElegido,resultados[i]), color=cmap(i))
        lista_graficos[0,0].set_xlabel('Número de tirada')
        lista_graficos[0,0].set_ylabel('Frecuencia relativa')
        lista_graficos[0,0].set_title('Frecuencia relativa por tiradas')
        lista_graficos[0,0].set_yticks(np.linspace(0, 1, 11))
        lista_graficos[0,0].legend()
        lista_graficos[0,0].grid(True)

        lista_graficos[0,1].plot(x1,calcular_numero_promedio_por_tirada(resultados[i]), color=cmap(i))
        lista_graficos[0,1].set_xlabel('Número de tirada')
        lista_graficos[0,1].set_ylabel('Número')
        lista_graficos[0,1].set_title('Promedio por tiradas')
        lista_graficos[0,1].legend()
        lista_graficos[0,1].grid(True)

        lista_graficos[1,0].plot(x1,calcular_desviacion_estandar_por_tirada(resultados[i],numeroElegido), color=cmap(i))
        lista_graficos[1,0].set_xlabel('Número de tirada')
        lista_graficos[1,0].set_ylabel('Número')
        lista_graficos[1,0].set_title('Desviacion estandar por tiradas')
        lista_graficos[1,0].legend()
        lista_graficos[1,0].grid(True)

        lista_graficos[1, 1].plot(x1, calcular_varianza_calculada( resultados[i], tiradas),color=cmap(i))
        lista_graficos[1, 1].set_ylabel('Valor de varianza')
        lista_graficos[1, 1].set_title('Varianza esperada vs Varianza calculada en función del número de tiradas')
        lista_graficos[1, 1].legend()
        lista_graficos[1, 1].grid(True)

plt.tight_layout()
plt.show()