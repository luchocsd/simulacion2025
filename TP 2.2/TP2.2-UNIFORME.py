import numpy as np
import matplotlib.pyplot as plt

def generador_uniforme_inversa(a, b, n=1000):

    # Generar array de n números aleatorios uniformes entre 0 y 1
    u = np.random.random(n)
    
    # Aplicar la transformada inversa para distribución uniforme: F^(-1)(u) = a + (b-a)*u
    # Esta operación se aplica a todo el array u elemento por elemento
    x = a + (b-a) * u
    
    return x  # Devuelve el array completo con n elementos


a = 5
b = 15
n_muestras = 10000

# Generar array de números aleatorios
numeros = generador_uniforme_inversa(a, b, n_muestras)

# Mostrar que efectivamente tenemos un array con n_muestras elementos
print(f"Tipo de dato devuelto: {type(numeros)}")
print(f"Forma del array: {numeros.shape}")
print(f"Total de números generados: {len(numeros)}")
print(f"Primeros 10 números generados: {numeros[:10]}")

# Calcular media y varianza teórica
media_teorica = (a + b) / 2
varianza_teorica = (b - a)**2 / 12

# Calcular media y varianza empírica
media_empirica = np.mean(numeros)
varianza_empirica = np.var(numeros)

print(f"\nDistribución Uniforme ({a}, {b})")
print(f"Media teórica: {media_teorica}")
print(f"Media empírica: {media_empirica}")
print(f"Varianza teórica: {varianza_teorica}")
print(f"Varianza empírica: {varianza_empirica}")

# Generar histograma para visualizar la distribución
plt.figure(figsize=(10, 6))
plt.hist(numeros, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black')

# Añadir la función de densidad teórica
x = np.linspace(a-1, b+1, 1000)
y = np.where((x >= a) & (x <= b), 1/(b-a), 0)
plt.plot(x, y, 'r-', linewidth=2, label='PDF teórica')

plt.title(f'Distribución Uniforme ({a}, {b}) - Método de la Transformada Inversa')
plt.xlabel('Valor')
plt.ylabel('Densidad')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()