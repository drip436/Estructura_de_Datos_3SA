import tkinter as tk
from tkinter import messagebox
import time
import math

# ══════════════════════════════════════════════════════════════
#  CONSTANTES DE DISEÑO  —  estilo piedra antigua / templo maya
# ══════════════════════════════════════════════════════════════
BG          = "#1a1008"
SKY_TOP     = "#0e0a04"
SKY_BOT     = "#2a1a06"
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
SEL_RING    = "#ffffff"
FONT_TITLE  = ("Georgia", 22, "bold")
FONT_LABEL  = ("Georgia", 11, "bold")
FONT_MONO   = ("Courier New", 10, "bold")
FONT_SMALL  = ("Courier New", 9)
FONT_BIG    = ("Georgia", 28, "bold")

# Paleta de discos (del más grande al más pequeño → colores cálidos a fríos)
DISK_COLORS = [
    ("#c0392b", "#922b21"),  # rojo oscuro
    ("#e67e22", "#b85c12"),  # naranja
    ("#d4ac0d", "#9a7d0a"),  # dorado
    ("#27ae60", "#1a7a40"),  # verde
    ("#2980b9", "#1a5276"),  # azul
    ("#8e44ad", "#6c3483"),  # púrpura
    ("#17a589", "#0e6655"),  # teal
    ("#e91e63", "#ad1457"),  # rosa
]

MIN_DISKS = 2
MAX_DISKS = 8

# ══════════════════════════════════════════════════════════════
#  LÓGICA
# ══════════════════════════════════════════════════════════════
class Hanoi:
    def __init__(self, n=3):
        self.n = n
        self.torres = [list(range(n, 0, -1)), [], []]  # [fondo..tope]
        self.movimientos = 0
        self.seleccionada = None   # índice de torre seleccionada (0,1,2)
        self.historia = []

    def seleccionar(self, torre_idx):
        """Retorna (ok, mensaje)"""
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
            return False, f"No puedes colocar disco {disco} sobre disco {t_dest[-1]}"
        t_orig.pop()
        t_dest.append(disco)
        self.movimientos += 1
        self.historia.append(f"T{origen+1}→T{destino+1}  disco {disco}")
        self.seleccionada = None
        return True, f"Disco {disco} movido a Torre {destino+1}"

    def ganado(self):
        return len(self.torres[2]) == self.n

    def reset(self, n=None):
        if n is not None:
            self.n = n
        self.torres = [list(range(self.n, 0, -1)), [], []]
        self.movimientos = 0
        self.seleccionada = None
        self.historia.clear()

    def minimo_movimientos(self):
        return (2 ** self.n) - 1

    # ── Auto-solve (generador de pasos) ──
    def pasos_solucion(self):
        pasos = []
        def hanoi_rec(n, origen, destino, aux):
            if n == 0: return
            hanoi_rec(n-1, origen, aux, destino)
            pasos.append((origen, destino))
            hanoi_rec(n-1, aux, destino, origen)
        hanoi_rec(self.n, 0, 2, 1)
        return pasos


# ══════════════════════════════════════════════════════════════
#  GUI
# ══════════════════════════════════════════════════════════════
class HanoiGUI:
    W = 860
    H = 580
    POLE_H_RATIO = 0.52
    BASE_H = 22
    BASE_W_RATIO = 0.28
    POLE_W = 14
    DISK_H = 22
    DISK_MIN_W = 36
    DISK_MAX_W_RATIO = 0.22   # fracción del ancho del canvas

    def __init__(self, root):
        self.root = root
        self.hanoi = Hanoi(3)
        self._solving = False
        self._solve_after = None

        root.title("🏛  Torre de Hanoi")
        root.configure(bg=BG)
        root.resizable(False, False)
        root.geometry(f"{self.W}x{self.H+170}")

        self._build_ui()
        self._redraw()

    # ── Layout ────────────────────────────────────────────────
    def _build_ui(self):
        # Título
        hdr = tk.Frame(self.root, bg=BG)
        hdr.pack(pady=(14, 0))
        tk.Label(hdr, text="⊕  TORRE  DE  HANOI  ⊕",
                 font=FONT_TITLE, bg=BG, fg=ACCENT).pack()
        tk.Label(hdr, text="Haz clic en una torre para tomar el disco del tope · vuelve a hacer clic para colocarlo",
                 font=FONT_SMALL, bg=BG, fg=TEXT_DIM).pack()

        # Canvas principal
        self.canvas = tk.Canvas(self.root, width=self.W, height=self.H,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_click)

        # Panel de controles
        ctrl = tk.Frame(self.root, bg=BG)
        ctrl.pack(pady=6)

        # Discos
        tk.Label(ctrl, text="DISCOS:", font=FONT_MONO, bg=BG, fg=TEXT_MAIN).grid(
            row=0, column=0, padx=(0, 4))
        self.disk_var = tk.IntVar(value=3)
        for i, n in enumerate(range(MIN_DISKS, MAX_DISKS+1)):
            rb = tk.Radiobutton(ctrl, text=str(n), variable=self.disk_var, value=n,
                                command=self._on_change_disks,
                                bg=BG, fg=ACCENT, selectcolor="#3d2b0e",
                                activebackground=BG, activeforeground=ACCENT2,
                                font=FONT_MONO, indicatoron=True)
            rb.grid(row=0, column=i+1, padx=3)

        # Botones
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(pady=4)

        self._btn(btn_frame, "↺  REINICIAR", ACCENT,     "#2a1800", self._on_reset ).grid(row=0, column=0, padx=8)
        self._btn(btn_frame, "⬆  +DISCO",   "#44cc88",  "#001a0a", self._on_add   ).grid(row=0, column=1, padx=8)
        self._btn(btn_frame, "⬇  −DISCO",   ACCENT2,    "#1a0800", self._on_remove).grid(row=0, column=2, padx=8)
        self._btn(btn_frame, "🤖  AUTO",     "#88aaff",  "#00081a", self._on_auto  ).grid(row=0, column=3, padx=8)
        self._btn(btn_frame, "✕  PARAR",    "#cc4488",  "#1a0010", self._on_stop  ).grid(row=0, column=4, padx=8)

        # Info bar
        info = tk.Frame(self.root, bg=BG)
        info.pack()
        self.lbl_movs  = tk.Label(info, text="Movimientos: 0",
                                   font=FONT_LABEL, bg=BG, fg=TEXT_MAIN)
        self.lbl_movs.grid(row=0, column=0, padx=20)
        self.lbl_min   = tk.Label(info, text="Mínimo: 7",
                                   font=FONT_LABEL, bg=BG, fg=TEXT_DIM)
        self.lbl_min.grid(row=0, column=1, padx=20)
        self.lbl_msg   = tk.Label(info, text="",
                                   font=FONT_LABEL, bg=BG, fg=ACCENT2, width=36)
        self.lbl_msg.grid(row=0, column=2, padx=20)

    def _btn(self, parent, text, fg, bg, cmd):
        b = tk.Button(parent, text=text, font=FONT_MONO,
                      fg=fg, bg=bg, activeforeground=BG, activebackground=fg,
                      relief="flat", padx=12, pady=6, cursor="hand2",
                      highlightthickness=1, highlightbackground=fg, command=cmd)
        b.bind("<Enter>", lambda e, b=b, c=fg: b.config(bg=c, fg=BG))
        b.bind("<Leave>", lambda e, b=b, c=bg, d=fg: b.config(bg=c, fg=d))
        return b

    # ── Dibujo ────────────────────────────────────────────────
    def _pole_x(self, idx):
        """Centro X de cada poste (0,1,2)"""
        section = self.W // 3
        return section * idx + section // 2

    def _redraw(self, flash_torre=None, flash_ok=True):
        c = self.canvas
        c.delete("all")
        W, H = self.W, self.H

        # Fondo degradado (franjas simuladas)
        steps = 18
        for i in range(steps):
            t = i / steps
            r1, g1, b1 = 0x0e, 0x0a, 0x04
            r2, g2, b2 = 0x2a, 0x1a, 0x06
            r = int(r1 + (r2-r1)*t)
            g = int(g1 + (g2-g1)*t)
            b_c = int(b1 + (b2-b1)*t)
            color = f"#{r:02x}{g:02x}{b_c:02x}"
            y0 = int(H * i / steps)
            y1 = int(H * (i+1) / steps)
            c.create_rectangle(0, y0, W, y1, fill=color, outline="")

        # Suelo
        ground_y = int(H * 0.82)
        c.create_rectangle(0, ground_y, W, H, fill=GROUND, outline="")
        c.create_line(0, ground_y, W, ground_y, fill=GROUND_LINE, width=2)
        # Textura suelo (líneas)
        for i in range(0, W, 40):
            c.create_line(i, ground_y, i+20, H, fill=GROUND_LINE, width=1)

        pole_h = int(H * self.POLE_H_RATIO)
        base_w = int(W * self.BASE_W_RATIO)
        base_h = self.BASE_H
        base_y = ground_y - base_h

        n = self.hanoi.n
        disk_max_w = int(W * self.DISK_MAX_W_RATIO)
        disk_step  = (disk_max_w - self.DISK_MIN_W) // max(n - 1, 1)

        for ti in range(3):
            px = self._pole_x(ti)
            # Base
            bx0, bx1 = px - base_w//2, px + base_w//2
            c.create_rectangle(bx0+4, base_y+4, bx1+4, base_y+base_h+4,
                                fill="#1a0e00", outline="")
            c.create_rectangle(bx0, base_y, bx1, base_y+base_h,
                                fill=BASE_COLOR, outline=BASE_SHADE, width=2)
            # Grabado en la base
            c.create_text(px, base_y + base_h//2,
                          text=f"  {'I II III'.split()[ti]}  ",
                          fill=LABEL_COLOR, font=("Georgia", 9, "bold"))

            # Poste (sombra + cuerpo + brillo)
            pole_top = base_y - pole_h
            c.create_rectangle(px - self.POLE_W//2 + 3, pole_top + 3,
                                px + self.POLE_W//2 + 3, base_y + 3,
                                fill="#0a0500", outline="")
            c.create_rectangle(px - self.POLE_W//2, pole_top,
                                px + self.POLE_W//2, base_y,
                                fill=POLE_COLOR, outline=POLE_SHADE, width=1)
            # Brillo
            c.create_rectangle(px - self.POLE_W//2 + 2, pole_top,
                                px - self.POLE_W//2 + 4, base_y,
                                fill="#d4a017", outline="")

            # Anillo de selección
            if self.hanoi.seleccionada == ti:
                ring_color = WIN_COLOR if flash_ok else "#ff4444"
                c.create_oval(px - base_w//2 - 4, base_y - pole_h - 8,
                              px + base_w//2 + 4, base_y + base_h + 4,
                              outline=ring_color, width=3, dash=(6, 3))

            # Flash de error/ok sobre torre
            if flash_torre == ti:
                flash_col = "#44ff44" if flash_ok else "#ff2222"
                c.create_rectangle(bx0 - 6, pole_top - 6, bx1 + 6, base_y + base_h + 6,
                                   outline=flash_col, width=3, dash=(4, 2))

            # Discos
            discos = self.hanoi.torres[ti]
            for di, disco in enumerate(discos):
                # disco 1=más pequeño, n=más grande
                w = self.DISK_MIN_W + (disco - 1) * disk_step
                h = self.DISK_H
                y_bot = base_y - di * (h + 3)
                y_top = y_bot - h
                x0, x1 = px - w//2, px + w//2
                fill_c, shade_c = DISK_COLORS[(disco - 1) % len(DISK_COLORS)]

                # Sombra
                c.create_rectangle(x0+3, y_top+3, x1+3, y_bot+3,
                                   fill="#000000", outline="")
                # Cuerpo
                c.create_rectangle(x0, y_top, x1, y_bot,
                                   fill=fill_c, outline=shade_c, width=2)
                # Brillo superior
                c.create_rectangle(x0+3, y_top+3, x1-3, y_top+6,
                                   fill="#ffffff33" if False else self._lighten(fill_c),
                                   outline="")
                # Número del disco
                c.create_text(px, (y_top+y_bot)//2,
                              text=str(disco), fill="white",
                              font=("Courier New", 9, "bold"))

        # Etiquetas de torres
        for ti in range(3):
            px = self._pole_x(ti)
            names = ["ORIGEN", "AUXILIAR", "DESTINO"]
            c.create_text(px, ground_y + 30, text=names[ti],
                          fill=LABEL_COLOR, font=("Georgia", 10, "bold"))

        # Victoria
        if self.hanoi.ganado() and not self._solving:
            self._draw_win_banner()

        # Actualizar info
        self.lbl_movs.config(text=f"Movimientos: {self.hanoi.movimientos}")
        self.lbl_min.config(text=f"Mínimo: {self.hanoi.minimo_movimientos()}")

    def _lighten(self, hex_color):
        r = min(255, int(hex_color[1:3], 16) + 40)
        g = min(255, int(hex_color[3:5], 16) + 40)
        b = min(255, int(hex_color[5:7], 16) + 40)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _draw_win_banner(self):
        c = self.canvas
        W, H = self.W, self.H
        c.create_rectangle(W//2 - 220, H//2 - 55, W//2 + 220, H//2 + 55,
                           fill="#001a08", outline=WIN_COLOR, width=3)
        c.create_text(W//2, H//2 - 20, text="🏆  ¡COMPLETADO!  🏆",
                      fill=WIN_COLOR, font=FONT_BIG)
        c.create_text(W//2, H//2 + 22,
                      text=f"Resuelto en {self.hanoi.movimientos} movimientos  (mínimo: {self.hanoi.minimo_movimientos()})",
                      fill=TEXT_MAIN, font=FONT_LABEL)

    # ── Interacción ───────────────────────────────────────────
    def _on_click(self, event):
        if self._solving:
            return
        section = self.W // 3
        torre_idx = event.x // section
        if torre_idx > 2:
            torre_idx = 2
        ok, msg = self.hanoi.seleccionar(torre_idx)
        self.lbl_msg.config(text=msg, fg=ACCENT if ok else ACCENT2)
        flash_col = torre_idx if not ok else None
        self._redraw(flash_torre=flash_col if not ok else None, flash_ok=ok)

        if self.hanoi.ganado():
            self._redraw()

    def _on_change_disks(self):
        if self._solving:
            return
        n = self.disk_var.get()
        self.hanoi.reset(n)
        self.lbl_msg.config(text=f"Nueva partida con {n} discos", fg=ACCENT)
        self._redraw()

    def _on_reset(self):
        if self._solving:
            self._stop_auto()
        self.hanoi.reset()
        self.lbl_msg.config(text="Partida reiniciada", fg=ACCENT)
        self._redraw()

    def _on_add(self):
        if self._solving:
            return
        if self.hanoi.n >= MAX_DISKS:
            self.lbl_msg.config(text=f"Máximo {MAX_DISKS} discos", fg=ACCENT2)
            return
        self.hanoi.reset(self.hanoi.n + 1)
        self.disk_var.set(self.hanoi.n)
        self.lbl_msg.config(text=f"Ahora {self.hanoi.n} discos — ¡partida reiniciada!", fg=ACCENT)
        self._redraw()

    def _on_remove(self):
        if self._solving:
            return
        if self.hanoi.n <= MIN_DISKS:
            self.lbl_msg.config(text=f"Mínimo {MIN_DISKS} discos", fg=ACCENT2)
            return
        self.hanoi.reset(self.hanoi.n - 1)
        self.disk_var.set(self.hanoi.n)
        self.lbl_msg.config(text=f"Ahora {self.hanoi.n} discos — ¡partida reiniciada!", fg=ACCENT)
        self._redraw()

    # ── Auto-solve ────────────────────────────────────────────
    def _on_auto(self):
        if self._solving:
            return
        self.hanoi.reset()
        self._solving = True
        self._solve_steps = self.hanoi.pasos_solucion()
        self._solve_idx = 0
        delay = max(120, 700 - self.hanoi.n * 60)
        self.lbl_msg.config(text="🤖 Resolviendo automáticamente...", fg="#88aaff")
        self._auto_step(delay)

    def _auto_step(self, delay):
        if not self._solving or self._solve_idx >= len(self._solve_steps):
            self._solving = False
            self._redraw()
            if self.hanoi.ganado():
                self.lbl_msg.config(text="🤖 ¡Solución encontrada!", fg=WIN_COLOR)
            return
        origen, destino = self._solve_steps[self._solve_idx]
        # Ejecutar movimiento directamente
        t_orig = self.hanoi.torres[origen]
        t_dest = self.hanoi.torres[destino]
        if t_orig:
            disco = t_orig.pop()
            t_dest.append(disco)
            self.hanoi.movimientos += 1
        self._solve_idx += 1
        self._redraw()
        self._solve_after = self.root.after(delay, lambda: self._auto_step(delay))

    def _on_stop(self):
        self._stop_auto()

    def _stop_auto(self):
        if self._solve_after:
            self.root.after_cancel(self._solve_after)
            self._solve_after = None
        self._solving = False
        self.lbl_msg.config(text="Auto-resolución detenida", fg=ACCENT2)
        self._redraw()


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app = HanoiGUI(root)
    root.mainloop()