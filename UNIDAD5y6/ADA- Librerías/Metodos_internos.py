class SortAlgorithms:
    """Librería de algoritmos de ordenamiento interno."""

    @staticmethod
    def bubble_sort(arr, callback= None):
        """1. Burbuja: Compara elementos adyacentes y los intercambia."""
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    if callback:
                        callback(arr, {j: "red", j+1: "red"})
        return arr

    @staticmethod
    def insertion_sort(arr, callback=None):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                if callback: callback(arr, {j + 1: "red", i: "yellow"})
            arr[j + 1] = key
            if callback: callback(arr, {j + 1: "green"})
        return arr

    @staticmethod
    def selection_sort(arr, callback = None):
        for i in range(len(arr)):
            min_idx = i
            for j in range(i+1, len(arr)):
                if callback: callback(arr, {j: "yellow", min_idx: "red"})
                if arr[j] < arr[min_idx]: min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            if callback: callback(arr, {i: "green"})
        return arr

    @staticmethod
    def shell_sort(arr, callback = None):
        n = len(arr)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    j -= gap
                    if callback: callback(arr, {j: "red", i: "yellow"})
                arr[j] = temp
            gap //= 2
        return arr

    @staticmethod
    def quicksort(arr, low, high, callback=None):
        if low < high:
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    if callback: callback(arr, {i: "red", j: "yellow"})
            arr[i+1], arr[high] = arr[high], arr[i+1]
            pi = i + 1
            SortAlgorithms.quicksort(arr, low, pi - 1, callback)
            SortAlgorithms.quicksort(arr, pi + 1, high, callback)
            
    @staticmethod
    def heap_sort(arr, callback=None):
        def heapify(n, i):
            largest = i
            l, r = 2 * i + 1, 2 * i + 2
            if l < n and arr[i] < arr[l]: largest = l
            if r < n and arr[largest] < arr[r]: largest = r
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                if callback: callback(arr, {i: "red", largest: "yellow"})
                heapify(n, largest)
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1): heapify(n, i)
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            if callback: callback(arr, {i: "green", 0: "red"})
            heapify(i, 0)
        return arr

    @staticmethod
    def radix_sort(arr, callback=None):
        if not arr: return arr
        max_val = max(arr)
        exp = 1
        while max_val // exp > 0:
            output = [0] * len(arr)
            count = [0] * 10
            for i in range(len(arr)):
                index = (arr[i] // exp) % 10
                count[index] += 1
            for i in range(1, 10): count[i] += count[i - 1]
            i = len(arr) - 1
            while i >= 0:
                index = (arr[i] // exp) % 10
                output[count[index] - 1] = arr[i]
                count[index] -= 1
                i -= 1
            for i in range(len(arr)):
                arr[i] = output[i]
                if callback: callback(arr, {i: "red"})
            exp *= 10
        return arr

# --- Ejemplo de uso ---
if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {data}")
    
    # Ejemplo con Quicksort
    sorted_data = data.copy()
    SortAlgorithms.quicksort(sorted_data, 0, len(sorted_data) - 1)
    print(f"Ordenado (Quicksort): {sorted_data}")