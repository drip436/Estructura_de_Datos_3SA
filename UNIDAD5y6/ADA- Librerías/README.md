# 📚 Librerías de Ordenamiento en Python

Este repositorio contiene dos módulos especializados en la organización de datos: uno para estructuras en memoria y otro para archivos de gran volumen.

---

## 🛠️ 1. Métodos de Ordenamiento Interno (`SortAlgorithms`)

Estos algoritmos están diseñados para procesar datos que residen en la **Memoria RAM**. Son ideales para listas y arreglos de tamaño moderado.

| Algoritmo | Descripción | Complejidad |
| :--- | :--- | :--- |
| **Burbuja** | Intercambia elementos adyacentes de forma repetida. | $O(n^2)$ |
| **Inserción** | Inserta cada elemento en su posición correcta respecto a los anteriores. | $O(n^2)$ |
| **Selección** | Busca el menor elemento y lo coloca al inicio en cada iteración. | $O(n^2)$ |
| **ShellSort** | Mejora la inserción comparando elementos separados por una brecha. | $O(n^{1.5})$ |
| **Quicksort** | Divide el arreglo usando un pivote y ordena recursivamente. | $O(n \log n)$ |
| **Heapsort** | Utiliza una estructura de montículo binario para extraer el máximo. | $O(n \log n)$ |
| **Radix** | Ordena procesando los dígitos de los números individualmente. | $O(nk)$ |

---

## 🗄️ 2. Métodos de Ordenamiento Externo (`ExternalSorting`)

Diseñados específicamente para cuando los datos **no caben en la RAM** y deben procesarse directamente en el disco duro mediante archivos.

### 2.1 Intercalación (Simple Merge)
Es el proceso base para la mayoría de los ordenamientos externos.
*   **Funcionamiento:** Toma dos archivos (A y B) que **ya deben estar ordenados**. Compara el primer elemento de cada uno, escribe el menor en el archivo de salida y avanza el puntero. Repite hasta vaciar ambos archivos.

### 2.2 Mezcla Directa (Straight Merge)
Un algoritmo de "pasadas" que no requiere que los datos iniciales tengan orden alguno.
*   **Funcionamiento:**
    1.  **Distribución:** Divide el archivo original en bloques de tamaño $N$ (empieza en 1) y los reparte en dos archivos auxiliares.
    2.  **Fusión:** Mezcla los bloques de los archivos auxiliares de vuelta al original, creando bloques de tamaño $2N$.
    3.  El proceso se repite duplicando el tamaño de los bloques en cada pasada hasta que el archivo esté totalmente ordenado.

### 2.3 Mezcla Equilibrada (Natural Merge)
Es una versión optimizada de la mezcla directa que aprovecha el orden parcial preexistente.
*   **Funcionamiento:** En lugar de bloques fijos, identifica **secuencias naturales** (tramos de números que ya están ordenados por casualidad). Distribuye estas secuencias entre los archivos auxiliares y las fusiona. Es mucho más eficiente que la Mezcla Directa si los datos tienen cierto orden previo.

---

## 🚀 Ejemplos de Uso

### Uso de Ordenamiento Interno
```python
from internal_sort import SortAlgorithms

lista = [45, 1, 32, 10, 5]
# Ordenar usando Quicksort
ordenada = SortAlgorithms.quicksort(lista)
print(ordenada)