from collections import deque
#Importacion de Clase Cola
from Clase_Cola import Cola as Cola

def sumar_colas(cola_a: Cola, cola_b: Cola) -> Cola:
    if cola_a.tamanio() != cola_b.tamanio():
        raise ValueError("Las colas deben tener el mismo número de elementos")

    resultado = Cola()
    temp_a = Cola()
    temp_b = Cola()

    while not cola_a.esta_vacia():
        a = cola_a.desencolar()
        b = cola_b.desencolar()
        resultado.encolar(a + b)
        temp_a.encolar(a)
        temp_b.encolar(b)

    while not temp_a.esta_vacia():
        cola_a.encolar(temp_a.desencolar())
        cola_b.encolar(temp_b.desencolar())

    return resultado


def pedir_cola(nombre: str, cantidad: int) -> Cola:
    cola = Cola()
    print(f"\n  Ingrese los {cantidad} números enteros para la {nombre}:")
    for i in range(1, cantidad + 1):
        while True:
            try:
                n = int(input(f"    Elemento {i}: "))
                cola.encolar(n)
                break
            except ValueError:
                print("    [!] Debe ingresar un número entero. Intente de nuevo.")
    return cola


if __name__ == "__main__":
    print("=" * 45)
    print("   EJERCICIO 1 – Suma de colas")
    print("=" * 45)

    while True:
        try:
            cantidad = int(input("\n¿Cuántos elementos tendrán las colas? "))
            if cantidad <= 0:
                print("  [!] Debe ser un número mayor a 0.")
                continue
            break
        except ValueError:
            print("  [!] Ingrese un número entero válido.")

    cola_a = pedir_cola("Cola A", cantidad)
    cola_b = pedir_cola("Cola B", cantidad)

    cola_resultado = sumar_colas(cola_a, cola_b)

    print("\n" + "=" * 45)
    print(f"  {'Cola A':<12} {'Cola B':<12} {'Resultado'}")
    print("  " + "-" * 38)

    while not cola_a.esta_vacia():
        a = cola_a.desencolar()
        b = cola_b.desencolar()
        r = cola_resultado.desencolar()
        print(f"  {a:<12} {b:<12} {r}")

    print("=" * 45)