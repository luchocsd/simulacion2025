# El trabajo investigar consiste en construir una programa en lenguaje Python 3.x que simule el funcionamiento del plato
# de una ruleta. Para esto se debe tener en cuenta lo siguientes temas:
# • Generación de valores aleatorios enteros.
# • Uso de listas para el almacenamiento de datos.
# • Uso de la estructura de control FOR para iterar las listas.
# • Empleo de funciones estadísticas.
# • Gráficas de los resultados mediante el paquete Matplotlib.
# • Ingreso por consola de parámetros para la simulación (cantidad de tiradas, corridas y número elegido, Ejemplo
#   python -c XXX -n YYY -e ZZ).

import random
import sys
import matplotlib as plb

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



# x1= list(range(1,numeroDeTiradas+1))
# cmap = get_cmap(corridas)
# colores=['g','r','c','m','y','k','b']
# figura, lista_graficos = plt.subplots(nrows=2, ncols=2, figsize=(18, 6))
# lista_graficos[0,0].plot(x1,calcular_frecuencia_relativa_esperada(numeroDeTiradas),label='Frecuencia relativa esperada',linestyle='--',color='blue')
# lista_graficos[0,1].plot(x1,calcular_promedio_esperado(numeroDeTiradas),label='Promedio esperado',linestyle='--',color='blue')
# lista_graficos[1,0].plot(x1,calcular_desviacion_estandar_esperada(numeroDeTiradas),label='Desviación estándar esperada',linestyle='--',color='blue')
# lista_graficos[1,1].plot(x1,calcular_varianza_esperada(numeroDeTiradas),label='Varianza esperada',linestyle='--',color='blue')
# for i in range(1,corridas+1):
#         color = list(np.random.choice(range(256), size=3)) 
#         lista_graficos[0,0].plot(x1, calcular_frecuencias_relativas_por_tiradas(numeroElegido,valoresAleatorios[i-1]), color=cmap(i-1))
#         lista_graficos[0,0].set_xlabel('Número de tirada')
#         lista_graficos[0,0].set_ylabel('Frecuencia relativa')
#         lista_graficos[0,0].set_title('Frecuencia relativa por tiradas')
#         lista_graficos[0,0].legend()
#         lista_graficos[0,0].grid(True)

#         lista_graficos[0,1].plot(x1,calcular_numero_promedio_por_tirada(valoresAleatorios[i-1]), color=cmap(i-1))
#         lista_graficos[0,1].set_xlabel('Número de tirada')
#         lista_graficos[0,1].set_ylabel('Número')
#         lista_graficos[0,1].set_title('Promedio por tiradas')
#         lista_graficos[0,1].legend()
#         lista_graficos[0,1].grid(True)

#         lista_graficos[1,0].plot(x1,calcular_desviacion_estandar_por_tirada(valoresAleatorios[i-1],numeroElegido), color=cmap(i-1))
#         lista_graficos[1,0].set_xlabel('Número de tirada')
#         lista_graficos[1,0].set_ylabel('Número')
#         lista_graficos[1,0].set_title('Desviacion estandar por tiradas')
#         lista_graficos[1,0].legend()
#         lista_graficos[1,0].grid(True)

#         lista_graficos[1, 1].plot(x1, calcular_varianza_calculada(numeroElegido, valoresAleatorios[i-1], numeroDeTiradas),color=cmap(i-1))
#         lista_graficos[1, 1].set_ylabel('Valor de varianza')
#         lista_graficos[1, 1].set_title('Varianza esperada vs Varianza calculada en función del número de tiradas')
#         lista_graficos[1, 1].legend()
#         lista_graficos[1, 1].grid(True)

# plt.tight_layout()
# plt.show()


# def get_cmap(n, name='hsv'):
#     '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
#     RGB color; the keyword argument name must be a standard mpl colormap name.'''
#     return plt.cm.get_cmap(name, n)