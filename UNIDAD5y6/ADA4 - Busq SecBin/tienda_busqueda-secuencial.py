# Importamos todas las funciones de tu librería
import libreria_secuencial as bs

# --- NUESTRO BANCO DE DATOS (Simulación de la Tienda) ---
# Una lista de diccionarios que representa el inventario actual
inventario = [
    {"id": "PROD01", "nombre": "Laptop ASUS", "categoria": "Computo", "precio": 850.00, "stock": 12},
    {"id": "PROD02", "nombre": "Mouse Logi", "categoria": "Accesorios", "precio": 25.50, "stock": 45},
    {"id": "PROD03", "nombre": "Monitor Dell", "categoria": "Computo", "precio": 200.00, "stock": 8},
    {"id": "PROD04", "nombre": "Teclado Mecánico", "categoria": "Accesorios", "precio": 75.00, "stock": 0}, # Sin stock
    {"id": "PROD05", "nombre": "Audífonos Sony", "categoria": "Audio", "precio": 150.00, "stock": 20},
    {"id": "PROD06", "nombre": "Mouse Razer", "categoria": "Accesorios", "precio": 60.00, "stock": 15},
    {"id": "PROD07", "nombre": "Laptop HP", "categoria": "Computo", "precio": 700.00, "stock": 5},
]

# Una lista simple para búsquedas rápidas de códigos de barras / IDs de pasillo
codigos_rapidos = ["PROD01", "PROD02", "PROD03", "PROD04", "PROD05", "PROD06", "PROD07"]


# --- DEMOSTRACIÓN DEL SISTEMA DE GESTIÓN ---
def ejecutar_sistema_tienda():
    print("=" * 60)
    print("         SISTEMA DE GESTIÓN DE TIENDA ELECTRÓNICA       ")
    print("=" * 60)

    # -------------------------------------------------------------------------
    # Caso 1: Uso de `contiene`
    # El cajero escanea un código rápido para ver si el producto pertenece a esta sucursal
    # -------------------------------------------------------------------------
    codigo_a_revisar = "PROD05"
    print(f"\n🔍 [1. Contiene] ¿El código {codigo_a_revisar} pertenece a este pasillo?")
    
    if bs.contiene(codigos_rapidos, codigo_a_revisar):
        print(f"   🟢 Sí, el producto {codigo_a_revisar} está registrado en este sector.")
    else:
        print(f"   🔴 No se encontró el código {codigo_a_revisar}.")


    # -------------------------------------------------------------------------
    # Caso 2: Uso de `buscar`
    # Queremos saber en qué posición física de la estantería (índice) está un código
    # -------------------------------------------------------------------------
    codigo_buscar = "PROD03"
    print(f"\n🔍 [2. Buscar] Localizando el índice en estante para: {codigo_buscar}")
    
    indice = bs.buscar(codigos_rapidos, codigo_buscar)
    if indice != -1:
        print(f"   📍 Encontrado en el Compartimiento/Índice: {indice}")
        print(f"   📦 Datos del producto: {inventario[indice]['nombre']} - ${inventario[indice]['precio']}")
    else:
        print("   ❌ El producto no existe en el inventario.")


    # -------------------------------------------------------------------------
    # Caso 3: Uso de `buscar_con_condicion` (Uso de lambdas/funciones)
    # El cliente tiene un presupuesto máximo y busca la PRIMERA laptop que le alcance
    # -------------------------------------------------------------------------
    presupuesto = 800.00
    print(f"\n🔍 [3. Buscar con Condición] Buscando la primera Laptop de menos de ${presupuesto}:")
    
    # Pasamos una función lambda que evalúa cada diccionario del inventario
    condicion_cliente = lambda prod: prod["categoria"] == "Computo" and prod["precio"] <= presupuesto
    
    idx_encontrado, producto = bs.buscar_con_condicion(inventario, condicion_cliente)
    
    if idx_encontrado != -1:
        print(f"   💡 Opción ideal encontrada (Índice {idx_encontrado}):")
        print(f"      - Modelo: {producto['nombre']}")
        print(f"      - Precio: ${producto['precio']} (¡Ahorra ${presupuesto - producto['precio']}!)")
    else:
        print(f"   ❌ No hay ninguna laptop que cueste menos o igual a ${presupuesto}.")


    # -------------------------------------------------------------------------
    # Caso 4: Uso de `buscar_todos`
    # El gerente quiere hacer una auditoría de todos los productos de la categoría 'Accesorios'
    # -------------------------------------------------------------------------
    categoria_auditar = "Accesorios"
    print(f"\n🔍 [4. Buscar Todos] Extrayendo todos los productos de la categoría: '{categoria_auditar}'")
    
    # Para usar tu función tal cual, primero extraemos las categorías en una lista simple
    lista_categorias = [prod["categoria"] for prod in inventario]
    
    indices_accesorios = bs.buscar_todos(lista_categorias, categoria_auditar)
    
    print(f"   📊 Se encontraron {len(indices_accesorios)} productos en esa categoría (Índices: {indices_accesorios}):")
    for idx in indices_accesorios:
        prod = inventario[idx]
        print(f"      • [{prod['id']}] {prod['nombre']} - Stock: {prod['stock']} unidades.")


    # -------------------------------------------------------------------------
    # Caso 5: Uso de `buscar_rango`
    # Supongamos que el inventario se divide por pasillos: 
    # Pasillo A (Índices 0 a 3), Pasillo B (Índices 4 a fin).
    # Queremos buscar el código "PROD06" únicamente en el Pasillo B.
    # -------------------------------------------------------------------------
    codigo_critico = "PROD06"
    print(f"\n🔍 [5. Buscar Rango] Buscando {codigo_critico} exclusivamente en el Pasillo B (Índices 4 al 7):")
    
    idx_rango = bs.buscar_rango(codigos_rapidos, codigo_critico, inicio=4, fin=7)
    
    if idx_rango != -1:
        print(f"   🟢 Encontrado con éxito en el rango seleccionado. Índice global: {idx_rango}")
        print(f"      Producto: {inventario[idx_rango]['nombre']}")
    else:
        print(f"   ❌ El producto {codigo_critico} no se encuentra en ese pasillo.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    ejecutar_sistema_tienda()