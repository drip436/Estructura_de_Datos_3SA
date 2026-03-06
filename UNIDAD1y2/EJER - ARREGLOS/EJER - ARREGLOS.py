import time
class VentasDepartamentos:
    def __init__(self):
        """Inicializa la matriz de ventas (12 meses × 3 departamentos)"""
        self.meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        self.departamentos = ["Ropa", "Deportes", "Juguetería"]
        
        # Crear matriz 12x3 inicializada con 0.0
        self.ventas = [[0.0 for _ in range(3)] for _ in range(12)]
    
    # -----------------------------------------------------------------
    # 4. MÉTODO PARA BUSCAR VENTAS
    # -----------------------------------------------------------------
    def buscar_ventas(self, criterio_busqueda=None, valor=None):
        """
        Busca ventas según diferentes criterios
        
        Args:
            criterio_busqueda: 'mes', 'departamento', 'monto', 'rango', 'mayor', 'menor'
            valor: valor específico para el criterio
        
        Returns:
            list: Lista de ventas que coinciden
        """
        try:
            resultados = []
            
            if criterio_busqueda is None:
                # Buscar todas las ventas (distintas de 0)
                print("BUSCANDO TODAS LAS VENTAS REGISTRADAS...")
                for i, mes in enumerate(self.meses):
                    for j, dept in enumerate(self.departamentos):
                        if self.ventas[i][j] > 0:
                            resultados.append({
                                'mes': mes,
                                'departamento': dept,
                                'monto': self.ventas[i][j],
                                'indices': (i, j)
                            })
                return resultados
            
            criterio_busqueda = criterio_busqueda.lower()
            
            if criterio_busqueda == 'mes':
                # Buscar por mes específico
                if valor not in self.meses:
                    print(f"❌ Error: Mes '{valor}' no válido")
                    return []
                
                mes_idx = self.meses.index(valor)
                print(f"🔍 BUSCANDO VENTAS EN {valor.upper()}...")
                
                for j, dept in enumerate(self.departamentos):
                    if self.ventas[mes_idx][j] > 0:
                        resultados.append({
                            'mes': valor,
                            'departamento': dept,
                            'monto': self.ventas[mes_idx][j],
                            'indices': (mes_idx, j)
                        })
            
            elif criterio_busqueda == 'departamento':
                # Buscar por departamento específico
                if valor not in self.departamentos:
                    print(f"❌ Error: Departamento '{valor}' no válido")
                    return []
                
                dept_idx = self.departamentos.index(valor)
                print(f"🔍 BUSCANDO VENTAS EN {valor.upper()}...")
                
                for i, mes in enumerate(self.meses):
                    if self.ventas[i][dept_idx] > 0:
                        resultados.append({
                            'mes': mes,
                            'departamento': valor,
                            'monto': self.ventas[i][dept_idx],
                            'indices': (i, dept_idx)
                        })
            
            elif criterio_busqueda == 'monto':
                # Buscar por monto exacto
                try:
                    monto_buscar = float(valor)
                    print(f"🔍 BUSCANDO VENTAS CON MONTO EXACTO ${monto_buscar:,.2f}...")
                    
                    for i, mes in enumerate(self.meses):
                        for j, dept in enumerate(self.departamentos):
                            if abs(self.ventas[i][j] - monto_buscar) < 0.01:  # Tolerancia para floats
                                resultados.append({
                                    'mes': mes,
                                    'departamento': dept,
                                    'monto': self.ventas[i][j],
                                    'indices': (i, j)
                                })
                
                except ValueError:
                    print("❌ Error: El monto debe ser un número válido")
                    return []
            
            elif criterio_busqueda == 'rango':
                # Buscar por rango de montos
                try:
                    if isinstance(valor, (list, tuple)) and len(valor) == 2:
                        min_monto, max_monto = float(valor[0]), float(valor[1])
                    else:
                        print("❌ Error: Formato de rango incorrecto. Use [min, max]")
                        return []
                    
                    print(f"🔍 BUSCANDO VENTAS ENTRE ${min_monto:,.2f} Y ${max_monto:,.2f}...")
                    
                    for i, mes in enumerate(self.meses):
                        for j, dept in enumerate(self.departamentos):
                            if min_monto <= self.ventas[i][j] <= max_monto:
                                resultados.append({
                                    'mes': mes,
                                    'departamento': dept,
                                    'monto': self.ventas[i][j],
                                    'indices': (i, j)
                                })
                
                except (ValueError, TypeError):
                    print("❌ Error: Los valores del rango deben ser números")
                    return []
            
            elif criterio_busqueda == 'mayor':
                # Buscar ventas mayores a un valor
                try:
                    monto_min = float(valor)
                    print(f"🔍 BUSCANDO VENTAS MAYORES A ${monto_min:,.2f}...")
                    
                    for i, mes in enumerate(self.meses):
                        for j, dept in enumerate(self.departamentos):
                            if self.ventas[i][j] > monto_min:
                                resultados.append({
                                    'mes': mes,
                                    'departamento': dept,
                                    'monto': self.ventas[i][j],
                                    'indices': (i, j)
                                })
                
                except ValueError:
                    print("❌ Error: El monto debe ser un número válido")
                    return []
            
            elif criterio_busqueda == 'menor':
                # Buscar ventas menores a un valor
                try:
                    monto_max = float(valor)
                    print(f"🔍 BUSCANDO VENTAS MENORES A ${monto_max:,.2f}...")
                    
                    for i, mes in enumerate(self.meses):
                        for j, dept in enumerate(self.departamentos):
                            if 0 < self.ventas[i][j] < monto_max:
                                resultados.append({
                                    'mes': mes,
                                    'departamento': dept,
                                    'monto': self.ventas[i][j],
                                    'indices': (i, j)
                                })
                
                except ValueError:
                    print("❌ Error: El monto debe ser un número válido")
                    return []
            
            else:
                print("❌ Error: Criterio de búsqueda no válido")
                return []
            
            return resultados
            
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return []
    
    def buscar_ventas_interactivo(self):
        """Interfaz interactiva para buscar ventas"""
        print("\n" + "=" * 60)
        print("🔍 BUSQUEDA DE VENTAS - MODO INTERACTIVO")
        print("=" * 60)
        
        while True:
            print("\n📊 CRITERIOS DE BÚSQUEDA DISPONIBLES:")
            print("1. Por mes específico")
            print("2. Por departamento específico")
            print("3. Por monto exacto")
            print("4. Por rango de montos")
            print("5. Mayores a un monto")
            print("6. Menores a un monto")
            print("7. Todas las ventas registradas")
            print("8. Volver al menú principal")
            
            try:
                opcion = input("\nSeleccione criterio (1-8): ").strip()
                
                if opcion == "8":
                    print("\n👋 Regresando al menú principal...")
                    break
                
                resultados = []
                
                if opcion == "1":
                    print("\n📅 MESES DISPONIBLES:")
                    for i, mes in enumerate(self.meses, 1):
                        print(f"  {i:2d}. {mes}")
                    
                    entrada = input("\nIngrese nombre o número del mes: ").strip()
                    if entrada.isdigit() and 1 <= int(entrada) <= 12:
                        mes = self.meses[int(entrada) - 1]
                    else:
                        mes = entrada.capitalize()
                    
                    resultados = self.buscar_ventas('mes', mes)
                
                elif opcion == "2":
                    print("\n🏬 DEPARTAMENTOS DISPONIBLES:")
                    for i, dept in enumerate(self.departamentos, 1):
                        print(f"  {i}. {dept}")
                    
                    entrada = input("\nIngrese nombre o número del departamento: ").strip()
                    if entrada.isdigit() and 1 <= int(entrada) <= 3:
                        departamento = self.departamentos[int(entrada) - 1]
                    else:
                        departamento = entrada.capitalize()
                    
                    resultados = self.buscar_ventas('departamento', departamento)
                
                elif opcion == "3":
                    monto = input("\nIngrese el monto exacto a buscar: $").strip()
                    resultados = self.buscar_ventas('monto', monto)
                
                elif opcion == "4":
                    print("\n📈 BUSCAR POR RANGO DE MONTOS")
                    min_monto = input("Monto mínimo: $").strip()
                    max_monto = input("Monto máximo: $").strip()
                    resultados = self.buscar_ventas('rango', [min_monto, max_monto])
                
                elif opcion == "5":
                    monto = input("\nIngrese monto mínimo: $").strip()
                    resultados = self.buscar_ventas('mayor', monto)
                
                elif opcion == "6":
                    monto = input("\nIngrese monto máximo: $").strip()
                    resultados = self.buscar_ventas('menor', monto)
                
                elif opcion == "7":
                    resultados = self.buscar_ventas()
                
                else:
                    print("❌ Opción inválida")
                    continue
                
                # Mostrar resultados
                if resultados:
                    print(f"\n✅ ENCONTRADAS {len(resultados)} VENTAS:")
                    print("-" * 60)
                    print(f"{'MES':<12} {'DEPARTAMENTO':<12} {'MONTO':<15}")
                    print("-" * 60)
                    
                    total = 0
                    for venta in resultados:
                        print(f"{venta['mes']:<12} {venta['departamento']:<12} ${venta['monto']:<14,.2f}")
                        total += venta['monto']
                    
                    print("-" * 60)
                    print(f"{'TOTAL':<24} ${total:,.2f}")
                    print("=" * 60)
                    
                    # Exportar opciones
                    exportar = input("\n¿Exportar resultados a archivo? (s/n): ").strip().lower()
                    if exportar == 's':
                        self.exportar_resultados(resultados)
                else:
                    print("\n❌ No se encontraron ventas con los criterios especificados")
                
                # Preguntar por otra búsqueda
                otra = input("\n¿Realizar otra búsqueda? (s/n): ").strip().lower()
                if otra != 's':
                    break
                    
            except KeyboardInterrupt:
                print("\n\n⚠️ Búsqueda interrumpida")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def exportar_resultados(self, resultados, nombre_archivo="resultados_busqueda.txt"):
        """Exporta resultados de búsqueda a archivo"""
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("RESULTADOS DE BÚSQUEDA DE VENTAS\n")
                f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total de ventas encontradas: {len(resultados)}\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"{'MES':<12} {'DEPARTAMENTO':<12} {'MONTO':<15}\n")
                f.write("-" * 60 + "\n")
                
                total = 0
                for venta in resultados:
                    f.write(f"{venta['mes']:<12} {venta['departamento']:<12} ${venta['monto']:<14,.2f}\n")
                    total += venta['monto']
                
                f.write("-" * 60 + "\n")
                f.write(f"{'TOTAL':<24} ${total:,.2f}\n")
                f.write("=" * 60 + "\n")
            
            print(f"✅ Resultados exportados a '{nombre_archivo}'")
            
        except Exception as e:
            print(f"❌ Error al exportar: {e}")
    
    # -----------------------------------------------------------------
    # 5. MÉTODO PARA ELIMINAR VENTA
    # -----------------------------------------------------------------
    def eliminar_venta(self, mes=None, departamento=None, confirmar=True):
        """
        Elimina una venta específica
        
        Args:
            mes: Nombre o número del mes
            departamento: Nombre o número del departamento
            confirmar: Si True, pide confirmación antes de eliminar
        
        Returns:
            bool: True si se eliminó, False en caso contrario
        """
        try:
            # Si no se proporcionan parámetros, modo interactivo
            if mes is None or departamento is None:
                return self.eliminar_venta_interactivo()
            
            # Procesar mes
            if isinstance(mes, int):
                if 1 <= mes <= 12:
                    mes_nombre = self.meses[mes - 1]
                    mes_idx = mes - 1
                else:
                    print(f"❌ Error: Número de mes {mes} fuera de rango (1-12)")
                    return False
            elif isinstance(mes, str):
                if mes.isdigit():
                    mes_num = int(mes)
                    if 1 <= mes_num <= 12:
                        mes_nombre = self.meses[mes_num - 1]
                        mes_idx = mes_num - 1
                    else:
                        print(f"❌ Error: Número de mes {mes_num} fuera de rango (1-12)")
                        return False
                else:
                    if mes in self.meses:
                        mes_nombre = mes
                        mes_idx = self.meses.index(mes)
                    else:
                        print(f"❌ Error: Mes '{mes}' no válido")
                        return False
            else:
                print("❌ Error: Tipo de dato no válido para mes")
                return False
            
            # Procesar departamento
            if isinstance(departamento, int):
                if 1 <= departamento <= 3:
                    dept_nombre = self.departamentos[departamento - 1]
                    dept_idx = departamento - 1
                else:
                    print(f"❌ Error: Número de departamento {departamento} fuera de rango (1-3)")
                    return False
            elif isinstance(departamento, str):
                if departamento.isdigit():
                    dept_num = int(departamento)
                    if 1 <= dept_num <= 3:
                        dept_nombre = self.departamentos[dept_num - 1]
                        dept_idx = dept_num - 1
                    else:
                        print(f"❌ Error: Número de departamento {dept_num} fuera de rango (1-3)")
                        return False
                else:
                    if departamento in self.departamentos:
                        dept_nombre = departamento
                        dept_idx = self.departamentos.index(departamento)
                    else:
                        print(f"❌ Error: Departamento '{departamento}' no válido")
                        return False
            else:
                print("❌ Error: Tipo de dato no válido para departamento")
                return False
            
            # Verificar si existe venta
            venta_actual = self.ventas[mes_idx][dept_idx]
            if venta_actual == 0:
                print(f"❌ No hay venta registrada en {mes_nombre} - {dept_nombre}")
                return False
            
            # Confirmar eliminación
            if confirmar:
                print(f"\n⚠️  CONFIRMAR ELIMINACIÓN")
                print(f"   Mes: {mes_nombre}")
                print(f"   Departamento: {dept_nombre}")
                print(f"   Monto a eliminar: ${venta_actual:,.2f}")
                
                respuesta = input("\n¿Está seguro de eliminar esta venta? (s/n): ").strip().lower()
                if respuesta != 's':
                    print("❌ Eliminación cancelada")
                    return False
            
            # Eliminar venta
            self.ventas[mes_idx][dept_idx] = 0.0
            
            print(f"✅ VENTA ELIMINADA: {mes_nombre} - {dept_nombre}: ${venta_actual:,.2f}")
            return True
            
        except Exception as e:
            print(f"❌ Error al eliminar venta: {e}")
            return False
    
    def eliminar_venta_interactivo(self):
        """Modo interactivo para eliminar ventas"""
        print("\n" + "=" * 60)
        print("🗑️  ELIMINACIÓN DE VENTAS - MODO INTERACTIVO")
        print("=" * 60)
        
        while True:
            try:
                # Mostrar meses
                print("\n📅 MESES DISPONIBLES:")
                for i, mes in enumerate(self.meses, 1):
                    print(f"  {i:2d}. {mes}")
                
                # Solicitar mes
                entrada_mes = input("\nIngrese número o nombre del mes: ").strip()
                
                # Mostrar departamentos
                print("\n🏬 DEPARTAMENTOS DISPONIBLES:")
                for i, dept in enumerate(self.departamentos, 1):
                    print(f"  {i}. {dept}")
                
                # Solicitar departamento
                entrada_dept = input("\nIngrese número o nombre del departamento: ").strip()
                
                # Eliminar venta
                if self.eliminar_venta(entrada_mes, entrada_dept, confirmar=True):
                    print(f"\n✅ Venta eliminada exitosamente!")
                else:
                    print(f"\n❌ No se pudo eliminar la venta")
                
                # Preguntar si continuar
                continuar = input("\n¿Eliminar otra venta? (s/n): ").strip().lower()
                if continuar != 's':
                    print("\n👋 Regresando al menú principal...")
                    break
                    
            except KeyboardInterrupt:
                print("\n\n⚠️ Eliminación interrumpida")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def eliminar_ventas_por_criterio(self, criterio, valor):
        """
        Elimina múltiples ventas según un criterio
        
        Args:
            criterio: 'mes', 'departamento', 'mayor', 'menor', 'rango'
            valor: valor del criterio
        
        Returns:
            dict: Estadísticas de eliminación
        """
        try:
            # Primero buscar las ventas que coinciden
            resultados = self.buscar_ventas(criterio, valor)
            
            if not resultados:
                print(f"❌ No se encontraron ventas con el criterio especificado")
                return {"eliminadas": 0, "total": 0}
            
            print(f"\n⚠️  SE ELIMINARÁN {len(resultados)} VENTAS:")
            total_monto = sum(v['monto'] for v in resultados)
            print(f"   Monto total a eliminar: ${total_monto:,.2f}")
            
            # Confirmar
            confirmar = input("\n¿Está seguro de eliminar todas estas ventas? (s/n): ").strip().lower()
            if confirmar != 's':
                print("❌ Eliminación masiva cancelada")
                return {"eliminadas": 0, "total": len(resultados)}
            
            # Eliminar cada venta
            eliminadas = 0
            for venta in resultados:
                i, j = venta['indices']
                self.ventas[i][j] = 0.0
                eliminadas += 1
            
            print(f"\n✅ ELIMINADAS {eliminadas} VENTAS")
            print(f"   Monto eliminado: ${total_monto:,.2f}")
            
            return {"eliminadas": eliminadas, "total": len(resultados), "monto": total_monto}
            
        except Exception as e:
            print(f"❌ Error en eliminación masiva: {e}")
            return {"eliminadas": 0, "total": 0}
    
    # -----------------------------------------------------------------
    # 6. MÉTODO PARA CARGAR DATOS DE EJEMPLO
    # -----------------------------------------------------------------
    def cargar_datos_ejemplo(self, conjunto="completo"):
        """
        Carga datos de ejemplo predefinidos
        
        Args:
            conjunto: 'completo', 'basico', 'aleatorio', 'estacional'
        
        Returns:
            dict: Estadísticas de carga
        """
        try:
            print(f"\n📂 CARGANDO DATOS DE EJEMPLO ({conjunto.upper()})...")
            
            # Guardar datos originales para posible restauración
            datos_originales = [fila[:] for fila in self.ventas]
            
            # Definir conjuntos de datos de ejemplo
            conjuntos_datos = {
                'basico': [
                    ("Enero", "Ropa", 12000),
                    ("Febrero", "Deportes", 8500),
                    ("Marzo", "Juguetería", 9600),
                ],
                'completo': [
                    # Enero
                    ("Enero", "Ropa", 12500),
                    ("Enero", "Deportes", 8200),
                    ("Enero", "Juguetería", 11300),
                    # Febrero
                    ("Febrero", "Ropa", 9800),
                    ("Febrero", "Deportes", 10500),
                    ("Febrero", "Juguetería", 7600),
                    # Marzo
                    ("Marzo", "Ropa", 13200),
                    ("Marzo", "Deportes", 7400),
                    ("Marzo", "Juguetería", 8900),
                    # Abril
                    ("Abril", "Ropa", 11500),
                    ("Abril", "Deportes", 9200),
                    ("Abril", "Juguetería", 10100),
                    # Mayo
                    ("Mayo", "Ropa", 14200),
                    ("Mayo", "Deportes", 11300),
                    ("Mayo", "Juguetería", 12500),
                    # Junio
                    ("Junio", "Ropa", 16200),
                    ("Junio", "Deportes", 14500),
                    ("Junio", "Juguetería", 18300),
                    # Julio
                    ("Julio", "Ropa", 15200),
                    ("Julio", "Deportes", 13800),
                    ("Julio", "Juguetería", 17200),
                    # Agosto
                    ("Agosto", "Ropa", 14800),
                    ("Agosto", "Deportes", 12600),
                    ("Agosto", "Juguetería", 16500),
                    # Septiembre
                    ("Septiembre", "Ropa", 13500),
                    ("Septiembre", "Deportes", 11800),
                    ("Septiembre", "Juguetería", 14200),
                    # Octubre
                    ("Octubre", "Ropa", 12800),
                    ("Octubre", "Deportes", 11200),
                    ("Octubre", "Juguetería", 13600),
                    # Noviembre
                    ("Noviembre", "Ropa", 17500),
                    ("Noviembre", "Deportes", 14200),
                    ("Noviembre", "Juguetería", 19800),
                    # Diciembre
                    ("Diciembre", "Ropa", 23800),
                    ("Diciembre", "Deportes", 18500),
                    ("Diciembre", "Juguetería", 31200),
                ],
                'estacional': [
                    # Temporada alta (Nov-Dic) - Juguetería y Ropa altas
                    ("Noviembre", "Juguetería", 25000),
                    ("Noviembre", "Ropa", 22000),
                    ("Diciembre", "Juguetería", 45000),
                    ("Diciembre", "Ropa", 32000),
                    # Temporada media (Ene-Feb) - Deportes altos
                    ("Enero", "Deportes", 18000),
                    ("Febrero", "Deportes", 16500),
                    # Temporada baja (Abr-Mayo) - Valores moderados
                    ("Abril", "Ropa", 9500),
                    ("Mayo", "Juguetería", 8500),
                ],
                'aleatorio': [
                    # Datos aleatorios para pruebas
                    ("Enero", "Ropa", 15000),
                    ("Marzo", "Deportes", 12000),
                    ("Mayo", "Juguetería", 18000),
                    ("Julio", "Ropa", 14000),
                    ("Septiembre", "Deportes", 11000),
                    ("Noviembre", "Juguetería", 22000),
                ]
            }
            
            # Seleccionar conjunto
            if conjunto not in conjuntos_datos:
                print(f"❌ Conjunto '{conjunto}' no disponible. Usando 'completo'")
                conjunto = 'completo'
            
            datos = conjuntos_datos[conjunto]
            
            # Preguntar si limpiar datos existentes
            if any(any(venta > 0 for venta in fila) for fila in self.ventas):
                print("\n⚠️  ADVERTENCIA: Ya existen datos en el sistema")
                opcion = input("¿Desea limpiar datos existentes antes de cargar? (s/n): ").strip().lower()
                
                if opcion == 's':
                    # Limpiar todos los datos
                    self.ventas = [[0.0 for _ in range(3)] for _ in range(12)]
                    print("✅ Datos existentes limpiados")
                else:
                    print("⚠️  Los nuevos datos se agregarán a los existentes")
            
            # Cargar datos
            exitosos = 0
            fallidos = 0
            total_monto = 0
            
            for mes, dept, monto in datos:
                print(f"  Cargando: {mes} - {dept}: ${monto:,.2f}")
                
                if self.escribir_monto(mes, dept, monto, mostrar_mensaje=False):
                    exitosos += 1
                    total_monto += monto
                else:
                    fallidos += 1
            
            # Mostrar resumen
            print(f"\n📊 RESUMEN DE CARGA ({conjunto.upper()}):")
            print(f"   ✅ Éxitos: {exitosos}")
            print(f"   ❌ Fallos: {fallidos}")
            print(f"   💰 Monto total cargado: ${total_monto:,.2f}")
            print(f"   📈 Promedio por venta: ${total_monto/exitosos:,.2f}" if exitosos > 0 else "")
            
            # Guardar referencia a datos originales para posible "deshacer"
            self.datos_originales = datos_originales
            
            return {
                "conjunto": conjunto,
                "exitosos": exitosos,
                "fallidos": fallidos,
                "total": len(datos),
                "monto_total": total_monto
            }
            
        except Exception as e:
            print(f"❌ Error al cargar datos de ejemplo: {e}")
            return {"exitosos": 0, "fallidos": 0, "total": 0}
    
    def restaurar_datos_originales(self):
        """Restaura los datos originales (antes de cargar ejemplo)"""
        try:
            if hasattr(self, 'datos_originales'):
                self.ventas = self.datos_originales
                print("✅ Datos originales restaurados")
                return True
            else:
                print("❌ No hay datos originales guardados")
                return False
        except Exception as e:
            print(f"❌ Error al restaurar datos: {e}")
            return False
    
    # -----------------------------------------------------------------
    # MÉTODOS AUXILIARES
    # -----------------------------------------------------------------
    def escribir_monto(self, mes, departamento, monto, mostrar_mensaje=True):
        """Método mejorado para escribir montos"""
        # (Implementación existente del método escribir_monto)
        # ... código del método escribir_monto ...
        pass
    
    def mostrar_tabla_completa(self):
        """Muestra la tabla completa"""
        # (Implementación existente)
        # ... código del método mostrar_tabla_completa ...
        pass
    
    # -----------------------------------------------------------------
    # MENÚ PRINCIPAL COMPLETO
    # -----------------------------------------------------------------
    def menu_principal(self):
        """Menú principal completo"""
        import time
        
        while True:
            print("\n" + "=" * 60)
            print("🏬 SISTEMA DE GESTIÓN DE VENTAS - MENÚ PRINCIPAL")
            print("=" * 60)
            print("1. 📝 Escribir monto (individual)")
            print("2. 📦 Escribir montos (por lote)")
            print("3. 📊 Mostrar tabla completa")
            print("4. 🔍 Buscar ventas")
            print("5. 🗑️  Eliminar venta")
            print("6. 📂 Cargar datos de ejemplo")
            print("7. 🔄 Restaurar datos originales")
            print("8. 💾 Exportar datos a archivo")
            print("9. 🚪 Salir del sistema")
            print("=" * 60)
            
            try:
                opcion = input("\nSeleccione opción (1-9): ").strip()
                
                if opcion == "1":
                    self.escribir_monto_interactivo()
                
                elif opcion == "2":
                    print("\n📦 ESCRITURA POR LOTE")
                    print("Formato: mes,departamento,monto")
                    print("Ejemplo: Enero,Ropa,1500.50")
                    print("Deje línea vacía para terminar\n")
                    
                    lote = []
                    while True:
                        entrada = input("Dato: ").strip()
                        if not entrada:
                            break
                        
                        partes = entrada.split(',')
                        if len(partes) == 3:
                            lote.append((partes[0].strip(), partes[1].strip(), partes[2].strip()))
                        else:
                            print("❌ Formato incorrecto")
                    
                    if lote:
                        self.escribir_montos_por_lote(lote)
                
                elif opcion == "3":
                    self.mostrar_tabla_completa()
                
                elif opcion == "4":
                    self.buscar_ventas_interactivo()
                
                elif opcion == "5":
                    print("\n🗑️  ELIMINAR VENTAS")
                    print("1. Eliminar venta específica")
                    print("2. Eliminar por criterio (masivo)")
                    
                    sub_opcion = input("\nSeleccione (1-2): ").strip()
                    
                    if sub_opcion == "1":
                        self.eliminar_venta_interactivo()
                    elif sub_opcion == "2":
                        print("\n📊 CRITERIOS PARA ELIMINACIÓN MASIVA:")
                        print("1. Por mes")
                        print("2. Por departamento")
                        print("3. Mayores a un monto")
                        print("4. Menores a un monto")
                        
                        criterio_opc = input("\nSeleccione criterio (1-4): ").strip()
                        
                        criterios_map = {
                            '1': 'mes',
                            '2': 'departamento',
                            '3': 'mayor',
                            '4': 'menor'
                        }
                        
                        if criterio_opc in criterios_map:
                            valor = input(f"\nIngrese valor para '{criterios_map[criterio_opc]}': ").strip()
                            self.eliminar_ventas_por_criterio(criterios_map[criterio_opc], valor)
                        else:
                            print("❌ Opción inválida")
                    else:
                        print("❌ Opción inválida")
                
                elif opcion == "6":
                    print("\n📂 CONJUNTOS DE DATOS DE EJEMPLO:")
                    print("1. Completo (datos anuales completos)")
                    print("2. Básico (solo 3 meses)")
                    print("3. Estacional (ventas por temporada)")
                    print("4. Aleatorio (datos variados)")
                    
                    conjunto_opc = input("\nSeleccione conjunto (1-4): ").strip()
                    
                    conjuntos_map = {
                        '1': 'completo',
                        '2': 'basico',
                        '3': 'estacional',
                        '4': 'aleatorio'
                    }
                    
                    if conjunto_opc in conjuntos_map:
                        self.cargar_datos_ejemplo(conjuntos_map[conjunto_opc])
                    else:
                        print("❌ Opción inválida")
                
                elif opcion == "7":
                    self.restaurar_datos_originales()
                
                elif opcion == "8":
                    print("\n💾 EXPORTAR DATOS")
                    print("1. Exportar tabla completa")
                    print("2. Exportar resultados de búsqueda")
                    
                    export_opc = input("\nSeleccione (1-2): ").strip()
                    
                    if export_opc == "1":
                        self.exportar_tabla_completa()
                    elif export_opc == "2":
                        print("⚠️  Primero realice una búsqueda para exportar resultados")
                    else:
                        print("❌ Opción inválida")
                
                elif opcion == "9":
                    print("\n" + "=" * 60)
                    print("👋 ¡GRACIAS POR USAR EL SISTEMA DE GESTIÓN DE VENTAS!")
                    print("=" * 60)
                    break
                
                else:
                    print("\n❌ Opción inválida")
            
            except KeyboardInterrupt:
                print("\n\n⚠️ Programa interrumpido por el usuario")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    sistema = VentasDepartamentos()
    
    print("=" * 60)
    print("🏬 SISTEMA DE GESTIÓN DE VENTAS POR DEPARTAMENTO")
    print("=" * 60)
    print("📅 Meses: Enero a Diciembre")
    print("🏬 Departamentos: Ropa, Deportes, Juguetería")
    print("=" * 60)
    
    # Cargar datos de ejemplo automáticamente
    cargar_ejemplo = input("\n¿Cargar datos de ejemplo automáticamente? (s/n): ").strip().lower()
    if cargar_ejemplo == 's':
        sistema.cargar_datos_ejemplo('basico')
    
    # Ejecutar menú principal
    sistema.menu_principal()