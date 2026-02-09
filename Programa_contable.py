# Copnectar a una base de datos

class ProgramaContable:
    """Sistema de gestión contable simple"""
    
    def __init__(self):
        self.facturas_proveedores = {}  # {numero: monto}
        self.facturas_clientes = {}     # {numero: monto}
        self.saldo_inicial = 0
    
    def establecer_saldo_inicial(self, saldo):
        """Establecer el saldo inicial"""
        self.saldo_inicial = saldo
        print(f"Saldo inicial: ${saldo:.2f}")
    
    def registrar_factura_proveedor(self, numero, monto):
        """Registrar factura de proveedor"""
        if numero in self.facturas_proveedores:
            print("Ya existe una factura con ese número")
            return
        
        self.facturas_proveedores[numero] = monto
        print(f"Factura proveedor #{numero} registrada")
    
    def registrar_factura_cliente(self, numero, monto):
        """Registrar factura de cliente"""
        if numero in self.facturas_clientes:
            print("Ya existe una factura con ese número")
            return
        
        self.facturas_clientes[numero] = monto
        print(f"Factura cliente #{numero} registrada")
    
    def calcular_total_ingresos(self):
        """Calcular total de ingresos"""
        return sum(self.facturas_clientes.values())
    
    def calcular_total_egresos(self):
        """Calcular total de egresos"""
        return sum(self.facturas_proveedores.values())
    
    def calcular_saldo_total(self):
        """Calcular saldo total"""
        return self.saldo_inicial + self.calcular_total_ingresos() - self.calcular_total_egresos()
    
    def mostrar_ingresos(self):
        """Mostrar ingresos"""
        print("\n--- INGRESOS (Facturas de Clientes) ---")
        
        if not self.facturas_clientes:
            print("No hay ingresos registrados")
        else:
            for numero, monto in self.facturas_clientes.items():
                print(f"Factura #{numero}: ${monto:.2f}")
            print(f"\nTOTAL INGRESOS: ${self.calcular_total_ingresos():.2f}")
    
    def mostrar_egresos(self):
        """Mostrar egresos"""
        print("\n--- EGRESOS (Facturas de Proveedores) ---")
        
        if not self.facturas_proveedores:
            print("No hay egresos registrados")
        else:
            for numero, monto in self.facturas_proveedores.items():
                print(f"Factura #{numero}: ${monto:.2f}")
            print(f"\nTOTAL EGRESOS: ${self.calcular_total_egresos():.2f}")
    
    def mostrar_saldo_total(self):
        """Mostrar saldo total"""
        print("\n--- SALDO TOTAL ---")
        print(f"Saldo Inicial:  ${self.saldo_inicial:.2f}")
        print(f"Total Ingresos: ${self.calcular_total_ingresos():.2f}")
        print(f"Total Egresos:  ${self.calcular_total_egresos():.2f}")
        print(f"SALDO TOTAL:    ${self.calcular_saldo_total():.2f}")
    
    def comparar_facturas(self, num_proveedor, num_cliente):
        """Comparar factura de proveedor con factura de cliente"""
        print("\n--- COMPARACIÓN DE FACTURAS ---")
        
        if num_proveedor not in self.facturas_proveedores:
            print(f"No existe factura de proveedor #{num_proveedor}")
            return
        
        if num_cliente not in self.facturas_clientes:
            print(f"No existe factura de cliente #{num_cliente}")
            return
        
        monto_prov = self.facturas_proveedores[num_proveedor]
        monto_cli = self.facturas_clientes[num_cliente]
        
        print(f"Factura Proveedor #{num_proveedor}: ${monto_prov:.2f}")
        print(f"Factura Cliente #{num_cliente}: ${monto_cli:.2f}")
        
        diferencia = monto_cli - monto_prov
        print(f"\nDiferencia: ${abs(diferencia):.2f}")
        
        if diferencia > 0:
            print(f"*** HAY GANANCIAS de ${diferencia:.2f} ***")
        elif diferencia < 0:
            print(f"*** HAY PÉRDIDAS de ${abs(diferencia):.2f} ***")
        else:
            print("*** Sin ganancias ni pérdidas (están iguales) ***")


def main():
    """Función principal"""
    sistema = ProgramaContable()
    
    while True:
        print("\n=== SISTEMA CONTABLE ===")
        print("1. Establecer saldo inicial")
        print("2. Registrar factura de proveedor")
        print("3. Registrar factura de cliente")
        print("4. Mostrar saldo total")
        print("5. Mostrar ingresos")
        print("6. Mostrar egresos")
        print("7. Comparar facturas")
        print("8. Salir")
        
        opcion = input("\nOpción: ")
        
        if opcion == "1":
            saldo = float(input("Saldo inicial: $"))
            sistema.establecer_saldo_inicial(saldo)
        
        elif opcion == "2":
            numero = input("Número de factura: ")
            monto = float(input("Monto: $"))
            sistema.registrar_factura_proveedor(numero, monto)
        
        elif opcion == "3":
            numero = input("Número de factura: ")
            monto = float(input("Monto: $"))
            sistema.registrar_factura_cliente(numero, monto)
        
        elif opcion == "4":
            sistema.mostrar_saldo_total()
        
        elif opcion == "5":
            sistema.mostrar_ingresos()
        
        elif opcion == "6":
            sistema.mostrar_egresos()
        
        elif opcion == "7":
            num_prov = input("Número factura proveedor: ")
            num_cli = input("Número factura cliente: ")
            sistema.comparar_facturas(num_prov, num_cli)
        
        elif opcion == "8":
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción inválida")


if __name__ == "__main__":
    main()

""""
class Programa_contable:

    def __init__(self, id_cuenta, nombre, saldo, tipo, fecha_creacion, estado):
        self.id_cuentas = None
        self.nombre = nombre
        self.saldo = 0
        self.tipo = tipo
        self.fecha_creacion = fecha_creacion
        self.estado = "activa"

    def agregar_cuenta (self):
        self.nombre = input("Ingrese su nombre")
        self.tipo = input ("Ingrese el tipo de cuenta")
        self.id_cuentas = len(cuenta) +1

        for cuenta in cuentas:
            if cuenta.nombre == self.nombre:
                print ("Cuenta ya existente")
                return
            
        cuentas.append(self):
        print("Cuenta creada exitosamente")


    def cargar():
        pass

    def abonar ():
        pass

    def main():
        pass

    if __name__ == "__main__":
        
        print (" ")
"""""
