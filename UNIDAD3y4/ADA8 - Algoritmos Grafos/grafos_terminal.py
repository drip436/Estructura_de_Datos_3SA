"""
=============================================================
  ALGORITMOS DE GRAFOS
  - Dijkstra
  - Floyd-Warshall (distancias)
  - Warshall (clausura transitiva)
  - Kruskal (árbol de expansión mínima)
=============================================================
"""

import heapq

INF = float('inf')


# ─────────────────────────────────────────────
# 1. ALGORITMO DE DIJKSTRA
# ─────────────────────────────────────────────
def dijkstra(grafo: dict, inicio: str) -> dict:
    """
    Encuentra la distancia más corta desde 'inicio' hacia
    todos los demás nodos usando el algoritmo de Dijkstra.

    Parámetros:
        grafo  : dict  → { nodo: [(vecino, peso), ...] }
        inicio : str   → nodo de partida

    Retorna:
        dict con la distancia mínima a cada nodo.
    """
    distancias = {nodo: INF for nodo in grafo}
    distancias[inicio] = 0
    cola = [(0, inicio)]          # (costo, nodo)

    while cola:
        costo_actual, nodo_actual = heapq.heappop(cola)

        if costo_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in grafo[nodo_actual]:
            nueva_dist = distancias[nodo_actual] + peso
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                heapq.heappush(cola, (nueva_dist, vecino))

    return distancias


# ─────────────────────────────────────────────
# 2. ALGORITMO DE FLOYD-WARSHALL
# ─────────────────────────────────────────────
def floyd_warshall(matriz: list) -> list:
    """
    Calcula las distancias más cortas entre TODOS los pares
    de nodos usando el algoritmo de Floyd-Warshall.

    Parámetros:
        matriz : list[list[float]] → matriz de adyacencia N×N
                 (usa INF para indicar que no hay arista directa)

    Retorna:
        Matriz N×N con las distancias mínimas entre cada par.
    """
    n = len(matriz)
    dist = [fila[:] for fila in matriz]   # copia profunda

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


# ─────────────────────────────────────────────
# 3. ALGORITMO DE WARSHALL (Clausura Transitiva)
# ─────────────────────────────────────────────
def warshall(matriz: list) -> list:
    """
    Determina la clausura transitiva de un grafo dirigido.
    Si alcance[i][j] == 1, existe un camino de i hacia j.

    Parámetros:
        matriz : list[list[int]] → matriz de adyacencia N×N (0/1)

    Retorna:
        Matriz N×N de alcanzabilidad (0/1).
    """
    n = len(matriz)
    alcance = [fila[:] for fila in matriz]   # copia profunda

    # Un nodo siempre se alcanza a sí mismo
    for i in range(n):
        alcance[i][i] = 1

    for k in range(n):
        for i in range(n):
            for j in range(n):
                alcance[i][j] = alcance[i][j] or (alcance[i][k] and alcance[k][j])

    return alcance


# ─────────────────────────────────────────────
# 4. ALGORITMO DE KRUSKAL
# ─────────────────────────────────────────────
class _UnionFind:
    """Estructura Union-Find para el algoritmo de Kruskal."""
    def __init__(self, nodos):
        self.padre = {n: n for n in nodos}
        self.rango  = {n: 0 for n in nodos}

    def encontrar(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.encontrar(self.padre[x])
        return self.padre[x]

    def unir(self, x, y) -> bool:
        rx, ry = self.encontrar(x), self.encontrar(y)
        if rx == ry:
            return False
        if self.rango[rx] < self.rango[ry]:
            rx, ry = ry, rx
        self.padre[ry] = rx
        if self.rango[rx] == self.rango[ry]:
            self.rango[rx] += 1
        return True


def kruskal(nodos: list, aristas: list) -> tuple:
    """
    Construye el Árbol de Expansión Mínima (MST) usando
    el algoritmo de Kruskal.

    Parámetros:
        nodos   : list → lista de nodos del grafo
        aristas : list → [(peso, u, v), ...]

    Retorna:
        (mst, costo_total)
        mst         → lista de aristas seleccionadas [(peso, u, v)]
        costo_total → suma de los pesos del MST
    """
    uf = _UnionFind(nodos)
    aristas_ordenadas = sorted(aristas, key=lambda e: e[0])
    mst = []
    costo_total = 0

    for peso, u, v in aristas_ordenadas:
        if uf.unir(u, v):
            mst.append((peso, u, v))
            costo_total += peso
            if len(mst) == len(nodos) - 1:
                break

    return mst, costo_total


# =============================================================
#  DEMOSTRACIÓN DE LOS ALGORITMOS
# =============================================================
def _separador(titulo: str):
    print("\n" + "=" * 55)
    print(f"  {titulo}")
    print("=" * 55)


def _demo_dijkstra():
    _separador("DIJKSTRA – Camino más corto desde un origen")
    grafo = {
        "A": [("B", 4), ("C", 2)],
        "B": [("C", 5), ("D", 10)],
        "C": [("E", 3)],
        "D": [("F", 11)],
        "E": [("D", 4), ("F", 7)],
        "F": [],
    }
    inicio = "A"
    distancias = dijkstra(grafo, inicio)
    print(f"\n  Grafo : A→B(4), A→C(2), B→C(5), B→D(10),")
    print(f"          C→E(3), E→D(4), E→F(7), D→F(11)")
    print(f"\n  Distancias mínimas desde '{inicio}':")
    for nodo, dist in sorted(distancias.items()):
        valor = str(dist) if dist != INF else "∞"
        print(f"    {inicio} → {nodo} : {valor}")


def _demo_floyd():
    _separador("FLOYD-WARSHALL – Todos los caminos más cortos")
    I = INF
    matriz = [
        # A   B   C   D
        [0,  3,  I,  7],   # A
        [8,  0,  2,  I],   # B
        [5,  I,  0,  1],   # C
        [2,  I,  I,  0],   # D
    ]
    nodos = ["A", "B", "C", "D"]
    resultado = floyd_warshall(matriz)
    print("\n  Matriz de distancias original (∞ = sin arista):")
    print("       " + "  ".join(f"{n:>4}" for n in nodos))
    for i, fila in enumerate(matriz):
        valores = ["  ∞" if v == INF else f"{v:>4}" for v in fila]
        print(f"  {nodos[i]}  {'  '.join(valores)}")
    print("\n  Matriz de distancias mínimas tras Floyd-Warshall:")
    print("       " + "  ".join(f"{n:>4}" for n in nodos))
    for i, fila in enumerate(resultado):
        valores = ["  ∞" if v == INF else f"{v:>4}" for v in fila]
        print(f"  {nodos[i]}  {'  '.join(valores)}")


def _demo_warshall():
    _separador("WARSHALL – Clausura Transitiva")
    matriz = [
        # 0  1  2  3
        [0, 1, 0, 0],   # 0
        [0, 0, 1, 0],   # 1
        [0, 0, 0, 1],   # 2
        [0, 0, 0, 0],   # 3
    ]
    resultado = warshall(matriz)
    print("\n  Matriz de adyacencia original:")
    print("      0  1  2  3")
    for i, fila in enumerate(matriz):
        print(f"  {i}  {'  '.join(map(str, fila))}")
    print("\n  Clausura transitiva (1 = existe camino):")
    print("      0  1  2  3")
    for i, fila in enumerate(resultado):
        print(f"  {i}  {'  '.join(map(str, fila))}")
    print()
    for i in range(len(resultado)):
        for j in range(len(resultado)):
            if resultado[i][j]:
                print(f"    Nodo {i} puede alcanzar al nodo {j}")


def _demo_kruskal():
    _separador("KRUSKAL – Árbol de Expansión Mínima (MST)")
    nodos   = ["A", "B", "C", "D", "E"]
    aristas = [
        (1, "A", "B"),
        (3, "A", "C"),
        (4, "B", "C"),
        (2, "B", "D"),
        (5, "C", "D"),
        (6, "C", "E"),
        (7, "D", "E"),
    ]
    mst, costo = kruskal(nodos, aristas)
    print("\n  Aristas disponibles (peso, u, v):")
    for peso, u, v in aristas:
        print(f"    {u} — {v} : {peso}")
    print("\n  Aristas seleccionadas en el MST:")
    for peso, u, v in mst:
        print(f"    {u} — {v} : {peso}")
    print(f"\n  Costo total del MST : {costo}")


if __name__ == "__main__":
    _demo_dijkstra()
    _demo_floyd()
    _demo_warshall()
    _demo_kruskal()
    print("\n" + "=" * 55 + "\n")