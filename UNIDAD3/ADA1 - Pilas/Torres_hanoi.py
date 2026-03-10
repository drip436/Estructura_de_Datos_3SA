# ============================================================
#  PROGRAMA 2: Torres de Hanoi
#  usando la clase Pila
# ============================================================

from Clase_Pila import Pila as Pila

# ─────────────────────────────────────────────
#  Pedir número de discos al usuario
# ─────────────────────────────────────────────
MAX_DISCOS = 15  # Con 15 discos se realizan 32.767 movimientos

def pedir_num_discos() -> int:
    """
    Solicita al usuario un número de discos válido entre 1 y MAX_DISCOS.
    Retorna el número ingresado.
    """
    print(f"\n  Ingrese el número de discos (mínimo 1, máximo {MAX_DISCOS}).")
    print(f"  Nota: con {MAX_DISCOS} discos se realizan {2**MAX_DISCOS - 1:,} movimientos.")
    while True:
        try:
            n = int(input(f"\n  Número de discos [1-{MAX_DISCOS}]: "))
            if n < 1:
                print("  [!] Debe ser al menos 1 disco.")
            elif n > MAX_DISCOS:
                print(f"  [!] El máximo permitido es {MAX_DISCOS} discos.")
            else:
                return n
        except ValueError:
            print("  [!] Ingrese un número entero válido.")


# ─────────────────────────────────────────────
#  Visualización de las torres
# ─────────────────────────────────────────────
def mostrar_torres(origen: Pila, auxiliar: Pila, destino: Pila, num_discos: int):
    """Dibuja el estado actual de las tres torres en consola."""
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
    """
    A = Pila("Origen")
    B = Pila("Auxiliar")
    C = Pila("Destino")

    for disco in range(num_discos, 0, -1):
        A.apilar(disco)

    total_movimientos = (2 ** num_discos) - 1
    paso = [0]

    if num_discos % 2 == 0:
        pilas = [A, B, C]
    else:
        pilas = [A, C, B]

    print(f"\nEstado inicial:")
    mostrar_torres(A, B, C, num_discos)

    for _ in range(total_movimientos):
        for i in range(3):
            p1 = pilas[i % 3]
            p2 = pilas[(i + 1) % 3]
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

    print("=" * 42)
    print("        TORRES DE HANOI")
    print("=" * 42)

    NUM_DISCOS = pedir_num_discos()

    print("\n" + "=" * 42)
    print(f"   TORRES DE HANOI  —  {NUM_DISCOS} disco(s)")
    print("=" * 42)
    print(f"Movimientos necesarios: {2**NUM_DISCOS - 1:,}")

    # ── Método recursivo ──
    print("\n★  SOLUCIÓN RECURSIVA  ★")

    origen   = Pila("Origen")
    auxiliar = Pila("Auxiliar")
    destino  = Pila("Destino")

    for disco in range(NUM_DISCOS, 0, -1):
        origen.apilar(disco)

    print("\nEstado inicial:")
    mostrar_torres(origen, auxiliar, destino, NUM_DISCOS)

    paso = [0]
    hanoi(NUM_DISCOS, origen, destino, auxiliar, paso, NUM_DISCOS)

    print(f"\n✓ Resuelto en {paso[0]:,} movimientos.")
    print("\nEstado final (todos los discos en 'Destino'):")
    mostrar_torres(origen, auxiliar, destino, NUM_DISCOS)