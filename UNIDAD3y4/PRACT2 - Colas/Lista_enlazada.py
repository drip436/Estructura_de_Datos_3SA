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

    def delete_at(self, pos):
        """Elimina el elemento en la posición indicada (empezando en 1)
        usando una cola auxiliar para conservar el orden."""
        if self.is_empty():
            print("La cola está vacía.")
            return None
        if pos < 1 or pos > self._size:
            print(f"Posición inválida. Elige entre 1 y {self._size}.")
            return None

        cola_auxiliar = Queue()
        elemento_eliminado = None

        # Sacar todos los elementos y guardar el que toca eliminar
        for i in range(1, self._size + 1):
            elemento = self.dequeue()
            if i == pos:
                elemento_eliminado = elemento  # Este no lo reinsertamos
            else:
                cola_auxiliar.enqueue(elemento)

        # Reinsertar los elementos restantes en la cola original
        while not cola_auxiliar.is_empty():
            self.enqueue(cola_auxiliar.dequeue())

        return elemento_eliminado

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

    # Menú principal
    while True:
        print("\n¿Qué deseas hacer?")
        print("  1. Agregar un pedido")
        print("  2. Eliminar un elemento por posición")
        print("  3. Ver la cola actual")
        print("  4. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            print("\n--- Nuevo pedido ---")
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
            print(f"\nPedido de '{customer}' agregado correctamente.")
            print("\n--- Cola actualizada ---")
            mi_cola.print_info()

        elif opcion == "2":
            if mi_cola.is_empty():
                print("La cola está vacía, no hay elementos que eliminar.")
            else:
                print("\n--- Cola actual ---")
                mi_cola.print_info()
                while True:
                    try:
                        pos = int(input(f"\n¿Qué posición quieres eliminar? (1 - {mi_cola.size()}): "))
                        if pos < 1 or pos > mi_cola.size():
                            print(f"Posición inválida. Elige entre 1 y {mi_cola.size()}.")
                        else:
                            break
                    except ValueError:
                        print("Entrada inválida. Ingresa un número entero.")

                eliminado = mi_cola.delete_at(pos)
                print(f"\nElemento eliminado:")
                print(f"  Cliente: {eliminado.getCustomer()}, Cantidad: {eliminado.getQty()}")
                print("\n--- Cola actualizada ---")
                mi_cola.print_info()

        elif opcion == "3":
            print("\n--- Cola actual ---")
            mi_cola.print_info()

        elif opcion == "4":
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida. Elige entre 1 y 4.")