# ──────────────────────────────────────────
# Nodo para la lista enlazada de ingredientes
# ──────────────────────────────────────────

class NodoIngrediente:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None  # apunta al siguiente ingrediente (NIL si es el último)


# ──────────────────────────────────────────
# Nodo para el arreglo de postres
# ──────────────────────────────────────────

class NodoPostre:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ingredientes = None  # apunta a la lista enlazada de ingredientes (NIL si vacía)


# ──────────────────────────────────────────
# Arreglo POSTRES (lista de NodoPostre)
# ordenado alfabéticamente
# ──────────────────────────────────────────

POSTRES = []


# ══════════════════════════════════════════
# Operaciones sobre lista enlazada de ingredientes
# ══════════════════════════════════════════

def agregar_ingrediente(nodo_postre, dato):

    #Inserta un ingrediente al final de la lista enlazada.

    nuevo = NodoIngrediente(dato.strip().lower())
    if nodo_postre.ingredientes is None:
        nodo_postre.ingredientes = nuevo
    else:
        actual = nodo_postre.ingredientes
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo


def buscar_ingrediente(nodo_postre, dato):

    #Regresa el nodo del ingrediente o None si no existe.

    actual = nodo_postre.ingredientes
    while actual is not None:
        if actual.dato == dato.strip().lower():
            return actual
        actual = actual.siguiente
    return None


def eliminar_ingrediente_lista(nodo_postre, dato):

    #Elimina un ingrediente de la lista enlazada. Regresa True si lo encontró.

    dato = dato.strip().lower()
    actual = nodo_postre.ingredientes
    anterior = None

    while actual is not None:
        if actual.dato == dato:
            if anterior is None:
                nodo_postre.ingredientes = actual.siguiente  # era la cabeza
            else:
                anterior.siguiente = actual.siguiente
            actual.siguiente = None  # liberar nodo
            return True
        anterior = actual
        actual = actual.siguiente
    return False


def imprimir_lista_ingredientes(nodo_postre):

    # Recorre e imprime la lista enlazada de ingredientes.

    if nodo_postre.ingredientes is None:
        print(f"  [!] '{nodo_postre.nombre}' no tiene ingredientes (NIL).")
        return
    print(f"  Ingredientes de '{nodo_postre.nombre}':")
    actual = nodo_postre.ingredientes
    while actual is not None:
        flecha = " --> " if actual.siguiente else " --> NIL"
        print(f"    [{actual.dato}]{flecha}", end="")
        actual = actual.siguiente
    print()


# ══════════════════════════════════════════
# Operaciones sobre el arreglo POSTRES
# ══════════════════════════════════════════

def buscar_postre(nombre):
    # Regresa el NodoPostre o None si no existe.
    nombre = nombre.strip().lower()
    for nodo in POSTRES:
        if nodo.nombre.lower() == nombre:
            return nodo
    return None


def insertar_postre_ordenado(nodo_postre):

    # Inserta el NodoPostre manteniendo orden alfabético.
    
    pos = len(POSTRES)
    for i, nodo in enumerate(POSTRES):
        if nodo_postre.nombre.lower() < nodo.nombre.lower():
            pos = i
            break
    POSTRES.insert(pos, nodo_postre)


def mostrar_postres():
    if not POSTRES:
        print("\n  POSTRES --> NIL  (arreglo vacío)")
        return
    print("\n  ARREGLO POSTRES:")
    print("  " + "-" * 50)
    for nodo in POSTRES:
        print(f"  [{nodo.nombre}]", end="")
        actual = nodo.ingredientes
        if actual is None:
            print(" --> NIL")
        else:
            while actual is not None:
                print(f" --> [{actual.dato}]", end="")
                actual = actual.siguiente
            print(" --> NIL")
    print("  " + "-" * 50)


# ══════════════════════════════════════════
# Opciones del menú
# ══════════════════════════════════════════

# a) Imprimir ingredientes
def op_imprimir():
    nombre = input("\n  Nombre del postre: ").strip()
    nodo = buscar_postre(nombre)
    if nodo is None:
        print(f"  [!] '{nombre}' no existe en POSTRES.")
        return
    imprimir_lista_ingredientes(nodo)


# b) Insertar ingredientes
def op_insertar_ingredientes():
    nombre = input("\n  Nombre del postre: ").strip()
    nodo = buscar_postre(nombre)
    if nodo is None:
        print(f"  [!] '{nombre}' no existe en POSTRES.")
        return
    entrada = input("  Ingredientes a agregar (separados por coma): ").strip()
    if not entrada:
        print("  [!] No ingresaste ningún ingrediente.")
        return
    agregados = 0
    for ing in entrada.split(","):
        ing = ing.strip().lower()
        if buscar_ingrediente(nodo, ing):
            print(f"  [!] '{ing}' ya existe, no se duplica.")
        else:
            agregar_ingrediente(nodo, ing)
            agregados += 1
    if agregados:
        print(f"  [OK] {agregados} ingrediente(s) agregado(s) a '{nodo.nombre}'.")


# c) Eliminar un ingrediente
def op_eliminar_ingrediente():
    nombre = input("\n  Nombre del postre: ").strip()
    nodo = buscar_postre(nombre)
    if nodo is None:
        print(f"  [!] '{nombre}' no existe en POSTRES.")
        return
    if nodo.ingredientes is None:
        print(f"  [!] '{nodo.nombre}' no tiene ingredientes (NIL).")
        return
    imprimir_lista_ingredientes(nodo)
    ing = input("  Ingrediente a eliminar: ").strip()
    if eliminar_ingrediente_lista(nodo, ing):
        print(f"  [OK] '{ing}' eliminado correctamente.")
    else:
        print(f"  [!] '{ing}' no se encontró en la lista.")


# d) Alta de postre
def op_alta():
    nombre = input("\n  Nombre del nuevo postre: ").strip()
    if not nombre:
        print("  [!] El nombre no puede estar vacío.")
        return
    if buscar_postre(nombre) is not None:
        print(f"  [!] '{nombre}' ya existe en POSTRES.")
        return
    entrada = input("  Ingredientes (separados por coma): ").strip()
    if not entrada:
        print("  [!] Debes ingresar al menos un ingrediente.")
        return
    nuevo_nodo = NodoPostre(nombre)
    for ing in entrada.split(","):
        agregar_ingrediente(nuevo_nodo, ing)
    insertar_postre_ordenado(nuevo_nodo)
    print(f"  [OK] '{nombre}' dado de alta y ordenado alfabéticamente.")


# e) Baja de postre
def op_baja():
    nombre = input("\n  Nombre del postre a eliminar: ").strip()
    nodo = buscar_postre(nombre)
    if nodo is None:
        print(f"  [!] '{nombre}' no existe en POSTRES.")
        return
    conf = input(f"  ¿Eliminar '{nodo.nombre}' y toda su lista? (s/n): ").strip().lower()
    if conf != "s":
        print("  Operación cancelada.")
        return
    # Liberar lista enlazada antes de eliminar el nodo
    actual = nodo.ingredientes
    while actual is not None:
        siguiente = actual.siguiente
        actual.siguiente = None  # liberar nodo
        actual = siguiente
    nodo.ingredientes = None
    POSTRES.remove(nodo)
    print(f"  [OK] '{nodo.nombre}' y su lista enlazada eliminados (NIL).")


# ══════════════════════════════════════════
# Ejercicio 2: Eliminar postres repetidos
# ══════════════════════════════════════════

def op_eliminar_repetidos():
    vistos = set()
    eliminados = []
    i = 0
    while i < len(POSTRES):
        nombre_lower = POSTRES[i].nombre.lower()
        if nombre_lower in vistos:
            nodo = POSTRES.pop(i)
            # contar ingredientes en la lista enlazada
            cont = 0
            actual = nodo.ingredientes
            while actual:
                cont += 1
                actual = actual.siguiente
            eliminados.append((nodo.nombre, cont))
        else:
            vistos.add(nombre_lower)
            i += 1

    if eliminados:
        print("\n  [ADVERTENCIA] Duplicados encontrados y eliminados:")
        for nombre, cont in eliminados:
            print(f"    - '{nombre}' tenía {cont} ingrediente(s) → lista enlazada PERDIDA")
        print()
        print("  CONCLUSIÓN: Al eliminar un nodo duplicado del arreglo,")
        print("  su lista enlazada de ingredientes también se pierde.")
        print("  Si los duplicados tenían ingredientes distintos, esa")
        print("  información es irrecuperable. Se recomienda revisar")
        print("  manualmente o respaldar antes de ejecutar esta opción.")
    else:
        print("\n  [OK] No se encontraron postres repetidos.")


# ══════════════════════════════════════════
# Datos iniciales de prueba
# ══════════════════════════════════════════

def cargar_datos_iniciales():
    datos = [
        ("Arroz con leche", ["arroz", "leche", "azucar", "canela"]),
        ("Flan",            ["huevo", "leche", "azucar", "vainilla"]),
        ("Flan",            ["huevo", "leche", "azucar", "vainilla"]),
        ("Gelatina",        ["grenetina", "agua", "azucar", "colorante"]),
        ("Pay de limon",    ["galleta", "mantequilla", "leche condensada", "limon"]),
    ]
    for nombre, ings in datos:
        nodo = NodoPostre(nombre)
        for ing in ings:
            agregar_ingrediente(nodo, ing)
        insertar_postre_ordenado(nodo)


# ══════════════════════════════════════════
# Menú principal
# ══════════════════════════════════════════

def menu():
    cargar_datos_iniciales()

    opciones = {
        "1": ("(a) Imprimir ingredientes de un postre",       op_imprimir),
        "2": ("(b) Insertar ingredientes a un postre",        op_insertar_ingredientes),
        "3": ("(c) Eliminar un ingrediente de un postre",     op_eliminar_ingrediente),
        "4": ("(d) Dar de alta un postre",                    op_alta),
        "5": ("(e) Dar de baja un postre",                    op_baja),
        "6": ("    Mostrar todos los postres",                mostrar_postres),
        "7": ("    Eliminar postres repetidos (Ejercicio 2)", op_eliminar_repetidos),
        "0": ("    Salir",                                    None),
    }

    while True:
        print("\n" + "=" * 52)
        print("      GESTIÓN DE POSTRES – Listas Enlazadas")
        print("=" * 52)
        for clave, (desc, _) in opciones.items():
            print(f"  {clave}. {desc}")
        print("=" * 52)

        opcion = input("  Elige una opción: ").strip()

        if opcion == "0":
            print("\n  Programa finalizado\n")
            break
        elif opcion in opciones:
            _, funcion = opciones[opcion]
            funcion()
            input("\n  Presiona Enter para continuar...")
        else:
            print("  [!] Opción no válida.")


if __name__ == "__main__":
    menu()