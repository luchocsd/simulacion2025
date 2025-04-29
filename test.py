import random

# para probar la azarosidad de la función random.randint

average = 0
acum = 0
for j in range(1000):
  for i in range(10000):
    aux = random.randint(0, 1)
    if aux == 1:
      acum += 1
    else:
      acum -= 1
  average += acum
average /= 100
print("Average: ", average)