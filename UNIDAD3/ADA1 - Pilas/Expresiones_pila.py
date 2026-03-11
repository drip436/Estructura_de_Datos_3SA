from Clase_Pila import Pila as Pila

# ─────────────────────────────────────────────
# Utilidades
# ─────────────────────────────────────────────

OPERADORES = {'+', '-', '*', '/'}

def es_operador(token):
    return token in OPERADORES

def es_numero(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

def aplicar_operacion(op, a, b):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError("División por cero.")
        return a / b


# ─────────────────────────────────────────────
# Evaluadores
# ─────────────────────────────────────────────

def evaluar_postfija(expresion):
    tokens = expresion.split()
    pila = Pila("postfija")

    print(f"\n  {'Token':<10} {'Acción':<35} {'Pila'}")
    print(f"  {'-'*65}")

    for token in tokens:
        if es_numero(token):
            pila.apilar(float(token))
            accion = f"Apilar {token}"
        elif es_operador(token):
            b = pila.desapilar()
            a = pila.desapilar()
            resultado = aplicar_operacion(token, a, b)
            pila.apilar(resultado)
            accion = f"{a} {token} {b} = {resultado}"
        else:
            raise ValueError(f"Token desconocido: '{token}'")
        print(f"  {token:<10} {accion:<35} {pila.contenido()}")

    if len(pila) != 1:
        raise ValueError("Expresión malformada: sobran o faltan tokens.")
    return pila.desapilar()


def evaluar_prefija(expresion):
    tokens = expresion.split()
    pila = Pila("prefija")

    print(f"\n  {'Token':<10} {'Acción':<35} {'Pila'}")
    print(f"  {'-'*65}")

    for token in reversed(tokens):
        if es_numero(token):
            pila.apilar(float(token))
            accion = f"Apilar {token}"
        elif es_operador(token):
            a = pila.desapilar()
            b = pila.desapilar()
            resultado = aplicar_operacion(token, a, b)
            pila.apilar(resultado)
            accion = f"{a} {token} {b} = {resultado}"
        else:
            raise ValueError(f"Token desconocido: '{token}'")
        print(f"  {token:<10} {accion:<35} {pila.contenido()}")

    if len(pila) != 1:
        raise ValueError("Expresión malformada: sobran o faltan tokens.")
    return pila.desapilar()


# ─────────────────────────────────────────────
# Programa principal — solo modo interactivo
# ─────────────────────────────────────────────

def main():
    print("=" * 67)
    print("  Evaluador de expresiones aritméticas con Pila")
    print("  Operadores soportados: + - * /")
    print("  Los tokens deben ir separados por espacios.")
    print()
    print("  Postfija : operandos primero, operador al final  →  3 4 +")
    print("  Prefija  : operador primero, operandos después   →  + 3 4")
    print("=" * 67)

    while True:
        print("\n  ┌─────────────────────────────┐")
        print("  │  [1] Notación Postfija      │")
        print("  │  [2] Notación Prefija       │")
        print("  │  [0] Salir                  │")
        print("  └─────────────────────────────┘")
        opcion = input("  Elige opción: ").strip()

        if opcion == '0':
            print("\n  ¡Hasta luego!")
            break

        elif opcion in ('1', '2'):
            tipo = "postfija" if opcion == '1' else "prefija"
            expr = input(f"  Ingresa la expresión {tipo}: ").strip()

            if not expr:
                print("  ✗ No ingresaste ninguna expresión.")
                continue

            print(f"\n  Evaluando: {expr}")
            try:
                if opcion == '1':
                    resultado = evaluar_postfija(expr)
                else:
                    resultado = evaluar_prefija(expr)

                if resultado == int(resultado):
                    resultado = int(resultado)
                print(f"\n  ✓ Resultado: {resultado}")

            except (IndexError, ValueError, ZeroDivisionError) as e:
                print(f"\n  ✗ Error: {e}")

        else:
            print("  Opción no válida, elige 0, 1 o 2.")


if __name__ == "__main__":
    main()