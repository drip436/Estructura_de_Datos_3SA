from collections import deque

class Cola:
    def __init__(self):
        self._datos = deque()

    def encolar(self, elemento):
        self._datos.append(elemento)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self._datos.popleft()

    def esta_vacia(self):
        return len(self._datos) == 0

    def tamanio(self):
        return len(self._datos)

    def __repr__(self):
        return f"Cola({list(self._datos)})"