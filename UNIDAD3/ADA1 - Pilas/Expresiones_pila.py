# ============================================================
#  PROGRAMA 1: Evaluador de expresiones Postfija / Prefija
#  usando una clase Pila implementada desde cero
# ============================================================

#Invoca el fichero con la clase Pila
from Clase_Pila import Pila as Pila

# ─────────────────────────────────────────────
#  Operadores soportados
# ─────────────────────────────────────────────
OPERADORES = {'+', '-', '*', '/'}


def aplicar_operacion(operador: str, a: float, b: float) -> float:
    """Aplica una operación binaria sobre dos operandos."""
    if operador == '+':
        return a + b
    elif operador == '-':
        return a - b
    elif operador == '*':
        return a * b
    elif operador == '/':
        if b == 0:
            raise ZeroDivisionError("División por cero.")
        return a / b


# ─────────────────────────────────────────────
#  Evaluación POSTFIJA  (ej: "3 4 + 2 *")
# ─────────────────────────────────────────────
def evaluar_postfija(expresion: str) -> float:
    """
    Evalúa una expresión en notación postfija (Notación Polaca Inversa).
    Los tokens deben estar separados por espacios.
    Ejemplo: "3 4 + 2 *"  →  14.0
    """
    pila = Pila()
    tokens = expresion.strip().split()

    for token in tokens:
        if token in OPERADORES:
            b = pila.desapilar()   # segundo operando
            a = pila.desapilar()   # primer operando
            resultado = aplicar_operacion(token, a, b)
            pila.apilar(resultado)
        else:
            pila.apilar(float(token))

    if len(pila) != 1:
        raise ValueError("Expresión postfija inválida.")
    return pila.desapilar()


# ─────────────────────────────────────────────
#  Evaluación PREFIJA  (ej: "* + 3 4 2")
# ─────────────────────────────────────────────
def evaluar_prefija(expresion: str) -> float:
    """
    Evalúa una expresión en notación prefija (Notación Polaca).
    Los tokens deben estar separados por espacios.
    Ejemplo: "* + 3 4 2"  →  14.0
    """
    pila = Pila()
    tokens = expresion.strip().split()

    # Se recorre de derecha a izquierda
    for token in reversed(tokens):
        if token in OPERADORES:
            a = pila.desapilar()   # primer operando
            b = pila.desapilar()   # segundo operando
            resultado = aplicar_operacion(token, a, b)
            pila.apilar(resultado)
        else:
            pila.apilar(float(token))

    if len(pila) != 1:
        raise ValueError("Expresión prefija inválida.")
    return pila.desapilar()


# ─────────────────────────────────────────────
#  Demo / Pruebas
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  EVALUADOR DE EXPRESIONES CON PILA")
    print("=" * 50)

    # ---------- POSTFIJA ----------
    ejemplos_postfija = [
        ("3 4 +",         7.0),    # 3 + 4
        ("3 4 + 2 *",    14.0),    # (3 + 4) * 2
        ("5 1 2 + 4 * + 3 -",  14.0),  # 5 + ((1+2)*4) - 3
        ("10 2 /",         5.0),   # 10 / 2
        ("2 3 4 * +",     14.0),   # 2 + (3 * 4)
    ]

    print("\n--- Notación POSTFIJA ---")
    for expr, esperado in ejemplos_postfija:
        resultado = evaluar_postfija(expr)
        estado = "✓" if abs(resultado - esperado) < 1e-9 else "✗"
        print(f"  {estado}  \"{expr}\"  =  {resultado}")

    # ---------- PREFIJA ----------
    ejemplos_prefija = [
        ("+ 3 4",          7.0),
        ("* + 3 4 2",     14.0),
        ("+ 5 - * + 1 2 4 3",  14.0),
        ("/ 10 2",          5.0),
        ("+ 2 * 3 4",      14.0),
    ]

    print("\n--- Notación PREFIJA ---")
    for expr, esperado in ejemplos_prefija:
        resultado = evaluar_prefija(expr)
        estado = "✓" if abs(resultado - esperado) < 1e-9 else "✗"
        print(f"  {estado}  \"{expr}\"  =  {resultado}")

    # ---------- Entrada interactiva ----------
    print("\n" + "=" * 50)
    print("  MODO INTERACTIVO")
    print("=" * 50)
    print("Ingrese expresiones con tokens separados por espacios.")
    print("Escriba 'salir' para terminar.\n")

    while True:
        modo = input("Modo (postfija/prefija): ").strip().lower()
        if modo == "salir":
            break
        if modo not in ("postfija", "prefija"):
            print("  Modo no reconocido. Use 'postfija' o 'prefija'.")
            continue

        expresion = input("Expresión: ").strip()
        if expresion.lower() == "salir":
            break

        try:
            if modo == "postfija":
                res = evaluar_postfija(expresion)
            else:
                res = evaluar_prefija(expresion)
            print(f"  Resultado: {res}\n")
        except Exception as e:
            print(f"  Error: {e}\n")