Sistema de Gestión de Calificaciones con Matrices
Descripción
Sistema de gestión de calificaciones que implementa una matriz bidimensional para almacenar y manipular calificaciones de alumnos y materias. El programa incluye funcionalidades de creación, búsqueda, visualización y medición de rendimiento.

///////////////////////////////////////////////////////
Características Principales
Funcionalidades Implementadas
- Creación de matriz bidimensional de calificaciones

- Búsqueda rápida de calificaciones por alumno y materia

- Visualización completa de la matriz en formato tabla

- Medición precisa de tiempos de ejecución

- Configuración flexible de dimensiones

- Generación de datos aleatorios para pruebas

- Dimensiones por Defecto
100,000 alumnos × 100 materias = 10 millones de calificaciones

////////////////////////////////////////////////////////

Rango de calificaciones: 0 a 100 puntos

Instalación y Ejecución
Requisitos
Python 3.6 o superior

Módulos estándar: random, time

Ejecución Directa
bash
# Clonar o copiar el archivo
python gestion_calificaciones.py
Modificar Dimensiones
Edita las variables de configuración al inicio del archivo:

python
NUM_ALUMNOS = 50000    # Cambiar número de alumnos
NUM_MATERIAS = 50      # Cambiar número de materias

/////Estructura del Programa/////
1. Configuración
python
NUM_ALUMNOS = 100000   # Número de alumnos (filas)
NUM_MATERIAS = 100     # Número de materias (columnas)

2. Funciones Principales
crear_matriz(num_alumnos, num_materias)
Crea una matriz de calificaciones aleatorias.

Parámetros: Número de alumnos y materias

Retorno: Matriz bidimensional (lista de listas)

Complejidad: O(n×m) donde n=alumnos, m=materias

buscar_calificacion(matriz, num_alumno, num_materia)
Busca una calificación específica.

Índices: Usan base 1 (Alumno 1, Materia 1 = [0][0])

Acceso directo: O(1) tiempo constante

Validación: Conversión automática a índices base 0

imprimir_matriz(matriz, num_alumnos, num_materias)
Visualiza la matriz completa.

Formato: Tabla con encabezados

Alineación: Números alineados para mejor legibilidad

Limitación: Recomendado solo para matrices pequeñas

medir_tiempo_busqueda(matriz, num_alumno, num_materia, repeticiones)
Realiza benchmarking de búsquedas.

Precisión: Usa time.perf_counter() para microsegundos

Repeticiones: 100,000 por defecto para estadísticas confiables

Resultados: Tiempo total y promedio por operación

3. Flujo del Programa
text
main()
├── Crear matriz (10M calificaciones)
├── Medir tiempo de búsqueda
├── Visualizar muestra de la matriz
└── Mostrar información y ejemplos


/////Ejemplos de Uso/////
Ejecución Básica
python
# Buscar calificación del alumno 321 en materia 5
calificacion = buscar_calificacion(matriz, 321, 5)
print(f"Calificación: {calificacion}")
Benchmarking
python
# Medir rendimiento de búsqueda
medir_tiempo_busqueda(matriz, 321, 5, repeticiones=100000)

# Salida esperada:
# Tiempo promedio por búsqueda: 0.15 microsegundos
Visualización Parcial
python
# Ver primeras 10 filas y 5 columnas
matriz_pequena = [fila[:5] for fila in matriz[:10]]
imprimir_matriz(matriz_pequena, 10, 5)


/////Rendimiento y Optimización////
Tiempos de Ejecución Típicos
Operación	                         Tiempo	                             Notas
Creación de matriz	              ~1.5 segundos                 	10M elementos
Búsqueda individual	                ~0.15 µs	                        Acceso O(1)
100,000 búsquedas	            ~0.015 segundos	                        Benchmarking


Optimizaciones Implementadas
Acceso directo por índices: O(1) tiempo constante

List comprehensions: Creación eficiente de matrices

Medición precisa: time.perf_counter() para benchmarking

Conversión eficiente: Índices base 1 a base 0

Consideraciones de Memoria
text
Cálculo de uso de memoria:
100,000 alumnos × 100 materias = 10,000,000 elementos
Cada entero Python: ~28 bytes
Memoria estimada: ~280 MB


////Análisis de Complejidad/////
Complejidad Temporal
Función	                        Complejidad	D                               escripción
crear_matriz()	                    O(n×m)	                        Lineal con tamaño de matriz
buscar_calificacion()	             O(1)	                        Acceso directo por índice
imprimir_matriz()	                O(n×m)	                        Recorre toda la matriz
medir_tiempo_busqueda()            	O(k)	                        k = número de repeticiones


Complejidad Espacial
Función	                Complejidad	                Descripción
crear_matriz()	            O(n×m)	                Almacena toda la matriz
Otras funciones	             O(1)	                Uso constante de memoria adicional


Personalización y Extensión
Modificar Rango de Calificaciones
python
# En la función crear_matriz, línea 22:
fila = [random.randint(0, 100) for _ in range(num_materias)]
# Cambiar a:
fila = [random.randint(60, 100) for _ in range(num_materias)]  # Solo aprobados
Añadir Funcionalidades
python
def promedio_alumno(matriz, num_alumno):
    """Calcula el promedio de un alumno"""
    indice = num_alumno - 1
    calificaciones = matriz[indice]
    return sum(calificaciones) / len(calificaciones)

def promedio_materia(matriz, num_materia):
    """Calcula el promedio de una materia"""
    indice = num_materia - 1
    total = sum(fila[indice] for fila in matriz)
    return total / len(matriz)


////Casos de Uso/////
Educativo
Enseñanza de estructuras de datos bidimensionales

Demostración de complejidades algorítmicas

Ejemplos de acceso aleatorio vs secuencial

Pruebas de Rendimiento
Benchmarking de operaciones de matriz

Comparación de estructuras de datos

Análisis de uso de memoria

Prototipado
Base para sistemas de calificaciones reales

Prueba de conceptos para bases de datos

///Modelado de datos tabulares///

Limitaciones y Consideraciones
Limitaciones Conocidas
Memoria: Matrices grandes consumen mucha RAM

Visualización: imprimir_matriz() es solo para muestras pequeñas

Persistencia: Datos en memoria, no se guardan en disco

Recomendaciones
Para >1 millón de elementos, considerar bases de datos

Usar numpy para operaciones matemáticas intensivas

Implementar paginación para visualización de grandes conjuntos

Flujo de Trabajo Recomendado
Para Desarrollo
python
# 1. Configurar dimensiones pequeñas para pruebas
NUM_ALUMNOS = 100
NUM_MATERIAS = 10

# 2. Probar funcionalidades
matriz = crear_matriz(NUM_ALUMNOS, NUM_MATERIAS)
print(buscar_calificacion(matriz, 1, 1))

# 3. Escalar progresivamente
Para Producción
Implementar persistencia (archivos/DB)

Añadir validación de entradas

Incluir manejo de errores

Optimizar para conjuntos de datos específicos

Recursos Relacionados
Conceptos Teóricos
Matrices bidimensionales

Acceso aleatorio vs secuencial

Complejidad algorítmica (O(1), O(n))

Benchmarking y profiling

Extensiones Posibles
Interfaz gráfica con Tkinter

Exportación a CSV/Excel

Integración con bases de datos SQL

Análisis estadístico de calificaciones

/////Aprendizajes Clave////
Para Estudiantes
Estructuras de datos bidimensionales

Indexación base 0 vs base 1

Medición de rendimiento de algoritmos

Generación de datos de prueba

Para Desarrolladores
Optimización de acceso a matrices

Técnicas de benchmarking en Python

Manejo de grandes conjuntos de datos en memoria

Buenas prácticas de documentación de código

/////Contribución////
Mejoras Sugeridas
Persistencia: Guardar/recuperar de archivos

Interfaz: Añadir menú interactivo

Análisis: Funciones estadísticas

Visualización: Gráficos de distribución

////Reportar Problemas/////
Describir el error específico

Incluir configuración del sistema

Proporcionar pasos para reproducir

Sugerir posibles soluciones

///Licencia///
Código educativo de uso libre. Atribución recomendada pero no requerida.

Nota: Este programa es principalmente educativo. Para sistemas de calificaciones en producción, se recomienda usar bases de datos especializadas y considerar aspectos como seguridad, concurrencia y respaldos.