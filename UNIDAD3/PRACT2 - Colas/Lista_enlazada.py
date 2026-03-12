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
        self.top = None
        self.tail = None
        self._size = 0

    def size(self):
        return self._size

    def is_empty(self):
        return self.top is None

    def front(self):
        if self.is_empty():
            return None
        return self.top.info

    def enqueue(self, info):
        new_node = Node(info)
        if self.is_empty():
            self.top = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        extracted = self.top.info
        self.top = self.top.next
        if self.top is None:
            self.tail = None
        self._size -= 1
        return extracted

    def print_info(self):
        print("********* QUEUE DUMP *********")
        print(f"  Size: {self._size}")
        current = self.top
        count = 1
        while current is not None:
            print(f"** Element {count}")
            current.info.print()
            current = current.next
            count += 1
        print("******************************")


# --- Bloque de prueba ---
if __name__ == "__main__":
    mi_cola = Queue()

    while True:
        try:
            n = int(input("¿Cuántos pedidos quieres agregar a la cola? "))
            if n <= 0:
                print("Por favor ingresa un número mayor a 0.")
            else:
                break
        except ValueError:
            print("Entrada inválida. Ingresa un número entero.")

    for i in range(1, n + 1):
        print(f"\n--- Pedido {i} ---")
        customer = input("  Nombre del cliente: ")
        while True:
            try:
                qty = int(input("  Cantidad: "))
                if qty <= 0:
                    print("  La cantidad debe ser mayor a 0.")
                else:
                    break
            except ValueError:
                print("  Entrada inválida. Ingresa un número entero.")
        mi_cola.enqueue(Order(customer, qty))

    print("\n--- Cola inicial ---")
    mi_cola.print_info()

    print(f"\nPrimer elemento (front): {mi_cola.front().getCustomer()}")

    print("\n--- Desencolando un elemento ---")
    atendido = mi_cola.dequeue()
    print(f"Atendido: {atendido.getCustomer()}, Cantidad: {atendido.getQty()}")

    print("\n--- Cola después del dequeue ---")
    mi_cola.print_info()
