# ◈ Grafos · República Mexicana

Aplicación de escritorio desarrollada en **Python + Tkinter** que modela 7 estados de la República Mexicana como un grafo ponderado no dirigido y resuelve sobre él dos tipos de recorridos hamiltonianos, mostrando el resultado de forma visual e interactiva.

---

## Tabla de contenidos

- [Descripción](#descripción)
- [Requisitos](#requisitos)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Estructura del grafo](#estructura-del-grafo)
- [Funcionalidades](#funcionalidades)
- [Algoritmos implementados](#algoritmos-implementados)
- [Interfaz de usuario](#interfaz-de-usuario)
- [Resultados esperados](#resultados-esperados)
- [Estructura del código](#estructura-del-código)

---

## Descripción

El programa construye un grafo con **7 nodos** (estados) y **12 aristas** (conexiones con costo en kilómetros) y permite:

- **Inciso a)** — Recorrer los 7 estados **sin repetir** ninguno (camino hamiltoniano óptimo).
- **Inciso b)** — Recorrer los 7 estados **repitiendo al menos uno** (camino hamiltoniano con repetición de costo mínimo).
- **Inciso c)** — Mostrar el **costo total** del recorrido para ambos casos.
- **Inciso d)** — **Dibujar el grafo** con nodos, aristas y etiquetas de distancia en un canvas interactivo.
- **Inciso e)** — Listar todos los **estados y sus relaciones** dentro de la propia interfaz.

---

## Requisitos

| Componente | Versión mínima |
|---|---|
| Python | 3.7 o superior |
| Tkinter | Incluido en la instalación estándar de Python |

No se requieren dependencias externas. Todas las librerías utilizadas son parte de la biblioteca estándar de Python:

```
tkinter · math · heapq · itertools · collections
```

### Verificar que Tkinter esté disponible

```bash
python -c "import tkinter; print(tkinter.TkVersion)"
```

Si el comando devuelve un número de versión, el entorno está listo.

> **Linux (Debian/Ubuntu):** si Tkinter no está instalado, ejecuta:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## Instalación y ejecución

```bash
# 1. Clona o descarga el archivo
git clone <url-del-repositorio>
cd grafos-mexico

# 2. Ejecuta el programa
python grafos_mexico.py
```

No se necesita instalar ningún paquete adicional con `pip`.

---

## Estructura del grafo

### Nodos — 7 estados

```
Mérida · Campeche · Villahermosa · Veracruz · Oaxaca · Puebla · CDMX
```

### Aristas — 12 conexiones (km)

| Estado A | Estado B | Distancia |
|---|---|---|
| Mérida | Campeche | 197 km |
| Campeche | Villahermosa | 444 km |
| Villahermosa | Veracruz | 516 km |
| Veracruz | Oaxaca | 341 km |
| Oaxaca | Puebla | 363 km |
| Puebla | CDMX | 131 km |
| Mérida | Villahermosa | 535 km |
| Campeche | Oaxaca | 700 km |
| Veracruz | Puebla | 300 km |
| Puebla | Oaxaca | 363 km |
| CDMX | Veracruz | 420 km |
| CDMX | Oaxaca | 470 km |

El grafo es **no dirigido** (todas las aristas son bidireccionales) y **ponderado** (cada arista tiene un costo en kilómetros).

---

## Funcionalidades

### ▶ Botón a) — Recorrido sin repetición
Calcula y muestra el **camino hamiltoniano de menor costo** que visita los 7 estados exactamente una vez. Resalta en azul las aristas y nodos del recorrido sobre el canvas.

### ▶ Botón b) — Recorrido con repetición
Calcula el **camino de menor costo** que cubre todos los estados permitiendo pasar por uno o más nodos más de una vez. Los nodos repetidos se resaltan en **naranja/rojo** para diferenciarlos del resto.

### ↺ Botón Limpiar
Restablece el grafo a su estado original (sin ningún recorrido resaltado) y limpia el panel de resultados.

---

## Algoritmos implementados

### a) Fuerza Bruta — `hamiltoniano_sin_repeticion()`

Evalúa todas las **permutaciones posibles** de los 6 estados restantes (partiendo desde Mérida), comprueba si existe arista entre cada par consecutivo y conserva la ruta válida de menor costo.

```
Complejidad: O((n-1)!) = O(6!) = 720 permutaciones
```

Dado que `n = 7`, el espacio de búsqueda es suficientemente pequeño para que la fuerza bruta sea instantánea.

### b) Dijkstra sobre espacio de estados — `hamiltoniano_con_repeticion()`

Utiliza un **heap de mínimos** (cola de prioridad) donde cada estado del sistema es el par `(nodo_actual, frozenset_de_estados_visitados)`. Esto permite explorar rutas que revisitan nodos mientras garantiza encontrar el camino óptimo gracias a la propiedad de Dijkstra.

```
Estado del sistema: (nodo, frozenset_visitados)
Espacio de estados: n × 2ⁿ = 7 × 128 = 896 estados posibles
```

Se aplican dos podas para controlar la memoria y el tiempo:
- **Poda por costo:** se descarta cualquier expansión que supere el mejor costo encontrado.
- **Poda por completitud:** cuando se alcanza un camino que visita todos los estados y tiene al menos un nodo repetido, se registra como candidato y no se expande más.

---

## Interfaz de usuario

```
┌─────────────────────────────────────────────────────────────┐
│  ◈  GRAFOS · REPÚBLICA MEXICANA   7 estados · Hamiltonianos │
├──────────────────────┬──────────────────────────────────────┤
│ ▸ ESTADOS Y          │                                      │
│   RELACIONES         │                                      │
│  • Mérida            │         GRAFO INTERACTIVO            │
│  • Campeche          │                                      │
│  • ...               │   [nodos circulares + aristas        │
│  Mérida ↔ Campeche   │    con etiquetas de distancia]       │
│  197 km              │                                      │
│  ...                 │                                      │
├──────────────────────┤                                      │
│ ▸ ACCIONES           │                                      │
│  [▶ Sin repetición]  │                                      │
│  [▶ Con repetición]  │                                      │
│  [↺ Limpiar]         │                                      │
├──────────────────────┤                                      │
│ ▸ RESULTADOS         │                                      │
│  Ruta óptima:        │                                      │
│  Mérida → Campeche…  │                                      │
│  COSTO TOTAL: X km   │                                      │
└──────────────────────┴──────────────────────────────────────┘
```

### Leyenda de colores en el canvas

| Color | Significado |
|---|---|
| 🔵 Azul (`#58a6ff`) | Nodo visitado en el recorrido a) |
| 🔴 Naranja-rojo (`#f78166`) | Nodo repetido en el recorrido b) |
| Azul brillante | Arista activa del recorrido a) |
| Naranja | Arista activa del recorrido b) |
| Gris oscuro | Nodo/arista no incluido en el recorrido |

El canvas es **redimensionable**: al cambiar el tamaño de la ventana, el grafo se re-escala automáticamente para ajustarse al espacio disponible.

---

## Resultados esperados

### Inciso a) — Sin repetición

```
Ruta óptima:
  Mérida → Campeche → Villahermosa → Veracruz → Oaxaca → Puebla → CDMX

Desglose:
  Mérida        → Campeche        197 km
  Campeche      → Villahermosa    444 km
  Villahermosa  → Veracruz        516 km
  Veracruz      → Oaxaca          341 km
  Oaxaca        → Puebla          363 km
  Puebla        → CDMX            131 km

  ✔  COSTO TOTAL:  1,992 km
```

### Inciso b) — Con repetición

```
Ruta encontrada:
  Mérida → Campeche → Villahermosa → Veracruz → Puebla → CDMX → Oaxaca → Veracruz

Nodos repetidos:
  ⚠  Veracruz  ×2

  ✔  COSTO TOTAL:  2,399 km
```

---

## Estructura del código

```
grafos_mexico.py
│
├── DATOS DEL GRAFO
│   ├── ESTADOS          — Lista de los 7 nodos
│   ├── ARISTAS          — Tuplas (estado_a, estado_b, km)
│   └── POSICIONES       — Coordenadas base para el canvas
│
├── LÓGICA DE GRAFOS
│   ├── construir_grafo()                  — Dict de adyacencia bidireccional
│   ├── hamiltoniano_sin_repeticion()      — Fuerza bruta O(6!)
│   └── hamiltoniano_con_repeticion()      — Dijkstra sobre (nodo, visitados)
│
├── PALETA Y FUENTES
│   └── Constantes de color y tipografía (tema oscuro)
│
└── CLASE App (tk.Tk)
    ├── _build_ui()          — Layout principal (header + body)
    ├── _build_left()        — Panel izquierdo (lista + botones + resultados)
    ├── _build_canvas()      — Panel derecho (canvas del grafo)
    ├── _dibujar_grafo()     — Renderiza nodos, aristas y leyenda
    ├── _resolver_a/b()      — Llaman al algoritmo y actualizan la vista
    ├── _limpiar()           — Restablece el estado inicial
    ├── _escribir()          — Escribe en el widget de resultados con etiquetas
    └── _mostrar_a/b()       — Formatea y muestra el resultado de cada inciso
```

---

## Autor

Proyecto académico — Materia: Estructura de Datos / Teoría de Grafos  
Lenguaje: Python 3 · Interfaz: Tkinter · Sin dependencias externas