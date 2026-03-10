# Estructuras de Datos en Python — Clase Cola & Torres de Hanoi

Actividad **ADA2-COLAS** y **ADA-PILAS**. Implementación de las estructuras de datos Cola y Pila aplicadas a tres programas distintos.

---

## Archivos del proyecto

```
📁 proyecto/
├── Clase_Cola.py               # Clase Cola (base para los ejercicios 1 y 2)
├── Suma_de_dos_colas.py        # Ejercicio 1 – Suma de colas
├── Sistemas_de_Atencion.py     # Ejercicio 2 – Sistema de atención
├── Clase_Pila.py               # Clase Pila (base para Torres de Hanoi)
└── Torres_Hanoi.py             # Ejercicio 3 – Torres de Hanoi
```

---

## Clase_Cola.py

Clase base que implementa la estructura de datos **Cola (FIFO)** usando `collections.deque`.

**Métodos disponibles:**

| Método | Descripción |
|---|---|
| `encolar(elemento)` | Agrega un elemento al final de la cola |
| `desencolar()` | Elimina y retorna el elemento del frente |
| `esta_vacia()` | Retorna `True` si la cola no tiene elementos |
| `tamanio()` | Retorna la cantidad de elementos en la cola |

> Esta clase es importada por `Suma_de_dos_colas.py` y `Sistemas_de_Atencion.py`.

---

## Ejercicio 1 — Suma de dos colas (`Suma_de_dos_colas.py`)

Solicita al usuario dos colas de enteros del mismo tamaño y devuelve una nueva cola con cada par de elementos sumados uno a uno.

**Cómo ejecutarlo:**

```bash
python Suma_de_dos_colas.py
```

**Ejemplo de uso:**

```
¿Cuántos elementos tendrán las colas? 3

  Ingrese los 3 números enteros para la Cola A:
    Elemento 1: 3
    Elemento 2: 4
    Elemento 3: 2

  Ingrese los 3 números enteros para la Cola B:
    Elemento 1: 6
    Elemento 2: 2
    Elemento 3: 9

=============================================
  Cola A       Cola B       Resultado
  --------------------------------------
  3            6            9
  4            2            6
  2            9            11
=============================================
```

**Lógica del algoritmo:**

1. Desencola un elemento de cada cola simultáneamente.
2. Suma ambos valores y encola el resultado en una nueva cola.
3. Restaura las colas originales al terminar para no perder los datos.

---

## Ejercicio 2 — Sistema de atención (`Sistemas_de_Atencion.py`)

Simula el sistema de colas de servicio de una compañía de seguros. Cada servicio tiene su propia cola de turnos. Los clientes llegan y el personal de atención los va llamando por orden de llegada.

**Cómo ejecutarlo:**

```bash
python Sistemas_de_Atencion.py
```

**Servicios disponibles:**

| Número | Servicio |
|---|---|
| 1 | Consultas generales |
| 2 | Siniestros |
| 3 | Pagos y cobranzas |

**Comandos:**

| Comando | Descripción |
|---|---|
| `C <nro>` | Registra la llegada de un cliente al servicio indicado y le asigna un número de turno |
| `A <nro>` | Llama al siguiente cliente en espera del servicio indicado |
| `S` | Cierra el sistema |

**Ejemplo de uso:**

```
Comando: C 1
  >> Turno asignado: 1  (Servicio: Consultas generales)

Comando: C 1
  >> Turno asignado: 2  (Servicio: Consultas generales)

Comando: A 1
  >> Llamando turno: 1  (Servicio: Consultas generales)

Comando: S
  Sistema cerrado.
```

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

## Requisitos

- Python 3.8 o superior
- No se requieren librerías externas (`collections` es parte de la biblioteca estándar)

---

## Dependencias entre archivos

```
Clase_Cola.py  ◄──  Suma_de_dos_colas.py
               ◄──  Sistemas_de_Atencion.py

Clase_Pila.py  ◄──  Torres_Hanoi.py
```

> Los archivos `Clase_Cola.py` y `Clase_Pila.py` deben estar en la **misma carpeta** que los programas que los importan.
