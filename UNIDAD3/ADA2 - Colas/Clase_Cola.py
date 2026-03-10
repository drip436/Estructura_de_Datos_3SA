from collections import deque

# Clase Cola (conecta con los dos ficheros Suma_de_dos_colas.py y Sistemas_de_Atencion.py de la actividad ADA2-COLAS)
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