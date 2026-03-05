import tkinter as tk
from tkinter import messagebox
import time
import threading

# ══════════════════════════════════════════════════════════════
#  CONSTANTES DE DISEÑO
# ══════════════════════════════════════════════════════════════
BG          = "#1a1008"
GROUND      = "#3d2b0e"
GROUND_LINE = "#5a3f18"
POLE_COLOR  = "#8B6914"
POLE_SHADE  = "#5a4008"
BASE_COLOR  = "#6b4f1a"
BASE_SHADE  = "#3d2b0e"
LABEL_COLOR = "#c8a84b"
TEXT_MAIN   = "#f0d080"
TEXT_DIM    = "#7a5c28"
ACCENT      = "#ffcc44"
ACCENT2     = "#ff8c44"
WIN_COLOR   = "#44ff88"
TIMER_COLOR = "#00e5ff"
TIMER_RUN   = "#ff4444"

FONT_TITLE  = ("Georgia", 20, "bold")
FONT_LABEL  = ("Georgia", 11, "bold")
FONT_MONO   = ("Courier New", 10, "bold")
FONT_SMALL  = ("Courier New", 9)
FONT_BIG    = ("Georgia", 24, "bold")
FONT_TIMER  = ("Courier New", 28, "bold")
FONT_TIMER_S= ("Courier New", 13, "bold")

DISK_COLORS = [
    ("#c0392b", "#922b21"), ("#e67e22", "#b85c12"), ("#d4ac0d", "#9a7d0a"),
    ("#27ae60", "#1a7a40"), ("#2980b9", "#1a5276"), ("#8e44ad", "#6c3483"),
    ("#17a589", "#0e6655"), ("#e91e63", "#ad1457"),
]

# Presets de discos disponibles
DISK_PRESETS = [2, 3, 4, 5, 6, 7, 8, 10, 30, 64]

# Discos que muestran animación (>= este valor → simulación instantánea)
ANIM_MAX = 20

MIN_DISKS = 2
MAX_DISKS = 64


# ══════════════════════════════════════════════════════════════
#  LÓGICA
# ══════════════════════════════════════════════════════════════
class Hanoi:
    def __init__(self, n=3):
        self.n = n
        self.torres = [list(range(n, 0, -1)), [], []]
        self.movimientos = 0
        self.seleccionada = None

    def seleccionar(self, torre_idx):
        if self.seleccionada is None:
            if not self.torres[torre_idx]:
                return False, "Torre vacía"
            self.seleccionada = torre_idx
            return True, f"Disco {self.torres[torre_idx][-1]} tomado de Torre {torre_idx+1}"
        else:
            if self.seleccionada == torre_idx:
                self.seleccionada = None
                return True, "Selección cancelada"
            return self._mover(self.seleccionada, torre_idx)

    def _mover(self, origen, destino):
        t_orig = self.torres[origen]
        t_dest = self.torres[destino]
        disco = t_orig[-1]
        if t_dest and t_dest[-1] < disco:
            self.seleccionada = None
            return False, f"❌ No puedes poner disco {disco} sobre {t_dest[-1]}"
        t_orig.pop()
        t_dest.append(disco)
        self.movimientos += 1
        self.seleccionada = None
        return True, f"Disco {disco}: Torre {origen+1} → Torre {destino+1}"

    def ganado(self):
        return len(self.torres[2]) == self.n

    def reset(self, n=None):
        if n is not None:
            self.n = n
        self.torres = [list(range(self.n, 0, -1)), [], []]
        self.movimientos = 0
        self.seleccionada = None

    def minimo_movimientos(self):
        return (2 ** self.n) - 1

    def pasos_solucion(self):
        """Genera la lista de pasos iterativamente para n grande."""
        pasos = []
        stack = [(self.n, 0, 2, 1)]
        while stack:
            n, origen, destino, aux = stack.pop()
            if n == 0:
                continue
            stack.append((n-1, aux, destino, origen))
            pasos.append((origen, destino))
            stack.append((n-1, origen, aux, destino))
        return pasos

    def resolver_instantaneo(self):
        """Resuelve sin animar, solo calculando el estado final."""
        self.torres = [[], [], list(range(self.n, 0, -1))]
        self.movimientos = self.minimo_movimientos()


# ══════════════════════════════════════════════════════════════
#  CRONÓMETRO
# ══════════════════════════════════════════════════════════════
class Cronometro:
    def __init__(self):
        self._inicio = None
        self._fin = None
        self._corriendo = False

    def iniciar(self):
        self._inicio = time.perf_counter()
        self._fin = None
        self._corriendo = True

    def detener(self):
        if self._corriendo:
            self._fin = time.perf_counter()
            self._corriendo = False

    def reset(self):
        self._inicio = None
        self._fin = None
        self._corriendo = False

    def elapsed(self):
        if self._inicio is None:
            return 0.0
        if self._corriendo:
            return time.perf_counter() - self._inicio
        return (self._fin or self._inicio) - self._inicio

    def corriendo(self):
        return self._corriendo

    def formato(self):
        t = self.elapsed()
        h  = int(t // 3600)
        m  = int((t % 3600) // 60)
        s  = int(t % 60)
        ms = int((t % 1) * 1000)
        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
        return f"{m:02d}:{s:02d}.{ms:03d}"


# ══════════════════════════════════════════════════════════════
#  GUI
# ══════════════════════════════════════════════════════════════
class HanoiGUI:
    W = 900
    H = 500
    POLE_H_RATIO = 0.50
    BASE_H = 20
    BASE_W_RATIO = 0.27
    POLE_W = 12
    DISK_H = 18           # altura de cada disco visual
    DISK_MIN_W = 20
    DISK_MAX_W_RATIO = 0.21

    def __init__(self, root):
        self.root = root
        self.hanoi = Hanoi(3)
        self.cronometro = Cronometro()
        self._solving = False
        self._solve_after = None
        self._timer_after = None
        self._primer_mov = False  # cronómetro inicia en primer movimiento manual
        self._tiempo_auto_inicio = None
        self._tiempo_auto_fin = None

        root.title("🏛  Torre de Hanoi")
        root.configure(bg=BG)
        root.resizable(False, False)
        root.geometry(f"{self.W}x{self.H + 230}")

        self._build_ui()
        self._redraw()
        self._tick_timer()

    # ── Layout ────────────────────────────────────────────────
    def _build_ui(self):
        # Título
        hdr = tk.Frame(self.root, bg=BG)
        hdr.pack(pady=(10, 0))
        tk.Label(hdr, text="⊕  TORRE  DE  HANOI  ⊕",
                 font=FONT_TITLE, bg=BG, fg=ACCENT).pack()
        tk.Label(hdr, text="Clic en una torre: tomar disco del tope · clic de nuevo: colocar",
                 font=FONT_SMALL, bg=BG, fg=TEXT_DIM).pack()

        # Canvas principal
        self.canvas = tk.Canvas(self.root, width=self.W, height=self.H,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_click)

        # ── Panel central: cronómetro + info ──────────────────
        mid = tk.Frame(self.root, bg=BG)
        mid.pack(fill="x", padx=20, pady=(4, 0))

        # Cronómetro (izquierda)
        timer_box = tk.Frame(mid, bg="#0a0d14",
                              highlightthickness=1, highlightbackground=TIMER_COLOR)
        timer_box.pack(side="left", padx=(0, 16), pady=2)
        tk.Label(timer_box, text=" ⏱  TIEMPO ", font=FONT_SMALL,
                 bg="#0a0d14", fg=TIMER_COLOR).pack(anchor="w", padx=6, pady=(4, 0))
        self.lbl_timer = tk.Label(timer_box, text="00:00.000",
                                   font=FONT_TIMER, bg="#0a0d14", fg=TIMER_COLOR,
                                   width=11, anchor="center")
        self.lbl_timer.pack(padx=10, pady=(0, 6))

        # Info (centro/derecha)
        info_box = tk.Frame(mid, bg=BG)
        info_box.pack(side="left", fill="x", expand=True)

        row1 = tk.Frame(info_box, bg=BG)
        row1.pack(anchor="w")
        self.lbl_discos = tk.Label(row1, text="Discos: 3",
                                    font=FONT_MONO, bg=BG, fg=TEXT_MAIN)
        self.lbl_discos.pack(side="left", padx=(0, 20))
        self.lbl_movs = tk.Label(row1, text="Movimientos: 0",
                                  font=FONT_MONO, bg=BG, fg=TEXT_MAIN)
        self.lbl_movs.pack(side="left", padx=(0, 20))
        self.lbl_min = tk.Label(row1, text=f"Mínimo: {2**3-1}",
                                 font=FONT_MONO, bg=BG, fg=TEXT_DIM)
        self.lbl_min.pack(side="left")

        row2 = tk.Frame(info_box, bg=BG)
        row2.pack(anchor="w", pady=(2, 0))
        self.lbl_msg = tk.Label(row2, text="Selecciona una torre para comenzar",
                                 font=FONT_MONO, bg=BG, fg=ACCENT2, width=52, anchor="w")
        self.lbl_msg.pack()

        # ── Selector de discos ────────────────────────────────
        ctrl = tk.Frame(self.root, bg=BG)
        ctrl.pack(pady=(6, 2))
        tk.Label(ctrl, text="DISCOS:", font=FONT_MONO, bg=BG, fg=TEXT_MAIN).grid(
            row=0, column=0, padx=(0, 6))

        self.disk_var = tk.IntVar(value=3)
        for i, n in enumerate(DISK_PRESETS):
            color = ACCENT if n <= 8 else ("#ff9944" if n <= 10 else
                    ("#ff5544" if n <= 30 else "#ff2244"))
            rb = tk.Radiobutton(ctrl, text=str(n), variable=self.disk_var, value=n,
                                command=self._on_change_disks,
                                bg=BG, fg=color, selectcolor="#3d2b0e",
                                activebackground=BG, activeforeground=ACCENT2,
                                font=FONT_MONO, indicatoron=True)
            rb.grid(row=0, column=i+1, padx=4)

        # Advertencia para n grande
        self.lbl_warn = tk.Label(self.root, text="",
                                  font=FONT_SMALL, bg=BG, fg="#ff5544")
        self.lbl_warn.pack()

        # ── Botones de acción ─────────────────────────────────
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(pady=4)
        self._btn(btn_frame, "↺  REINICIAR",  ACCENT,    "#2a1800", self._on_reset  ).grid(row=0, column=0, padx=7)
        self._btn(btn_frame, "⬆  +DISCO",    "#44cc88", "#001a0a",  self._on_add    ).grid(row=0, column=1, padx=7)
        self._btn(btn_frame, "⬇  −DISCO",    ACCENT2,   "#1a0800",  self._on_remove ).grid(row=0, column=2, padx=7)
        self._btn(btn_frame, "🤖  AUTO",      "#88aaff", "#00081a",  self._on_auto   ).grid(row=0, column=3, padx=7)
        self._btn(btn_frame, "⚡  INSTANTÁNEO","#ffaa00","#1a0e00",  self._on_instant).grid(row=0, column=4, padx=7)
        self._btn(btn_frame, "✕  PARAR",     "#cc4488", "#1a0010",  self._on_stop   ).grid(row=0, column=5, padx=7)

    def _btn(self, parent, text, fg, bg, cmd):
        b = tk.Button(parent, text=text, font=FONT_MONO,
                      fg=fg, bg=bg, activeforeground=BG, activebackground=fg,
                      relief="flat", padx=10, pady=5, cursor="hand2",
                      highlightthickness=1, highlightbackground=fg, command=cmd)
        b.bind("<Enter>", lambda e, b=b, c=fg: b.config(bg=c, fg=BG))
        b.bind("<Leave>", lambda e, b=b, c=bg, d=fg: b.config(bg=c, fg=d))
        return b

    # ── Cronómetro tick ───────────────────────────────────────
    def _tick_timer(self):
        if self.cronometro.corriendo():
            self.lbl_timer.config(text=self.cronometro.formato(), fg=TIMER_RUN)
        else:
            self.lbl_timer.config(fg=TIMER_COLOR)
        self._timer_after = self.root.after(33, self._tick_timer)   # ~30fps

    # ── Dibujo ────────────────────────────────────────────────
    def _pole_x(self, idx):
        section = self.W // 3
        return section * idx + section // 2

    def _redraw(self, flash_torre=None, flash_ok=True):
        c = self.canvas
        c.delete("all")
        W, H = self.W, self.H
        n = self.hanoi.n

        # Fondo degradado
        steps = 16
        for i in range(steps):
            t = i / steps
            r = int(0x0e + (0x2a - 0x0e) * t)
            g = int(0x0a + (0x1a - 0x0a) * t)
            b = int(0x04 + (0x06 - 0x04) * t)
            c.create_rectangle(0, int(H*i/steps), W, int(H*(i+1)/steps),
                                fill=f"#{r:02x}{g:02x}{b:02x}", outline="")

        # Suelo
        ground_y = int(H * 0.84)
        c.create_rectangle(0, ground_y, W, H, fill=GROUND, outline="")
        c.create_line(0, ground_y, W, ground_y, fill=GROUND_LINE, width=2)
        for i in range(0, W, 36):
            c.create_line(i, ground_y, i+18, H, fill=GROUND_LINE, width=1)

        pole_h  = int(H * self.POLE_H_RATIO)
        base_w  = int(W * self.BASE_W_RATIO)
        base_h  = self.BASE_H
        base_y  = ground_y - base_h

        # Dimensiones de disco — se adaptan según n
        if n <= 8:
            disk_max_w = int(W * self.DISK_MAX_W_RATIO)
            disk_step  = (disk_max_w - self.DISK_MIN_W) // max(n - 1, 1)
            disk_h     = self.DISK_H
        elif n <= 15:
            disk_max_w = int(W * 0.20)
            disk_step  = max(2, (disk_max_w - 14) // max(n - 1, 1))
            disk_h     = 14
        else:
            # Para n grande: discos ultra-delgados, sin números
            disk_max_w = int(W * 0.19)
            disk_step  = max(1, (disk_max_w - 10) // max(n - 1, 1))
            disk_h     = max(3, min(10, int(pole_h / (n + 1))))

        for ti in range(3):
            px = self._pole_x(ti)
            bx0, bx1 = px - base_w//2, px + base_w//2

            # Base (sombra + cuerpo)
            c.create_rectangle(bx0+4, base_y+4, bx1+4, base_y+base_h+4,
                                fill="#1a0e00", outline="")
            c.create_rectangle(bx0, base_y, bx1, base_y+base_h,
                                fill=BASE_COLOR, outline=BASE_SHADE, width=2)
            c.create_text(px, base_y + base_h//2,
                          text=["  I  ","  II ","  III"][ti],
                          fill=LABEL_COLOR, font=("Georgia", 9, "bold"))

            # Poste
            pole_top = base_y - pole_h
            c.create_rectangle(px - self.POLE_W//2 + 3, pole_top+3,
                                px + self.POLE_W//2 + 3, base_y+3,
                                fill="#0a0500", outline="")
            c.create_rectangle(px - self.POLE_W//2, pole_top,
                                px + self.POLE_W//2, base_y,
                                fill=POLE_COLOR, outline=POLE_SHADE, width=1)
            c.create_rectangle(px - self.POLE_W//2 + 2, pole_top,
                                px - self.POLE_W//2 + 4, base_y,
                                fill="#d4a017", outline="")

            # Anillo de selección
            if self.hanoi.seleccionada == ti:
                ring_c = WIN_COLOR if flash_ok else "#ff4444"
                c.create_oval(px - base_w//2 - 4, base_y - pole_h - 8,
                              px + base_w//2 + 4, base_y + base_h + 4,
                              outline=ring_c, width=3, dash=(6, 3))

            if flash_torre == ti:
                flash_c = "#44ff44" if flash_ok else "#ff2222"
                c.create_rectangle(bx0 - 6, pole_top - 6, bx1 + 6, base_y+base_h+6,
                                   outline=flash_c, width=3, dash=(4, 2))

            # Discos
            discos = self.hanoi.torres[ti]
            # Para n muy grande limitamos lo que dibujamos visualmente
            max_draw = min(len(discos), int(pole_h // max(disk_h + 1, 1)))
            dibujar = discos[-max_draw:] if max_draw < len(discos) else discos

            for di, disco in enumerate(dibujar):
                w   = self.DISK_MIN_W + (disco - 1) * disk_step
                h   = disk_h
                gap = max(1, disk_h // 5)
                y_bot = base_y - di * (h + gap)
                y_top = y_bot - h
                x0, x1 = px - w//2, px + w//2
                fill_c, shade_c = DISK_COLORS[(disco - 1) % len(DISK_COLORS)]

                c.create_rectangle(x0+2, y_top+2, x1+2, y_bot+2, fill="#000000", outline="")
                c.create_rectangle(x0, y_top, x1, y_bot, fill=fill_c, outline=shade_c, width=1)

                if disk_h >= 12:
                    # Brillo
                    r2 = min(255, int(fill_c[1:3], 16)+40)
                    g2 = min(255, int(fill_c[3:5], 16)+40)
                    b2 = min(255, int(fill_c[5:7], 16)+40)
                    c.create_rectangle(x0+3, y_top+2, x1-3, y_top+4,
                                       fill=f"#{r2:02x}{g2:02x}{b2:02x}", outline="")
                if disk_h >= 10 and n <= 20:
                    c.create_text(px, (y_top+y_bot)//2, text=str(disco),
                                  fill="white", font=("Courier New", 7, "bold"))

            # Si hay discos que no se dibujaron, mostrar indicador
            if len(discos) > max_draw:
                ocultos = len(discos) - max_draw
                c.create_text(px, pole_top + 14, text=f"+{ocultos}",
                              fill=ACCENT, font=("Courier New", 8, "bold"))

        # Etiquetas
        names = ["ORIGEN", "AUXILIAR", "DESTINO"]
        for ti in range(3):
            px = self._pole_x(ti)
            c.create_text(px, ground_y + 28, text=names[ti],
                          fill=LABEL_COLOR, font=("Georgia", 10, "bold"))
            # Cantidad de discos en la torre
            cant = len(self.hanoi.torres[ti])
            if cant > 0:
                c.create_text(px, ground_y + 44, text=f"({cant})",
                              fill=TEXT_DIM, font=("Courier New", 8))

        # Victoria
        if self.hanoi.ganado() and not self._solving:
            self._draw_win_banner()

        # Labels info
        self.lbl_movs.config(text=f"Movimientos: {self.hanoi.movimientos:,}")
        self.lbl_min.config(text=f"Mínimo: {self.hanoi.minimo_movimientos():,}")
        self.lbl_discos.config(text=f"Discos: {self.hanoi.n}")

    def _draw_win_banner(self):
        c = self.canvas
        W, H = self.W, self.H
        elapsed = self.cronometro.formato()
        movs = self.hanoi.movimientos
        minimo = self.hanoi.minimo_movimientos()
        eficiencia = "¡PERFECTO!" if movs == minimo else f"+{movs - minimo} extra"

        c.create_rectangle(W//2-260, H//2-70, W//2+260, H//2+70,
                           fill="#001408", outline=WIN_COLOR, width=3)
        c.create_text(W//2, H//2-38, text="🏆  ¡COMPLETADO!  🏆",
                      fill=WIN_COLOR, font=FONT_BIG)
        c.create_text(W//2, H//2-6, text=f"⏱  Tiempo: {elapsed}",
                      fill=TIMER_COLOR, font=FONT_TIMER_S)
        c.create_text(W//2, H//2+18,
                      text=f"Movimientos: {movs:,}  |  Mínimo: {minimo:,}  |  {eficiencia}",
                      fill=TEXT_MAIN, font=FONT_LABEL)
        c.create_text(W//2, H//2+44,
                      text=f"Discos resueltos: {self.hanoi.n}",
                      fill=ACCENT, font=FONT_LABEL)

    # ── Interacción manual ────────────────────────────────────
    def _on_click(self, event):
        if self._solving:
            return
        section = self.W // 3
        torre_idx = min(event.x // section, 2)

        # Iniciar cronómetro en primer movimiento real
        if not self.cronometro.corriendo() and not self.hanoi.ganado():
            if self.hanoi.seleccionada is None:
                if self.hanoi.torres[torre_idx]:
                    self.cronometro.iniciar()

        ok, msg = self.hanoi.seleccionar(torre_idx)
        self.lbl_msg.config(text=msg, fg=ACCENT if ok else ACCENT2)
        self._redraw(flash_torre=torre_idx if not ok else None, flash_ok=ok)

        if self.hanoi.ganado():
            self.cronometro.detener()
            self._redraw()

    # ── Selectores ───────────────────────────────────────────
    def _on_change_disks(self):
        if self._solving:
            self._stop_auto()
        n = self.disk_var.get()
        self.hanoi.reset(n)
        self.cronometro.reset()
        self.lbl_timer.config(text="00:00.000", fg=TIMER_COLOR)
        self._update_warn(n)
        self.lbl_msg.config(text=f"Nueva partida — {n} discos  ({self.hanoi.minimo_movimientos():,} movimientos mínimos)",
                             fg=ACCENT)
        self._redraw()

    def _update_warn(self, n):
        if n <= 8:
            self.lbl_warn.config(text="")
        elif n <= 10:
            self.lbl_warn.config(text=f"⚠  {n} discos = {2**n-1:,} movimientos mínimos")
        elif n <= 30:
            self.lbl_warn.config(
                text=f"⚠  {n} discos = {2**n-1:,} movimientos  |  AUTO usará simulación instantánea")
        else:
            import math
            segundos = (2**n - 1)
            años = segundos / (365.25 * 24 * 3600)
            self.lbl_warn.config(
                text=f"⚠  {n} discos = {2**n-1:,} movimientos  ≈  {años:.2e} años a 1 mov/seg  |  Solo modo INSTANTÁNEO")

    def _on_reset(self):
        if self._solving:
            self._stop_auto()
        self.hanoi.reset()
        self.cronometro.reset()
        self.lbl_timer.config(text="00:00.000", fg=TIMER_COLOR)
        self.lbl_msg.config(text="Partida reiniciada", fg=ACCENT)
        self._redraw()

    def _on_add(self):
        if self._solving: return
        new_n = min(self.hanoi.n + 1, MAX_DISKS)
        if new_n not in DISK_PRESETS:
            # buscar siguiente preset
            candidates = [p for p in DISK_PRESETS if p > self.hanoi.n]
            new_n = candidates[0] if candidates else MAX_DISKS
        self.disk_var.set(new_n)
        self._on_change_disks()

    def _on_remove(self):
        if self._solving: return
        candidates = [p for p in DISK_PRESETS if p < self.hanoi.n]
        new_n = candidates[-1] if candidates else MIN_DISKS
        self.disk_var.set(new_n)
        self._on_change_disks()

    # ── Auto-solve (animado para n<=ANIM_MAX, instantáneo si no) ─
    def _on_auto(self):
        if self._solving: return
        n = self.hanoi.n
        if n > ANIM_MAX:
            self._on_instant()
            return
        self.hanoi.reset()
        self.cronometro.reset()
        self._solving = True
        self._solve_steps = self.hanoi.pasos_solucion()
        self._solve_idx   = 0
        self._tiempo_auto_inicio = time.perf_counter()
        self.cronometro.iniciar()
        delay = max(30, 600 - n * 50)
        self.lbl_msg.config(text=f"🤖 Resolviendo {n} discos ({len(self._solve_steps):,} pasos)…",
                             fg="#88aaff")
        self._auto_step(delay)

    def _auto_step(self, delay):
        if not self._solving or self._solve_idx >= len(self._solve_steps):
            self._solving = False
            self.cronometro.detener()
            self._redraw()
            if self.hanoi.ganado():
                self.lbl_msg.config(text=f"🤖 ¡Resuelto en {self.cronometro.formato()}!", fg=WIN_COLOR)
            return
        origen, destino = self._solve_steps[self._solve_idx]
        t_orig = self.hanoi.torres[origen]
        t_dest = self.hanoi.torres[destino]
        if t_orig:
            t_dest.append(t_orig.pop())
            self.hanoi.movimientos += 1
        self._solve_idx += 1
        self._redraw()
        self._solve_after = self.root.after(delay, lambda: self._auto_step(delay))

    def _on_instant(self):
        """Resolución instantánea: calcula estado final y muestra resultado."""
        if self._solving:
            self._stop_auto()
        self.hanoi.reset()
        self.cronometro.reset()
        self.lbl_msg.config(text="⚡ Calculando solución…", fg="#ffaa00")
        self.root.update()

        t0 = time.perf_counter()
        self.hanoi.resolver_instantaneo()
        t1 = time.perf_counter()
        elapsed_calc = t1 - t0

        # Mostrar el tiempo de cálculo en el cronómetro como tiempo "real"
        self.cronometro._inicio = t0
        self.cronometro._fin    = t1
        self.cronometro._corriendo = False

        self._redraw()
        movs = self.hanoi.movimientos
        ms   = elapsed_calc * 1000
        self.lbl_msg.config(
            text=f"⚡ ¡{self.hanoi.n} discos resueltos!  {movs:,} movs  |  cálculo: {ms:.2f} ms",
            fg=WIN_COLOR)

    def _on_stop(self):
        self._stop_auto()

    def _stop_auto(self):
        if self._solve_after:
            self.root.after_cancel(self._solve_after)
            self._solve_after = None
        self._solving = False
        self.cronometro.detener()
        self.lbl_msg.config(text="Auto-resolución detenida", fg=ACCENT2)
        self._redraw()


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app = HanoiGUI(root)
    root.mainloop()