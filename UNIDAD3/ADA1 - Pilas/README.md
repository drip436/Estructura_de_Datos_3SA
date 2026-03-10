# Estructuras de Datos — Pila en Python

Colección de dos programas que demuestran el uso de la estructura de datos **Pila (Stack)** para resolver problemas clásicos de programación.

---

## Archivos

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

## 2️⃣ Torres de Hanoi — `torres_hanoi.py`

### ¿Qué hace?

Resuelve el clásico problema de las **Torres de Hanoi** para 3 discos, representando cada torre físicamente como una `Pila`. Muestra en consola una animación ASCII del estado de las torres después de cada movimiento.

### Reglas del juego

1. Solo se puede mover **un disco a la vez**.
2. Solo se puede mover el disco que está en el **tope** de una torre.
3. Ningún disco puede colocarse sobre un disco **más pequeño**.

El objetivo es mover todos los discos desde la torre **Origen** hasta la torre **Destino**, usando la torre **Auxiliar** como apoyo.

### ¿Cómo funciona?

Se usa un algoritmo **recursivo** clásico:

- Para mover `n` discos de Origen → Destino:
  1. Mover los `n-1` discos superiores de Origen → Auxiliar.
  2. Mover el disco más grande de Origen → Destino.
  3. Mover los `n-1` discos de Auxiliar → Destino.

Cada "movimiento" es en realidad una operación real sobre las pilas: `desapilar()` de la torre fuente y `apilar()` en la torre destino.

### Ejemplo de ejecución

```
Estado inicial:
──────────────────────────────────────
     ■          |          |     
    ■■          |          |     
    ■■■         |          |     
  ───────    ───────    ───────
  Origen     Auxiliar    Destino

Paso  1: Mover disco 1 de 'Origen' → 'Destino'
Paso  2: Mover disco 2 de 'Origen' → 'Auxiliar'
Paso  3: Mover disco 1 de 'Destino' → 'Auxiliar'
Paso  4: Mover disco 3 de 'Origen' → 'Destino'
Paso  5: Mover disco 1 de 'Auxiliar' → 'Origen'
Paso  6: Mover disco 2 de 'Auxiliar' → 'Destino'
Paso  7: Mover disco 1 de 'Origen' → 'Destino'

Estado final:
──────────────────────────────────────
     |          |          ■     
     |          |         ■■     
     |          |         ■■■    
  ───────    ───────    ───────
  Origen     Auxiliar    Destino

✓ Resuelto en 7 movimientos.
```

### Número de movimientos

Para `n` discos, el número mínimo de movimientos es siempre **2ⁿ − 1**:

| Discos | Movimientos |
|---|---|
| 1 | 1 |
| 2 | 3 |
| 3 | 7 |
| 4 | 15 |

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
