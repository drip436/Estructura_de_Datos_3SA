import tkinter as tk
from tkinter import ttk, messagebox

class NodoNario:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []  # Lista dinámica de hijos
        self.x = 0
        self.y = 0
        # --- NUEVO PARA SOLUCIONAR LA RAMA CAÍDA ---
        # Guardamos el lado visual preferido si es hijo único: 'izq', 'der' o None
        self.lado_visual_hijo_unico = None 

    def es_hoja(self):
        return len(self.hijos) == 0

class ArbolProApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Constructor de Árboles N-arios - Control Posicional Mejorado")
        self.geometry("1100x750")
        self.config(bg="#f1f3f5")

        self.raiz = None
        self.nodo_seleccionado = None
        
        self.setup_ui()

    def setup_ui(self):
        # --- Panel Superior de Controles ---
        frame_controles = tk.Frame(self, bg="#212529", height=90)
        frame_controles.pack(side="top", fill="x")

        tk.Label(frame_controles, text="Valor:", bg="#212529", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=(20, 5))
        self.entry_valor = ttk.Entry(frame_controles, width=12)
        self.entry_valor.pack(side="left", padx=5)

        # Botones de acción
        ttk.Button(frame_controles, text="Crear Raíz", command=self.crear_raiz).pack(side="left", padx=10)
        
        # Botones de posición
        # He actualizado los textos para mayor claridad
        btn_izq = ttk.Button(frame_controles, text="Añadir Lado Izquierdo", command=lambda: self.añadir_hijo("inicio"))
        btn_izq.pack(side="left", padx=5)
        
        btn_der = ttk.Button(frame_controles, text="Añadir Lado Derecho", command=lambda: self.añadir_hijo("final"))
        btn_der.pack(side="left", padx=5)

        ttk.Button(frame_controles, text="Limpiar Árbol", command=self.limpiar).pack(side="right", padx=20)

        # --- Barra de Estado ---
        self.label_status = tk.Label(self, text="Instrucciones: Crea la raíz y selecciona nodos para añadir hijos.", 
                                    bg="#e9ecef", fg="#495057", font=("Arial", 10, "italic"))
        self.label_status.pack(fill="x")

        # --- Lienzo (Canvas) ---
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=15)
        self.canvas.bind("<Button-1>", self.detectar_clic)

    def crear_raiz(self):
        val = self.entry_valor.get()
        if not val:
            messagebox.showwarning("Campo Vacío", "Escribe un valor para la raíz.")
            return
        if self.raiz:
            messagebox.showwarning("Error", "Ya hay una raíz. Usa 'Limpiar' para empezar de cero.")
            return
        
        self.raiz = NodoNario(val)
        self.entry_valor.delete(0, tk.END)
        self.dibujar()

    def añadir_hijo(self, posicion):
        if not self.nodo_seleccionado:
            messagebox.showwarning("Selección", "Haz clic en un nodo para seleccionarlo (se pondrá amarillo).")
            return
        
        val = self.entry_valor.get()
        if not val:
            messagebox.showwarning("Campo Vacío", "Escribe el valor del nuevo hijo.")
            return

        nuevo_nodo = NodoNario(val)
        
        # --- NUEVA LÓGICA PARA POSICIONAR AL HIJO ÚNICO ---
        # Si el padre NO tiene hijos, este nuevo hijo será el hijo único y 
        # establecerá el lado visual preferido.
        if len(self.nodo_seleccionado.hijos) == 0:
            if posicion == "inicio":
                self.nodo_seleccionado.lado_visual_hijo_unico = "izq"
            else:
                self.nodo_seleccionado.lado_visual_hijo_unico = "der"
        # Si ya tiene hijos (N-arios), no necesitamos un lado preferido 
        # ya que la lógica de reparto se encargará.
        # -----------------------------------------------------------------

        if posicion == "inicio":
            # Insertar al principio (extremo izquierdo de la lista)
            self.nodo_seleccionado.hijos.insert(0, nuevo_nodo)
        else:
            # Insertar al final (extremo derecho de la lista)
            self.nodo_seleccionado.hijos.append(nuevo_nodo)
        
        self.entry_valor.delete(0, tk.END)
        self.dibujar()

    def detectar_clic(self, event):
        # Buscamos el nodo cerca del clic (radio de 25px)
        self.nodo_seleccionado = self.buscar_nodo_recursivo(self.raiz, event.x, event.y)
        if self.nodo_seleccionado:
            self.label_status.config(text=f"Seleccionado: {self.nodo_seleccionado.valor} | Puedes añadirle n hijos.")
        self.dibujar()

    def buscar_nodo_recursivo(self, nodo, x, y):
        if not nodo: return None
        dist = ((nodo.x - x)**2 + (nodo.y - y)**2)**0.5
        if dist < 25: return nodo
        for h in nodo.hijos:
            res = self.buscar_nodo_recursivo(h, x, y)
            if res: return res
        return None

    def dibujar(self):
        self.canvas.delete("all")
        if self.raiz:
            # Empezamos el dibujo con un ancho inicial grande para que no colisionen
            self.dibujar_nodo(self.raiz, self.canvas.winfo_width()/2, 50, self.canvas.winfo_width()/3)

    def dibujar_nodo(self, nodo, x, y, ancho_hijos):
        nodo.x = x
        nodo.y = y
        radio = 22
        vertical_gap = 90

        n = len(nodo.hijos)
        puntos_x = [] # Inicializar lista de puntos X para hijos

        # --- LÓGICA DE DIBUJO MEJORADA ---
        if n == 0:
            puntos_x = []
        elif n == 1:
            # ANTES: puntos_x = [x] -> Esto causaba la rama caída recta.
            # AHORA: Chequeamos el lado visual guardado en el PADRE para el hijo ÚNICO.
            # Calculamos un offset diagonal estándar (usando la mitad del ancho disponible).
            offset_diagonal = ancho_hijos / 2
            
            if nodo.lado_visual_hijo_unico == "izq":
                # Apuntar diagonalmente a la izquierda
                puntos_x = [x - offset_diagonal]
            elif nodo.lado_visual_hijo_unico == "der":
                # Apuntar diagonalmente a la derecha
                puntos_x = [x + offset_diagonal]
            else:
                # Fallback por si acaso (volver al centro)
                puntos_x = [x]
        else:
            # Lógica N-aria existente para repartir 2 o más hijos
            inicio_x = x - ancho_hijos / 2
            paso = ancho_hijos / (n - 1)
            puntos_x = [inicio_x + i * paso for i in range(n)]
        # ----------------------------------

        # Lógica de dibujo existente (crear línea y nodo) ...
        if n > 0:
            for i, hijo in enumerate(nodo.hijos):
                nx, ny = puntos_x[i], y + vertical_gap
                # Dibujar línea
                self.canvas.create_line(x, y, nx, ny, fill="#dee2e6", width=2)
                # Dibujar hijo (reducimos el ancho para el siguiente nivel)
                self.dibujar_nodo(hijo, nx, ny, ancho_hijos * 0.55)

        # Colores según estado
        if nodo == self.nodo_seleccionado:
            color_bg, color_text = "#ffc107", "black" # Amarillo: Seleccionado
        elif nodo.es_hoja():
            color_bg, color_text = "#28a745", "white" # Verde: Hoja
        else:
            color_bg, color_text = "#007bff", "white" # Azul: Padre

        # Dibujar el círculo
        self.canvas.create_oval(x-radio, y-radio, x+radio, y+radio, fill=color_bg, outline="#adb5bd", width=2)
        self.canvas.create_text(x, y, text=nodo.valor, fill=color_text, font=("Arial", 10, "bold"))

    def limpiar(self):
        if messagebox.askyesno("Confirmar", "¿Borrar todo el árbol?"):
            self.raiz = None
            self.nodo_seleccionado = None
            self.dibujar()

if __name__ == "__main__":
    app = ArbolProApp()
    app.update()
    app.dibujar()
    app.mainloop()