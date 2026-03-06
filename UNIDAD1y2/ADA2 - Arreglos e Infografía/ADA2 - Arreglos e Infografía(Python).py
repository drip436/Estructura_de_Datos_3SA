"""
Programa de Gestión de Calificaciones con Matrices
Implementa una matriz bidimensional para gestionar calificaciones de alumnos y materias
"""

import random
import time

# ============================================================================
# CONFIGURACIÓN - Modifica estos valores para cambiar las dimensiones
# ============================================================================
NUM_ALUMNOS = 100000
NUM_MATERIAS = 100


# ============================================================================
# FUNCIÓN DE INICIALIZACIÓN
# ============================================================================

def crear_matriz(num_alumnos, num_materias):
    """
    Crea la matriz: Filas = Alumnos, Columnas = Materias
    Retorna una lista de listas donde matriz[alumno][materia] = calificación
    """
    matriz = []
    for alumno in range(num_alumnos):
        #random.randint(a, b): Genera un número entero aleatorio entre a y b (inclusive)
        fila = [random.randint(0, 100) for _ in range(num_materias)]
        matriz.append(fila)
    return matriz


# ============================================================================
# FUNCIÓN DE BÚSQUEDA
# ============================================================================

def buscar_calificacion(matriz, num_alumno, num_materia):
    """
    Busca la calificación en la matriz (Alumnos × Materias)
    num_alumno y num_materia están en base 1 (se convierten a base 0 internamente)
    """
    # Convertir de base 1 a base 0
    indice_alumno = num_alumno - 1
    indice_materia = num_materia - 1
    
    # Acceso: matriz[alumno][materia]
    return matriz[indice_alumno][indice_materia]


# ============================================================================
# FUNCIÓN DE VISUALIZACIÓN
# ============================================================================

def imprimir_matriz(matriz, num_alumnos, num_materias):
    """
    Imprime la matriz en formato de tabla
    Encabezados: Materias (columnas)
    Filas: Alumnos
    """
    print("\n" + "="*80)
    print("MATRIZ DE CALIFICACIONES: Filas = Alumnos, Columnas = Materias")
    print("="*80)
    
    # Imprimir encabezado con números de materia
    header = "Alumno     |"
    for i in range(num_materias):
        header += f" Materia{i+1} |"
    print(header)
    print("-" * len(header))
    
    # Imprimir cada fila (alumno)
    for alumno_idx in range(num_alumnos):
        fila = f"Alumno {alumno_idx+1:3d} |"
        for materia_idx in range(num_materias):
            calificacion = matriz[alumno_idx][materia_idx]
            fila += f"   {calificacion:3d}   |"
        print(fila)
    print("="*80 + "\n")


# ============================================================================
# FUNCIÓN DE MEDICIÓN DE TIEMPO
# ============================================================================

def medir_tiempo_busqueda(matriz, num_alumno, num_materia, repeticiones=100000):
    #Mide el tiempo de ejecución de búsquedas en la matriz usando benchmarking.
    """
    Mide el tiempo de búsqueda de una calificación
    Ejecuta múltiples repeticiones para obtener mediciones más precisas
    """
    print("\n" + "="*80)
    print("MEDICIÓN DE TIEMPO DE BÚSQUEDA")
    print("="*80)
    print(f"Buscando: Alumno {num_alumno}, Materia {num_materia}")
    print(f"Repeticiones: {repeticiones:,}")
    print("-"*80)
    
    # Medir tiempo de búsqueda
    """""
    time.perf_counter(): Devuelve el tiempo en segundos con la mayor precisión
    disponible en el sistema. Es ideal para medir pequeños intervalos de tiempo.
    """""
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        resultado = buscar_calificacion(matriz, num_alumno, num_materia)
    fin = time.perf_counter()
    tiempo_total = fin - inicio
    
    # Mostrar resultados
    # Calcular y mostrar tiempo promedio por búsqueda
    # Convertir a microsegundos para números más legibles
    # 1 segundo = 1,000,000 microsegundos
    print(f"Calificación encontrada: {resultado}")
    print(f"Tiempo total: {tiempo_total:.6f} segundos")
    print(f"Tiempo promedio por búsqueda: {(tiempo_total/repeticiones)*1000000:.2f} microsegundos")
    print("="*80 + "\n")


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    """
    Función principal que ejecuta todo el programa
    """
    print("\n")
    print("="*80)
    print(" SISTEMA DE GESTIÓN DE CALIFICACIONES")
    print("="*80)
    print(f"Configuración: {NUM_ALUMNOS} alumnos, {NUM_MATERIAS} materias")
    print("="*80)
    
    # ========================================================================
    # PASO 1: Crear la matriz
    # ========================================================================
    print("\n[1/3] Creando matriz de calificaciones...")
    inicio_creacion = time.perf_counter()
    matriz = crear_matriz(NUM_ALUMNOS, NUM_MATERIAS)
    fin_creacion = time.perf_counter()
    tiempo_creacion = fin_creacion - inicio_creacion

    # Confirmar que la matriz se creó exitosamente
    print(f"✓ Matriz creada: {NUM_ALUMNOS} alumnos × {NUM_MATERIAS} materias")
    print(f"✓ Tiempo de creación: {tiempo_creacion:.6f} segundos")
    
    # ========================================================================
    # PASO 2: Medir tiempo de búsqueda
    # ========================================================================
    print("\n[2/3] Midiendo tiempo de búsqueda...")
    medir_tiempo_busqueda(matriz, 321, 5)
    
    # ========================================================================
    # PASO 3: Visualizar la matriz completa
    # ========================================================================
    print("\n[3/3] Visualizando matriz completa...")
    imprimir_matriz(matriz, NUM_ALUMNOS, NUM_MATERIAS)
    
    # ========================================================================
    # INFORMACIÓN ADICIONAL
    # ========================================================================
    print("\n" + "="*80)
    print("INFORMACIÓN DE LA MATRIZ:")
    print("="*80)
    print(f"• Total de alumnos: {NUM_ALUMNOS}")
    print(f"• Total de materias: {NUM_MATERIAS}")
    print(f"• Total de calificaciones almacenadas: {NUM_ALUMNOS * NUM_MATERIAS}")
    print(f"• Rango de calificaciones: [0, 100]")
    print(f"• Estructura: Filas = Alumnos, Columnas = Materias")
    print("="*80)
    
    # Ejemplo de búsquedas adicionales
    print("\nEJEMPLOS DE BÚSQUEDA:")
    print("-"*80)
    ejemplos = [(1, 1), (100, 3), (321, 5), (500, 6)]
    for alumno, materia in ejemplos:
        cal = buscar_calificacion(matriz, alumno, materia)
        # Mostrar el resultado formateado
        # :3d alinea los números para mejor visualización
        print(f"Alumno {alumno:3d}, Materia {materia}: {cal:3d}")
    print("="*80 + "\n")


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    main()