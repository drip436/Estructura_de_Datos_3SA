# ============================================================
#  PROGRAMA 2: Torres de Hanoi para 3 discos
#  usando la clase Pila
# ============================================================

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


# ─────────────────────────────────────────────
#  Visualización de las torres
# ─────────────────────────────────────────────
def mostrar_torres(origen: Pila, auxiliar: Pila, destino: Pila,
                   num_discos: int = 3):
    
    #Dibuja el estado actual de las tres torres en consola.
    
    pilas = [origen, auxiliar, destino]
    print("\n" + "─" * 42)
    for nivel in range(num_discos, 0, -1):
        fila = ""
        for pila in pilas:
            contenido = pila.contenido()
            if len(contenido) >= nivel:
                disco = contenido[nivel - 1]
                fila += f"  {'■' * disco:^7}  "
            else:
                fila += f"  {'|':^7}  "
        print(fila)
    # Base y etiquetas
    print("  " + "─" * 7 + "    " + "─" * 7 + "    " + "─" * 7)
    print(f"  {origen.nombre:^7}    {auxiliar.nombre:^7}    {destino.nombre:^7}")
    print("─" * 42)


# ─────────────────────────────────────────────
#  Mover un disco entre dos pilas
# ─────────────────────────────────────────────
def mover_disco(desde: Pila, hacia: Pila,
                origen: Pila, auxiliar: Pila, destino: Pila,
                paso: list, num_discos: int):
    """Extrae el tope de 'desde' y lo apila en 'hacia'."""
    disco = desde.desapilar()
    hacia.apilar(disco)
    paso[0] += 1
    print(f"\nPaso {paso[0]:>2}: Mover disco {disco} "
          f"de '{desde.nombre}' → '{hacia.nombre}'")
    mostrar_torres(origen, auxiliar, destino, num_discos)


# ─────────────────────────────────────────────
#  Torres de Hanoi — solución recursiva con Pila
# ─────────────────────────────────────────────
def hanoi(n: int, origen: Pila, destino: Pila, auxiliar: Pila,
          paso: list, num_discos: int):
    """
    Resuelve las Torres de Hanoi moviendo n discos
    desde 'origen' hacia 'destino' usando 'auxiliar'.
    """
    if n == 1:
        mover_disco(origen, destino, origen, auxiliar, destino, paso, num_discos)
        return
    hanoi(n - 1, origen, auxiliar, destino, paso, num_discos)
    mover_disco(origen, destino, origen, auxiliar, destino, paso, num_discos)
    hanoi(n - 1, auxiliar, destino, origen, paso, num_discos)


# ─────────────────────────────────────────────
#  Solución iterativa con Pilas (sin recursión)
# ─────────────────────────────────────────────
def hanoi_iterativo(num_discos: int):
    """
    Resuelve las Torres de Hanoi de forma iterativa usando tres Pilas.
    Funciona para cualquier número de discos.
    """
    A = Pila("Origen")
    B = Pila("Auxiliar")
    C = Pila("Destino")

    # Cargar discos (el más grande en la base)
    for disco in range(num_discos, 0, -1):
        A.apilar(disco)

    total_movimientos = (2 ** num_discos) - 1
    paso = [0]

    # Para número impar de discos: A→C→B→A (ciclo)
    # Para número par de discos:   A→B→C→A (ciclo)
    if num_discos % 2 == 0:
        pilas = [A, B, C]
    else:
        pilas = [A, C, B]

    print(f"\nEstado inicial:")
    mostrar_torres(A, B, C, num_discos)

    for _ in range(total_movimientos):
        # Movimiento legal entre pilas[(i) % 3] y pilas[(i+1) % 3]
        for i in range(3):
            p1 = pilas[i % 3]
            p2 = pilas[(i + 1) % 3]
            # Mover solo si es un movimiento legal
            if p1.esta_vacia() and p2.esta_vacia():
                continue
            if p1.esta_vacia():
                mover_disco(p2, p1, A, B, C, paso, num_discos)
            elif p2.esta_vacia():
                mover_disco(p1, p2, A, B, C, paso, num_discos)
            elif p1.tope() < p2.tope():
                mover_disco(p1, p2, A, B, C, paso, num_discos)
            else:
                mover_disco(p2, p1, A, B, C, paso, num_discos)
            if paso[0] >= total_movimientos:
                break
        if paso[0] >= total_movimientos:
            break

    return paso[0]


# ─────────────────────────────────────────────
#  Programa principal
# ─────────────────────────────────────────────
if __name__ == "__main__":
    NUM_DISCOS = 3

    print("=" * 42)
    print("   TORRES DE HANOI  —  {} discos".format(NUM_DISCOS))
    print("=" * 42)
    print(f"Movimientos necesarios: {2**NUM_DISCOS - 1}")

    # ── Método recursivo ──
    print("\n★  SOLUCIÓN RECURSIVA  ★")

    origen   = Pila("Origen")
    auxiliar = Pila("Auxiliar")
    destino  = Pila("Destino")

    # Cargar discos en la pila origen (mayor abajo, menor arriba)
    for disco in range(NUM_DISCOS, 0, -1):
        origen.apilar(disco)

    print("\nEstado inicial:")
    mostrar_torres(origen, auxiliar, destino, NUM_DISCOS)

    paso = [0]
    hanoi(NUM_DISCOS, origen, destino, auxiliar, paso, NUM_DISCOS)

    print(f"\n✓ Resuelto en {paso[0]} movimientos.")
    print("\nEstado final (todos los discos en 'Destino'):")
    mostrar_torres(origen, auxiliar, destino, NUM_DISCOS)