import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os, threading, re, random
from Metodos_internos import SortAlgorithms
from Metodos_externos import ExternalSorting

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ADA: Visualizador y Generador de Archivos Ordenados")
        self.root.geometry("1100x950")
        self.data = []
        self.file_paths = []

        # --- 1. SECCIÓN DE CARGA Y GENERACIÓN ---
        frame_top = ttk.LabelFrame(root, text=" 1. Entrada de Datos ")
        frame_top.pack(fill="x", padx=20, pady=5)
        
        ttk.Label(frame_top, text="Cantidad Aleatoria:").grid(row=0, column=0, padx=5)
        self.count_entry = ttk.Entry(frame_top, width=10)
        self.count_entry.grid(row=0, column=1, padx=5)
        # Permite poner el número, dar Enter y generar la lista desordenada
        self.count_entry.bind("<Return>", lambda e: self.gen_rand())
        
        ttk.Button(frame_top, text="📁 Cargar Archivo", command=self.add_file).grid(row=0, column=2, padx=10)

        # --- 2. MONITOR DE VALORES LEÍDOS ---
        frame_monitor = ttk.LabelFrame(root, text=" 2. Monitor de Valores (Lo que el programa está leyendo) ")
        frame_monitor.pack(fill="x", padx=20, pady=5)
        
        self.txt_monitor = tk.Text(frame_monitor, height=8, font=("Consolas", 10), bg="#f8f9fa")
        self.txt_monitor.pack(fill="x", padx=5, pady=5)

        # --- 3. CONTROLES DE ALGORITMOS ---
        frame_ctrl = ttk.Frame(root)
        frame_ctrl.pack(fill="x", padx=20, pady=5)
        
        self.combo = ttk.Combobox(frame_ctrl, values=[
            "Burbuja", "Selección", "Inserción", "ShellSort", "Quicksort", 
            "Heapsort", "Radix", "Mezcla Directa", "Mezcla Natural", "Intercalación"
        ], state="readonly", width=20)
        self.combo.set("Burbuja")
        self.combo.pack(side="left", padx=10)
        
        self.btn_run = ttk.Button(frame_ctrl, text="▶ INICIAR ORDENAMIENTO", command=self.start)
        self.btn_run.pack(side="left")
        
        self.speed = ttk.Scale(frame_ctrl, from_=0.5, to=0.0, orient="horizontal")
        self.speed.set(0.05)
        self.speed.pack(side="right", padx=10)
        ttk.Label(frame_ctrl, text="Velocidad:").pack(side="right")

        # --- 4. ÁREA VISUAL (CANVAS) ---
        self.canvas = tk.Canvas(root, bg="#1e1e1e", height=400)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)

    def gen_rand(self):
        """Genera N números desordenados al presionar Enter."""
        try:
            n = int(self.count_entry.get())
            nums = [random.randint(1, 1000) for _ in range(n)]
            self.txt_monitor.delete("1.0", tk.END)
            self.txt_monitor.insert(tk.END, f"LISTA MANUAL GENERADA ({n} elementos):\n{nums}")
            self.refresh_data_logic()
        except: 
            messagebox.showerror("Error", "Ingresa un número válido")

    def add_file(self):
        """Agrega un archivo a la cola de procesamiento."""
        p = filedialog.askopenfilename(filetypes=[("Archivos de datos", "*.txt *.csv *.xlsx")])
        if p and p not in self.file_paths:
            self.file_paths.append(p)
            self.refresh_data_logic()

    def refresh_data_logic(self):
        """Lee todos los archivos y actualiza el monitor con lo que encontró."""
        all_nums = []
        monitor_text = ""
        
        # 1. Leer lo que haya en la lista manual (si existe)
        manual_raw = re.findall(r'-?\d+', self.txt_monitor.get("1.0", tk.END))
        if manual_raw:
            all_nums.extend([int(n) for n in manual_raw])
            monitor_text += f"VALORES MANUALES: {len(manual_raw)} detectados.\n"

        # 2. Leer cada archivo cargado
        for p in self.file_paths:
            try:
                content = ""
                if p.endswith('.csv'): content = pd.read_csv(p).to_string()
                elif p.endswith('.xlsx'): content = pd.read_excel(p).to_string()
                else: content = open(p, 'r').read()
                
                nums_in_file = [int(n) for n in re.findall(r'-?\d+', content)]
                all_nums.extend(nums_in_file)
                monitor_text += f"ARCHIVO '{os.path.basename(p)}': {len(nums_in_file)} números leídos.\n"
            except Exception as e:
                monitor_text += f"ERROR EN '{os.path.basename(p)}': {str(e)}\n"
        
        self.data = all_nums
        self.txt_monitor.delete("1.0", tk.END)
        self.txt_monitor.insert(tk.END, monitor_text + "\nDATOS TOTALES A ORDENAR:\n" + str(self.data))
        self.draw(self.data)

    def draw(self, arr, colors={}):
        """Dibuja las barras en el Canvas."""
        self.canvas.delete("all")
        if not arr: return
        w, h, n = self.canvas.winfo_width(), self.canvas.winfo_height(), len(arr)
        bw = w / n
        max_v = max(arr) if arr else 1
        for i, v in enumerate(arr):
            norm_h = (v / max_v) * (h * 0.9)
            self.canvas.create_rectangle(i*bw, h-norm_h, (i+1)*bw, h, 
                                        fill=colors.get(i, "#4fa8ff"), outline="")
        self.root.update()
        import time
        time.sleep(self.speed.get())

    def start(self):
        if not self.data:
            return messagebox.showwarning("Atención", "No hay datos para ordenar.")
        
        self.btn_run.config(state="disabled")
        method = self.combo.get()
        # Ejecutar en hilo para no congelar la pantalla
        threading.Thread(target=self.execute_sort, args=(method,), daemon=True).start()

    def execute_sort(self, method):
        """Ejecuta el algoritmo y al final guarda el archivo."""
        # --- LLAMADA A LIBRERÍAS ---
        if method == "Burbuja": SortAlgorithms.bubble_sort(self.data, self.draw)
        elif method == "Selección": SortAlgorithms.selection_sort(self.data, self.draw)
        elif method == "Inserción": SortAlgorithms.insertion_sort(self.data, self.draw)
        elif method == "ShellSort": SortAlgorithms.shell_sort(self.data, self.draw)
        elif method == "Quicksort": SortAlgorithms.quicksort(self.data, 0, len(self.data)-1, self.draw)
        elif method == "Heapsort": SortAlgorithms.heap_sort(self.data, self.draw)
        elif method == "Radix": SortAlgorithms.radix_sort(self.data, self.draw)
        
        elif method in ["Mezcla Directa", "Mezcla Natural", "Intercalación"]:
            # Guardamos a temporal para la lib externa
            with open("temp_externo.txt", "w") as f:
                for x in self.data: f.write(f"{x}\n")
            
            if method == "Mezcla Directa": ExternalSorting.mezcla_directa("temp_externo.txt")
            elif method == "Mezcla Natural": ExternalSorting.mezcla_equilibrada("temp_externo.txt")
            elif method == "Intercalación":
                # Simulación de dos archivos para intercalar
                mid = len(self.data)//2
                with open("archivoA.txt","w") as f: 
                    for x in sorted(self.data[:mid]): f.write(f"{x}\n")
                with open("archivoB.txt","w") as f: 
                    for x in sorted(self.data[mid:]): f.write(f"{x}\n")
                ExternalSorting.intercalacion("archivoA.txt", "archivoB.txt", "temp_externo.txt")

            with open("temp_externo.txt", "r") as f:
                self.data = [int(line.strip()) for line in f]
            self.draw(self.data, {i: "green" for i in range(len(self.data))})

        # --- FINALIZACIÓN Y GUARDADO ---
        self.btn_run.config(state="normal")
        self.save_sorted_data(method)

    def save_sorted_data(self, method_name):
        """Crea un archivo nuevo con los resultados."""
        answer = messagebox.askyesno("Guardar", f"Ordenamiento por {method_name} completo.\n¿Deseas guardar el resultado en un archivo?")
        if answer:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivo de texto", "*.txt"), ("CSV", "*.csv")],
                title="Guardar números ordenados"
            )
            if file_path:
                try:
                    with open(file_path, "w") as f:
                        for n in self.data:
                            f.write(f"{n}\n")
                    messagebox.showinfo("Éxito", f"Archivo guardado correctamente en:\n{file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()