import tkinter as tk
from tkinter import messagebox
import random

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

    def eliminar_en(self, idx):
        """Elimina elemento en posición idx y devuelve los que estaban encima."""
        if idx < 0 or idx >= len(self.elementos):
            return None
        eliminado = self.elementos[idx]
        self.elementos.pop(idx)
        return eliminado

    def peek(self):
        return self.elementos[-1] if not self.esta_vacia() else None

    def esta_vacia(self):
        return len(self.elementos) == 0

    def esta_llena(self):
        return len(self.elementos) >= self.capacidad

    def tamanio(self):
        return len(self.elementos)


class PilaGUI:
    BG          = "#0d0d0d"
    PANEL_BG    = "#111827"
    BORDER      = "#00ff99"
    ACCENT      = "#00ffcc"
    ACCENT2     = "#ff6b6b"
    ACCENT3     = "#ffd93d"
    PURPLE      = "#c084fc"
    TEXT_MAIN   = "#e0ffe8"
    TEXT_DIM    = "#4a7c59"
    BLOCK_FILL  = "#003322"
    BLOCK_EMPTY = "#1a1a2e"
    BLOCK_EMPTY_BORDER = "#1e3a2f"
    BTN_PUSH    = "#003322"
    BTN_POP     = "#2d0a0a"
    BTN_FILL    = "#1a1a00"
    BTN_CLEAR   = "#1a001a"
    FONT_MONO   = ("Courier New", 11, "bold")
    FONT_TITLE  = ("Courier New", 18, "bold")
    FONT_BTN    = ("Courier New", 11, "bold")
    FONT_SMALL  = ("Courier New", 9)

    SLOT_W = 200
    SLOT_H = 52
    SLOT_GAP = 6
    CANVAS_PAD_TOP = 40

    def __init__(self, root):
        self.root = root
        self.pila = Pila(capacidad=8)
        self._animating = False
        self._selected_idx = None   # índice en pila del elemento seleccionado

        root.title("Visualizador de Pila - Selección")
        root.configure(bg=self.BG)
        root.resizable(False, False)
        root.geometry("780x800")

        self._build_ui()
        self._draw_stack()

    def _build_ui(self):
        title_frame = tk.Frame(self.root, bg=self.BG)
        title_frame.pack(pady=(14, 0))
        tk.Label(title_frame, text="PILA / STACK",
                 font=self.FONT_TITLE, bg=self.BG, fg=self.BORDER).pack()
        tk.Label(title_frame, text="[ Haz clic en un elemento para seleccionarlo y eliminarlo ]",
                 font=self.FONT_SMALL, bg=self.BG, fg=self.ACCENT3).pack()

        canvas_h = self.pila.capacidad * (self.SLOT_H + self.SLOT_GAP) + self.CANVAS_PAD_TOP + 30
        self.canvas = tk.Canvas(self.root, width=400, height=canvas_h,
                                bg=self.PANEL_BG, highlightthickness=2,
                                highlightbackground=self.BORDER, cursor="hand2")
        self.canvas.pack(pady=12)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        info_frame = tk.Frame(self.root, bg=self.BG)
        info_frame.pack()
        self.lbl_size = tk.Label(info_frame, text="TAMANO: 0/8",
                                  font=self.FONT_MONO, bg=self.BG, fg=self.ACCENT)
        self.lbl_size.grid(row=0, column=0, padx=20)
        self.lbl_top = tk.Label(info_frame, text="TOPE: --",
                                 font=self.FONT_MONO, bg=self.BG, fg=self.ACCENT3)
        self.lbl_top.grid(row=0, column=1, padx=20)
        self.lbl_sel = tk.Label(info_frame, text="SELECCIONADO: ninguno",
                                 font=self.FONT_MONO, bg=self.BG, fg=self.PURPLE)
        self.lbl_sel.grid(row=1, column=0, columnspan=2, pady=4)

        # Instrucción de selección
        self.lbl_hint = tk.Label(self.root,
                                  text="",
                                  font=self.FONT_SMALL, bg=self.BG, fg=self.ACCENT3)
        self.lbl_hint.pack()

        btn_frame = tk.Frame(self.root, bg=self.BG)
        btn_frame.pack(pady=10)
        self._make_btn(btn_frame, "PUSH", self.BORDER, self.BTN_PUSH,
                       self._on_push).grid(row=0, column=0, padx=6)
        self.btn_eliminar = self._make_btn(btn_frame, "ELIMINAR SELECCIONADO",
                                            self.ACCENT2, self.BTN_POP, self._on_eliminar_seleccionado)
        self.btn_eliminar.grid(row=0, column=1, padx=6)
        self._make_btn(btn_frame, "LLENAR", self.ACCENT3, self.BTN_FILL,
                       self._on_llenar).grid(row=0, column=2, padx=6)
        self._make_btn(btn_frame, "VACIAR", self.PURPLE, self.BTN_CLEAR,
                       self._on_vaciar).grid(row=0, column=3, padx=6)

        log_frame = tk.Frame(self.root, bg=self.PANEL_BG,
                              highlightthickness=1, highlightbackground=self.TEXT_DIM)
        log_frame.pack(fill="x", padx=30, pady=(8, 12))
        tk.Label(log_frame, text=" REGISTRO DE OPERACIONES ",
                 font=self.FONT_SMALL, bg=self.PANEL_BG, fg=self.TEXT_DIM).pack(anchor="w", padx=4)
        self.log_text = tk.Text(log_frame, height=5, bg=self.PANEL_BG, fg=self.ACCENT,
                                font=self.FONT_SMALL, state="disabled", relief="flat", wrap="word")
        self.log_text.pack(fill="x", padx=4, pady=(0, 4))

    def _make_btn(self, parent, text, fg, bg, cmd):
        btn = tk.Button(parent, text=text, font=self.FONT_BTN,
                        fg=fg, bg=bg, activeforeground=self.BG,
                        activebackground=fg, relief="flat",
                        padx=10, pady=7, cursor="hand2",
                        bd=0, highlightthickness=1,
                        highlightbackground=fg, command=cmd)
        btn.bind("<Enter>", lambda e, b=btn, c=fg: b.config(bg=c, fg=self.BG))
        btn.bind("<Leave>", lambda e, b=btn, c=bg, d=fg: b.config(bg=c, fg=d))
        return btn

    # ── Detectar clic en bloque ────────────────
    def _on_canvas_click(self, event):
        if self._animating:
            return
        if self.pila.esta_vacia():
            return

        cap = self.pila.capacidad
        cw = int(self.canvas["width"])
        x0 = (cw - self.SLOT_W) // 2
        x1 = x0 + self.SLOT_W

        if not (x0 <= event.x <= x1):
            # Clic fuera del bloque → deseleccionar
            self._selected_idx = None
            self.lbl_sel.config(text="SELECCIONADO: ninguno")
            self.lbl_hint.config(text="")
            self._draw_stack()
            return

        for i in range(cap):
            stack_pos = cap - 1 - i
            y_top = self.CANVAS_PAD_TOP + i * (self.SLOT_H + self.SLOT_GAP)
            y_bot = y_top + self.SLOT_H
            if y_top <= event.y <= y_bot and stack_pos < self.pila.tamanio():
                # Seleccionar / deseleccionar
                if self._selected_idx == stack_pos:
                    self._selected_idx = None
                    self.lbl_sel.config(text="SELECCIONADO: ninguno")
                    self.lbl_hint.config(text="")
                else:
                    self._selected_idx = stack_pos
                    val = self.pila.elementos[stack_pos]
                    encima = self.pila.tamanio() - 1 - stack_pos
                    self.lbl_sel.config(text=f"SELECCIONADO: '{val}' (pos {stack_pos})")
                    if encima > 0:
                        self.lbl_hint.config(
                            text=f"Se eliminara '{val}' y se restauraran {encima} elemento(s) encima.")
                    else:
                        self.lbl_hint.config(text=f"Se eliminara '{val}' del tope.")
                self._draw_stack()
                return

    # ── Dibujo ────────────────────────────────
    def _draw_stack(self, override_elems=None, highlight_idx=None,
                    highlight_color=None, caida_idx=None):
        self.canvas.delete("all")
        cap = self.pila.capacidad
        elems = override_elems if override_elems is not None else list(self.pila.elementos)
        n = len(elems)
        cw = int(self.canvas["width"])

        self.canvas.create_text(cw // 2, 20, text="TOPE (TOP)",
                                 fill=self.BORDER, font=self.FONT_SMALL)

        for i in range(cap):
            stack_pos = cap - 1 - i
            y_top = self.CANVAS_PAD_TOP + i * (self.SLOT_H + self.SLOT_GAP)
            y_bot = y_top + self.SLOT_H
            x0 = (cw - self.SLOT_W) // 2
            x1 = x0 + self.SLOT_W

            occupied = stack_pos < n

            if occupied:
                val = elems[stack_pos]
                is_selected = (override_elems is None and self._selected_idx == stack_pos)
                is_highlight = (highlight_idx == stack_pos and highlight_color)

                if is_highlight:
                    fill = highlight_color
                    border = "#ffffff"
                elif is_selected:
                    fill = "#1a0033"
                    border = self.PURPLE
                else:
                    fill = self.BLOCK_FILL
                    border = self.BORDER if stack_pos != (n - 1) else self.ACCENT3

                text_col = self.TEXT_MAIN

                # Animación de caída: elementos encima bajan un slot
                if caida_idx is not None and stack_pos > caida_idx:
                    fill = "#002244"
                    border = self.ACCENT
            else:
                fill = self.BLOCK_EMPTY
                border = self.BLOCK_EMPTY_BORDER
                text_col = self.TEXT_DIM
                val = "."

            self.canvas.create_rectangle(x0+3, y_top+3, x1+3, y_bot+3,
                                          fill="#000000", outline="")
            self.canvas.create_rectangle(x0, y_top, x1, y_bot,
                                          fill=fill, outline=border, width=2)

            if occupied:
                if override_elems is None and self._selected_idx == stack_pos:
                    self.canvas.create_text(x0-22, (y_top+y_bot)//2,
                                             text=">>", fill=self.PURPLE,
                                             font=("Courier New", 11, "bold"))
                elif stack_pos == n - 1 and highlight_idx is None:
                    self.canvas.create_text(x0-18, (y_top+y_bot)//2,
                                             text="->", fill=self.ACCENT3,
                                             font=("Courier New", 13, "bold"))

                self.canvas.create_text((x0+x1)//2, (y_top+y_bot)//2,
                                         text=str(val), fill=text_col,
                                         font=("Courier New", 16, "bold"))

            self.canvas.create_text(x1+22, (y_top+y_bot)//2,
                                     text=f"[{stack_pos}]",
                                     fill=self.TEXT_DIM, font=self.FONT_SMALL)

        y_base = self.CANVAS_PAD_TOP + cap * (self.SLOT_H + self.SLOT_GAP)
        self.canvas.create_text(cw // 2, y_base + 10, text="FONDO (BOTTOM)",
                                 fill=self.TEXT_DIM, font=self.FONT_SMALL)

        top_val = self.pila.peek() if not self.pila.esta_vacia() else "--"
        self.lbl_size.config(text=f"TAMANO: {self.pila.tamanio()}/{self.pila.capacidad}")
        self.lbl_top.config(text=f"TOPE: {top_val}")

    # ── Animación eliminar + restaurar ─────────
    def _on_eliminar_seleccionado(self):
        if self._animating:
            return
        if self._selected_idx is None:
            messagebox.showinfo("Sin seleccion", "Haz clic en un elemento de la pila para seleccionarlo.")
            return
        if self.pila.esta_vacia():
            return

        idx = self._selected_idx
        valor = self.pila.elementos[idx]
        snap_antes = list(self.pila.elementos)   # copia ANTES de eliminar
        encima = self.pila.tamanio() - 1 - idx   # cuántos elementos hay encima

        # Realizar el pop del elemento seleccionado
        self.pila.eliminar_en(idx)
        snap_despues = list(self.pila.elementos)  # copia DESPUÉS de eliminar

        self._animating = True
        self._selected_idx = None
        self.lbl_sel.config(text="SELECCIONADO: ninguno")
        self.lbl_hint.config(text="")

        # FASE 1: parpadear el elemento seleccionado (mostrar que se va a eliminar)
        flashes = [True, False, True, False, True, False]
        def fase1(i=0):
            if i >= len(flashes):
                fase2()
                return
            color = "#4d0000" if flashes[i] else "#1a0033"
            self._draw_stack(override_elems=snap_antes,
                             highlight_idx=idx, highlight_color=color)
            self.root.after(100, lambda: fase1(i + 1))

        # FASE 2: mostrar "hueco" donde estaba el elemento (snap_antes sin ese elemento visualmente)
        def fase2():
            # Dibujar snap_antes pero el slot eliminado vacío
            snap_hueco = list(snap_antes)
            snap_hueco[idx] = None  # marcador de hueco
            _draw_con_hueco(snap_hueco)
            self.root.after(300, fase3)

        def _draw_con_hueco(snap):
            """Dibuja la pila con un hueco donde estaba el eliminado."""
            self.canvas.delete("all")
            cap = self.pila.capacidad
            cw = int(self.canvas["width"])
            self.canvas.create_text(cw // 2, 20, text="TOPE (TOP)",
                                     fill=self.BORDER, font=self.FONT_SMALL)
            n = len(snap)
            for i in range(cap):
                stack_pos = cap - 1 - i
                y_top = self.CANVAS_PAD_TOP + i * (self.SLOT_H + self.SLOT_GAP)
                y_bot = y_top + self.SLOT_H
                x0 = (cw - self.SLOT_W) // 2
                x1 = x0 + self.SLOT_W

                if stack_pos < n and snap[stack_pos] is not None:
                    val = snap[stack_pos]
                    # Elementos encima del hueco se resaltan en azul
                    if stack_pos > idx:
                        fill, border, text_col = "#002244", self.ACCENT, self.TEXT_MAIN
                    else:
                        fill, border, text_col = self.BLOCK_FILL, self.BORDER, self.TEXT_MAIN
                    self.canvas.create_rectangle(x0+3, y_top+3, x1+3, y_bot+3, fill="#000000", outline="")
                    self.canvas.create_rectangle(x0, y_top, x1, y_bot, fill=fill, outline=border, width=2)
                    self.canvas.create_text((x0+x1)//2, (y_top+y_bot)//2,
                                             text=str(val), fill=text_col,
                                             font=("Courier New", 16, "bold"))
                elif stack_pos == idx:
                    # Hueco: slot vacío resaltado en rojo tenue
                    self.canvas.create_rectangle(x0+3, y_top+3, x1+3, y_bot+3, fill="#000000", outline="")
                    self.canvas.create_rectangle(x0, y_top, x1, y_bot,
                                                  fill="#2d0000", outline=self.ACCENT2, width=2)
                    self.canvas.create_text((x0+x1)//2, (y_top+y_bot)//2,
                                             text="[ ELIMINADO ]", fill=self.ACCENT2,
                                             font=("Courier New", 11, "bold"))
                else:
                    self.canvas.create_rectangle(x0+3, y_top+3, x1+3, y_bot+3, fill="#000000", outline="")
                    self.canvas.create_rectangle(x0, y_top, x1, y_bot,
                                                  fill=self.BLOCK_EMPTY, outline=self.BLOCK_EMPTY_BORDER, width=2)
                self.canvas.create_text(x1+22, (y_top+y_bot)//2,
                                         text=f"[{stack_pos}]",
                                         fill=self.TEXT_DIM, font=self.FONT_SMALL)
            y_base = self.CANVAS_PAD_TOP + cap * (self.SLOT_H + self.SLOT_GAP)
            self.canvas.create_text(cw//2, y_base+10, text="FONDO (BOTTOM)",
                                     fill=self.TEXT_DIM, font=self.FONT_SMALL)

        # FASE 3: animación de caída - los elementos encima bajan uno a uno
        def fase3():
            if encima == 0:
                fase_final()
                return
            # Parpadear en azul los elementos que van a caer
            pasos = [True, False, True, False]
            def parpadeo(i=0):
                if i >= len(pasos):
                    # Mostrar resultado final con animación
                    self._draw_stack(override_elems=snap_despues,
                                     caida_idx=-1)
                    self.root.after(250, fase_final)
                    return
                color = "#003366" if pasos[i] else "#002244"
                snap_hueco = list(snap_antes)
                snap_hueco[idx] = None
                _draw_con_hueco(snap_hueco)
                self.root.after(120, lambda: parpadeo(i+1))
            parpadeo()

        def fase_final():
            self._draw_stack()
            msg = f"Eliminado: '{valor}'"
            if encima > 0:
                msg += f"  |  {encima} elemento(s) restaurados encima"
            msg += f"  |  Quedan: {self.pila.tamanio()}"
            self._log(msg, self.ACCENT2)
            self._animating = False

        fase1()

    # ── PUSH ──────────────────────────────────
    def _on_push(self):
        if self._animating:
            return
        if self.pila.esta_llena():
            self._log("OVERFLOW -- La pila esta llena.", self.ACCENT2)
            messagebox.showwarning("Pila Llena", "La pila esta llena.")
            return
        # Ventana simple para ingresar valor
        win = tk.Toplevel(self.root)
        win.title("PUSH")
        win.configure(bg=self.BG)
        win.resizable(False, False)
        win.geometry("300x130")
        win.grab_set()
        tk.Label(win, text="Valor a insertar:", font=self.FONT_MONO,
                 bg=self.BG, fg=self.BORDER).pack(pady=(18, 4))
        entry = tk.Entry(win, font=self.FONT_MONO, bg=self.PANEL_BG,
                         fg=self.TEXT_MAIN, insertbackground=self.BORDER,
                         relief="flat", width=18)
        entry.pack()
        entry.focus()

        def confirmar(event=None):
            val = entry.get().strip() or "?"
            win.destroy()
            self._animating = True
            self.pila.push(val)
            idx = self.pila.tamanio() - 1
            flashes = [True, False, True, False, True]
            def anim(i=0):
                if i >= len(flashes):
                    self._draw_stack()
                    self._log(f"PUSH <- '{val}'  |  Tamano: {self.pila.tamanio()}", self.BORDER)
                    self._animating = False
                    return
                color = "#004d33" if flashes[i] else self.BLOCK_FILL
                self._draw_stack(highlight_idx=idx, highlight_color=color)
                self.root.after(100, lambda: anim(i+1))
            anim()

        entry.bind("<Return>", confirmar)
        self._make_btn(win, "INSERTAR", self.BORDER, self.BTN_PUSH, confirmar).pack(pady=10)

    # ── LLENAR ────────────────────────────────
    def _on_llenar(self):
        if self._animating:
            return
        if self.pila.esta_llena():
            self._log("La pila ya esta llena.", self.ACCENT3)
            return
        self._animating = True
        datos = ["A", "B", "C", "D", "E", "F", "42", "X", "Z", "7", "K", "M"]
        def paso():
            if self.pila.esta_llena():
                self._draw_stack()
                self._log("LLENAR completado.", self.ACCENT3)
                self._animating = False
                return
            val = random.choice(datos)
            self.pila.push(val)
            self._draw_stack(highlight_idx=self.pila.tamanio()-1, highlight_color="#003322")
            self.root.after(180, paso)
        paso()

    # ── VACIAR ────────────────────────────────
    def _on_vaciar(self):
        if self._animating:
            return
        if self.pila.esta_vacia():
            self._log("La pila ya esta vacia.", self.PURPLE)
            return
        if not messagebox.askyesno("Vaciar", "Seguro que deseas vaciar toda la pila?"):
            return
        self._animating = True
        def paso():
            if self.pila.esta_vacia():
                self._draw_stack()
                self._log("VACIAR completado.", self.PURPLE)
                self._animating = False
                return
            idx = self.pila.tamanio() - 1
            self._draw_stack(highlight_idx=idx, highlight_color="#2d002d")
            self.root.after(120, quitar)
        def quitar():
            self.pila.pop()
            self.root.after(60, paso)
        paso()

    # ── LOG ───────────────────────────────────
    def _log(self, msg, color=None):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = PilaGUI(root)
    root.mainloop()