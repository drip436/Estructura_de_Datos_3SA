# ◈ Simulador Educativo — Bubble Sort

> Visualización interactiva del algoritmo de ordenamiento por burbuja,  
> desarrollada en Python 3 con Tkinter. Sin dependencias externas.

---

## Captura del programa

```
┌─────────────────────────────────────────────────────────────────────┐
│  ◈  SIMULADOR EDUCATIVO — BUBBLE SORT  ◈         Vector: [17,23,21,45,67] │
├──────────────────────────────────────┬──────────────────────────────┤
│                                      │  ▸ Estadísticas              │
│   [barras animadas del vector]       │  Pasada (i):         2       │
│                                      │  Comparación (j):    1       │
│   ▼              ▼                   │  Total comparaciones: 5      │
│  ████  ██  ███  █████  ███           │  Intercambios:        3      │
│   45   17   23   67    21            │                              │
│  [0]  [1]  [2]  [3]   [4]           │  ▸ Explicación del paso      │
│                                      │  Pasada 2, pos 0: Compa-     │
│  ■ Normal  ■ Comparando(i)           │  rando 17 y 23 → Sin cambio  │
│  ■ Comp(i+1)  ■ Ordenado ✓          │  (17 ≤ 23)                   │
├──────────────────────────────────────┴──────────────────────────────┤
│  ▸ Historial de Pasos                                               │
│  [001]  Pasada 1, pos 0: Comparando 45 y 17 → Se intercambia (...)  │
│  [002]  Pasada 1, pos 1: Comparando 45 y 23 → Se intercambia (...)  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Descripción

Este programa visualiza paso a paso cómo funciona el **Método de la Burbuja** (*Bubble Sort*), uno de los algoritmos de ordenamiento más didácticos en ciencias de la computación. Está diseñado para ser usado en clase o como herramienta de autoestudio.

**Vector de ejemplo (referencia):** `[45, 17, 23, 67, 21]`

---

## Requisitos

| Requisito | Versión mínima |
|-----------|---------------|
| Python    | 3.6+          |
| Tkinter   | Incluido en Python estándar |
| Sistema operativo | Windows / macOS / Linux |

> **Nota:** Tkinter viene incluido en la instalación oficial de Python para Windows y macOS. En Linux puede requerirse instalación adicional (ver sección de instalación).

---

## Instalación

### Windows / macOS
No se requieren pasos adicionales. Python incluye Tkinter por defecto.

```bash
# Verificar que Python está instalado
python --version

# Ejecutar directamente
python bubble_sort_simulator.py
```

### Linux (Ubuntu / Debian)
```bash
# Instalar Tkinter si no está disponible
sudo apt-get update
sudo apt-get install python3-tk

# Ejecutar
python3 bubble_sort_simulator.py
```

### Linux (Fedora / RHEL)
```bash
sudo dnf install python3-tkinter
python3 bubble_sort_simulator.py
```

---

## Uso

### Controles principales

| Control | Acción |
|---------|--------|
| **▶ Paso a Paso** | Avanza una sola comparación a la vez |
| **⏵ Reproducción Auto** | Ejecuta el algoritmo automáticamente |
| **⏸ Pausar** | Pausa la reproducción automática |
| **↺ Reiniciar** | Vuelve al vector original `[45, 17, 23, 67, 21]` |
| **Slider de velocidad** | Ajusta la velocidad de animación (lento ↔ rápido) |

### Código de colores de las barras

| Color | Significado |
|-------|-------------|
| 🔵 Azul-índigo | Elemento en estado neutro (no involucrado en la comparación actual) |
| 🔴 Rojo | Elemento en posición `j` (primer elemento de la comparación) |
| 🟡 Amarillo | Elemento en posición `j+1` (segundo elemento de la comparación) |
| 🟢 Verde | Elemento ya ordenado y en su posición final definitiva |

### Panel de explicación

Cada paso muestra una descripción como:

```
Pasada 1, pos 0: Comparando 45 y 17  →  Se intercambia (45 > 17)
Pasada 1, pos 1: Comparando 45 y 23  →  Se intercambia (45 > 23)
Pasada 1, pos 2: Comparando 45 y 67  →  Sin cambio (45 ≤ 67)
```

### Estadísticas en tiempo real

- **Pasada (i):** Número de la iteración externa actual del algoritmo.
- **Comparación (j):** Posición actual dentro de la pasada.
- **Total comparaciones:** Cuántas veces se han comparado dos elementos.
- **Intercambios:** Cuántos intercambios reales se han realizado.

---

## Cómo funciona el algoritmo

El **Bubble Sort** recorre el vector repetidamente comparando pares de elementos adyacentes y los intercambia si están en el orden equivocado:

```
Vector inicial: [45, 17, 23, 67, 21]

Pasada 1:
  [45, 17, ...] → 45 > 17 → intercambio → [17, 45, 23, 67, 21]
  [17, 45, 23, ...] → 45 > 23 → intercambio → [17, 23, 45, 67, 21]
  [..., 45, 67, ...] → 45 ≤ 67 → sin cambio
  [..., 67, 21] → 67 > 21 → intercambio → [17, 23, 45, 21, 67]
                                                              ^^^
                                                         ya ordenado ✓
Pasada 2, 3, 4... continúan hasta ordenar todo el vector.

Resultado final: [17, 21, 23, 45, 67]
```

### Complejidad

| Caso | Complejidad temporal |
|------|---------------------|
| Mejor caso (ya ordenado) | O(n) |
| Caso promedio | O(n²) |
| Peor caso (orden inverso) | O(n²) |
| Espacio | O(1) — in-place |

---

## Estructura del código

```
bubble_sort_simulator.py
│
├── COLORES (dict)          — Paleta de colores centralizada
├── FUENTE_* (constantes)   — Fuentes usadas en la UI
│
└── class BubbleSortSimulator
    │
    ├── __init__()              — Inicialización del estado y la UI
    ├── _configurar_ventana()   — Tamaño y posición de la ventana
    │
    ├── ── Construcción de UI ──
    ├── _construir_ui()
    ├── _crear_cabecera()
    ├── _crear_cuerpo_principal()
    ├── _crear_canvas_visualizacion()
    ├── _crear_leyenda()
    ├── _crear_panel_lateral()
    ├── _crear_botones()
    └── _crear_panel_inferior()
    │
    ├── ── Lógica del algoritmo ──
    ├── _paso_siguiente()       — Ejecuta UNA comparación del Bubble Sort
    └── _marcar_finalizado()    — Estado final: todo ordenado
    │
    ├── ── Reproducción automática ──
    ├── _toggle_auto()          — Enciende / apaga la animación
    └── _ciclo_auto()           — Loop no bloqueante con root.after()
    │
    ├── _reiniciar()            — Restaura el vector original
    │
    ├── ── Renderizado ──
    ├── _dibujar_barras()       — Pinta las barras en el Canvas
    └── _aclarar_color()        — Utilidad: aclara un color hex
    │
    └── ── Actualizaciones de UI ──
        ├── _actualizar_contadores()
        ├── _actualizar_explicacion()
        ├── _agregar_log()
        └── _texto_vector()
```

---

## Decisiones de diseño

- **`root.after()` en lugar de `time.sleep()`:** La animación automática usa llamadas recursivas a `root.after()` para no bloquear el event loop de Tkinter. Esto mantiene la interfaz responsiva durante la reproducción.
- **Orientado a objetos:** Todo el estado del algoritmo y de la UI vive en una sola clase (`BubbleSortSimulator`), lo que facilita su lectura y extensión.
- **Paleta centralizada:** El diccionario `COLORES` en el nivel de módulo permite cambiar toda la apariencia modificando un solo lugar.
- **Sin dependencias externas:** El programa usa únicamente la biblioteca estándar de Python (`tkinter`), por lo que funciona en cualquier instalación de Python 3 sin necesidad de `pip install`.

---

## Posibles extensiones

- Permitir ingresar un vector personalizado por el usuario.
- Agregar comparación visual con otros algoritmos (Selection Sort, Insertion Sort).
- Exportar el historial de pasos a un archivo `.txt`.
- Agregar sonido (pitidos de diferente tono según si hay intercambio o no).

---

## Licencia

Proyecto educativo de uso libre. Sin restricciones de uso académico o personal.

---

*Desarrollado con Python 3 + Tkinter · Sin dependencias externas*