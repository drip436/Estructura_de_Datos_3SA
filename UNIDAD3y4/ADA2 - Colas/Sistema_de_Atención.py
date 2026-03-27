from collections import deque
#Importacion de Clase Cola
from Clase_Cola import Cola as Cola
#.

SERVICIOS = {
    1: "Consultas generales",
    2: "Siniestros",
    3: "Pagos y cobranzas",
}


class SistemaAtencion:
    def __init__(self):
        self.colas = {s: Cola() for s in SERVICIOS}
        self.contadores = {s: 0 for s in SERVICIOS}

    def cliente_llega(self, servicio):
        self.contadores[servicio] += 1
        turno = self.contadores[servicio]
        self.colas[servicio].encolar(turno)
        print(f"  >> Turno asignado: {turno}  (Servicio: {SERVICIOS[servicio]})")

    def atender_cliente(self, servicio):
        if self.colas[servicio].esta_vacia():
            print(f"  >> No hay clientes en espera para: {SERVICIOS[servicio]}")
            return
        turno = self.colas[servicio].desencolar()
        print(f"  >> Llamando turno: {turno}  (Servicio: {SERVICIOS[servicio]})")

    def ejecutar(self):
        print("=" * 55)
        print("   COMPAÑÍA DE SEGUROS – Sistema de colas")
        print("=" * 55)
        print("  Servicios disponibles:")
        for num, nombre in SERVICIOS.items():
            print(f"    {num} = {nombre}")
        print()
        print("  Comandos:")
        print("    C (numero de servicio)     → 1. Llega un cliente al servicio")
        print("    A (numero de servicio)     → 2. Atender siguiente cliente")
        print("    S                          → 3. Salir")
        print()
        print("  Ejemplo:  C 1   (llega cliente a Consultas generales)")
        print("            A 2   (atender siguiente en Siniestros)")
        print("=" * 55)

        while True:
            try:
                entrada = input("\nComando: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n  Sistema cerrado.")
                break

            if not entrada:
                continue

            partes = entrada.split()
            comando = partes[0].upper()

            if comando == "S":
                print("  Sistema cerrado.")
                break

            elif comando in ("C", "A"):
                if len(partes) < 2:
                    print("  [!] Falta el número de servicio.")
                    print("      Ejemplo: C 1  o  A 2")
                    continue
                try:
                    servicio = int(partes[1])
                except ValueError:
                    print("  [!] El número de servicio debe ser entero.")
                    continue

                if servicio not in SERVICIOS:
                    print(f"  [!] Servicio '{servicio}' no existe.")
                    print(f"      Servicios válidos: {list(SERVICIOS.keys())}")
                    continue

                if comando == "C":
                    self.cliente_llega(servicio)
                else:
                    self.atender_cliente(servicio)

            else:
                print(f"  [!] Comando '{comando}' no reconocido.")
                print("      Use C <nro>, A <nro> o S para salir.")


if __name__ == "__main__":
    sistema = SistemaAtencion()
    sistema.ejecutar()