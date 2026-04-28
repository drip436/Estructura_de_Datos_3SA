import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

# ─────────────────────────────────────────────
#  ALGORITMOS DE ORDENAMIENTO
# ─────────────────────────────────────────────

def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left   = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right  = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def heap_sort(arr):
    n = len(arr)

    def heapify(arr, n, i):
        largest = i
        l, r = 2 * i + 1, 2 * i + 2
        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr


def radix_sort(arr):
    if not arr:
        return arr
    negatives = [-x for x in arr if x < 0]
    positives = [x for x in arr if x >= 0]

    def counting_sort(a, exp):
        n = len(a)
        output = [0] * n
        count  = [0] * 10
        for i in range(n):
            index = (a[i] // exp) % 10
            count[index] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for i in range(n - 1, -1, -1):
            index = (a[i] // exp) % 10
            output[count[index] - 1] = a[i]
            count[index] -= 1
        return output

    def radix(a):
        if not a:
            return a
        max_val = max(a)
        exp = 1
        while max_val // exp > 0:
            a = counting_sort(a, exp)
            exp *= 10
        return a

    sorted_neg = [-x for x in radix(negatives)][::-1]
    sorted_pos = radix(positives)
    return sorted_neg + sorted_pos


# ─────────────────────────────────────────────
#  INTERFAZ GRÁFICA
# ─────────────────────────────────────────────

METHODS = {
    "ShellSort":  shell_sort,
    "Quicksort":  quick_sort,
    "Heapsort":   heap_sort,
    "Radix Sort": radix_sort,
}

DESCRIPTIONS = {
    "ShellSort": (
        "ShellSort mejora el Insertion Sort al comparar e intercambiar elementos "
        "separados por un 'gap' que se va reduciendo hasta llegar a 1.\n"
        "Complejidad: O(n log² n) promedio."
    ),
    "Quicksort": (
        "Quicksort elige un pivote y divide el arreglo en dos subarreglos: "
        "elementos menores y mayores al pivote, ordenándolos recursivamente.\n"
        "Complejidad: O(n log n) promedio, O(n²) peor caso."
    ),
    "Heapsort": (
        "Heapsort construye un Max-Heap y extrae el máximo repetidamente para "
        "ordenar el arreglo in-place.\n"
        "Complejidad: O(n log n) siempre."
    ),
    "Radix Sort": (
        "Radix Sort ordena los números dígito por dígito (de menos al más "
        "significativo) usando Counting Sort como subrutina.\n"
        "Complejidad: O(nk) donde k es el número de dígitos."
    ),
}

COLORS = {
    "bg":       "#1e1e2e",
    "panel":    "#2a2a3e",
    "accent":   "#7c6af7",
    "accent2":  "#5ad4e6",
    "text":     "#cdd6f4",
    "subtext":  "#a6adc8",
    "green":    "#a6e3a1",
    "red":      "#f38ba8",
    "yellow":   "#f9e2af",
    "border":   "#45475a",
}


class SortApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ADA2 – Métodos de Ordenamiento")
        self.configure(bg=COLORS["bg"])
        self.resizable(True, True)
        self.geometry("860x640")
        self._build_ui()

    # ── construcción de la UI ──────────────────

    def _build_ui(self):
        # Título
        tk.Label(
            self, text="Métodos de Ordenamiento", font=("Segoe UI", 18, "bold"),
            bg=COLORS["bg"], fg=COLORS["accent"]
        ).pack(pady=(18, 4))

        tk.Label(
            self, text="ADA2 · Unidad 5", font=("Segoe UI", 10),
            bg=COLORS["bg"], fg=COLORS["subtext"]
        ).pack(pady=(0, 12))

        # Frame principal
        main = tk.Frame(self, bg=COLORS["bg"])
        main.pack(fill="both", expand=True, padx=20, pady=4)

        # ── Panel izquierdo (entrada) ──────────
        left = tk.Frame(main, bg=COLORS["panel"], bd=0, relief="flat")
        left.pack(side="left", fill="y", padx=(0, 10), pady=4, ipadx=12, ipady=12)

        self._section(left, "Cantidad de números")
        self.qty_var = tk.StringVar(value="10")
        self._entry(left, self.qty_var)

        btn_gen = tk.Button(
            left, text="🎲 Generar aleatorio", font=("Segoe UI", 9),
            bg=COLORS["accent"], fg="white", relief="flat", cursor="hand2",
            command=self._generate_random
        )
        btn_gen.pack(fill="x", pady=(4, 10))

        self._section(left, "Números (separados por coma o espacio)")
        self.numbers_text = tk.Text(
            left, height=6, width=28, font=("Consolas", 10),
            bg=COLORS["bg"], fg=COLORS["text"], insertbackground=COLORS["text"],
            relief="flat", bd=4
        )
        self.numbers_text.pack(fill="x", pady=(0, 10))

        self._section(left, "Método de ordenamiento")
        self.method_var = tk.StringVar(value="ShellSort")
        for name in METHODS:
            rb = tk.Radiobutton(
                left, text=name, variable=self.method_var, value=name,
                bg=COLORS["panel"], fg=COLORS["text"], selectcolor=COLORS["bg"],
                activebackground=COLORS["panel"], font=("Segoe UI", 10),
                command=self._update_description
            )
            rb.pack(anchor="w")

        # Separator line
        tk.Frame(left, bg=COLORS["border"], height=2).pack(fill="x", pady=(14, 10))

        tk.Button(
            left, text="▶  ORDENAR", font=("Segoe UI", 13, "bold"),
            bg=COLORS["accent2"], fg=COLORS["bg"], relief="flat", cursor="hand2",
            pady=10, command=self._sort
        ).pack(fill="x", pady=(0, 6))

        tk.Button(
            left, text="✕  Limpiar", font=("Segoe UI", 9),
            bg=COLORS["border"], fg=COLORS["text"], relief="flat", cursor="hand2",
            command=self._clear
        ).pack(fill="x")

        # ── Panel derecho (resultado + descripción) ──
        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side="left", fill="both", expand=True, pady=4)

        # Descripción del método
        desc_frame = tk.Frame(right, bg=COLORS["panel"], bd=0)
        desc_frame.pack(fill="x", pady=(0, 8), ipadx=10, ipady=8)
        tk.Label(
            desc_frame, text="¿En qué consiste?", font=("Segoe UI", 10, "bold"),
            bg=COLORS["panel"], fg=COLORS["accent"]
        ).pack(anchor="w", padx=8, pady=(4, 0))
        self.desc_label = tk.Label(
            desc_frame, text=DESCRIPTIONS["ShellSort"],
            font=("Segoe UI", 9), bg=COLORS["panel"], fg=COLORS["subtext"],
            justify="left", wraplength=480
        )
        self.desc_label.pack(anchor="w", padx=8, pady=(2, 4))

        # Resultado
        res_frame = tk.Frame(right, bg=COLORS["panel"], bd=0)
        res_frame.pack(fill="both", expand=True, ipadx=10, ipady=8)

        tk.Label(
            res_frame, text="Resultado", font=("Segoe UI", 10, "bold"),
            bg=COLORS["panel"], fg=COLORS["accent"]
        ).pack(anchor="w", padx=8, pady=(4, 0))

        self.result_text = tk.Text(
            res_frame, font=("Consolas", 11),
            bg=COLORS["bg"], fg=COLORS["green"],
            insertbackground=COLORS["text"], relief="flat",
            state="disabled", wrap="word"
        )
        self.result_text.pack(fill="both", expand=True, padx=8, pady=4)

        self.status_var = tk.StringVar(value="Listo.")
        tk.Label(
            self, textvariable=self.status_var, font=("Segoe UI", 9),
            bg=COLORS["bg"], fg=COLORS["subtext"]
        ).pack(pady=(4, 10))

    def _section(self, parent, text):
        tk.Label(
            parent, text=text, font=("Segoe UI", 9, "bold"),
            bg=COLORS["panel"], fg=COLORS["subtext"]
        ).pack(anchor="w", pady=(6, 2))

    def _entry(self, parent, var):
        e = tk.Entry(
            parent, textvariable=var, font=("Consolas", 11),
            bg=COLORS["bg"], fg=COLORS["text"],
            insertbackground=COLORS["text"], relief="flat", bd=4, width=10
        )
        e.pack(anchor="w", pady=(0, 4))

    # ── lógica ────────────────────────────────

    def _update_description(self):
        method = self.method_var.get()
        self.desc_label.config(text=DESCRIPTIONS[method])

    def _generate_random(self):
        try:
            qty = int(self.qty_var.get())
            if qty < 1 or qty > 200:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingresa una cantidad válida (1–200).")
            return
        nums = [random.randint(-999, 999) for _ in range(qty)]
        self.numbers_text.delete("1.0", "end")
        self.numbers_text.insert("end", ", ".join(map(str, nums)))

    def _parse_numbers(self):
        raw = self.numbers_text.get("1.0", "end").strip()
        raw = raw.replace(",", " ")
        tokens = raw.split()
        nums = []
        for t in tokens:
            try:
                nums.append(int(t))
            except ValueError:
                raise ValueError(f"'{t}' no es un número entero válido.")
        return nums

    def _sort(self):
        try:
            nums = self._parse_numbers()
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
            return
        if not nums:
            messagebox.showwarning("Sin datos", "Ingresa al menos un número.")
            return

        method = self.method_var.get()
        func   = METHODS[method]

        arr = nums[:]
        start = time.perf_counter()
        sorted_arr = func(arr)
        elapsed = (time.perf_counter() - start) * 1000  # ms

        result = (
            f"Método:    {method}\n"
            f"Elementos: {len(nums)}\n"
            f"Tiempo:    {elapsed:.4f} ms\n"
            f"\nOriginal:\n{nums}\n"
            f"\nOrdenado:\n{sorted_arr}"
        )

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", result)
        self.result_text.config(state="disabled")
        self.status_var.set(f"✔  Ordenado con {method} en {elapsed:.4f} ms")

    def _clear(self):
        self.numbers_text.delete("1.0", "end")
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.config(state="disabled")
        self.status_var.set("Listo.")


if __name__ == "__main__":
    app = SortApp()
    app.mainloop()