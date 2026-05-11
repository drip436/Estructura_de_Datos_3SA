class SortAlgorithms:
    """Librería de algoritmos de ordenamiento interno."""

    @staticmethod
    def bubble_sort(arr):
        """1. Burbuja: Compara elementos adyacentes y los intercambia."""
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    @staticmethod
    def insertion_sort(arr):
        """2. Inserción: Construye el arreglo ordenado un elemento a la vez."""
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    @staticmethod
    def selection_sort(arr):
        """3. Selección: Busca el mínimo y lo coloca al principio."""
        for i in range(len(arr)):
            min_idx = i
            for j in range(i + 1, len(arr)):
                if arr[min_idx] > arr[j]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    @staticmethod
    def shell_sort(arr):
        """4. ShellSort: Variación de inserción que usa brechas (gaps)."""
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

    @staticmethod
    def quicksort(arr):
        """5. Quicksort: Divide y vencerás usando un pivote."""
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return SortAlgorithms.quicksort(left) + middle + SortAlgorithms.quicksort(right)

    @staticmethod
    def heap_sort(arr):
        """6. Heapsort: Basado en una estructura de datos de montículo (Heap)."""
        def heapify(n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2
            if l < n and arr[i] < arr[l]:
                largest = l
            if r < n and arr[largest] < arr[r]:
                largest = r
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(n, largest)

        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i)
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            heapify(i, 0)
        return arr

    @staticmethod
    def radix_sort(arr):
        """7. Radix: Ordena por dígitos, de menos a más significativos."""
        if not arr:
            return arr
        max_val = max(arr)
        exp = 1
        while max_val // exp > 0:
            # Uso de Counting Sort como subrutina
            output = [0] * len(arr)
            count = [0] * 10
            for i in range(len(arr)):
                index = (arr[i] // exp) % 10
                count[index] += 1
            for i in range(1, 10):
                count[i] += count[i - 1]
            i = len(arr) - 1
            while i >= 0:
                index = (arr[i] // exp) % 10
                output[count[index] - 1] = arr[i]
                count[index] -= 1
                i -= 1
            for i in range(len(arr)):
                arr[i] = output[i]
            exp *= 10
        return arr

# --- Ejemplo de uso ---
if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {data}")
    
    # Ejemplo con Quicksort
    sorted_data = SortAlgorithms.quicksort(data.copy())
    print(f"Ordenado (Quicksort): {sorted_data}")