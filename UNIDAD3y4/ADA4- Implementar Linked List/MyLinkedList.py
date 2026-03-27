"""
MyLinkedList - Implementación propia de una Linked List en Python
"""


class Node:
    """Nodo individual de la lista enlazada."""

    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class MyLinkedList:
    """
    Implementación de una Singly Linked List (Lista Enlazada Simple).

    Métodos disponibles:
        - append(data)         → Agrega al final
        - prepend(data)        → Agrega al inicio
        - insert(index, data)  → Inserta en posición específica
        - delete(data)         → Elimina primer nodo con ese valor
        - delete_at(index)     → Elimina nodo en posición específica
        - get(index)           → Obtiene el valor en una posición
        - search(data)         → Busca un valor, devuelve índice o -1
        - update(index, data)  → Actualiza el valor en una posición
        - reverse()            → Invierte la lista in-place
        - to_list()            → Convierte a lista de Python
        - clear()              → Vacía la lista
        - is_empty()           → Verifica si está vacía
        - size()               → Número de elementos
        - __len__              → Soporte para len()
        - __iter__             → Soporte para iteración (for x in lista)
        - __contains__         → Soporte para operador 'in'
        - __repr__ / __str__   → Representación legible
    """

    def __init__(self, initial_data=None):
        """
        Inicializa la lista.
        Se puede pasar un iterable para poblarla desde el inicio.
        """
        self.head = None
        self._size = 0

        if initial_data is not None:
            for item in initial_data:
                self.append(item)

    # ──────────────────────────────────────────────
    # INSERCIÓN
    # ──────────────────────────────────────────────

    def append(self, data):
        """Agrega un nuevo nodo al FINAL de la lista. O(n)"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def prepend(self, data):
        """Agrega un nuevo nodo al INICIO de la lista. O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def insert(self, index, data):
        """
        Inserta un nodo en la posición indicada. O(n)
        Lanza IndexError si el índice está fuera de rango.
        """
        if index < 0 or index > self._size:
            raise IndexError(f"Índice {index} fuera de rango (tamaño: {self._size})")

        if index == 0:
            self.prepend(data)
            return

        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self._size += 1

    # ──────────────────────────────────────────────
    # ELIMINACIÓN
    # ──────────────────────────────────────────────

    def delete(self, data):
        """
        Elimina el PRIMER nodo que contenga el valor indicado. O(n)
        Lanza ValueError si el valor no se encuentra.
        """
        if self.head is None:
            raise ValueError("La lista está vacía.")

        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return

        current = self.head
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return
            current = current.next

        raise ValueError(f"Valor '{data}' no encontrado en la lista.")

    def delete_at(self, index):
        """
        Elimina el nodo en la posición indicada. O(n)
        Lanza IndexError si el índice está fuera de rango.
        """
        if index < 0 or index >= self._size:
            raise IndexError(f"Índice {index} fuera de rango (tamaño: {self._size})")

        if index == 0:
            self.head = self.head.next
            self._size -= 1
            return

        current = self.head
        for _ in range(index - 1):
            current = current.next
        current.next = current.next.next
        self._size -= 1

    # ──────────────────────────────────────────────
    # ACCESO Y BÚSQUEDA
    # ──────────────────────────────────────────────

    def get(self, index):
        """
        Devuelve el valor del nodo en la posición indicada. O(n)
        Lanza IndexError si el índice está fuera de rango.
        """
        if index < 0 or index >= self._size:
            raise IndexError(f"Índice {index} fuera de rango (tamaño: {self._size})")

        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def search(self, data):
        """
        Busca el valor en la lista. O(n)
        Devuelve el índice si lo encuentra, o -1 si no existe.
        """
        current = self.head
        index = 0
        while current is not None:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def update(self, index, data):
        """
        Actualiza el valor del nodo en la posición indicada. O(n)
        Lanza IndexError si el índice está fuera de rango.
        """
        if index < 0 or index >= self._size:
            raise IndexError(f"Índice {index} fuera de rango (tamaño: {self._size})")

        current = self.head
        for _ in range(index):
            current = current.next
        current.data = data

    # ──────────────────────────────────────────────
    # OPERACIONES SOBRE LA LISTA
    # ──────────────────────────────────────────────

    def reverse(self):
        """Invierte la lista in-place. O(n)"""
        prev = None
        current = self.head
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def to_list(self):
        """Convierte la lista enlazada a una lista de Python. O(n)"""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def clear(self):
        """Vacía la lista. O(1)"""
        self.head = None
        self._size = 0

    def is_empty(self):
        """Devuelve True si la lista está vacía. O(1)"""
        return self._size == 0

    def size(self):
        """Devuelve el número de elementos. O(1)"""
        return self._size

    # ──────────────────────────────────────────────
    # MÉTODOS ESPECIALES (DUNDER)
    # ──────────────────────────────────────────────

    def __len__(self):
        return self._size

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def __contains__(self, data):
        return self.search(data) != -1

    def __repr__(self):
        nodes = " -> ".join(str(item) for item in self)
        return f"MyLinkedList([{nodes}])"

    def __str__(self):
        nodes = " -> ".join(str(item) for item in self)
        return f"[{nodes}]"

    def __eq__(self, other):
        if not isinstance(other, MyLinkedList):
            return False
        return self.to_list() == other.to_list()


# ──────────────────────────────────────────────────────
# DEMO / PRUEBAS BÁSICAS
# ──────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 45)
    print("     Demo de MyLinkedList")
    print("=" * 45)

    # Crear lista desde iterable
    ll = MyLinkedList([10, 20, 30, 40])
    print(f"Lista inicial:       {ll}")
    print(f"Tamaño:              {len(ll)}")

    # append y prepend
    ll.append(50)
    ll.prepend(0)
    print(f"Después append/prepend: {ll}")

    # insert
    ll.insert(3, 99)
    print(f"Insert 99 en idx 3:  {ll}")

    # get
    print(f"get(3):              {ll.get(3)}")

    # search
    print(f"search(99):          índice {ll.search(99)}")
    print(f"search(999):         índice {ll.search(999)}")

    # update
    ll.update(3, 88)
    print(f"update(3, 88):       {ll}")

    # delete
    ll.delete(88)
    print(f"delete(88):          {ll}")

    # delete_at
    ll.delete_at(0)
    print(f"delete_at(0):        {ll}")

    # contains
    print(f"20 in lista:         {20 in ll}")
    print(f"99 in lista:         {99 in ll}")

    # reverse
    ll.reverse()
    print(f"reverse():           {ll}")

    # to_list
    print(f"to_list():           {ll.to_list()}")

    # iteración
    print("Iteración for:      ", end=" ")
    for val in ll:
        print(val, end=" ")
    print()

    # clear
    ll.clear()
    print(f"Después clear():     {ll}  | is_empty: {ll.is_empty()}")
    print("=" * 45)