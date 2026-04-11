# 📊 Algoritmos de Grafos — Visualización con Tkinter

Aplicación de escritorio en Python que implementa y visualiza **4 algoritmos clásicos de grafos** con interfaz gráfica interactiva usando Tkinter. Los grafos se dibujan con nodos y aristas sobre un Canvas, sin matrices.

---

## 🗂️ Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `algoritmos_grafos.py` | Implementación pura de los 4 algoritmos (sin interfaz) |
| `algoritmos_grafos_gui.py` | Interfaz gráfica con tablas y resultados en texto |
| `algoritmos_grafos_visual.py` | ⭐ Interfaz gráfica con grafos dibujados visualmente |

---

## 🧮 Algoritmos implementados

### 1. Dijkstra
Encuentra el **camino más corto** desde un nodo origen hacia todos los demás nodos del grafo.

- **Tipo de grafo:** Dirigido con pesos positivos
- **Complejidad:** O((V + E) log V) con cola de prioridad
- **Visualización:** Resalta en verde el camino más corto encontrado

### 2. Floyd-Warshall
Calcula las **distancias mínimas entre todos los pares** de nodos del grafo.

- **Tipo de grafo:** Dirigido con pesos (admite pesos negativos sin ciclos negativos)
- **Complejidad:** O(V³)
- **Visualización:** Grafo dirigido con aristas curvas bidireccionales y tabla de resultados

### 3. Warshall (Clausura Transitiva)
Determina si **existe algún camino** entre cada par de nodos, sin importar la distancia.

- **Tipo de grafo:** Dirigido
- **Complejidad:** O(V³)
- **Visualización:** Muestra el grafo original y el grafo resultante con las aristas inferidas resaltadas

### 4. Kruskal
Construye el **Árbol de Expansión Mínima (MST)** seleccionando las aristas de menor peso sin formar ciclos.

- **Tipo de grafo:** No dirigido con pesos
- **Estructura auxiliar:** Union-Find (con compresión de caminos)
- **Complejidad:** O(E log E)
- **Visualización:** Aristas del MST en dorado, aristas descartadas en gris punteado

---

## ▶️ Requisitos

- **Python 3.7+**
- **Tkinter** (incluido por defecto en la mayoría de instalaciones de Python)

> No se requieren librerías externas ni instalación adicional.

### Verificar que Tkinter está disponible

```bash
python -m tkinter
```

Si se abre una pequeña ventana de prueba, Tkinter está correctamente instalado.

---

## 🚀 Cómo ejecutar

### Versión con grafos visuales (recomendada)

```bash
python algoritmos_grafos_visual.py
```

### Versión con tablas

```bash
python algoritmos_grafos_gui.py
```

### Solo los algoritmos en consola

```bash
python algoritmos_grafos.py
```

---

## 🖥️ Interfaz gráfica

La aplicación se organiza en **4 pestañas**, una por algoritmo:

| Pestaña | Color | Contenido |
|---|---|---|
| Dijkstra | 🔵 Azul | Grafo con camino mínimo resaltado + tabla de distancias |
| Floyd | 🟣 Púrpura | Grafo dirigido + matriz de distancias mínimas |
| Warshall | 🟠 Naranja | Grafo original y grafo de clausura transitiva |
| Kruskal | 🟡 Dorado | Grafo completo con MST resaltado + lista de aristas seleccionadas |

Todas las pestañas tienen **scroll vertical** para ver el contenido completo.

---

## 📐 Datos de ejemplo utilizados

### Dijkstra
```
A→B(4), A→C(2), B→C(5), B→D(10)
C→E(3), E→D(4), E→F(7), D→F(11)
Origen: A
```

### Floyd-Warshall
```
Matriz 4×4 con nodos A, B, C, D
Aristas: A→B(3), A→D(7), B→A(8), B→C(2),
         C→A(5), C→D(1), D→A(2)
```

### Warshall
```
Grafo lineal: 0→1→2→3
Resultado: todos los nodos anteriores alcanzan a los posteriores
```

### Kruskal
```
Nodos: A, B, C, D, E
Aristas: A-B(1), B-D(2), A-C(3), B-C(4),
         C-D(5), C-E(6), D-E(7)
MST: A-B(1) + B-D(2) + A-C(3) + C-E(6) = 12
```

---

## 🗂️ Estructura del código

```
algoritmos_grafos_visual.py
│
├── Algoritmos
│   ├── dijkstra()
│   ├── floyd_warshall()
│   ├── warshall()
│   ├── UnionFind (clase auxiliar)
│   └── kruskal()
│
├── GraphCanvas (clase)
│   ├── place_nodes_circle()
│   ├── place_nodes_custom()
│   ├── draw_edge()
│   ├── draw_curved_edge()
│   ├── draw_node()
│   ├── draw_all_nodes()
│   └── draw_legend()
│
└── Pestañas
    ├── build_dijkstra()
    ├── build_floyd()
    ├── build_warshall()
    └── build_kruskal()
```

---

## 📚 Referencias

- Cormen, T. H. et al. — *Introduction to Algorithms* (CLRS)
- Sedgewick, R. — *Algorithms in Java*
- Documentación oficial de Python: [tkinter](https://docs.python.org/3/library/tkinter.html)