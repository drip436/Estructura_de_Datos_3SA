# Para medir el tiempo de ejecucion 
import time

###### Funcion Iterativa ####
def fibonacci_iterativo(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

###### Funcion Recursiva ####
def fibonacci_recursivo(n):
    if n <= 1:
        return n
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)

# Prueba de rendimiento
n_objetivo = 35

### TIEMPO DE ####
# Medir Iterativo
inicio = time.time()
resultado_iterativo = fibonacci_iterativo(n_objetivo)
fin = time.time()
tiempo_i = fin - inicio

### TIEMPO DE ####
# Medir Recursivo
inicio = time.time()
resultado_recursivo = fibonacci_recursivo(n_objetivo)
fin = time.time()
tiempo_r = fin - inicio

print(" ")
print("/////////// FUNCION ITERATIVA  /////////////")
print(f"Resultado con funcion iterativa para n={n_objetivo}: {resultado_iterativo}")
print(f"Tiempo Iterativo: {tiempo_i:.6f} segundos")
print("")
print("/////////// FUNCION RECURSIVA  /////////////")
print(f"Resultado con funcion recursivo para n={n_objetivo}: {resultado_recursivo}")
print(f"Tiempo Recursivo: {tiempo_r:.6f} segundos")