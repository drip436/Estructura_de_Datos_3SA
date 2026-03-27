"""
TDA Grafo - Aplicación Visual Completa
Implementa todas las operaciones del TDA Grafo de las diapositivas.
Requiere: pip install networkx matplotlib
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches


# ─────────────────────────────────────────────
#  TDA GRAFO  (lógica pura, sin UI)
# ─────────────────────────────────────────────
class TDAGrafo:
    """Implementa el TDA Grafo con todas las operaciones de las diapositivas."""

    def __init__(self):
        self._G = nx.Graph()          # grafo mixto simulado
        self._directed_edges = set()  # aristas marcadas como dirigidas
        self._vertex_data = {}        # vértice -> objeto info
        self._edge_data = {}          # (u,v) -> objeto info
        self._vertex_id = 0
        self._edge_id = 0

    # ── Operaciones posicionales ────────────────
    def tamano(self):
        return self.numVertices() + self.numAristas()

    def estaVacio(self):
        return self.numVertices() == 0

    def elementos(self):
        v_elems = {v: self._vertex_data.get(v, "") for v in self._G.nodes()}
        e_elems = {e: self._edge_data.get(e, "") for e in self._G.edges()}
        return v_elems, e_elems

    def posiciones(self):
        return list(self._G.nodes()), list(self._G.edges())

    def reemplazar(self, p, r):
        """Reemplaza el elemento en posición p (vértice o arista) por r."""
        if p in self._G.nodes():
            self._vertex_data[p] = r
            return True
        for e in self._G.edges():
            if e == p or (e[1], e[0]) == p:
                self._edge_data[e] = r
                return True
        return False

    def intercambiar(self, p, q):
        """Intercambia los elementos en posiciones p y q."""
        dp = self._vertex_data.get(p) if p in self._G.nodes() else self._edge_data.get(p)
        dq = self._vertex_data.get(q) if q in self._G.nodes() else self._edge_data.get(q)
        self.reemplazar(p, dq)
        self.reemplazar(q, dp)

    # ── Operaciones generales ───────────────────
    def numVertices(self):
        return self._G.number_of_nodes()

    def numAristas(self):
        return self._G.number_of_edges()

    def vertices(self):
        return list(self._G.nodes())

    def aristas(self):
        return list(self._G.edges())

    def grado(self, v):
        if v not in self._G:
            raise ValueError(f"Vértice '{v}' no existe.")
        return self._G.degree(v)

    def verticesAdyacentes(self, v):
        if v not in self._G:
            raise ValueError(f"Vértice '{v}' no existe.")
        return list(self._G.neighbors(v))

    def aristasIncidentes(self, v):
        if v not in self._G:
            raise ValueError(f"Vértice '{v}' no existe.")
        return list(self._G.edges(v))

    def verticesFinales(self, e):
        if len(e) != 2:
            raise ValueError("Arista debe ser tupla (u, v).")
        u, v = e
        if not self._G.has_edge(u, v):
            raise ValueError(f"Arista {e} no existe.")
        return [u, v]

    def opuesto(self, v, e):
        u, w = e
        if u == v:
            return w
        if w == v:
            return u
        raise ValueError(f"'{v}' no es extremo de {e}.")

    def esAdyacente(self, v, w):
        return self._G.has_edge(v, w)

    # ── Operaciones de actualización ────────────
    def insertaVertice(self, o=""):
        self._vertex_id += 1
        nombre = f"V{self._vertex_id}"
        self._G.add_node(nombre)
        self._vertex_data[nombre] = o
        return nombre

    def insertaArista(self, v, w, o=""):
        if not self._G.has_node(v) or not self._G.has_node(w):
            raise ValueError("Uno o ambos vértices no existen.")
        self._G.add_edge(v, w)
        self._edge_data[(v, w)] = o
        return (v, w)

    def insertaAristaDirigida(self, v, w, o=""):
        e = self.insertaArista(v, w, o)
        self._directed_edges.add(e)
        return e

    def eliminaVertice(self, v):
        if v not in self._G:
            raise ValueError(f"Vértice '{v}' no existe.")
        # eliminar aristas dirigidas asociadas
        to_remove = [e for e in self._directed_edges if v in e]
        for e in to_remove:
            self._directed_edges.discard(e)
        self._G.remove_node(v)
        self._vertex_data.pop(v, None)

    def eliminaArista(self, e):
        u, v = e
        if not self._G.has_edge(u, v):
            raise ValueError(f"Arista {e} no existe.")
        self._G.remove_edge(u, v)
        self._directed_edges.discard(e)
        self._directed_edges.discard((v, u))
        self._edge_data.pop(e, None)
        self._edge_data.pop((v, u), None)

    def convierteNoDirigida(self, e):
        self._directed_edges.discard(e)
        self._directed_edges.discard((e[1], e[0]))

    def invierteDir(self, e):
        if e in self._directed_edges:
            self._directed_edges.discard(e)
            self._directed_edges.add((e[1], e[0]))
        elif (e[1], e[0]) in self._directed_edges:
            self._directed_edges.discard((e[1], e[0]))
            self._directed_edges.add(e)

    def asignaDesde(self, e, v):
        """Arista dirigida e sale del vértice v."""
        u, w = e
        self._directed_edges.discard(e)
        self._directed_edges.discard((w, u))
        if v == u:
            self._directed_edges.add((u, w))
        else:
            self._directed_edges.add((w, u))

    def asignaA(self, e, v):
        """Arista dirigida e entra al vértice v."""
        u, w = e
        self._directed_edges.discard(e)
        self._directed_edges.discard((w, u))
        if v == w:
            self._directed_edges.add((u, w))
        else:
            self._directed_edges.add((w, u))

    # ── Operaciones con aristas dirigidas ───────
    def aristasDirigidas(self):
        return [e for e in self._directed_edges if self._G.has_edge(*e)]

    def aristasNoDirigidas(self):
        todas = set(self._G.edges())
        return [e for e in todas if e not in self._directed_edges
                and (e[1], e[0]) not in self._directed_edges]

    def gradoEnt(self, v):
        return sum(1 for e in self._directed_edges if e[1] == v and self._G.has_edge(*e))

    def gradoSalida(self, v):
        return sum(1 for e in self._directed_edges if e[0] == v and self._G.has_edge(*e))

    def aristasIncidentesEnt(self, v):
        return [e for e in self._directed_edges if e[1] == v and self._G.has_edge(*e)]

    def aristasIncidentesSal(self, v):
        return [e for e in self._directed_edges if e[0] == v and self._G.has_edge(*e)]

    def verticesAdyacentesEnt(self, v):
        return [e[0] for e in self.aristasIncidentesEnt(v)]

    def verticesAdyacentesSal(self, v):
        return [e[1] for e in self.aristasIncidentesSal(v)]

    def destino(self, e):
        if e in self._directed_edges:
            return e[1]
        raise ValueError(f"Arista {e} no es dirigida.")

    def origen(self, e):
        if e in self._directed_edges:
            return e[0]
        raise ValueError(f"Arista {e} no es dirigida.")

    def esDirigida(self, e):
        return e in self._directed_edges or (e[1], e[0]) in self._directed_edges


# ─────────────────────────────────────────────
#  APLICACIÓN TKINTER
# ─────────────────────────────────────────────
DARK_BG   = "#0d1b2a"
PANEL_BG  = "#112233"
ACCENT    = "#f5a623"
ACCENT2   = "#4fc3f7"
TEXT      = "#e8eaf6"
SUCCESS   = "#66bb6a"
DANGER    = "#ef5350"
BTN_BG    = "#1a3a5c"
BTN_HOV   = "#2a5f8f"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TDA Grafo — Visualizador Interactivo")
        self.configure(bg=DARK_BG)
        self.geometry("1300x820")
        self.resizable(True, True)

        self.grafo = TDAGrafo()
        self.selected_node = None

        self._build_ui()
        self._draw_graph()

    # ── Layout principal ────────────────────────
    def _build_ui(self):
        # título
        header = tk.Frame(self, bg=DARK_BG)
        header.pack(fill="x", padx=12, pady=(10, 0))
        tk.Label(header, text="⬡  TDA GRAFO", font=("Courier", 22, "bold"),
                 fg=ACCENT, bg=DARK_BG).pack(side="left")
        tk.Label(header, text="Visualizador Interactivo",
                 font=("Courier", 12), fg=ACCENT2, bg=DARK_BG).pack(side="left", padx=16)

        # cuerpo
        body = tk.Frame(self, bg=DARK_BG)
        body.pack(fill="both", expand=True, padx=12, pady=8)

        # panel izquierdo
        left = tk.Frame(body, bg=PANEL_BG, width=340)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        # panel derecho (canvas matplotlib)
        right = tk.Frame(body, bg=DARK_BG)
        right.pack(side="left", fill="both", expand=True)

        self._build_controls(left)
        self._build_canvas(right)
        self._build_log()

    def _build_canvas(self, parent):
        self.fig, self.ax = plt.subplots(figsize=(7, 6), facecolor="#0a1520")
        self.ax.set_facecolor("#0a1520")
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.mpl_connect("button_press_event", self._on_canvas_click)

        # barra de info
        self.info_var = tk.StringVar(value="Listo. Haz clic en un vértice para seleccionarlo.")
        tk.Label(parent, textvariable=self.info_var, font=("Courier", 10),
                 fg=ACCENT2, bg=DARK_BG, anchor="w").pack(fill="x", padx=4)

    def _build_log(self):
        log_frame = tk.Frame(self, bg=PANEL_BG, height=120)
        log_frame.pack(fill="x", padx=12, pady=(0, 8))
        log_frame.pack_propagate(False)

        tk.Label(log_frame, text="📋 LOG DE OPERACIONES",
                 font=("Courier", 9, "bold"), fg=ACCENT, bg=PANEL_BG).pack(anchor="w", padx=6, pady=2)

        self.log_text = tk.Text(log_frame, bg="#060e18", fg=SUCCESS,
                                font=("Courier", 9), height=5, state="disabled",
                                bd=0, insertbackground=SUCCESS)
        scroll = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.log_text.pack(fill="both", expand=True, padx=4, pady=2)

    def _build_controls(self, parent):
        nb = ttk.Notebook(parent)
        nb.pack(fill="both", expand=True, padx=6, pady=6)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=PANEL_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=BTN_BG, foreground=TEXT,
                        font=("Courier", 9, "bold"), padding=[8, 4])
        style.map("TNotebook.Tab", background=[("selected", ACCENT)],
                  foreground=[("selected", DARK_BG)])

        tabs = [
            ("Vértices", self._tab_vertices),
            ("Aristas",  self._tab_aristas),
            ("Consultar", self._tab_consultas),
            ("Dirigidas", self._tab_dirigidas),
        ]
        for name, builder in tabs:
            frame = tk.Frame(nb, bg=PANEL_BG)
            nb.add(frame, text=name)
            builder(frame)

        # Info rápida abajo del notebook
        self.stats_var = tk.StringVar()
        tk.Label(parent, textvariable=self.stats_var, font=("Courier", 9),
                 fg=TEXT, bg=PANEL_BG, justify="left").pack(padx=8, pady=4, anchor="w")
        self._update_stats()

    # ── Tabs ────────────────────────────────────
    def _tab_vertices(self, parent):
        self._section(parent, "INSERTAR VÉRTICE")
        tk.Label(parent, text="Info del vértice (opcional):",
                 fg=TEXT, bg=PANEL_BG, font=("Courier", 9)).pack(anchor="w", padx=8)
        self.vert_info = tk.Entry(parent, **self._entry_style())
        self.vert_info.pack(fill="x", padx=8, pady=4)
        self._btn(parent, "➕  insertaVertice(o)", self._op_insertaVertice)

        self._section(parent, "ELIMINAR VÉRTICE")
        tk.Label(parent, text="Vértice a eliminar:", fg=TEXT, bg=PANEL_BG,
                 font=("Courier", 9)).pack(anchor="w", padx=8)
        self.del_vert = tk.Entry(parent, **self._entry_style())
        self.del_vert.pack(fill="x", padx=8, pady=4)
        self._btn(parent, "➖  eliminaVertice(v)", self._op_eliminaVertice, color=DANGER)

        self._section(parent, "REEMPLAZAR ELEMENTO")
        tk.Label(parent, text="Posición (vértice):", fg=TEXT, bg=PANEL_BG,
                 font=("Courier", 9)).pack(anchor="w", padx=8)
        self.remp_pos = tk.Entry(parent, **self._entry_style())
        self.remp_pos.pack(fill="x", padx=8, pady=2)
        tk.Label(parent, text="Nuevo valor:", fg=TEXT, bg=PANEL_BG,
                 font=("Courier", 9)).pack(anchor="w", padx=8)
        self.remp_val = tk.Entry(parent, **self._entry_style())
        self.remp_val.pack(fill="x", padx=8, pady=2)
        self._btn(parent, "🔄  reemplazar(p, r)", self._op_reemplazar)

    def _tab_aristas(self, parent):
        self._section(parent, "INSERTAR ARISTA")
        for lbl, attr in [("Vértice origen:", "ar_v"),
                           ("Vértice destino:", "ar_w"),
                           ("Info (objeto o):", "ar_o")]:
            tk.Label(parent, text=lbl, fg=TEXT, bg=PANEL_BG,
                     font=("Courier", 9)).pack(anchor="w", padx=8)
            e = tk.Entry(parent, **self._entry_style())
            e.pack(fill="x", padx=8, pady=2)
            setattr(self, attr, e)

        self._btn(parent, "↔  insertaArista(v,w,o)", self._op_insertaArista)
        self._btn(parent, "→  insertaAristaDirigida(v,w,o)",
                  self._op_insertaAristaDirigida, color="#ab47bc")

        self._section(parent, "ELIMINAR / MODIFICAR ARISTA")
        tk.Label(parent, text="Arista  v,w  (ej: V1,V2):", fg=TEXT, bg=PANEL_BG,
                 font=("Courier", 9)).pack(anchor="w", padx=8)
        self.del_ar = tk.Entry(parent, **self._entry_style())
        self.del_ar.pack(fill="x", padx=8, pady=2)
        self._btn(parent, "➖  eliminaArista(e)", self._op_eliminaArista, color=DANGER)
        self._btn(parent, "↔  convierteNoDirigida(e)", self._op_convierteNoDirigida)
        self._btn(parent, "⇄  invierteDir(e)", self._op_invierteDir)

    def _tab_consultas(self, parent):
        self._section(parent, "CONSULTAS GENERALES")
        self._btn(parent, "📊  tamano()", lambda: self._show("tamano()",
                  f"Tamaño = {self.grafo.tamano()} (vértices + aristas)"))
        self._btn(parent, "❓  estaVacio()", lambda: self._show("estaVacio()",
                  f"¿Está vacío? → {self.grafo.estaVacio()}"))
        self._btn(parent, "🔢  numVertices()", lambda: self._show("numVertices()",
                  f"Número de vértices = {self.grafo.numVertices()}"))
        self._btn(parent, "🔢  numAristas()", lambda: self._show("numAristas()",
                  f"Número de aristas = {self.grafo.numAristas()}"))
        self._btn(parent, "📋  vertices()", lambda: self._show("vertices()",
                  f"Vértices: {self.grafo.vertices()}"))
        self._btn(parent, "📋  aristas()", lambda: self._show("aristas()",
                  f"Aristas: {self.grafo.aristas()}"))
        self._btn(parent, "📦  elementos()", self._op_elementos)

        self._section(parent, "CONSULTAS POR VÉRTICE")
        tk.Label(parent, text="Vértice v:", fg=TEXT, bg=PANEL_BG,
                 font=("Courier", 9)).pack(anchor="w", padx=8)
        self.qv = tk.Entry(parent, **self._entry_style())
        self.qv.pack(fill="x", padx=8, pady=2)
        self._btn(parent, "📐  grado(v)", self._op_grado)
        self._btn(parent, "🔗  verticesAdyacentes(v)", self._op_vertAdyac)
        self._btn(parent, "🔗  aristasIncidentes(v)", self._op_aristasInc)

        self._section(parent, "CONSULTAS POR ARISTA")
        tk.Label(parent, text="Arista  v,w:", fg=TEXT, bg=PANEL_BG,
                 font=("Courier", 9)).pack(anchor="w", padx=8)
        self.qe = tk.Entry(parent, **self._entry_style())
        self.qe.pack(fill="x", padx=8, pady=2)
        tk.Label(parent, text="Vértice v (para opuesto):", fg=TEXT, bg=PANEL_BG,
                 font=("Courier", 9)).pack(anchor="w", padx=8)
        self.qv2 = tk.Entry(parent, **self._entry_style())
        self.qv2.pack(fill="x", padx=8, pady=2)
        self._btn(parent, "🔚  verticesFinales(e)", self._op_vertFinales)
        self._btn(parent, "↔  opuesto(v, e)", self._op_opuesto)
        self._btn(parent, "✅  esAdyacente(v, w)", self._op_esAdyacente)

    def _tab_dirigidas(self, parent):
        self._section(parent, "LISTAS DE ARISTAS")
        self._btn(parent, "→  aristasDirigidas()", lambda: self._show(
            "aristasDirigidas()", f"{self.grafo.aristasDirigidas()}"))
        self._btn(parent, "↔  aristasNoDirigidas()", lambda: self._show(
            "aristasNoDirigidas()", f"{self.grafo.aristasNoDirigidas()}"))

        self._section(parent, "GRADO DIRIGIDO")
        tk.Label(parent, text="Vértice v:", fg=TEXT, bg=PANEL_BG,
                 font=("Courier", 9)).pack(anchor="w", padx=8)
        self.dv = tk.Entry(parent, **self._entry_style())
        self.dv.pack(fill="x", padx=8, pady=2)
        self._btn(parent, "⬇  gradoEnt(v)", self._op_gradoEnt)
        self._btn(parent, "⬆  gradoSalida(v)", self._op_gradoSal)
        self._btn(parent, "⬇  aristasIncidentesEnt(v)", self._op_arIncEnt)
        self._btn(parent, "⬆  aristasIncidentesSal(v)", self._op_arIncSal)
        self._btn(parent, "⬇  verticesAdyacentesEnt(v)", self._op_vAdyEnt)
        self._btn(parent, "⬆  verticesAdyacentesSal(v)", self._op_vAdySal)

        self._section(parent, "INFO DE ARISTA DIRIGIDA")
        tk.Label(parent, text="Arista  v,w:", fg=TEXT, bg=PANEL_BG,
                 font=("Courier", 9)).pack(anchor="w", padx=8)
        self.de = tk.Entry(parent, **self._entry_style())
        self.de.pack(fill="x", padx=8, pady=2)
        self._btn(parent, "🎯  destino(e)", self._op_destino)
        self._btn(parent, "🚀  origen(e)", self._op_origen)
        self._btn(parent, "❓  esDirigida(e)", self._op_esDirigida)

    # ── Helpers UI ──────────────────────────────
    def _section(self, parent, text):
        tk.Frame(parent, bg=ACCENT, height=1).pack(fill="x", padx=8, pady=(10, 2))
        tk.Label(parent, text=text, font=("Courier", 8, "bold"),
                 fg=ACCENT, bg=PANEL_BG).pack(anchor="w", padx=8)

    def _btn(self, parent, text, cmd, color=None):
        c = color or BTN_BG
        b = tk.Button(parent, text=text, command=cmd,
                      bg=c, fg=TEXT, activebackground=BTN_HOV,
                      activeforeground=TEXT, font=("Courier", 8, "bold"),
                      relief="flat", bd=0, cursor="hand2", pady=4)
        b.pack(fill="x", padx=8, pady=2)
        b.bind("<Enter>", lambda e, btn=b: btn.config(bg=BTN_HOV))
        b.bind("<Leave>", lambda e, btn=b, col=c: btn.config(bg=col))

    def _entry_style(self):
        return dict(bg="#0a1a2e", fg=ACCENT2, insertbackground=ACCENT2,
                    font=("Courier", 10), relief="flat", bd=2)

    def _parse_edge(self, text):
        parts = [x.strip() for x in text.split(",")]
        if len(parts) != 2:
            raise ValueError("Formato incorrecto. Usa: V1,V2")
        return tuple(parts)

    # ── Log / info ──────────────────────────────
    def _log(self, op, result):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"▶ {op}  →  {result}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
        self.info_var.set(f"Última op: {op}")
        self._update_stats()

    def _show(self, op, msg):
        self._log(op, msg)
        messagebox.showinfo(op, msg)

    def _update_stats(self):
        self.stats_var.set(
            f"Vértices: {self.grafo.numVertices()}   "
            f"Aristas: {self.grafo.numAristas()}   "
            f"Tamaño: {self.grafo.tamano()}\n"
            f"Seleccionado: {self.selected_node or '—'}"
        )

    # ── Dibujo del grafo ────────────────────────
    def _draw_graph(self):
        self.ax.clear()
        self.ax.set_facecolor("#0a1520")
        G = self.grafo._G

        if G.number_of_nodes() == 0:
            self.ax.text(0.5, 0.5, "Grafo vacío\nInserta vértices →",
                         ha="center", va="center", color=ACCENT2,
                         fontsize=14, fontfamily="monospace",
                         transform=self.ax.transAxes)
            self.ax.axis("off")
            self.canvas.draw()
            return

        try:
            pos = nx.spring_layout(G, seed=42, k=2)
        except Exception:
            pos = nx.circular_layout(G)

        self._pos = pos  # guardamos para hit-test

        # colores de nodos
        node_colors = []
        for n in G.nodes():
            if n == self.selected_node:
                node_colors.append(ACCENT)
            else:
                node_colors.append(ACCENT2)

        # dibujar nodos
        nx.draw_networkx_nodes(G, pos, ax=self.ax,
                               node_color=node_colors,
                               node_size=900, alpha=0.95)
        nx.draw_networkx_labels(G, pos, ax=self.ax,
                                font_color=DARK_BG,
                                font_size=9, font_weight="bold")

        # etiquetas de datos en vértices
        vert_labels = {v: d for v, d in self.grafo._vertex_data.items() if d}
        offset_pos = {n: (x, y + 0.1) for n, (x, y) in pos.items()}
        nx.draw_networkx_labels(G, offset_pos, labels=vert_labels,
                                ax=self.ax, font_color=ACCENT,
                                font_size=7)

        # aristas dirigidas vs no dirigidas
        dir_edges = [e for e in self.grafo._directed_edges if G.has_edge(*e)]
        nodir_edges = [e for e in G.edges()
                       if e not in self.grafo._directed_edges
                       and (e[1], e[0]) not in self.grafo._directed_edges]

        if nodir_edges:
            nx.draw_networkx_edges(G, pos, edgelist=nodir_edges, ax=self.ax,
                                   edge_color="#4fc3f7", width=2, alpha=0.8)
        if dir_edges:
            nx.draw_networkx_edges(G, pos, edgelist=dir_edges, ax=self.ax,
                                   edge_color=ACCENT, width=2, alpha=0.9,
                                   arrows=True, arrowstyle="-|>",
                                   arrowsize=20,
                                   connectionstyle="arc3,rad=0.1")

        # etiquetas de aristas
        edge_labels = {}
        for e, d in self.grafo._edge_data.items():
            if d and G.has_edge(*e):
                edge_labels[e] = d
        if edge_labels:
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                         ax=self.ax, font_color=SUCCESS,
                                         font_size=8)

        # leyenda
        patches = [
            mpatches.Patch(color=ACCENT2, label="No dirigida"),
            mpatches.Patch(color=ACCENT,  label="Dirigida"),
            mpatches.Patch(color=ACCENT,  label="Seleccionado"),
        ]
        self.ax.legend(handles=patches, loc="lower right",
                       fontsize=7, facecolor=PANEL_BG,
                       labelcolor=TEXT, framealpha=0.8)
        self.ax.axis("off")
        self.canvas.draw()

    def _on_canvas_click(self, event):
        if not hasattr(self, "_pos") or event.xdata is None:
            return
        min_d, nearest = float("inf"), None
        for node, (x, y) in self._pos.items():
            d = (event.xdata - x) ** 2 + (event.ydata - y) ** 2
            if d < min_d:
                min_d, nearest = d, node
        if min_d < 0.05:
            self.selected_node = nearest
            self._log("selección", f"Vértice '{nearest}' seleccionado")
            self._draw_graph()

    # ── Operaciones ─────────────────────────────
    def _op_insertaVertice(self):
        o = self.vert_info.get().strip()
        v = self.grafo.insertaVertice(o)
        self._log(f"insertaVertice('{o}')", f"Nuevo vértice: {v}")
        self.vert_info.delete(0, "end")
        self._draw_graph()

    def _op_eliminaVertice(self):
        v = self.del_vert.get().strip()
        try:
            self.grafo.eliminaVertice(v)
            if self.selected_node == v:
                self.selected_node = None
            self._log(f"eliminaVertice('{v}')", "Vértice eliminado")
            self.del_vert.delete(0, "end")
            self._draw_graph()
        except ValueError as ex:
            messagebox.showerror("Error", str(ex))

    def _op_insertaArista(self):
        try:
            v, w, o = self.ar_v.get().strip(), self.ar_w.get().strip(), self.ar_o.get().strip()
            e = self.grafo.insertaArista(v, w, o)
            self._log(f"insertaArista('{v}','{w}','{o}')", f"Arista: {e}")
            self._draw_graph()
        except ValueError as ex:
            messagebox.showerror("Error", str(ex))

    def _op_insertaAristaDirigida(self):
        try:
            v, w, o = self.ar_v.get().strip(), self.ar_w.get().strip(), self.ar_o.get().strip()
            e = self.grafo.insertaAristaDirigida(v, w, o)
            self._log(f"insertaAristaDirigida('{v}','{w}','{o}')", f"Arista dirigida: {e}")
            self._draw_graph()
        except ValueError as ex:
            messagebox.showerror("Error", str(ex))

    def _op_eliminaArista(self):
        try:
            e = self._parse_edge(self.del_ar.get())
            self.grafo.eliminaArista(e)
            self._log(f"eliminaArista({e})", "Eliminada")
            self._draw_graph()
        except (ValueError, Exception) as ex:
            messagebox.showerror("Error", str(ex))

    def _op_convierteNoDirigida(self):
        try:
            e = self._parse_edge(self.del_ar.get())
            self.grafo.convierteNoDirigida(e)
            self._log(f"convierteNoDirigida({e})", "Convertida a no dirigida")
            self._draw_graph()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _op_invierteDir(self):
        try:
            e = self._parse_edge(self.del_ar.get())
            self.grafo.invierteDir(e)
            self._log(f"invierteDir({e})", "Dirección invertida")
            self._draw_graph()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _op_reemplazar(self):
        p = self.remp_pos.get().strip()
        r = self.remp_val.get().strip()
        ok = self.grafo.reemplazar(p, r)
        if ok:
            self._log(f"reemplazar('{p}', '{r}')", "Elemento reemplazado")
            self._draw_graph()
        else:
            messagebox.showerror("Error", f"Posición '{p}' no encontrada")

    def _op_elementos(self):
        v_el, e_el = self.grafo.elementos()
        msg = f"Vértices:\n{v_el}\n\nAristas:\n{e_el}"
        self._log("elementos()", "Ver cuadro de diálogo")
        messagebox.showinfo("elementos()", msg)

    def _op_grado(self):
        v = self.qv.get().strip()
        try:
            self._show(f"grado('{v}')", f"Grado de {v} = {self.grafo.grado(v)}")
        except ValueError as ex:
            messagebox.showerror("Error", str(ex))

    def _op_vertAdyac(self):
        v = self.qv.get().strip()
        try:
            self._show(f"verticesAdyacentes('{v}')",
                       f"{self.grafo.verticesAdyacentes(v)}")
        except ValueError as ex:
            messagebox.showerror("Error", str(ex))

    def _op_aristasInc(self):
        v = self.qv.get().strip()
        try:
            self._show(f"aristasIncidentes('{v}')",
                       f"{self.grafo.aristasIncidentes(v)}")
        except ValueError as ex:
            messagebox.showerror("Error", str(ex))

    def _op_vertFinales(self):
        try:
            e = self._parse_edge(self.qe.get())
            self._show(f"verticesFinales({e})", f"{self.grafo.verticesFinales(e)}")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _op_opuesto(self):
        try:
            e = self._parse_edge(self.qe.get())
            v = self.qv2.get().strip()
            self._show(f"opuesto('{v}', {e})", f"{self.grafo.opuesto(v, e)}")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _op_esAdyacente(self):
        try:
            v, w = self._parse_edge(self.qe.get())
            self._show(f"esAdyacente('{v}','{w}')",
                       f"{self.grafo.esAdyacente(v, w)}")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _op_gradoEnt(self):
        v = self.dv.get().strip()
        self._show(f"gradoEnt('{v}')", f"Grado entrada = {self.grafo.gradoEnt(v)}")

    def _op_gradoSal(self):
        v = self.dv.get().strip()
        self._show(f"gradoSalida('{v}')", f"Grado salida = {self.grafo.gradoSalida(v)}")

    def _op_arIncEnt(self):
        v = self.dv.get().strip()
        self._show(f"aristasIncidentesEnt('{v}')",
                   f"{self.grafo.aristasIncidentesEnt(v)}")

    def _op_arIncSal(self):
        v = self.dv.get().strip()
        self._show(f"aristasIncidentesSal('{v}')",
                   f"{self.grafo.aristasIncidentesSal(v)}")

    def _op_vAdyEnt(self):
        v = self.dv.get().strip()
        self._show(f"verticesAdyacentesEnt('{v}')",
                   f"{self.grafo.verticesAdyacentesEnt(v)}")

    def _op_vAdySal(self):
        v = self.dv.get().strip()
        self._show(f"verticesAdyacentesSal('{v}')",
                   f"{self.grafo.verticesAdyacentesSal(v)}")

    def _op_destino(self):
        try:
            e = self._parse_edge(self.de.get())
            self._show(f"destino({e})", f"{self.grafo.destino(e)}")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _op_origen(self):
        try:
            e = self._parse_edge(self.de.get())
            self._show(f"origen({e})", f"{self.grafo.origen(e)}")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _op_esDirigida(self):
        try:
            e = self._parse_edge(self.de.get())
            self._show(f"esDirigida({e})", f"{self.grafo.esDirigida(e)}")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))


# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()