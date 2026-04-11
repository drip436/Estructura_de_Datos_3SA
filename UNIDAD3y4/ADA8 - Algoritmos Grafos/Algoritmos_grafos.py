"""
=============================================================
  ALGORITMOS DE GRAFOS  —  Visualización Gráfica con Tkinter
  Dibuja los grafos con nodos y aristas sobre Canvas
  - Dijkstra
  - Floyd-Warshall
  - Warshall (Clausura Transitiva)
  - Kruskal
=============================================================
"""

import heapq
import math
import tkinter as tk
from tkinter import ttk

INF = float('inf')

# ══════════════════════════════════════════════════════════
#  ALGORITMOS
# ══════════════════════════════════════════════════════════

def dijkstra(grafo, inicio):
    dist = {n: INF for n in grafo}
    dist[inicio] = 0
    prev = {n: None for n in grafo}
    heap = [(0, inicio)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in grafo[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def floyd_warshall(nodos, matriz):
    n = len(nodos)
    d = [r[:] for r in matriz]
    nxt = [[j if matriz[i][j] != INF and i != j else None
            for j in range(n)] for i in range(n)]
    for i in range(n):
        nxt[i][i] = i
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] != INF and d[k][j] != INF and d[i][k]+d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
                    nxt[i][j] = nxt[i][k]
    return d, nxt


def warshall(matriz):
    n = len(matriz)
    r = [row[:] for row in matriz]
    for i in range(n):
        r[i][i] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                r[i][j] = r[i][j] or (r[i][k] and r[k][j])
    return r


class UnionFind:
    def __init__(self, nodes):
        self.p = {n: n for n in nodes}
        self.r = {n: 0 for n in nodes}
    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return False
        if self.r[rx] < self.r[ry]: rx, ry = ry, rx
        self.p[ry] = rx
        if self.r[rx] == self.r[ry]: self.r[rx] += 1
        return True


def kruskal(nodos, aristas):
    uf = UnionFind(nodos)
    mst, cost = [], 0
    for w, u, v in sorted(aristas):
        if uf.union(u, v):
            mst.append((w, u, v))
            cost += w
            if len(mst) == len(nodos)-1: break
    return mst, cost


# ══════════════════════════════════════════════════════════
#  PALETA
# ══════════════════════════════════════════════════════════
BG       = "#0d1117"
PANEL    = "#161b22"
CARD     = "#1c2030"
BORDER   = "#30363d"
ACCENT   = "#58a6ff"
GREEN    = "#3fb950"
YELLOW   = "#d29922"
ORANGE   = "#f0883e"
RED      = "#f85149"
PURPLE   = "#bc8cff"
MUTED    = "#8b949e"
WHITE    = "#e6edf3"
GOLD     = "#ffd700"
NODE_BG  = "#21262d"
NODE_OUT = "#58a6ff"
EDGE_COL = "#444c56"
PATH_COL = "#3fb950"
MST_COL  = "#ffd700"
UNSEL    = "#30363d"

# ══════════════════════════════════════════════════════════
#  DIBUJADOR DE GRAFOS BASE
# ══════════════════════════════════════════════════════════

class GraphCanvas(tk.Canvas):
    """Canvas que dibuja un grafo con nodos, aristas y pesos."""

    R = 22   # radio del nodo

    def __init__(self, parent, width=680, height=300, **kw):
        super().__init__(parent, width=width, height=height,
                         bg=PANEL, highlightthickness=0, **kw)
        self.node_pos  = {}   # nombre → (cx, cy)
        self.drawn_nodes = {}

    # ── posiciones en círculo / custom ──────────────────
    def place_nodes_circle(self, names, cx, cy, r):
        n = len(names)
        for i, name in enumerate(names):
            angle = -math.pi/2 + 2*math.pi*i/n
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            self.node_pos[name] = (x, y)

    def place_nodes_custom(self, positions):
        self.node_pos = positions

    # ── dibujo de aristas ────────────────────────────────
    def draw_edge(self, u, v, label="", color=EDGE_COL,
                  width=2, arrow=False, dash=()):
        x1, y1 = self.node_pos[u]
        x2, y2 = self.node_pos[v]
        # acortar para no tapar nodos
        dx, dy = x2-x1, y2-y1
        dist = math.hypot(dx, dy) or 1
        ox, oy = dx/dist*self.R, dy/dist*self.R
        arr = tk.LAST if arrow else tk.NONE
        self.create_line(x1+ox, y1+oy, x2-ox, y2-oy,
                         fill=color, width=width,
                         arrow=arr, arrowshape=(10,12,4),
                         dash=dash, smooth=False)
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            # desplazar label perpendicular
            nx, ny = -dy/dist*13, dx/dist*13
            self.create_text(mx+nx, my+ny, text=label,
                             fill=YELLOW, font=("Consolas", 9, "bold"))

    def draw_curved_edge(self, u, v, label="", color=EDGE_COL,
                         width=2, arrow=False, curve=30):
        """Arista curva para grafos dirigidos con aristas bidireccionales."""
        x1, y1 = self.node_pos[u]
        x2, y2 = self.node_pos[v]
        dx, dy = x2-x1, y2-y1
        dist = math.hypot(dx, dy) or 1
        # punto de control perpendicular
        mx, my = (x1+x2)/2 + (-dy/dist)*curve, (y1+y2)/2 + (dx/dist)*curve
        arr = tk.LAST if arrow else tk.NONE
        self.create_line(x1, y1, mx, my, x2, y2,
                         fill=color, width=width, smooth=True,
                         arrow=arr, arrowshape=(10,12,4))
        if label:
            lx = (x1 + 2*mx + x2)/4
            ly = (y1 + 2*my + y2)/4
            self.create_text(lx, ly, text=label,
                             fill=YELLOW, font=("Consolas", 9, "bold"))

    # ── dibujo de nodo ───────────────────────────────────
    def draw_node(self, name, outline=NODE_OUT, fill=NODE_BG,
                  text_color=WHITE, radius=None):
        r = radius or self.R
        x, y = self.node_pos[name]
        self.create_oval(x-r, y-r, x+r, y+r,
                         fill=fill, outline=outline, width=2)
        self.create_text(x, y, text=str(name),
                         fill=text_color, font=("Consolas", 11, "bold"))

    def draw_all_nodes(self, names=None, outline=NODE_OUT,
                       fill=NODE_BG, highlights=None):
        highlights = highlights or {}
        ns = names or list(self.node_pos.keys())
        for name in ns:
            o = highlights.get(name, {}).get("outline", outline)
            f = highlights.get(name, {}).get("fill",    fill)
            t = highlights.get(name, {}).get("text",    WHITE)
            self.draw_node(name, outline=o, fill=f, text_color=t)

    # ── leyenda ──────────────────────────────────────────
    def draw_legend(self, items, x=10, y=10):
        """items = [(color, texto), ...]"""
        for i, (col, txt) in enumerate(items):
            yy = y + i*20
            self.create_oval(x, yy+2, x+12, yy+14,
                             fill=col, outline=col)
            self.create_text(x+20, yy+8, text=txt,
                             anchor="w", fill=MUTED,
                             font=("Consolas", 9))


# ══════════════════════════════════════════════════════════
#  FRAME DE SECCIÓN CON TÍTULO
# ══════════════════════════════════════════════════════════

def make_section(parent, title, accent=ACCENT):
    frm = tk.Frame(parent, bg=PANEL)
    frm.pack(fill="x", padx=0, pady=0)
    hdr = tk.Frame(frm, bg=CARD)
    hdr.pack(fill="x")
    tk.Frame(hdr, bg=accent, width=4).pack(side="left", fill="y")
    tk.Label(hdr, text=f"  {title}",
             font=("Consolas", 12, "bold"),
             bg=CARD, fg=accent,
             pady=8).pack(side="left")
    body = tk.Frame(frm, bg=PANEL)
    body.pack(fill="x", padx=0)
    return body


def info_row(parent, label, value, lc=MUTED, vc=WHITE):
    r = tk.Frame(parent, bg=PANEL)
    r.pack(anchor="w", padx=20, pady=1)
    tk.Label(r, text=label, font=("Consolas", 10),
             bg=PANEL, fg=lc).pack(side="left")
    tk.Label(r, text=value, font=("Consolas", 10, "bold"),
             bg=PANEL, fg=vc).pack(side="left")


# ══════════════════════════════════════════════════════════
#  PESTAÑA: DIJKSTRA
# ══════════════════════════════════════════════════════════

def build_dijkstra(parent):
    grafo = {
        "A": [("B", 4), ("C", 2)],
        "B": [("C", 5), ("D", 10)],
        "C": [("E", 3)],
        "D": [("F", 11)],
        "E": [("D", 4), ("F", 7)],
        "F": [],
    }
    inicio = "A"
    dist, prev = dijkstra(grafo, inicio)

    # reconstruir camino más corto a F
    camino_F = []
    n = "F"
    while n:
        camino_F.append(n)
        n = prev[n]
    camino_F.reverse()
    aristas_camino = set(zip(camino_F, camino_F[1:]))

    body = make_section(parent, "Dijkstra — Camino más corto desde A", ACCENT)

    cv = GraphCanvas(body, width=680, height=310)
    cv.pack(pady=(8, 4), padx=10)

    # posiciones
    pos = {
        "A": (80,  155),
        "B": (220, 70),
        "C": (220, 240),
        "E": (380, 240),
        "D": (380, 70),
        "F": (540, 155),
    }
    cv.place_nodes_custom(pos)

    # aristas
    aristas = [
        ("A","B",4), ("A","C",2), ("B","C",5), ("B","D",10),
        ("C","E",3), ("E","D",4), ("E","F",7), ("D","F",11),
    ]
    for u, v, w in aristas:
        en_path = (u,v) in aristas_camino
        cv.draw_edge(u, v, str(w),
                     color=PATH_COL if en_path else EDGE_COL,
                     width=3 if en_path else 1.5,
                     arrow=True)

    # nodos
    hl = {}
    for name in grafo:
        if name == inicio:
            hl[name] = {"fill": ACCENT,    "outline": WHITE,  "text": BG}
        elif name in camino_F:
            hl[name] = {"fill": "#1a3a1a", "outline": GREEN,  "text": GREEN}
        else:
            hl[name] = {"fill": NODE_BG,   "outline": EDGE_COL, "text": MUTED}
    cv.draw_all_nodes(highlights=hl)

    # leyenda
    cv.draw_legend([
        (ACCENT, "Nodo origen (A)"),
        (GREEN,  "Camino más corto → F"),
        (EDGE_COL, "Otras aristas"),
    ], x=14, y=10)

    # tabla de distancias
    body2 = make_section(parent, "Distancias mínimas desde A", GREEN)
    tbl = tk.Frame(body2, bg=PANEL)
    tbl.pack(padx=20, pady=6)
    hdr_cols = ["Nodo", "Distancia", "Ruta"]
    for c, h in enumerate(hdr_cols):
        tk.Label(tbl, text=h, font=("Consolas", 10, "bold"),
                 bg=CARD, fg=ACCENT, width=16, pady=5,
                 relief="flat").grid(row=0, column=c, padx=1, pady=1)
    for r, (nodo, d) in enumerate(sorted(dist.items()), 1):
        # reconstruir ruta
        ruta, n2 = [], nodo
        while n2:
            ruta.append(n2); n2 = prev[n2]
        ruta.reverse()
        ruta_txt = " → ".join(ruta) if ruta else nodo
        val = str(int(d)) if d != INF else "∞"
        bg = "#1a3a1a" if nodo in camino_F else CARD
        fc = GREEN if nodo in camino_F else WHITE
        for c, txt in enumerate([nodo, val, ruta_txt]):
            tk.Label(tbl, text=txt, font=("Consolas", 10),
                     bg=bg, fg=fc, width=16, pady=4).grid(
                row=r, column=c, padx=1, pady=1)


# ══════════════════════════════════════════════════════════
#  PESTAÑA: FLOYD-WARSHALL
# ══════════════════════════════════════════════════════════

def build_floyd(parent):
    nodos  = ["A", "B", "C", "D"]
    I = INF
    matriz = [
        [0, 3, I, 7],
        [8, 0, 2, I],
        [5, I, 0, 1],
        [2, I, I, 0],
    ]
    d, nxt = floyd_warshall(nodos, matriz)

    body = make_section(parent, "Floyd-Warshall — Todos los caminos más cortos", PURPLE)

    cv = GraphCanvas(body, width=680, height=280)
    cv.pack(pady=(8,4), padx=10)

    pos = {"A":(120,80), "B":(560,80), "C":(560,220), "D":(120,220)}
    cv.place_nodes_custom(pos)

    # aristas originales (bidireccionales — usar curvas)
    pares_dibujados = set()
    for i, u in enumerate(nodos):
        for j, v in enumerate(nodos):
            if i != j and matriz[i][j] != INF:
                par = tuple(sorted([u,v]))
                inv = matriz[j][i] != INF
                if par not in pares_dibujados:
                    if inv:
                        cv.draw_curved_edge(u, v, str(int(matriz[i][j])),
                                            color=EDGE_COL, arrow=True, curve=28)
                        cv.draw_curved_edge(v, u, str(int(matriz[j][i])),
                                            color=EDGE_COL, arrow=True, curve=28)
                    else:
                        cv.draw_edge(u, v, str(int(matriz[i][j])),
                                     color=EDGE_COL, arrow=True)
                    pares_dibujados.add(par)

    cv.draw_all_nodes(outline=PURPLE, fill=NODE_BG)

    cv.draw_legend([
        (PURPLE,   "Nodo del grafo"),
        (YELLOW,   "Peso de la arista"),
        (EDGE_COL, "Arista dirigida"),
    ], x=14, y=10)

    # tabla de resultado
    body2 = make_section(parent, "Matriz de distancias mínimas (resultado)", GREEN)
    tbl = tk.Frame(body2, bg=PANEL)
    tbl.pack(padx=20, pady=6)

    # cabecera
    tk.Label(tbl, text=" ", width=4, bg=CARD,
             font=("Consolas",10,"bold")).grid(row=0, column=0, padx=1, pady=1)
    for c, n in enumerate(nodos, 1):
        tk.Label(tbl, text=n, width=8, bg=CARD, fg=PURPLE,
                 font=("Consolas",10,"bold"), pady=5).grid(row=0, column=c, padx=1, pady=1)

    for i, n in enumerate(nodos):
        tk.Label(tbl, text=n, width=4, bg=CARD, fg=PURPLE,
                 font=("Consolas",10,"bold"), pady=4).grid(row=i+1, column=0, padx=1, pady=1)
        for j in range(len(nodos)):
            v = d[i][j]
            val = str(int(v)) if v != INF else "∞"
            bg = CARD if i == j else ("#1a2a1a" if v != INF else "#2a1a1a")
            fg = MUTED if i == j else (GREEN if v != INF else RED)
            tk.Label(tbl, text=val, width=8, bg=bg, fg=fg,
                     font=("Consolas",10), pady=4).grid(row=i+1, column=j+1, padx=1, pady=1)


# ══════════════════════════════════════════════════════════
#  PESTAÑA: WARSHALL
# ══════════════════════════════════════════════════════════

def build_warshall(parent):
    nodos  = ["0", "1", "2", "3"]
    matriz = [
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1],
        [0,0,0,0],
    ]
    result = warshall(matriz)

    body = make_section(parent, "Warshall — Clausura Transitiva (aristas directas)", ORANGE)

    cv = GraphCanvas(body, width=680, height=230)
    cv.pack(pady=(8,4), padx=10)

    pos = {"0":(120,115), "1":(280,115), "2":(420,115), "3":(560,115)}
    cv.place_nodes_custom(pos)

    for i in range(len(nodos)):
        for j in range(len(nodos)):
            if i != j and matriz[i][j]:
                cv.draw_edge(nodos[i], nodos[j], "",
                             color=ORANGE, width=2, arrow=True)

    cv.draw_all_nodes(outline=ORANGE)

    cv.draw_legend([
        (ORANGE, "Arista directa original"),
    ], x=14, y=10)

    # grafo de clausura
    body2 = make_section(parent, "Grafo tras clausura transitiva (todos los caminos)", GREEN)

    cv2 = GraphCanvas(body2, width=680, height=230)
    cv2.pack(pady=(8,4), padx=10)

    pos2 = {"0":(120,115), "1":(280,115), "2":(420,115), "3":(560,115)}
    cv2.place_nodes_custom(pos2)

    for i in range(len(nodos)):
        for j in range(len(nodos)):
            if i != j and result[i][j]:
                is_orig = bool(matriz[i][j])
                cv2.draw_curved_edge(nodos[i], nodos[j], "",
                                     color=GREEN if not is_orig else ORANGE,
                                     width=2 if not is_orig else 2.5,
                                     arrow=True,
                                     curve=0 if is_orig else 35)

    cv2.draw_all_nodes(outline=GREEN)
    cv2.draw_legend([
        (ORANGE, "Arista original"),
        (GREEN,  "Arista inferida (clausura)"),
    ], x=14, y=10)

    # tabla de alcanzabilidad
    body3 = make_section(parent, "Matriz de alcanzabilidad", ORANGE)
    tbl = tk.Frame(body3, bg=PANEL)
    tbl.pack(padx=20, pady=6)

    tk.Label(tbl, text=" ", width=4, bg=CARD,
             font=("Consolas",10,"bold")).grid(row=0, column=0, padx=1, pady=1)
    for c, n in enumerate(nodos,1):
        tk.Label(tbl, text=n, width=6, bg=CARD, fg=ORANGE,
                 font=("Consolas",10,"bold"),pady=5).grid(row=0,column=c,padx=1,pady=1)

    for i, ni in enumerate(nodos):
        tk.Label(tbl, text=ni, width=4, bg=CARD, fg=ORANGE,
                 font=("Consolas",10,"bold"),pady=4).grid(row=i+1,column=0,padx=1,pady=1)
        for j in range(len(nodos)):
            v = result[i][j]
            bg = "#1a2a1a" if v else "#2a1a1a"
            fg = GREEN     if v else RED
            tk.Label(tbl, text=str(v), width=6, bg=bg, fg=fg,
                     font=("Consolas",10),pady=4).grid(row=i+1,column=j+1,padx=1,pady=1)


# ══════════════════════════════════════════════════════════
#  PESTAÑA: KRUSKAL
# ══════════════════════════════════════════════════════════

def build_kruskal(parent):
    nodos   = ["A","B","C","D","E"]
    aristas = [
        (1,"A","B"),(3,"A","C"),(4,"B","C"),
        (2,"B","D"),(5,"C","D"),(6,"C","E"),(7,"D","E"),
    ]
    mst, costo = kruskal(nodos, aristas)
    mst_set = {(u,v) for _,u,v in mst} | {(v,u) for _,u,v in mst}

    body = make_section(parent, "Kruskal — Todas las aristas del grafo", GOLD)

    cv = GraphCanvas(body, width=680, height=290)
    cv.pack(pady=(8,4), padx=10)

    pos = {
        "A":(120,145),
        "B":(290, 65),
        "C":(290,225),
        "D":(460, 65),
        "E":(460,225),
    }
    cv.place_nodes_custom(pos)

    for w, u, v in aristas:
        en_mst = (u,v) in mst_set
        cv.draw_edge(u, v, str(w),
                     color=MST_COL  if en_mst else UNSEL,
                     width=3.5      if en_mst else 1.5,
                     dash=()        if en_mst else (4,3))

    hl = {}
    for n in nodos:
        hl[n] = {"fill": "#2a2200" if True else NODE_BG,
                 "outline": GOLD, "text": GOLD}
    cv.draw_all_nodes(highlights=hl)

    cv.draw_legend([
        (GOLD,  "Arista del MST"),
        (UNSEL, "Arista descartada"),
    ], x=14, y=10)

    # info del MST
    body2 = make_section(parent, "Árbol de Expansión Mínima — aristas seleccionadas", GREEN)
    tbl = tk.Frame(body2, bg=PANEL)
    tbl.pack(padx=20, pady=6)

    for c, h in enumerate(["#", "Nodo U", "Nodo V", "Peso"]):
        tk.Label(tbl, text=h, width=10, bg=CARD, fg=GOLD,
                 font=("Consolas",10,"bold"),pady=5).grid(row=0,column=c,padx=1,pady=1)

    for i, (w, u, v) in enumerate(mst, 1):
        for c, (txt, fc) in enumerate([
            (str(i),  MUTED),
            (u,       ACCENT),
            (v,       ACCENT),
            (str(w),  GOLD),
        ]):
            tk.Label(tbl, text=txt, width=10, bg="#1e1900", fg=fc,
                     font=("Consolas",10),pady=4).grid(row=i,column=c,padx=1,pady=1)

    body3 = make_section(parent, "Costo total del MST", GREEN)
    tk.Label(body3, text=f"  Σ pesos del MST  =  {costo}",
             font=("Consolas", 13, "bold"),
             bg=PANEL, fg=GREEN, pady=8).pack(anchor="w", padx=20)


# ══════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL
# ══════════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    root.title("Algoritmos de Grafos — Visualización")
    root.configure(bg=BG)
    root.geometry("740x700")
    root.resizable(True, True)

    # ── Header ──────────────────────────────────────────
    hdr = tk.Frame(root, bg="#1c2030", height=52)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    tk.Label(hdr, text="  ◈  Algoritmos de Grafos",
             font=("Consolas", 15, "bold"),
             bg="#1c2030", fg=WHITE).pack(side="left", padx=16)
    tk.Label(hdr, text="Visualización con nodos y aristas  ",
             font=("Consolas", 9),
             bg="#1c2030", fg=MUTED).pack(side="right", padx=16)
    tk.Frame(root, bg=ACCENT, height=2).pack(fill="x")

    # ── Tabs ────────────────────────────────────────────
    style = ttk.Style()
    style.theme_use("default")
    style.configure("G.TNotebook",
                    background=BG, borderwidth=0, tabmargins=0)
    style.configure("G.TNotebook.Tab",
                    background=CARD, foreground=MUTED,
                    font=("Consolas", 10, "bold"),
                    padding=[18, 9], borderwidth=0)
    style.map("G.TNotebook.Tab",
              background=[("selected", PANEL)],
              foreground=[("selected", WHITE)])

    nb = ttk.Notebook(root, style="G.TNotebook")
    nb.pack(fill="both", expand=True)

    tabs_info = [
        ("  Dijkstra  ",  ACCENT,  build_dijkstra),
        ("  Floyd     ",  PURPLE,  build_floyd),
        ("  Warshall  ",  ORANGE,  build_warshall),
        ("  Kruskal   ",  GOLD,    build_kruskal),
    ]

    for label, accent, builder in tabs_info:
        outer = tk.Frame(nb, bg=BG)
        nb.add(outer, text=label)
        tk.Frame(outer, bg=accent, height=2).pack(fill="x")

        canvas = tk.Canvas(outer, bg=PANEL, highlightthickness=0)
        sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=PANEL)
        win = canvas.create_window((0,0), window=inner, anchor="nw")

        inner.bind("<Configure>",
                   lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e, c=canvas, w=win: c.itemconfig(w, width=e.width))
        canvas.bind_all("<MouseWheel>",
                        lambda e, c=canvas: c.yview_scroll(int(-1*(e.delta/120)),"units"))

        builder(inner)

    root.mainloop()


if __name__ == "__main__":
    main()