# Calse Pila que conecta con los ficheros Expresiones_pila.py y Torres_hanoi.py de la actividad ADA1-Pilas.
class Pila:
    """Implementación de una Pila (Stack) con lista."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self._datos = []

    def apilar(self, elemento):
        self._datos.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError(f"La pila '{self.nombre}' está vacía.")
        return self._datos.pop()

    def tope(self):
        if self.esta_vacia():
            return None
        return self._datos[-1]

    def esta_vacia(self):
        return len(self._datos) == 0

    def contenido(self):
        """Devuelve una copia del contenido (base → tope)."""
        return list(self._datos)

    def __len__(self):
        return len(self._datos)

    def __repr__(self):
        return f"Pila '{self.nombre}': {self._datos}"