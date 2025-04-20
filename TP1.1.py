import random
import sys
import matplotlib.pyplot as plt
import numpy as np

#IMPORTANTE!! Funciona con una version mas vieja de matpolib, la 3.7.3 (pip install matplotlib==3.7.3)

#Ejemplo para usar el programa (20 tiradas, 5 corridas y numero elegido 22):  python TP1.1.py -c 20 -n 5 -e 22
if len(sys.argv) != 7 or sys.argv[1] != "-c" or sys.argv[3] != "-n" or sys.argv[5] != "-e":
  print("Uso: python TP1.1.py -c XXX -n YYY -e ZZ (cantidad de tiradas, corridas y número elegido)")
  sys.exit(1)

# Cantidad de veces que gira la ruleta en una corrida
tiradas = int(sys.argv[2])

# Cantidad de veces que se repite el ciclo de tiradas
corridas = int(sys.argv[4])

# Numero que se busca en el ciclo de tiradas
numeroElegido = int(sys.argv[6])

# calcula el promedio a medida que se va girando la ruleta cada vez y lo appendea
def prom_por_tirada(resultados):
  numeroDeTirada = 0
  suma = 0
  promedios = []
  for numero in resultados:
      numeroDeTirada += 1
      suma = suma + numero
      promedio = int(suma / numeroDeTirada)
      promedios.append(promedio)
  return promedios

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

# REVISAR. 
def desv_std_por_tirada(resultados, numeroElegido):
  desviaciones_por_tirada = []
  for i in range(1, len(resultados) + 1):
      valores_tirada = np.array(resultados[:i])
      desviacion = np.std(valores_tirada)
      desviaciones_por_tirada.append(desviacion)
  return desviaciones_por_tirada

# REVISAR la formula
def desv_est_teorica(tiradas):
  desviacion_estandar_esperada = ((((37)**2) - 1) / 12)**0.5
  desviacion_estandar_recta = []
  for _ in range(tiradas):
    desviacion_estandar_recta.append(desviacion_estandar_esperada)
  return desviacion_estandar_recta

# REVISAR la formula
def var_teorica(tiradas):
  varianza_esperada = (((37)**2) - 1) / 12
  varianza_recta = []
  for _ in range(tiradas):
    varianza_recta.append(varianza_esperada)
  return varianza_recta

#REVISAR
def varianza_calculada( resultados, numeroDeTiradas):
  valores_aleatorios = np.array(resultados)
  varianzas_calculadas = []
  for i in range(1, numeroDeTiradas + 1):
    diferencias_cuadradas = (valores_aleatorios[:i] - promedio_teorico) ** 2
    varianza_calculada = np.mean(diferencias_cuadradas)
    varianzas_calculadas.append(varianza_calculada)
  return varianzas_calculadas


#Array bidimensional, con todos los resultados de cada ruleta, de cada corrida
resultados = [[0 for i in range(tiradas)] for j in range(corridas)]

#Array con los promedios de cada ciclo 
promedios = [0 for i in range(corridas)]

#Array con la cantidad de veces por ciclo que aparece el numero elegido
frecuencias = [0 for i in range(corridas)]

promedio_teorico = sum(range(37))/37
arr_promedio_teorico = [promedio_teorico for i in range(tiradas)]

frec_rel_teorica = 1/37
arr_frec_rel_teorica = [frec_rel_teorica for i in range(tiradas)]

print("Tiradas: ", tiradas)
print("Corridas: ", corridas)
print("Número elegido: ", numeroElegido)

# calculo de resultados, promedios y frecuencia de aparicion de nuestro numero elegido 
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
print("Frecuencia de num elegido por corrida: ", frecuencias)
print("Promedio de resultados por corrida: ",promedios)


x1= list(range(1,tiradas+1))
cmap = plt.cm.get_cmap("hsv",corridas)
figura, lista_graficos = plt.subplots(nrows=2, ncols=2, figsize=(18, 6))
lista_graficos[0,0].plot(x1,arr_frec_rel_teorica,label='Frecuencia relativa teórica',linestyle='--',color='blue')
lista_graficos[0,1].plot(x1,arr_promedio_teorico,label='Promedio teórico',linestyle='--',color='blue')
lista_graficos[1,0].plot(x1,desv_est_teorica(tiradas),label='Desviación estándar teórica',linestyle='--',color='blue')
lista_graficos[1,1].plot(x1,var_teorica(tiradas),label='Varianza teórica',linestyle='--',color='blue')
for i in range(corridas):
  color = list(np.random.choice(range(256), size=3)) 
  #grafico de frecuencia relativa
  lista_graficos[0,0].plot(x1, f_rel_por_tirada(numeroElegido,resultados[i]), color=cmap(i))
  lista_graficos[0,0].set_xlabel('Número de tirada')
  lista_graficos[0,0].set_ylabel('Frecuencia relativa')
  lista_graficos[0,0].set_title('Frecuencia relativa por tiradas')
  lista_graficos[0,0].set_yticks(np.linspace(0, 1, 11))
  lista_graficos[0,0].legend()
  lista_graficos[0,0].grid(True)
  #grafico de promedio por tiradas
  lista_graficos[0,1].plot(x1,prom_por_tirada(resultados[i]), color=cmap(i))
  lista_graficos[0,1].set_xlabel('Número de tirada')
  lista_graficos[0,1].set_ylabel('Número')
  lista_graficos[0,1].set_title('Promedio por tiradas')
  lista_graficos[0,1].legend()
  lista_graficos[0,1].grid(True)
  #grafico de desviacion estandar por tiradas
  lista_graficos[1,0].plot(x1,desv_std_por_tirada(resultados[i],numeroElegido), color=cmap(i))
  lista_graficos[1,0].set_xlabel('Número de tirada')
  lista_graficos[1,0].set_ylabel('Número')
  lista_graficos[1,0].set_title('Desviacion estandar por tiradas')
  lista_graficos[1,0].legend()
  lista_graficos[1,0].grid(True)
  #grafico de varianza calculada por tiradas
  lista_graficos[1, 1].plot(x1, varianza_calculada( resultados[i], tiradas),color=cmap(i))
  lista_graficos[1,1].set_xlabel('Número de tirada')
  lista_graficos[1, 1].set_ylabel('Valor de varianza')
  lista_graficos[1, 1].set_title('Varianza esperada vs Varianza calculada en función del número de tiradas')
  lista_graficos[1, 1].legend()
  lista_graficos[1, 1].grid(True)

plt.tight_layout()
plt.show()