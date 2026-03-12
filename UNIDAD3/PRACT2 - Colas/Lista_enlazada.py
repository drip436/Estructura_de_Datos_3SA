class Node:
    def __init__(self, info, next_node=None):
        self.info = info
        self.next = next_node


class Order:
    def __init__(self, customer, qty):
        self.customer = customer
        self.qty = qty

    def print(self):
        print(f"    Customer: {self.customer}")
        print(f"    Quantity: {self.qty}")
        print(f"    ------------")

    def getQty(self):
        return self.qty

    def getCustomer(self):
        return self.customer


class Queue:
    def __init__(self):
        self.top = None    # Cabeza de la cola
        self.tail = None   # Último nodo
        self._size = 0

    def size(self):
        return self._size

    def is_empty(self):
        return self.top is None

    def front(self):
        """Devuelve el primer elemento SIN eliminarlo. None si vacía."""
        if self.is_empty():
            return None
        return self.top.info

    def enqueue(self, info):
        """Añade un nuevo elemento al final de la cola."""
        new_node = Node(info)
        if self.is_empty():
            self.top = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self._size += 1

    def dequeue(self):
        """Elimina y devuelve el primer elemento. None si vacía."""
        if self.is_empty():
            return None
        extracted = self.top.info
        self.top = self.top.next
        if self.top is None:
            self.tail = None
        self._size -= 1
        return extracted

    def print_info(self):
        """Recorre e imprime la cola con formato del enunciado."""
        print("********* QUEUE DUMP *********")
        print(f"  Size: {self._size}")
        current = self.top
        count = 1
        while current is not None:
            print(f"** Element {count}")
            current.info.print()   # Llama al método print() de Order
            current = current.next
            count += 1
        print("******************************")


# --- Bloque de prueba ---
if __name__ == "__main__":
    mi_cola = Queue()

    mi_cola.enqueue(Order("Cust1", 20))
    mi_cola.enqueue(Order("Cust2", 30))
    mi_cola.enqueue(Order("Cust3", 40))
    mi_cola.enqueue(Order("Cust3", 50))

    mi_cola.print_info()

    print(f"\nFront (sin eliminar): {mi_cola.front().getCustomer()}")
    print(f"Tamaño: {mi_cola.size()}")

    print("\n--- Dequeue ---")
    atendido = mi_cola.dequeue()
    print(f"Atendido: {atendido.getCustomer()}, qty: {atendido.getQty()}")

    print()
    mi_cola.print_info()