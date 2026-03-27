import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import random

# ─────────────────────────────────────────────
#  ESTRUCTURA DE DATOS: PILA
# ─────────────────────────────────────────────
class Pila:
    def __init__(self, capacidad=8):
        self.capacidad = capacidad
        self.elementos = []

    def push(self, valor):
        if self.esta_llena():
            return False
        self.elementos.append(valor)
        return True

    def pop(self):
        if self.esta_vacia():
            return None
        return self.elementos.pop()

    def peek(self):
        if self.esta_vacia():
            return None
        return self.elementos[-1]

    def esta_vacia(self):
        return len(self.elementos) == 0

    def esta_llena(self):
        return len(self.elementos) >= self.capacidad

    def vaciar(self):
        self.elementos.clear()

    def llenar(self):
        datos = ["🍎", "🚀", "💎", "🔥", "⚡", "🎯", "🌟", "🎲"]
        while not self.esta_llena():
            self.elementos.append(random.choice(datos))

    def tamanio(self):
        return len(self.elementos)


# ─────────────────────────────────────────────
#  INTERFAZ GRÁFICA
# ─────────────────────────────────────────────
class PilaGUI:
    # Paleta de colores – estilo terminal retro neón
    BG          = "#0d0d0d"
    PANEL_BG    = "#111827"
    BORDER      = "#00ff99"
    ACCENT      = "#00ffcc"
    ACCENT2     = "#ff6b6b"
    ACCENT3     = "#ffd93d"
    TEXT_MAIN   = "#e0ffe8"
    TEXT_DIM    = "#4a7c59"
    BLOCK_FILL  = "#003322"
    BLOCK_TOP   = "#00ff99"
    BLOCK_EMPTY = "#1a1a2e"
    BLOCK_EMPTY_BORDER = "#1e3a2f"
    BTN_PUSH    = "#003322"
    BTN_POP     = "#2d0a0a"
    BTN_FILL    = "#1a1a00"
    BTN_CLEAR   = "#1a001a"
    BTN_HOVER   = "#00ff99"
    FONT_MONO   = ("Courier New", 11, "bold")
    FONT_TITLE  = ("Courier New", 20, "bold")
    FONT_BTN    = ("Courier New", 12, "bold")
    FONT_SMALL  = ("Courier New", 9)
    FONT_BIG    = ("Courier New", 26, "bold")

    SLOT_W = 200
    SLOT_H = 52
    SLOT_GAP = 6
    CANVAS_PAD_X = 60
    CANVAS_PAD_TOP = 40

    def __init__(self, root):
        self.root = root
        self.pila = Pila(capacidad=8)
        self._animating = False

        root.title("⬆ Visualizador de Pila")
        root.configure(bg=self.BG)
        root.resizable(False, False)
        root.geometry("760x740")

        self._build_ui()
        self._draw_stack()

    # ── UI Layout ─────────────────────────────
    def _build_ui(self):
        # Título
        title_frame = tk.Frame(self.root, bg=self.BG)
        title_frame.pack(pady=(18, 0))
        tk.Label(title_frame, text="▓▒░ PILA / STACK ░▒▓",
                 font=self.FONT_TITLE, bg=self.BG, fg=self.BORDER).pack()
        tk.Label(title_frame, text="[ Estructura LIFO · Last In, First Out ]",
                 font=self.FONT_SMALL, bg=self.BG, fg=self.TEXT_DIM).pack()

        # Canvas (visualización)
        canvas_h = self.pila.capacidad * (self.SLOT_H + self.SLOT_GAP) + self.CANVAS_PAD_TOP + 30
        self.canvas = tk.Canvas(self.root, width=380, height=canvas_h,
                                bg=self.PANEL_BG, highlightthickness=2,
                                highlightbackground=self.BORDER)
        self.canvas.pack(pady=16)

        # Panel de info (tamaño / tope)
        info_frame = tk.Frame(self.root, bg=self.BG)
        info_frame.pack()
        self.lbl_size = tk.Label(info_frame, text="TAMAÑO: 0/8",
                                  font=self.FONT_MONO, bg=self.BG, fg=self.ACCENT)
        self.lbl_size.grid(row=0, column=0, padx=20)
        self.lbl_top = tk.Label(info_frame, text="TOPE:  —",
                                 font=self.FONT_MONO, bg=self.BG, fg=self.ACCENT3)
        self.lbl_top.grid(row=0, column=1, padx=20)

        # Botones
        btn_frame = tk.Frame(self.root, bg=self.BG)
        btn_frame.pack(pady=14)

        self._make_btn(btn_frame, "⬆  PUSH", self.BORDER, self.BTN_PUSH,
                       self._on_push).grid(row=0, column=0, padx=8, pady=5)
        self._make_btn(btn_frame, "⬇  POP", self.ACCENT2, self.BTN_POP,
                       self._on_pop).grid(row=0, column=1, padx=8, pady=5)
        self._make_btn(btn_frame, "⚡ LLENAR", self.ACCENT3, self.BTN_FILL,
                       self._on_llenar).grid(row=0, column=2, padx=8, pady=5)
        self._make_btn(btn_frame, "✕  VACIAR", "#c084fc", self.BTN_CLEAR,
                       self._on_vaciar).grid(row=0, column=3, padx=8, pady=5)

        # Log de operaciones
        log_frame = tk.Frame(self.root, bg=self.PANEL_BG,
                              highlightthickness=1, highlightbackground=self.TEXT_DIM)
        log_frame.pack(fill="x", padx=30, pady=(0, 16))
        tk.Label(log_frame, text=" REGISTRO DE OPERACIONES ",
                 font=self.FONT_SMALL, bg=self.PANEL_BG, fg=self.TEXT_DIM).pack(anchor="w", padx=4)
        self.log_text = tk.Text(log_frame, height=5, bg=self.PANEL_BG, fg=self.ACCENT,
                                font=self.FONT_SMALL, state="disabled",
                                relief="flat", wrap="word", insertbackground=self.BORDER)
        self.log_text.pack(fill="x", padx=4, pady=(0, 4))

    def _make_btn(self, parent, text, fg, bg, cmd):
        btn = tk.Button(parent, text=text, font=self.FONT_BTN,
                        fg=fg, bg=bg, activeforeground=self.BG,
                        activebackground=fg, relief="flat",
                        padx=14, pady=8, cursor="hand2",
                        bd=0, highlightthickness=1,
                        highlightbackground=fg, command=cmd)
        btn.bind("<Enter>", lambda e, b=btn, c=fg: b.config(bg=c, fg=self.BG))
        btn.bind("<Leave>", lambda e, b=btn, c=bg, d=fg: b.config(bg=c, fg=d))
        return btn

    # ── Dibujo del canvas ─────────────────────
    def _draw_stack(self, highlight_idx=None, highlight_color=None):
        self.canvas.delete("all")
        cap = self.pila.capacidad
        elems = self.pila.elementos
        n = len(elems)

        cw = int(self.canvas["width"])

        # Etiqueta "TOPE ↑" arriba
        self.canvas.create_text(cw // 2, 20, text="↑ TOPE (TOP)",
                                 fill=self.BORDER, font=self.FONT_SMALL)

        for i in range(cap):
            # i=0 → fondo, i=cap-1 → tope visual
            stack_pos = cap - 1 - i          # posición en la pila (0=fondo)
            y_top = self.CANVAS_PAD_TOP + i * (self.SLOT_H + self.SLOT_GAP)
            y_bot = y_top + self.SLOT_H
            x0 = (cw - self.SLOT_W) // 2
            x1 = x0 + self.SLOT_W

            occupied = stack_pos < n

            if occupied:
                val = elems[stack_pos]
                fill = self.BLOCK_FILL
                border = self.BORDER if stack_pos != (n - 1) else self.ACCENT3
                text_col = self.TEXT_MAIN
                if highlight_idx == stack_pos and highlight_color:
                    fill = highlight_color
                    border = "#ffffff"
            else:
                fill = self.BLOCK_EMPTY
                border = self.BLOCK_EMPTY_BORDER
                text_col = self.TEXT_DIM
                val = "·  ·  ·"

            # Sombra
            self.canvas.create_rectangle(x0 + 3, y_top + 3, x1 + 3, y_bot + 3,
                                          fill="#000000", outline="")
            # Bloque
            self.canvas.create_rectangle(x0, y_top, x1, y_bot,
                                          fill=fill, outline=border, width=2)

            # Indicador de tope
            if occupied and stack_pos == n - 1:
                self.canvas.create_text(x0 - 18, (y_top + y_bot) // 2,
                                         text="►", fill=self.ACCENT3,
                                         font=("Courier New", 13, "bold"))

            # Texto del elemento
            self.canvas.create_text((x0 + x1) // 2, (y_top + y_bot) // 2,
                                     text=str(val), fill=text_col,
                                     font=("Courier New", 16, "bold"))

            # Índice de posición
            self.canvas.create_text(x1 + 22, (y_top + y_bot) // 2,
                                     text=f"[{stack_pos}]",
                                     fill=self.TEXT_DIM, font=self.FONT_SMALL)

        # Etiqueta "FONDO ↓" abajo
        y_base = self.CANVAS_PAD_TOP + cap * (self.SLOT_H + self.SLOT_GAP)
        self.canvas.create_text(cw // 2, y_base + 10, text="↓ FONDO (BOTTOM)",
                                 fill=self.TEXT_DIM, font=self.FONT_SMALL)

        # Actualizar labels
        top_val = self.pila.peek() if not self.pila.esta_vacia() else "—"
        self.lbl_size.config(text=f"TAMAÑO: {self.pila.tamanio()}/{self.pila.capacidad}")
        self.lbl_top.config(text=f"TOPE:  {top_val}")

    # ── Animaciones ───────────────────────────
    def _flash(self, idx, color, callback):
        flashes = [True, False, True, False, True]
        def step(i=0):
            if i >= len(flashes):
                callback()
                return
            c = color if flashes[i] else self.BLOCK_FILL
            self._draw_stack(highlight_idx=idx, highlight_color=c)
            self.root.after(90, lambda: step(i + 1))
        step()

    # ── Operaciones ───────────────────────────
    def _on_push(self):
        if self._animating:
            return
        if self.pila.esta_llena():
            self._log("⚠  OVERFLOW — La pila está llena.", self.ACCENT2)
            messagebox.showwarning("Pila Llena", "¡La pila está llena!\nNo se pueden insertar más elementos.")
            return
        valor = simpledialog.askstring("PUSH", "Ingresa el valor a insertar:",
                                        parent=self.root)
        if valor is None:
            return
        valor = valor.strip() or "?"
        self._animating = True
        self.pila.push(valor)
        idx = self.pila.tamanio() - 1
        self._flash(idx, "#004d33", lambda: self._finish_push(valor))

    def _finish_push(self, valor):
        self._draw_stack()
        self._log(f"✔  PUSH ← '{valor}'  |  Tamaño: {self.pila.tamanio()}", self.BORDER)
        self._animating = False

    def _on_pop(self):
        if self._animating:
            return
        if self.pila.esta_vacia():
            self._log("⚠  UNDERFLOW — La pila está vacía.", self.ACCENT2)
            messagebox.showwarning("Pila Vacía", "¡La pila está vacía!\nNo hay elementos para eliminar.")
            return
        self._animating = True
        idx = self.pila.tamanio() - 1
        self._flash(idx, "#4d0000", lambda: self._finish_pop())

    def _finish_pop(self):
        valor = self.pila.pop()
        self._draw_stack()
        self._log(f"✔  POP  → '{valor}'  |  Tamaño: {self.pila.tamanio()}", self.ACCENT2)
        self._animating = False

    def _on_llenar(self):
        if self._animating:
            return
        if self.pila.esta_llena():
            self._log("⚠  La pila ya está llena.", self.ACCENT3)
            return
        self._animating = True
        self._llenar_paso()

    def _llenar_paso(self):
        if self.pila.esta_llena():
            self._draw_stack()
            self._log("⚡ LLENAR completado — Pila llena.", self.ACCENT3)
            self._animating = False
            return
        self.pila.llenar.__func__  # just reference
        datos = ["🍎", "🚀", "💎", "🔥", "⚡", "🎯", "🌟", "🎲", "42", "X", "π", "#"]
        val = random.choice(datos)
        self.pila.push(val)
        self._draw_stack(highlight_idx=self.pila.tamanio() - 1, highlight_color="#003322")
        self.root.after(180, self._llenar_paso)

    def _on_vaciar(self):
        if self._animating:
            return
        if self.pila.esta_vacia():
            self._log("⚠  La pila ya está vacía.", "#c084fc")
            return
        if not messagebox.askyesno("Vaciar Pila", "¿Seguro que deseas vaciar toda la pila?"):
            return
        self._animating = True
        self._vaciar_paso()

    def _vaciar_paso(self):
        if self.pila.esta_vacia():
            self._draw_stack()
            self._log("✕  VACIAR completado — Pila vacía.", "#c084fc")
            self._animating = False
            return
        idx = self.pila.tamanio() - 1
        self._draw_stack(highlight_idx=idx, highlight_color="#2d002d")
        self.root.after(120, lambda: self._vaciar_quitar())

    def _vaciar_quitar(self):
        self.pila.pop()
        self.root.after(60, self._vaciar_paso)

    # ── Log ───────────────────────────────────
    def _log(self, msg, color=None):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")


# ─────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = PilaGUI(root)
    root.mainloop()