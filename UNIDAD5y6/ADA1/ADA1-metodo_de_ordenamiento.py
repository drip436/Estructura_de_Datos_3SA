"""
INTEGRANTES: 
- SALAS POOT GLENDY PATRICIA
- JAROL GAEL LIZAMA CHAN
- MARVING ANTONIO TUT NOVELO
- YAMA UITZ ADRIAN ENRIQUE 
-GERARDO EMANUEL MENA MARTIN
-JESUS LEONARDO ROMERO PECH
-CARLOS JESUS LOPEZ SIERRA
"""

import tkinter as tk
from tkinter import ttk, font, messagebox
import time
import random

# ══════════════════════════════════════════════════════
#  CONFIGURACIÓN GLOBAL DE COLORES Y ESTILOS
# ══════════════════════════════════════════════════════
COLORES = {
    "fondo":           "#0F1117",   # Fondo principal oscuro
    "panel":           "#1A1D27",   # Fondo de paneles secundarios
    "borde":           "#2E3250",   # Color de bordes suaves
    "acento":           "#5B6EF5",   # Azul-índigo principal (acento)
    "acento_claro":    "#7B8FFF",   # Variante más clara del acento
    "barra_normal":    "#3D4A8A",   # Barra en estado neutro
    "barra_comparar1": "#F5495B",   # Primer elemento en comparación (rojo)
    "barra_comparar2": "#F5C842",   # Segundo elemento en comparación (amarillo)
    "barra_ordenada":  "#42C78C",   # Elemento ya en posición correcta (verde)
    "barra_pivot":     "#A855F7",   # Elemento siendo movido
    "texto":           "#E8EAF6",   # Texto principal blanco-azulado
    "texto_secundario":"#8892B0",   # Texto secundario gris
    "texto_numero":    "#FFFFFF",   # Números sobre barras
    "exito":           "#42C78C",   # Verde para mensaje de éxito
    "advertencia":     "#F5C842",   # Amarillo para advertencias
    "error":           "#F5495B",   # Rojo para intercambios
    "linea_log":       "#1E2235",   # Fondo alterno de líneas del log
}

FUENTE_TITULO   = ("Courier New", 13, "bold")
FUENTE_SUBTITULO= ("Courier New", 10, "bold")
FUENTE_NORMAL   = ("Courier New", 9)
FUENTE_CODIGO   = ("Courier New", 9)
FUENTE_GRANDE   = ("Courier New", 28, "bold")
FUENTE_BARRA    = ("Courier New", 11, "bold")


# ══════════════════════════════════════════════════════
#  CLASE PRINCIPAL: BubbleSortSimulator
# ══════════════════════════════════════════════════════
class BubbleSortSimulator:
    def __init__(self, root: tk.Tk):
        self.root = root
        # Vector por defecto inicial
        self.VECTOR_ORIGINAL = [45, 17, 23, 67, 21, 5, 17, 23, 67, 21]
        self._configurar_ventana()

        # ── Estado del algoritmo ──────────────────────────
        self.vector           = list(self.VECTOR_ORIGINAL)
        self.n                = len(self.vector)
        self.i_externo       = 0
        self.j_interno       = 0
        self.total_comparaciones = 0
        self.total_intercambios  = 0
        self.finalizado      = False
        self.reproduciendo   = False
        self._job_after      = None

        # ── Índices especiales para colorear ─────────────
        self.idx_comparando_1 = -1
        self.idx_comparando_2 = -1
        self.indices_ordenados = set()

        # ── Historial de pasos (log) ──────────────────────
        self.log_pasos = []

        # ── Construir la interfaz ─────────────────────────
        self._construir_ui()
        self._dibujar_barras()
        self._actualizar_contadores()

    def _configurar_ventana(self):
        self.root.title("SISTEMA DE GESTIÓN: Ordenamiento de Precios")
        self.root.configure(bg=COLORES["fondo"])
        self.root.resizable(False, False)

        ancho, alto = 950, 750
        x = (self.root.winfo_screenwidth()  - ancho) // 2
        y = (self.root.winfo_screenheight() - alto)  // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _construir_ui(self):
        self._crear_cabecera()
        self._crear_cuerpo_principal()
        self._crear_panel_inferior()

    def _crear_cabecera(self):
        frame = tk.Frame(self.root, bg=COLORES["panel"],
                         highlightbackground=COLORES["acento"],
                         highlightthickness=1)
        frame.pack(fill="x", padx=10, pady=(10, 0))

        tk.Label(frame,
                 text="◈  SISTEMA DE INVENTARIO: CARGA MASIVA  ◈",
                 font=FUENTE_TITULO,
                 fg=COLORES["acento_claro"],
                 bg=COLORES["panel"]).pack(side="left", padx=15, pady=8)

        self.lbl_vector = tk.Label(frame,
                                   text=f"Elementos: {len(self.vector)}",
                                   font=FUENTE_CODIGO,
                                   fg=COLORES["texto_secundario"],
                                   bg=COLORES["panel"])
        self.lbl_vector.pack(side="right", padx=15)

    def _crear_cuerpo_principal(self):
        frame_cuerpo = tk.Frame(self.root, bg=COLORES["fondo"])
        frame_cuerpo.pack(fill="both", expand=True, padx=10, pady=8)

        self._crear_canvas_visualizacion(frame_cuerpo)
        self._crear_panel_lateral(frame_cuerpo)

    def _crear_canvas_visualizacion(self, padre):
        frame_canvas = tk.Frame(padre, bg=COLORES["panel"],
                                highlightbackground=COLORES["borde"],
                                highlightthickness=1)
        frame_canvas.pack(side="left", fill="both", expand=True, padx=(0, 6))

        tk.Label(frame_canvas,
                 text="▸ Monitor de Densidad de Datos (Precios USD)",
                 font=FUENTE_SUBTITULO,
                 fg=COLORES["texto_secundario"],
                 bg=COLORES["panel"]).pack(anchor="w", padx=10, pady=(6, 0))

        self.canvas = tk.Canvas(frame_canvas,
                                width=600, height=350,
                                bg=COLORES["panel"],
                                highlightthickness=0)
        self.canvas.pack(padx=10, pady=(10, 6), fill="both", expand=True)

        self._crear_leyenda(frame_canvas)

    def _crear_leyenda(self, padre):
        frame = tk.Frame(padre, bg=COLORES["panel"])
        frame.pack(padx=10, pady=(0, 8))
        leyenda = [
            (COLORES["barra_normal"],    "Precio Base"),
            (COLORES["barra_comparar1"], "En Análisis"),
            (COLORES["barra_ordenada"],  "Organizado ✓"),
        ]
        for color, texto in leyenda:
            tk.Label(frame, text="■", fg=color, bg=COLORES["panel"],
                     font=("Courier New", 10)).pack(side="left", padx=(4, 0))
            tk.Label(frame, text=texto, fg=COLORES["texto_secundario"],
                     bg=COLORES["panel"], font=FUENTE_NORMAL).pack(side="left", padx=(0, 8))

    def _crear_panel_lateral(self, padre):
        frame = tk.Frame(padre, bg=COLORES["panel"],
                         highlightbackground=COLORES["borde"],
                         highlightthickness=1, width=300)
        frame.pack(side="right", fill="both")
        frame.pack_propagate(False)

        # ── ENTRADA DE DATOS (NUEVO) ──────────────────
        tk.Label(frame, text="▸ Carga de Elementos", font=FUENTE_SUBTITULO,
                 fg=COLORES["acento_claro"], bg=COLORES["panel"]).pack(anchor="w", padx=10, pady=(8, 2))
        
        self.txt_input = tk.Text(frame, height=4, bg=COLORES["fondo"], fg=COLORES["texto"],
                                 font=FUENTE_CODIGO, highlightthickness=1, highlightbackground=COLORES["borde"])
        self.txt_input.pack(fill="x", padx=10, pady=2)
        self.txt_input.insert("1.0", "45, 17, 23, 67, 21")

        frame_input_btns = tk.Frame(frame, bg=COLORES["panel"])
        frame_input_btns.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_input_btns, text="Cargar Manual", bg=COLORES["borde"], fg="#FFF",
                  command=self._cargar_manual, font=FUENTE_NORMAL, relief="flat").pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(frame_input_btns, text="Azar 1000", bg=COLORES["borde"], fg="#FFF",
                  command=self._cargar_1000, font=FUENTE_NORMAL, relief="flat").pack(side="left", expand=True, fill="x", padx=2)

        # ── STATS ──────────────────────────────────
        self.lbl_pasada      = self._stat_row(frame, "Ciclo Revisión:", COLORES["acento_claro"])
        self.lbl_total_comp  = self._stat_row(frame, "Revisiones:", COLORES["texto"])
        self.lbl_total_int   = self._stat_row(frame, "Intercambios:", COLORES["error"])

        # ── REGISTRO ──────────────────────────────
        tk.Label(frame, text="▸ Estado", font=FUENTE_SUBTITULO, fg=COLORES["texto_secundario"], bg=COLORES["panel"]).pack(anchor="w", padx=10)
        self.lbl_explicacion = tk.Label(frame, text="Listo para procesar.", font=FUENTE_NORMAL,
                                        fg=COLORES["texto"], bg=COLORES["fondo"], wraplength=260, height=3, anchor="nw", justify="left")
        self.lbl_explicacion.pack(fill="x", padx=10, pady=5)

        # ── VELOCIDAD ─────────────────────────────
        tk.Label(frame, text="▸ Velocidad (Turbo recomendado p/ 1000)", font=FUENTE_SUBTITULO, fg=COLORES["texto_secundario"], bg=COLORES["panel"]).pack(anchor="w", padx=10)
        self.slider_velocidad = tk.Scale(frame, from_=0, to=2000, orient="horizontal", bg=COLORES["panel"], fg=COLORES["texto"],
                                         troughcolor=COLORES["borde"], highlightthickness=0, bd=0, showvalue=False)
        self.slider_velocidad.set(1950)
        self.slider_velocidad.pack(fill="x", padx=10)

        self._crear_botones_control(frame)

    def _stat_row(self, parent, etiqueta, color_val):
        row = tk.Frame(parent, bg=COLORES["panel"])
        row.pack(fill="x", padx=10, pady=2)
        tk.Label(row, text=etiqueta, font=FUENTE_CODIGO, fg=COLORES["texto_secundario"], bg=COLORES["panel"]).pack(side="left")
        lbl = tk.Label(row, text="0", font=FUENTE_CODIGO, fg=color_val, bg=COLORES["panel"])
        lbl.pack(side="right")
        return lbl

    def _crear_botones_control(self, padre):
        frame = tk.Frame(padre, bg=COLORES["panel"])
        frame.pack(fill="x", padx=10, pady=10)
        
        btn_style = {"relief": "flat", "cursor": "hand2", "font": FUENTE_SUBTITULO, "pady": 8}
        
        self.btn_paso = tk.Button(frame, text="▶ Paso a Paso", bg=COLORES["acento"], fg="#FFF", command=self._paso_siguiente, **btn_style)
        self.btn_paso.pack(fill="x", pady=2)

        self.btn_auto = tk.Button(frame, text="⏵ Auto-Organizar", bg="#2E4A3E", fg=COLORES["exito"], command=self._toggle_auto, **btn_style)
        self.btn_auto.pack(fill="x", pady=2)

        self.btn_reset = tk.Button(frame, text="↺ Restablecer", bg="#3A2030", fg=COLORES["error"], command=self._reiniciar, **btn_style)
        self.btn_reset.pack(fill="x", pady=2)

    def _crear_panel_inferior(self):
        frame = tk.Frame(self.root, bg=COLORES["panel"], highlightbackground=COLORES["borde"], highlightthickness=1)
        frame.pack(fill="x", padx=10, pady=(0, 10))
        tk.Label(frame, text="▸ Log del Sistema", font=FUENTE_SUBTITULO, fg=COLORES["texto_secundario"], bg=COLORES["panel"]).pack(anchor="w", padx=10, pady=5)
        
        self.txt_log = tk.Text(frame, height=4, bg=COLORES["fondo"], fg=COLORES["texto"], font=FUENTE_CODIGO, relief="flat", state="disabled")
        self.txt_log.pack(fill="x", padx=10, pady=(0, 10))

    # ── LÓGICA DE CARGA ───────────────────────────────────────
    def _cargar_manual(self):
        try:
            raw = self.txt_input.get("1.0", "end-1c")
            nueva_lista = [int(x.strip()) for x in raw.replace(",", " ").split() if x.strip().isdigit()]
            if not nueva_lista: raise ValueError
            self.VECTOR_ORIGINAL = nueva_lista
            self._reiniciar()
        except:
            messagebox.showerror("Error", "Formato inválido. Use números separados por comas.")

    def _cargar_1000(self):
        self.VECTOR_ORIGINAL = [random.randint(5, 500) for _ in range(1000)]
        self._reiniciar()

    # ── LÓGICA DEL ALGORITMO ──────────────────────────────────
    def _paso_siguiente(self):
        if self.finalizado: return

        n = self.n
        i = self.i_externo
        j = self.j_interno

        if i > n - 2:
            self._marcar_finalizado()
            return

        a, b = self.vector[j], self.vector[j + 1]
        self.total_comparaciones += 1
        self.idx_comparando_1, self.idx_comparando_2 = j, j + 1

        hubo_cambio = False
        if a > b:
            self.vector[j], self.vector[j + 1] = self.vector[j + 1], self.vector[j]
            self.total_intercambios += 1
            hubo_cambio = True

        if j < n - i - 2:
            self.j_interno += 1
        else:
            self.indices_ordenados.add(n - 1 - i)
            self.j_interno = 0
            self.i_externo += 1
            if self.i_externo > n - 2:
                for k in range(n): self.indices_ordenados.add(k)

        # Solo actualizamos UI visual pesada si no son demasiados elementos o si es paso a paso
        if n < 100 or not self.reproduciendo or self.total_comparaciones % 5 == 0:
            self._dibujar_barras()
            self._actualizar_contadores()
            self.lbl_explicacion.config(text=f"Comparando indices {j} y {j+1}...")

        if len(self.indices_ordenados) == n:
            self._marcar_finalizado()

    def _marcar_finalizado(self):
        self.finalizado = True
        self.reproduciendo = False
        self.idx_comparando_1 = self.idx_comparando_2 = -1
        for k in range(self.n): self.indices_ordenados.add(k)
        self._dibujar_barras()
        self._actualizar_contadores()
        self.lbl_explicacion.config(text="✓ ORDENAMIENTO COMPLETO", fg=COLORES["exito"])
        self._agregar_log("Proceso finalizado con éxito.", "exito")

    def _toggle_auto(self):
        if self.finalizado: return
        self.reproduciendo = not self.reproduciendo
        if self.reproduciendo:
            self.btn_auto.config(text="⏸ Detener", bg="#4A3E10")
            self._ciclo_auto()
        else:
            self.btn_auto.config(text="⏵ Auto-Organizar", bg="#2E4A3E")

    def _ciclo_auto(self):
        if not self.reproduciendo or self.finalizado: return
        self._paso_siguiente()
        delay = max(1, 2001 - self.slider_velocidad.get())
        self._job_after = self.root.after(delay, self._ciclo_auto)

    def _reiniciar(self):
        if self._job_after: self.root.after_cancel(self._job_after)
        self.vector = list(self.VECTOR_ORIGINAL)
        self.n = len(self.vector)
        self.i_externo = self.j_interno = 0
        self.total_comparaciones = self.total_intercambios = 0
        self.finalizado = self.reproduciendo = False
        self.indices_ordenados = set()
        self.idx_comparando_1 = self.idx_comparando_2 = -1
        self.btn_auto.config(text="⏵ Auto-Organizar", bg="#2E4A3E")
        self.lbl_vector.config(text=f"Elementos: {self.n}")
        self._dibujar_barras()
        self._actualizar_contadores()

    def _dibujar_barras(self):
        self.canvas.delete("all")
        cw, ch = self.canvas.winfo_width(), self.canvas.winfo_height()
        if cw < 10: cw = 600 # Fallback inicial
        
        n = self.n
        margen_inf = 30
        max_val = max(self.vector) if self.vector else 1
        
        # Ajuste dinámico de anchos
        barra_w = cw / n
        
        for idx, valor in enumerate(self.vector):
            x1 = idx * barra_w
            x2 = x1 + barra_w
            # Dejar un pequeño borde si hay pocos elementos
            if n < 100: x2 -= 1
            
            altura = (valor / max_val) * (ch - margen_inf - 20)
            y1 = ch - margen_inf - altura
            y2 = ch - margen_inf

            if idx in self.indices_ordenados: color = COLORES["barra_ordenada"]
            elif idx == self.idx_comparando_1: color = COLORES["barra_comparar1"]
            elif idx == self.idx_comparando_2: color = COLORES["barra_comparar2"]
            else: color = COLORES["barra_normal"]

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

            # Solo dibujar texto si hay espacio suficiente (menos de 30 elementos)
            if n <= 30:
                cx = (x1 + x2) / 2
                self.canvas.create_text(cx, y1 - 10, text=f"${valor}", font=("Arial", 7), fill=COLORES["texto"])

    def _actualizar_contadores(self):
        self.lbl_pasada.config(text=str(self.i_externo + 1))
        self.lbl_total_comp.config(text=str(self.total_comparaciones))
        self.lbl_total_int.config(text=str(self.total_intercambios))

    def _agregar_log(self, texto, tag="normal"):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", f"[-] {texto}\n")
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = BubbleSortSimulator(root)
    root.mainloop()