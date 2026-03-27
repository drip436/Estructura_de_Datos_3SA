# Estructuras de Datos — Pila en Python

Colección de dos programas que demuestran el uso de la estructura de datos **Pila (Stack)** para resolver problemas clásicos de programación.

---

## Archivos

# Clase_Cola.py

Clase base que implementa la estructura de datos **Cola (LIFO)** usando `collections.deque`.

| Archivo | Descripción |
|---|---|
| `expresiones_pila.py` | Evaluador de expresiones aritméticas en notación Postfija y Prefija |
| `torres_hanoi.py` | Solución al juego de las Torres de Hanoi para 3 discos |

---

## La clase `Pila`

Ambos programas implementan su propia clase `Pila` desde cero, sin usar módulos externos. Esta clase modela el comportamiento clásico de una pila (LIFO — *Last In, First Out*) con los siguientes métodos:

| Método | Descripción |
|---|---|
| `apilar(elemento)` | Agrega un elemento al tope de la pila |
| `desapilar()` | Elimina y retorna el elemento del tope |
| `tope()` | Consulta el elemento del tope sin eliminarlo |
| `esta_vacia()` | Retorna `True` si la pila no tiene elementos |

---

## 1. Evaluador de Expresiones — `expresiones_pila.py`

### ¿Qué hace?

Evalúa expresiones aritméticas escritas en dos notaciones alternativas a la notación infija tradicional:

- **Notación Postfija** (Notación Polaca Inversa / RPN): el operador se escribe *después* de los operandos.
- **Notación Prefija** (Notación Polaca): el operador se escribe *antes* de los operandos.

Los operadores soportados son: `+`, `-`, `*`, `/`

### ¿Cómo funciona?

#### Postfija

Se recorren los tokens de **izquierda a derecha**:
1. Si el token es un **número** → se apila.
2. Si el token es un **operador** → se desapilan dos operandos, se aplica la operación y se apila el resultado.

```
Expresión: "3 4 + 2 *"

  Leer 3   → Pila: [3]
  Leer 4   → Pila: [3, 4]
  Leer +   → desapilar 4 y 3, calcular 3+4=7 → Pila: [7]
  Leer 2   → Pila: [7, 2]
  Leer *   → desapilar 2 y 7, calcular 7*2=14 → Pila: [14]

  Resultado: 14
```

#### Prefija

Se recorren los tokens de **derecha a izquierda**:
1. Si el token es un **número** → se apila.
2. Si el token es un **operador** → se desapilan dos operandos, se aplica la operación y se apila el resultado.

```
Expresión: "* + 3 4 2"

  Leer 2   → Pila: [2]
  Leer 4   → Pila: [2, 4]
  Leer 3   → Pila: [2, 4, 3]
  Leer +   → desapilar 3 y 4, calcular 3+4=7 → Pila: [2, 7]
  Leer *   → desapilar 7 y 2, calcular 7*2=14 → Pila: [14]

  Resultado: 14
```

### Ejemplos

| Tipo | Expresión | Resultado |
|---|---|---|
| Postfija | `3 4 +` | `7.0` |
| Postfija | `3 4 + 2 *` | `14.0` |
| Postfija | `5 1 2 + 4 * + 3 -` | `14.0` |
| Prefija | `+ 3 4` | `7.0` |
| Prefija | `* + 3 4 2` | `14.0` |
| Prefija | `/ 10 2` | `5.0` |

### Uso

```bash
python expresiones_pila.py
```

El programa ejecuta pruebas automáticas y luego abre un **modo interactivo** donde puedes ingresar tus propias expresiones:

```
Modo (postfija/prefija): postfija
Expresión: 8 3 - 2 *
  Resultado: 10.0
```

> **Nota:** Los tokens deben estar separados por espacios. Escribe `salir` para terminar.

---

## Ejercicio 3 — Torres de Hanoi (`Torres_Hanoi.py`)

Resuelve el clásico problema de las **Torres de Hanoi** usando la clase `Pila`. Incluye solución **recursiva** e **iterativa**. El usuario elige cuántos discos quiere usar.

**Cómo ejecutarlo:**

```bash
python Torres_Hanoi.py
```

**Límite de discos: 15**

Con 15 discos se realizan 32.767 movimientos. Se establece este límite para evitar tiempos de ejecución excesivos y alto uso de memoria por la recursión.

| Discos | Movimientos |
|---|---|
| 3 | 7 |
| 5 | 31 |
| 10 | 1.023 |
| 15 | 32.767 |

**Ejemplo de uso:**

```
==========================================
        TORRES DE HANOI
==========================================

  Ingrese el número de discos (mínimo 1, máximo 15).
  Nota: con 15 discos se realizan 32,767 movimientos.

  Número de discos [1-15]: 3

Paso  1: Mover disco 1 de 'Origen' → 'Destino'

──────────────────────────────────────────
  ■■■    |       |
  ────────────────────────
  Origen  Auxiliar  Destino
──────────────────────────────────────────
...
✓ Resuelto en 7 movimientos.
```

---
### Uso

```bash
python torres_hanoi.py
```

---

## ▶️ Requisitos

- Python 3.6 o superior
- No requiere librerías externas

```bash
# Ejecutar el evaluador de expresiones
python expresiones_pila.py

# Ejecutar las Torres de Hanoi
python torres_hanoi.py
```
