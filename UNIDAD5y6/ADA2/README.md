# ADA2 – MetOrdenamiento2 🗂️

Aplicación de escritorio en Python con interfaz gráfica (Tkinter) que implementa cuatro métodos clásicos de ordenamiento.

## Métodos implementados

| Método | Complejidad promedio | In-place |
|---|---|---|
| ShellSort | O(n log² n) | ✅ |
| Quicksort | O(n log n) | ✅ |
| Heapsort | O(n log n) | ✅ |
| Radix Sort | O(nk) | ❌ |

## Requisitos

- Python 3.x (Tkinter viene incluido por defecto)

## Cómo ejecutar

```bash
python MetOrdenamiento2.py
```

## Uso

1. Ingresa la **cantidad de números** y pulsa **Generar aleatorio**, o escribe tus propios números separados por coma o espacio en el cuadro de texto.
2. Selecciona el **método de ordenamiento**.
3. Pulsa **▶ ORDENAR**.
4. El panel derecho mostrará el arreglo original, el resultado ordenado y el tiempo de ejecución en milisegundos.

## Estructura del proyecto

```
ADA2-MetOrdenamiento2/
│
├── MetOrdenamiento2.py   # Aplicación principal con GUI
└── README.md
```
