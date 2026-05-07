"""
Visualizador de Métodos de Ordenamiento
- Intercalación (Insertion Sort)
- Mezcla Directa (Merge Sort iterativo)
- Mezcla Equilibrada (Balanced Merge Sort)

Desarrollado con Python + Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading

# ─────────────────────────────────────────────
#  PALETA DE COLORES
# ─────────────────────────────────────────────
BG_DARK      = "#0f1117"
BG_CARD      = "#1a1d27"
BG_PANEL     = "#141720"
ACCENT_BLUE  = "#4f8ef7"
ACCENT_GREEN = "#3ecf8e"
ACCENT_PINK  = "#f75f8e"
ACCENT_GOLD  = "#f5c842"
TEXT_MAIN    = "#e8eaf0"
TEXT_MUTED   = "#7b8094"
BAR_DEFAULT  = "#4f8ef7"
BAR_ACTIVE   = "#f5c842"
BAR_SORTED   = "#3ecf8e"
BAR_COMPARE  = "#f75f8e"


# ─────────────────────────────────────────────
#  ALGORITMOS
# ─────────────────────────────────────────────

def insertion_sort_steps(arr):
    """Genera pasos de Intercalación (Insertion Sort)."""
    a = arr[:]
    steps = []
    n = len(a)
    for i in range(1, n):
        key = a[i]
        j = i - 1
        steps.append(("key", i, a[:], f"Clave: a[{i}]={key}"))
        while j >= 0 and a[j] > key:
            steps.append(("compare", j, a[:], f"Comparando a[{j}]={a[j]} > {key}, desplazando"))
            a[j + 1] = a[j]
            j -= 1
            steps.append(("move", j + 1, a[:], f"Desplazado → posición {j+2}"))
        a[j + 1] = key
        steps.append(("place", j + 1, a[:], f"Insertado {key} en posición {j+1}"))
    steps.append(("done", -1, a[:], "¡Ordenamiento completado!"))
    return steps


def merge_sort_direct_steps(arr):
    """Genera pasos de Mezcla Directa (bottom-up iterativo)."""
    a = arr[:]
    n = len(a)
    steps = []
    size = 1
    while size < n:
        steps.append(("info", -1, a[:], f"Tamaño de bloque: {size}"))
        for left in range(0, n, size * 2):
            mid   = min(left + size, n)
            right = min(left + size * 2, n)
            if mid >= right:
                continue
            L = a[left:mid]
            R = a[mid:right]
            steps.append(("merge_range", (left, mid, right), a[:],
                          f"Mezclando [{left}..{mid-1}] con [{mid}..{right-1}]"))
            i = j = 0
            k = left
            while i < len(L) and j < len(R):
                steps.append(("compare", k, a[:],
                              f"Comparando {L[i]} vs {R[j]}"))
                if L[i] <= R[j]:
                    a[k] = L[i]; i += 1
                else:
                    a[k] = R[j]; j += 1
                steps.append(("place", k, a[:], f"Colocando {a[k]} en [{k}]"))
                k += 1
            while i < len(L):
                a[k] = L[i]; i += 1; k += 1
            while j < len(R):
                a[k] = R[j]; j += 1; k += 1
        size *= 2
    steps.append(("done", -1, a[:], "¡Ordenamiento completado!"))
    return steps


def balanced_merge_steps(arr):
    """Genera pasos de Mezcla Equilibrada (divide en 2 mitades recursivo visual)."""
    a = arr[:]
    steps = []

    def merge(arr, left, mid, right):
        L = arr[left:mid+1]
        R = arr[mid+1:right+1]
        steps.append(("merge_range", (left, mid+1, right+1), arr[:],
                      f"Mezcla equilibrada [{left}..{mid}] ↔ [{mid+1}..{right}]"))
        i = j = 0
        k = left
        while i < len(L) and j < len(R):
            steps.append(("compare", k, arr[:], f"Comparando {L[i]} vs {R[j]}"))
            if L[i] <= R[j]:
                arr[k] = L[i]; i += 1
            else:
                arr[k] = R[j]; j += 1
            steps.append(("place", k, arr[:], f"Colocando {arr[k]}"))
            k += 1
        while i < len(L):
            arr[k] = L[i]; i += 1; k += 1
        while j < len(R):
            arr[k] = R[j]; j += 1; k += 1

    def merge_sort_rec(arr, left, right, depth=0):
        if left >= right:
            return
        mid = (left + right) // 2
        steps.append(("split", (left, mid, right), arr[:],
                      f"División (nivel {depth}): [{left}..{mid}] | [{mid+1}..{right}]"))
        merge_sort_rec(arr, left, mid, depth+1)
        merge_sort_rec(arr, mid+1, right, depth+1)
        merge(arr, left, mid, right)

    merge_sort_rec(a, 0, len(a)-1)
    steps.append(("done", -1, a[:], "¡Ordenamiento completado!"))
    return steps


# ─────────────────────────────────────────────
#  WIDGET DE CANVAS PARA BARRAS
# ─────────────────────────────────────────────

class BarCanvas(tk.Canvas):
    def __init__(self, master, **kw):
        super().__init__(master, bg=BG_CARD, highlightthickness=0, **kw)
        self.data        = []
        self.highlights  = {}   # index -> color
        self.range_hl    = None  # (left, right, color)

    def set_data(self, data, highlights=None, range_hl=None):
        self.data       = data
        self.highlights = highlights or {}
        self.range_hl   = range_hl
        self.redraw()

    def redraw(self):
        self.delete("all")
        if not self.data:
            return
        w = self.winfo_width()  or 600
        h = self.winfo_height() or 220
        n = len(self.data)
        max_val  = max(self.data) if self.data else 1
        pad_x    = 10
        bar_w    = max(2, (w - 2*pad_x) / n - 1)
        gap      = 1

        # Range highlight background
        if self.range_hl:
            lft, rgt, rc = self.range_hl
            x0 = pad_x + lft * (bar_w + gap)
            x1 = pad_x + rgt * (bar_w + gap)
            self.create_rectangle(x0-2, 0, x1+bar_w+2, h, fill="#2a2d3a", outline="")

        for i, val in enumerate(self.data):
            x0 = pad_x + i * (bar_w + gap)
            x1 = x0 + bar_w
            bar_h = max(4, int((val / max_val) * (h - 30)))
            y0 = h - bar_h - 10
            y1 = h - 10
            color = self.highlights.get(i, BAR_DEFAULT)
            # Shadow
            self.create_rectangle(x0+2, y0+2, x1+2, y1+2,
                                   fill="#0a0c12", outline="")
            # Bar
            self.create_rectangle(x0, y0, x1, y1,
                                   fill=color, outline="", width=0)
            # Top glow line
            self.create_line(x0, y0, x1, y0, fill=color, width=2)

            # Value label (only if bars are wide enough)
            if bar_w >= 18:
                self.create_text((x0+x1)//2, y0-6, text=str(val),
                                  fill=TEXT_MUTED, font=("Consolas", 7))


# ─────────────────────────────────────────────
#  PANEL DE UN ALGORITMO
# ─────────────────────────────────────────────

class AlgoPanel(tk.Frame):
    def __init__(self, master, title, color, algo_func, data_getter, **kw):
        super().__init__(master, bg=BG_CARD, **kw)
        self.algo_func   = algo_func
        self.data_getter = data_getter
        self.steps       = []
        self.step_idx    = 0
        self.running     = False
        self.speed       = 100   # ms per step
        self._after_id   = None
        self.accent      = color

        self._build_ui(title, color)

    def _build_ui(self, title, color):
        # Header
        hdr = tk.Frame(self, bg=color, height=4)
        hdr.pack(fill="x")

        title_bar = tk.Frame(self, bg=BG_PANEL)
        title_bar.pack(fill="x", padx=0, pady=0)

        tk.Label(title_bar, text=title, bg=BG_PANEL, fg=TEXT_MAIN,
                 font=("Consolas", 11, "bold")).pack(side="left", padx=12, pady=8)

        # Step counter
        self.step_lbl = tk.Label(title_bar, text="Paso 0/0", bg=BG_PANEL,
                                  fg=TEXT_MUTED, font=("Consolas", 9))
        self.step_lbl.pack(side="right", padx=12)

        # Canvas
        self.canvas = BarCanvas(self, width=380, height=200)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=(4,0))

        # Status message
        self.msg_lbl = tk.Label(self, text="Presiona ▶ para iniciar",
                                 bg=BG_CARD, fg=TEXT_MUTED,
                                 font=("Consolas", 9), anchor="w")
        self.msg_lbl.pack(fill="x", padx=12, pady=3)

        # Controls
        ctrl = tk.Frame(self, bg=BG_CARD)
        ctrl.pack(fill="x", padx=8, pady=(0,8))

        btn_cfg = dict(bg=BG_PANEL, fg=TEXT_MAIN, relief="flat",
                       font=("Consolas", 10), cursor="hand2",
                       activebackground="#252836", activeforeground=TEXT_MAIN,
                       padx=8, pady=4)

        self.btn_start = tk.Button(ctrl, text="▶ Iniciar", command=self.start, **btn_cfg)
        self.btn_start.pack(side="left", padx=2)

        self.btn_pause = tk.Button(ctrl, text="⏸ Pausa", command=self.pause,
                                    state="disabled", **btn_cfg)
        self.btn_pause.pack(side="left", padx=2)

        self.btn_step = tk.Button(ctrl, text="→ Paso", command=self.single_step, **btn_cfg)
        self.btn_step.pack(side="left", padx=2)

        self.btn_reset = tk.Button(ctrl, text="↺ Reset", command=self.reset, **btn_cfg)
        self.btn_reset.pack(side="left", padx=2)

        # Speed slider
        tk.Label(ctrl, text="Vel:", bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Consolas", 8)).pack(side="left", padx=(10,2))
        self.speed_var = tk.IntVar(value=5)
        spd = ttk.Scale(ctrl, from_=1, to=10, variable=self.speed_var,
                        orient="horizontal", length=70,
                        command=lambda v: self._update_speed())
        spd.pack(side="left")

        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal",
                                         mode="determinate", length=100)
        self.progress.pack(fill="x", padx=8, pady=(0,6))

    def _update_speed(self):
        val = self.speed_var.get()
        self.speed = int(550 - val * 50)   # 500ms (slow) → 50ms (fast)

    def prepare(self):
        """Genera pasos con los datos actuales."""
        data = self.data_getter()
        self.steps    = self.algo_func(data)
        self.step_idx = 0
        self.progress["maximum"] = max(len(self.steps), 1)
        self.canvas.set_data(data)
        self.step_lbl.config(text=f"Paso 0/{len(self.steps)}")
        self.msg_lbl.config(text="Listo. Presiona ▶ para iniciar.")

    def _render_step(self):
        if self.step_idx >= len(self.steps):
            return
        kind, idx, arr, msg = self.steps[self.step_idx]
        hl    = {}
        range_hl = None

        if kind == "key":
            hl = {idx: ACCENT_GOLD}
        elif kind == "compare":
            hl = {idx: BAR_COMPARE}
        elif kind in ("move", "place"):
            hl = {idx: ACCENT_PINK}
        elif kind == "merge_range":
            lft, mid, rgt = idx
            range_hl = (lft, rgt, "#2a2d3a")
            for i in range(lft, rgt):
                hl[i] = ACCENT_BLUE
        elif kind == "split":
            lft, mid, rgt = idx
            for i in range(lft, mid+1):
                hl[i] = ACCENT_BLUE
            for i in range(mid+1, rgt+1):
                hl[i] = ACCENT_PINK
        elif kind == "done":
            for i in range(len(arr)):
                hl[i] = BAR_SORTED

        self.canvas.set_data(arr, hl, range_hl)
        self.msg_lbl.config(text=msg)
        self.step_lbl.config(text=f"Paso {self.step_idx+1}/{len(self.steps)}")
        self.progress["value"] = self.step_idx + 1

    def _auto_run(self):
        if not self.running:
            return
        if self.step_idx < len(self.steps):
            self._render_step()
            self.step_idx += 1
            self._after_id = self.after(self.speed, self._auto_run)
        else:
            self.running = False
            self.btn_start.config(state="disabled")
            self.btn_pause.config(state="disabled")

    def start(self):
        if not self.steps:
            self.prepare()
        if self.step_idx >= len(self.steps):
            return
        self.running = True
        self.btn_pause.config(state="normal")
        self.btn_start.config(state="disabled")
        self._auto_run()

    def pause(self):
        self.running = False
        if self._after_id:
            self.after_cancel(self._after_id)
        self.btn_start.config(state="normal", text="▶ Continuar")
        self.btn_pause.config(state="disabled")

    def single_step(self):
        if not self.steps:
            self.prepare()
        if self.step_idx < len(self.steps):
            self._render_step()
            self.step_idx += 1

    def reset(self):
        self.running = False
        if self._after_id:
            self.after_cancel(self._after_id)
        self.steps    = []
        self.step_idx = 0
        self.progress["value"] = 0
        self.btn_start.config(state="normal", text="▶ Iniciar")
        self.btn_pause.config(state="disabled")
        self.prepare()


# ─────────────────────────────────────────────
#  VENTANA PRINCIPAL
# ─────────────────────────────────────────────

class SortingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Ordenamiento — Intercalación · Mezcla Directa · Mezcla Equilibrada")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)
        self.geometry("1220x700")

        self._data = self._new_data(20)
        self._build_ui()
        self._init_panels()

        # Style
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Horizontal.TProgressbar",
                         background=ACCENT_BLUE, troughcolor=BG_PANEL,
                         borderwidth=0, thickness=4)
        style.configure("Horizontal.TScale",
                         background=BG_CARD, troughcolor=BG_PANEL,
                         sliderlength=14)

    # ── data helpers ──
    def _new_data(self, n=20):
        return random.sample(range(5, 100), min(n, 95))

    def _get_data(self):
        return self._data[:]

    # ── UI ──
    def _build_ui(self):
        # ── Top bar ──
        top = tk.Frame(self, bg=BG_DARK)
        top.pack(fill="x", padx=16, pady=(14, 0))

        tk.Label(top, text="⚙  Visualizador de Métodos de Ordenamiento",
                 bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Consolas", 15, "bold")).pack(side="left")

        # Controls
        ctrl = tk.Frame(top, bg=BG_DARK)
        ctrl.pack(side="right")

        tk.Label(ctrl, text="Elementos:", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Consolas", 9)).pack(side="left", padx=4)
        self.n_var = tk.IntVar(value=20)
        n_spin = tk.Spinbox(ctrl, from_=5, to=50, textvariable=self.n_var,
                             width=4, bg=BG_PANEL, fg=TEXT_MAIN,
                             buttonbackground=BG_PANEL,
                             relief="flat", font=("Consolas", 10))
        n_spin.pack(side="left", padx=4)

        btn_cfg = dict(bg=ACCENT_BLUE, fg="#fff", relief="flat",
                       font=("Consolas", 10, "bold"), cursor="hand2",
                       activebackground="#3a7be0", activeforeground="#fff",
                       padx=10, pady=5)

        tk.Button(ctrl, text="🔀 Nuevo arreglo", command=self._shuffle,
                  **btn_cfg).pack(side="left", padx=6)

        tk.Button(ctrl, text="▶▶ Iniciar Todo", command=self._start_all,
                  bg=ACCENT_GREEN, fg="#fff", relief="flat",
                  font=("Consolas", 10, "bold"), cursor="hand2",
                  activebackground="#2eb87a", activeforeground="#fff",
                  padx=10, pady=5).pack(side="left", padx=2)

        tk.Button(ctrl, text="↺ Reset Todo", command=self._reset_all,
                  bg=BG_PANEL, fg=TEXT_MUTED, relief="flat",
                  font=("Consolas", 10), cursor="hand2",
                  activebackground="#252836", activeforeground=TEXT_MAIN,
                  padx=10, pady=5).pack(side="left", padx=2)

        # Separator
        sep = tk.Frame(self, bg="#252836", height=1)
        sep.pack(fill="x", padx=16, pady=10)

        # Legend
        legend = tk.Frame(self, bg=BG_DARK)
        legend.pack(fill="x", padx=16, pady=(0, 8))
        for color, label in [
            (BAR_DEFAULT,  "Normal"),
            (BAR_ACTIVE,   "Elemento clave"),
            (BAR_COMPARE,  "Comparando"),
            (ACCENT_PINK,  "Moviendo"),
            (BAR_SORTED,   "Ordenado"),
            (ACCENT_BLUE,  "Rango activo"),
        ]:
            dot = tk.Frame(legend, bg=color, width=12, height=12)
            dot.pack(side="left", padx=(8,2), pady=2)
            tk.Label(legend, text=label, bg=BG_DARK, fg=TEXT_MUTED,
                     font=("Consolas", 8)).pack(side="left", padx=(0,6))

        # Panels container
        self.panels_frame = tk.Frame(self, bg=BG_DARK)
        self.panels_frame.pack(fill="both", expand=True, padx=16, pady=(0,12))
        self.panels_frame.columnconfigure((0,1,2), weight=1, uniform="col")
        self.panels_frame.rowconfigure(0, weight=1)

    def _init_panels(self):
        infos = [
            ("🔢  Intercalación\n(Insertion Sort)",  ACCENT_BLUE,  insertion_sort_steps),
            ("🔀  Mezcla Directa\n(Direct Merge)",    ACCENT_PINK,  merge_sort_direct_steps),
            ("⚖  Mezcla Equilibrada\n(Balanced Merge)", ACCENT_GREEN, balanced_merge_steps),
        ]
        self.panels = []
        for col, (title, color, func) in enumerate(infos):
            p = AlgoPanel(self.panels_frame, title, color, func,
                          self._get_data, bd=0, relief="flat")
            p.grid(row=0, column=col, sticky="nsew", padx=6)
            self.panels.append(p)

        # Wait for geometry, then prepare
        self.after(200, self._prepare_all)

    def _prepare_all(self):
        for p in self.panels:
            p.prepare()

    def _shuffle(self):
        n = self.n_var.get()
        self._data = self._new_data(n)
        for p in self.panels:
            p.reset()

    def _start_all(self):
        for p in self.panels:
            p.start()

    def _reset_all(self):
        for p in self.panels:
            p.reset()


# ─────────────────────────────────────────────
#  ENTRADA
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = SortingApp()
    app.mainloop()