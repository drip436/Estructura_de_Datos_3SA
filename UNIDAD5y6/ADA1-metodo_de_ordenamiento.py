"""
╔══════════════════════════════════════════════════════════════════╗
║        SISTEMA DE INVENTARIO - ORDENAMIENTO DE PRECIOS           ║
║        Caso Real: Catálogo de Productos (Precios en USD)         ║
║        Vector inicial: [45, 17, 23, 67, 21]                      ║
╚══════════════════════════════════════════════════════════════════╝

DESCRIPCIÓN:
    Visualización de cómo un sistema organiza los precios de productos
    de forma ascendente para mostrar un catálogo ordenado al cliente.
"""

import tkinter as tk
from tkinter import ttk, font
import time


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
FUENTE_BARRA    = ("Courier New", 11, "bold")   # Valores dentro de las barras


# ══════════════════════════════════════════════════════
#  CLASE PRINCIPAL: BubbleSortSimulator
# ══════════════════════════════════════════════════════
class BubbleSortSimulator:
    """
    Controlador principal del simulador.
    Simula la organización de precios de productos en un almacén.
    """

    # Vector original: Precios de 5 productos diferentes
    VECTOR_ORIGINAL = [45, 17, 23, 67, 21]

    def __init__(self, root: tk.Tk):
        self.root = root
        self._configurar_ventana()

        # ── Estado del algoritmo ──────────────────────────
        self.vector           = list(self.VECTOR_ORIGINAL)   # Copia mutable
        self.n                = len(self.vector)
        self.i_externo       = 0    # Iteración del bucle externo (pasadas)
        self.j_interno       = 0    # Posición en el bucle interno (comparación)
        self.total_comparaciones = 0
        self.total_intercambios  = 0
        self.finalizado      = False
        self.reproduciendo   = False    # True si está en modo automático
        self._job_after      = None     # Referencia al callback de tk.after

        # ── Índices especiales para colorear ─────────────
        self.idx_comparando_1 = -1
        self.idx_comparando_2 = -1
        self.indices_ordenados = set()   # Elementos ya en posición final

        # ── Historial de pasos (log) ──────────────────────
        self.log_pasos = []

        # ── Construir la interfaz ─────────────────────────
        self._construir_ui()
        self._dibujar_barras()
        self._actualizar_contadores()

    # ──────────────────────────────────────────────────────────
    #  CONFIGURACIÓN DE LA VENTANA RAÍZ
    # ──────────────────────────────────────────────────────────
    def _configurar_ventana(self):
        """Establece título, tamaño y color de la ventana principal."""
        self.root.title("SISTEMA DE GESTIÓN: Ordenamiento de Precios")
        self.root.configure(bg=COLORES["fondo"])
        self.root.resizable(False, False)

        # Centrar en la pantalla
        ancho, alto = 900, 680
        x = (self.root.winfo_screenwidth()  - ancho) // 2
        y = (self.root.winfo_screenheight() - alto)  // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ──────────────────────────────────────────────────────────
    #  CONSTRUCCIÓN DE LA INTERFAZ
    # ──────────────────────────────────────────────────────────
    def _construir_ui(self):
        """Ensambla todos los frames y widgets de la interfaz."""
        self._crear_cabecera()
        self._crear_cuerpo_principal()
        self._crear_panel_inferior()

    # ── Cabecera ──────────────────────────────────────────────
    def _crear_cabecera(self):
        """Barra superior con título y vector actual."""
        frame = tk.Frame(self.root, bg=COLORES["panel"],
                         highlightbackground=COLORES["acento"],
                         highlightthickness=1)
        frame.pack(fill="x", padx=10, pady=(10, 0))

        # Título Contextualizado
        tk.Label(frame,
                 text="◈  SISTEMA DE INVENTARIO: ORGANIZACIÓN DE CATÁLOGO  ◈",
                 font=FUENTE_TITULO,
                 fg=COLORES["acento_claro"],
                 bg=COLORES["panel"]).pack(side="left", padx=15, pady=8)

        # Vector actual (etiqueta dinámica)
        self.lbl_vector = tk.Label(frame,
                                   text="Precios: " + str(self.vector),
                                   font=FUENTE_CODIGO,
                                   fg=COLORES["texto_secundario"],
                                   bg=COLORES["panel"])
        self.lbl_vector.pack(side="right", padx=15)

    # ── Cuerpo principal ──────────────────────────────────────
    def _crear_cuerpo_principal(self):
        """Frame central que contiene el canvas y el panel lateral."""
        frame_cuerpo = tk.Frame(self.root, bg=COLORES["fondo"])
        frame_cuerpo.pack(fill="both", expand=True, padx=10, pady=8)

        self._crear_canvas_visualizacion(frame_cuerpo)
        self._crear_panel_lateral(frame_cuerpo)

    def _crear_canvas_visualizacion(self, padre):
        """
        Canvas donde se dibujan los precios como barras.
        """
        frame_canvas = tk.Frame(padre,
                                bg=COLORES["panel"],
                                highlightbackground=COLORES["borde"],
                                highlightthickness=1)
        frame_canvas.pack(side="left", fill="both", expand=True, padx=(0, 6))

        # Sub-cabecera del canvas
        tk.Label(frame_canvas,
                 text="▸ Comparativa de Costos por Producto (USD)",
                 font=FUENTE_SUBTITULO,
                 fg=COLORES["texto_secundario"],
                 bg=COLORES["panel"]).pack(anchor="w", padx=10, pady=(6, 0))

        self.canvas = tk.Canvas(frame_canvas,
                                width=556, height=300,
                                bg=COLORES["panel"],
                                highlightthickness=0)
        self.canvas.pack(padx=4, pady=(0, 6))

        # Leyenda de colores debajo del canvas
        self._crear_leyenda(frame_canvas)

    def _crear_leyenda(self, padre):
        """Pequeña leyenda que explica qué significa cada color."""
        frame = tk.Frame(padre, bg=COLORES["panel"])
        frame.pack(padx=10, pady=(0, 8))

        leyenda = [
            (COLORES["barra_normal"],    "Precio Base"),
            (COLORES["barra_comparar1"], "Producto A"),
            (COLORES["barra_comparar2"], "Producto B"),
            (COLORES["barra_ordenada"],  "Precio Correcto ✓"),
        ]
        for color, texto in leyenda:
            tk.Label(frame, text="■", fg=color, bg=COLORES["panel"],
                     font=("Courier New", 10)).pack(side="left", padx=(4, 0))
            tk.Label(frame, text=texto,
                     fg=COLORES["texto_secundario"],
                     bg=COLORES["panel"],
                     font=FUENTE_NORMAL).pack(side="left", padx=(0, 8))

    def _crear_panel_lateral(self, padre):
        """
        Panel derecho con contadores, explicación actual y botones.
        """
        frame = tk.Frame(padre, bg=COLORES["panel"],
                         highlightbackground=COLORES["borde"],
                         highlightthickness=1, width=290)
        frame.pack(side="right", fill="both")
        frame.pack_propagate(False)

        # ── Contadores ──────────────────────────────────
        tk.Label(frame, text="▸ Monitor de Procesamiento",
                 font=FUENTE_SUBTITULO,
                 fg=COLORES["texto_secundario"],
                 bg=COLORES["panel"]).pack(anchor="w", padx=10, pady=(8, 2))

        frame_stats = tk.Frame(frame, bg=COLORES["fondo"],
                               highlightbackground=COLORES["borde"],
                               highlightthickness=1)
        frame_stats.pack(fill="x", padx=10, pady=(0, 8))

        def stat_row(parent, etiqueta, color_val):
            row = tk.Frame(parent, bg=COLORES["fondo"])
            row.pack(fill="x", padx=8, pady=3)
            tk.Label(row, text=etiqueta, font=FUENTE_CODIGO,
                     fg=COLORES["texto_secundario"],
                     bg=COLORES["fondo"],
                     anchor="w").pack(side="left")
            lbl = tk.Label(row, text="0", font=FUENTE_CODIGO,
                            fg=color_val, bg=COLORES["fondo"])
            lbl.pack(side="right")
            return lbl

        self.lbl_pasada      = stat_row(frame_stats, "Ciclo Revisión:",
                                        COLORES["acento_claro"])
        self.lbl_comparacion = stat_row(frame_stats, "Par Analizado:",
                                        COLORES["advertencia"])
        self.lbl_total_comp  = stat_row(frame_stats, "Revisiones Totales:",
                                        COLORES["texto"])
        self.lbl_total_int   = stat_row(frame_stats, "Cambios Realizados:",
                                        COLORES["error"])

        # ── Explicación del paso actual ──────────────────
        tk.Label(frame, text="▸ Registro de Operaciones",
                 font=FUENTE_SUBTITULO,
                 fg=COLORES["texto_secundario"],
                 bg=COLORES["panel"]).pack(anchor="w", padx=10, pady=(0, 2))

        self.lbl_explicacion = tk.Label(frame,
                                        text="Inicie el proceso para organizar los precios.",
                                        font=FUENTE_NORMAL,
                                        fg=COLORES["texto"],
                                        bg=COLORES["fondo"],
                                        wraplength=260,
                                        justify="left",
                                        anchor="nw")
        self.lbl_explicacion.pack(fill="x", padx=10, pady=(0, 6),
                                  ipady=6, ipadx=6)

        # ── Velocidad de animación ───────────────────────
        tk.Label(frame, text="▸ Velocidad de Sistema",
                 font=FUENTE_SUBTITULO,
                 fg=COLORES["texto_secundario"],
                 bg=COLORES["panel"]).pack(anchor="w", padx=10, pady=(0, 2))

        frame_vel = tk.Frame(frame, bg=COLORES["panel"])
        frame_vel.pack(fill="x", padx=10, pady=(0, 8))

        tk.Label(frame_vel, text="Manual", font=FUENTE_NORMAL,
                 fg=COLORES["texto_secundario"],
                 bg=COLORES["panel"]).pack(side="left")

        self.slider_velocidad = tk.Scale(frame_vel,
                                         from_=100, to=2000,
                                         orient="horizontal",
                                         resolution=100,
                                         bg=COLORES["panel"],
                                         fg=COLORES["texto"],
                                         troughcolor=COLORES["borde"],
                                         highlightthickness=0,
                                         bd=0,
                                         sliderrelief="flat",
                                         showvalue=False)
        self.slider_velocidad.set(800)
        self.slider_velocidad.pack(side="left", fill="x", expand=True)

        tk.Label(frame_vel, text="Turbo", font=FUENTE_NORMAL,
                 fg=COLORES["texto_secundario"],
                 bg=COLORES["panel"]).pack(side="right")

        self._crear_botones(frame)

    def _crear_botones(self, padre):
        """Crea los tres botones principales de control."""
        frame = tk.Frame(padre, bg=COLORES["panel"])
        frame.pack(fill="x", padx=10, pady=4)

        estilo_btn = {
            "font":            FUENTE_SUBTITULO,
            "relief":          "flat",
            "cursor":          "hand2",
            "activeforeground":"#FFFFFF",
            "bd":               0,
            "pady":            7,
        }

        self.btn_paso = tk.Button(frame,
                                  text="▶  Siguiente Paso",
                                  bg=COLORES["acento"],
                                  fg="#FFFFFF",
                                  activebackground=COLORES["acento_claro"],
                                  command=self._paso_siguiente,
                                  **estilo_btn)
        self.btn_paso.pack(fill="x", pady=3)

        self.btn_auto = tk.Button(frame,
                                  text="⏵  Auto-Organizar",
                                  bg="#2E4A3E",
                                  fg=COLORES["exito"],
                                  activebackground="#3A5E4F",
                                  command=self._toggle_auto,
                                  **estilo_btn)
        self.btn_auto.pack(fill="x", pady=3)

        self.btn_reset = tk.Button(frame,
                                   text="↺  Restablecer Precios",
                                   bg="#3A2030",
                                   fg=COLORES["error"],
                                   activebackground="#4A2840",
                                   command=self._reiniciar,
                                   **estilo_btn)
        self.btn_reset.pack(fill="x", pady=3)

    # ── Panel inferior: historial de pasos ────────────────────
    def _crear_panel_inferior(self):
        """Log scrollable con todos los pasos realizados."""
        frame = tk.Frame(self.root, bg=COLORES["panel"],
                         highlightbackground=COLORES["borde"],
                         highlightthickness=1)
        frame.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(frame, text="▸ Log del Servidor de Inventario",
                 font=FUENTE_SUBTITULO,
                 fg=COLORES["texto_secundario"],
                 bg=COLORES["panel"]).pack(anchor="w", padx=10, pady=(6, 2))

        frame_txt = tk.Frame(frame, bg=COLORES["panel"])
        frame_txt.pack(fill="x", padx=10, pady=(0, 8))

        scroll = tk.Scrollbar(frame_txt, bg=COLORES["panel"])
        scroll.pack(side="right", fill="y")

        self.txt_log = tk.Text(frame_txt, height=5, bg=COLORES["fondo"],
                               fg=COLORES["texto"], font=FUENTE_CODIGO,
                               relief="flat", bd=0, state="disabled",
                               yscrollcommand=scroll.set, wrap="word")
        self.txt_log.pack(side="left", fill="x", expand=True)
        scroll.config(command=self.txt_log.yview)

        self.txt_log.tag_configure("intercambio", foreground=COLORES["error"])
        self.txt_log.tag_configure("normal", foreground=COLORES["texto_secundario"])
        self.txt_log.tag_configure("ordenado", foreground=COLORES["exito"])
        self.txt_log.tag_configure("inicio", foreground=COLORES["acento_claro"])

    # ──────────────────────────────────────────────────────────
    #  LÓGICA DEL ALGORITMO BUBBLE SORT (Contextualizado)
    # ──────────────────────────────────────────────────────────
    def _paso_siguiente(self):
        if self.finalizado:
            return

        n = self.n
        i = self.i_externo
        j = self.j_interno
        limite_j = n - i - 2

        if i > n - 2:
            self._marcar_finalizado()
            return

        a = self.vector[j]
        b = self.vector[j + 1]
        self.total_comparaciones += 1

        self.idx_comparando_1 = j
        self.idx_comparando_2 = j + 1

        if a > b:
            self.vector[j], self.vector[j + 1] = self.vector[j + 1], self.vector[j]
            self.total_intercambios += 1
            hubo_cambio = True
            explicacion = (f"Revisión {i+1}: El precio ${a} es mayor que ${b}. "
                           f"Se mueven de posición para el catálogo.")
            tag_log = "intercambio"
        else:
            hubo_cambio = False
            explicacion = (f"Revisión {i+1}: El precio ${a} es menor o igual a ${b}. "
                           f"Mantienen su orden actual.")
            tag_log = "normal"

        if j < limite_j:
            self.j_interno += 1
        else:
            self.indices_ordenados.add(n - 1 - i)
            self.j_interno  = 0
            self.i_externo += 1
            if self.i_externo > n - 2:
                for k in range(n): self.indices_ordenados.add(k)

        self._actualizar_explicacion(explicacion, hubo_cambio)
        self._agregar_log(explicacion, tag_log)
        self._dibujar_barras()
        self._actualizar_contadores()
        self.lbl_vector.config(text="Precios Actuales: " + str(self.vector))

        if len(self.indices_ordenados) == n:
            self._marcar_finalizado()

    def _marcar_finalizado(self):
        self.finalizado = True
        self.reproduciendo = False
        self.idx_comparando_1 = -1
        self.idx_comparando_2 = -1
        for k in range(self.n): self.indices_ordenados.add(k)
        self._dibujar_barras()
        self._actualizar_explicacion(
            f"✓ CATÁLOGO ORDENADO: Los precios están optimizados de menor a mayor.\n"
            f"  Revisiones: {self.total_comparaciones} | Intercambios: {self.total_intercambios}",
            es_exito=True)
        self._agregar_log(f"✓ ÉXITO: Inventario ordenado correctamente.", "ordenado")
        self.btn_auto.config(text="⏵ Auto-Organizar", bg="#2E4A3E", fg=COLORES["exito"])

    def _toggle_auto(self):
        if self.finalizado: return
        self.reproduciendo = not self.reproduciendo
        if self.reproduciendo:
            self.btn_auto.config(text="⏸ Detener", bg="#4A3E10", fg=COLORES["advertencia"])
            self._ciclo_auto()
        else:
            self.btn_auto.config(text="⏵ Auto-Organizar", bg="#2E4A3E", fg=COLORES["exito"])
            if self._job_after: self.root.after_cancel(self._job_after)

    def _ciclo_auto(self):
        if not self.reproduciendo or self.finalizado: return
        self._paso_siguiente()
        if not self.finalizado:
            delay_ms = 2100 - self.slider_velocidad.get()
            self._job_after = self.root.after(delay_ms, self._ciclo_auto)

    def _reiniciar(self):
        if self._job_after: self.root.after_cancel(self._job_after)
        self.vector = list(self.VECTOR_ORIGINAL)
        self.i_externo = 0; self.j_interno = 0
        self.total_comparaciones = 0; self.total_intercambios = 0
        self.finalizado = False; self.reproduciendo = False
        self.idx_comparando_1 = -1; self.idx_comparando_2 = -1
        self.indices_ordenados = set()
        self.btn_auto.config(text="⏵ Auto-Organizar", bg="#2E4A3E", fg=COLORES["exito"])
        self.txt_log.config(state="normal"); self.txt_log.delete("1.0", "end"); self.txt_log.config(state="disabled")
        self._dibujar_barras(); self._actualizar_contadores()
        self.lbl_vector.config(text="Precios: " + str(self.vector))
        self.lbl_explicacion.config(text="Precios restablecidos. Inicie el proceso de nuevo.", fg=COLORES["texto"])
        self._agregar_log(f"↺ Inventario restablecido: {self.VECTOR_ORIGINAL}", "inicio")

    # ──────────────────────────────────────────────────────────
    #  RENDERIZADO DEL CANVAS (Contexto de precios)
    # ──────────────────────────────────────────────────────────
    def _dibujar_barras(self):
        self.canvas.delete("all")
        canvas_w = 556; canvas_h = 300; margen_x = 40; margen_inf = 40; margen_sup = 30
        n = self.n; area_w = canvas_w - 2 * margen_x; hueco = 12
        barra_w = (area_w - hueco * (n - 1)) / n
        max_val = max(self.VECTOR_ORIGINAL) + 10
        area_h = canvas_h - margen_inf - margen_sup

        for idx, valor in enumerate(self.vector):
            x1 = margen_x + idx * (barra_w + hueco)
            x2 = x1 + barra_w
            altura = (valor / max_val) * area_h
            y1 = canvas_h - margen_inf - altura; y2 = canvas_h - margen_inf

            if idx in self.indices_ordenados: color = COLORES["barra_ordenada"]
            elif idx == self.idx_comparando_1: color = COLORES["barra_comparar1"]
            elif idx == self.idx_comparando_2: color = COLORES["barra_comparar2"]
            else: color = COLORES["barra_normal"]

            color_claro = self._aclarar_color(color, 0.18)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags="barra")
            self.canvas.create_rectangle(x1, y1, x1 + 3, y2, fill=color_claro, outline="", tags="brillo")

            cx = (x1 + x2) / 2
            # Se añade el símbolo de moneda para el caso real
            self.canvas.create_text(cx, y1 + 18, text=f"${valor}", font=FUENTE_BARRA,
                                    fill=COLORES["texto_numero"], tags="valor")
            self.canvas.create_text(cx, canvas_h - margen_inf + 16, text=f"Prod {idx+1}",
                                    font=FUENTE_NORMAL, fill=COLORES["texto_secundario"])

        self.canvas.create_line(margen_x, canvas_h - margen_inf, canvas_w - margen_x,
                                canvas_h - margen_inf, fill=COLORES["borde"], width=1)

    @staticmethod
    def _aclarar_color(hex_color: str, factor: float) -> str:
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = int(r + (255 - r) * factor); g = int(g + (255 - g) * factor); b = int(b + (255 - b) * factor)
        return f"#{r:02X}{g:02X}{b:02X}"

    def _actualizar_contadores(self):
        pasada_mostrar = min(self.i_externo + 1, self.n - 1)
        self.lbl_pasada.config(text=str(pasada_mostrar))
        self.lbl_comparacion.config(text=str(self.j_interno + 1) if not self.finalizado else "—")
        self.lbl_total_comp.config(text=str(self.total_comparaciones))
        self.lbl_total_int.config(text=str(self.total_intercambios))

    def _actualizar_explicacion(self, texto: str, hubo_cambio: bool = False, es_exito: bool = False):
        color = COLORES["exito"] if es_exito else (COLORES["error"] if hubo_cambio else COLORES["texto"])
        self.lbl_explicacion.config(text=texto, fg=color)

    def _agregar_log(self, texto: str, tag: str = "normal"):
        self.txt_log.config(state="normal")
        linea = f"[{len(self.log_pasos)+1:03d}]  {texto}\n"
        self.txt_log.insert("end", linea, tag); self.txt_log.see("end"); self.txt_log.config(state="disabled")
        self.log_pasos.append(texto)

def main():
    root = tk.Tk()
    app  = BubbleSortSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()