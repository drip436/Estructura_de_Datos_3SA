Sistema de Gestión de Ventas por Departamento
📋Descripción General
Sistema de gestión de ventas que permite administrar, consultar y analizar las ventas mensuales de tres departamentos (Ropa, Deportes y Juguetería) a lo largo de un año. Implementado tanto en Python como en Java, el sistema ofrece una interfaz de línea de comandos completa con múltiples funcionalidades.

Estructura del Proyecto
Implementación Python
text
VentasDepartamentos.py
├── Clase VentasDepartamentos
│   ├── __init__() - Inicializa matriz 12x3 de ventas
│   ├── buscar_ventas() - Búsqueda con múltiples criterios
│   ├── eliminar_venta() - Eliminación individual/masiva
│   ├── cargar_datos_ejemplo() - Carga datos predefinidos
│   ├── menu_principal() - Interfaz de usuario
│   └── Métodos auxiliares
└── Ejecución principal
Implementación Java
text
VentasDepartamentos.java
├── Clase principal VentasDepartamentos
│   ├── Constructor - Inicializa matriz 12x3
│   ├── buscarVentas() - Búsqueda con múltiples criterios
│   ├── eliminarVenta() - Eliminación individual/masiva
│   ├── cargarDatosEjemplo() - Carga datos predefinidos
│   ├── menuPrincipal() - Interfaz de usuario
│   └── Métodos auxiliares
├── Clase interna VentaResultado
└── Método main()

Estructura de Datos
Matriz de Ventas
Filas: 12 meses (Enero a Diciembre)

Columnas: 3 departamentos (Ropa, Deportes, Juguetería)

Tipo de dato: Float/Double (valores monetarios)

Datos de Ejemplo Predefinidos:

Conjunto	    Descripción	Ventas Incluidas
Completo	    Datos anuales completos	        36 ventas (todos los meses)
Básico	        Datos mínimos para prueba	    3 ventas (Ene, Feb, Mar)
Estacional	    Ventas por temporada	        8 ventas (alta/media/baja)
Aleatorio	    Datos variados para pruebas	    6 ventas distribuidas

Funcionalidades Comunes
1. Registro de Ventas
Individual: Registro una venta específica por mes y departamento

Por lote: Carga múltiples ventas con formato CSV (mes,departamento,monto)

2.. Sistema de Búsqueda
Criterio	                Descripción	                        Ejemplo
Por mes	            Ventas de un mes específico	                "Enero"
Por departamento	Ventas de un departamento	                "Ropa"
Monto exacto	    Ventas con monto específico	               "1500.50"
Rango	            Ventas entre dos montos	                  "1000-2000"
Mayor que	          Ventas mayores a un valor             	">1000"
Menor que	          Ventas menores a un valor	                "<500"
Todas	            Todas las ventas registradas	               -

3. Eliminación de Datos
Individual: Elimina una venta específica

Masiva: Elimina por criterio (mes, departamento, monto)

Confirmación: Solicita confirmación antes de eliminar

4. Gestión de Datos
Carga automática: 4 conjuntos de datos de ejemplo

Restauración: Recupera datos originales

Exportación: Guarda resultados en archivos de texto

5. Visualización
Tabla completa: Muestra todas las ventas con totales

Formato monetario: Valores formateados con separadores

Resúmenes: Totales por mes y departamento

Instrucciones de Ejecución
Versión Python
bash
# Requisito: Python 3.6+
python VentasDepartamentos.py
Versión Java
bash
# Requisito: Java 8+
javac VentasDepartamentos.java
java VentasDepartamentos

Guía de Uso Rápida
Primeros Pasos
Iniciar sistema: Ejecutar el programa

Cargar datos: Seleccionar opción 6 → Cargar datos de ejemplo

Explorar: Usar opción 3 para ver tabla completa

Buscar: Usar opción 4 para búsquedas específicas

Ejemplos de Comandos
Búsqueda por Mes
text
Seleccione criterio (1-8): 1
Ingrese nombre o número del mes: Enero
Eliminación Masiva
text
Seleccione opción (1-9): 5
1. Eliminar venta específica
2. Eliminar por criterio (masivo)
Seleccione (1-2): 2
Ingrese criterio: 3 (Mayores a un monto)
Ingrese valor: 10000
Exportación de Datos
text
¿Exportar resultados a archivo? (s/n): s
# Se crea archivo "resultados_busqueda.txt"
Formatos de Archivo
Exportación de Resultados
text
============================================================
RESULTADOS DE BÚSQUEDA DE VENTAS
Fecha: 2024-01-15 14:30:00
Total de ventas encontradas: 5
============================================================

MES          DEPARTAMENTO MONTO
------------------------------------------------------------
Enero        Ropa         $12,500.00
Febrero      Deportes     $10,500.00
...
------------------------------------------------------------
TOTAL                     $45,200.00
============================================================
Formato de Lote
text
Enero,Ropa,12500
Febrero,Deportes,10500
Marzo,Juguetería,8900


Diferencias entre Implementaciones
Python (Ventajas)
Manejo dinámico: Tipado dinámico facilita manipulación de datos

Sintaxis concisa: Código más corto y legible

Módulo time: Integración nativa para timestamps

Diccionarios: Estructuras de datos flexibles para resultados

Java (Ventajas)
Tipado estático: Mayor seguridad en tiempo de compilación

POO puro: Mejor estructura orientada a objetos

Manejo de excepciones: Sistema robusto de errores

Performance: Generalmente más rápido en ejecución

Características Específicas
Python
python
# Manejo flexible de tipos
resultados.append({
    'mes': mes,
    'departamento': dept,
    'monto': self.ventas[i][j],
    'indices': (i, j)
})

# Decoradores y métodos mágicos disponibles
# Manejo de archivos con context manager
Java
java
// Clase interna para resultados tipados
private class VentaResultado {
    String mes;
    String departamento;
    double monto;
    int[] indices;
}

// Manejo de recursos con try-with-resources
try (BufferedWriter writer = new BufferedWriter(new FileWriter(nombreArchivo))) {
    // Código de escritura
}
🛠️ Métodos Principales
Método buscar_ventas() / buscarVentas()
Parámetros:

criterio_busqueda: Tipo de búsqueda (mes, departamento, monto, etc.)

valor: Valor específico para el criterio

valor2 (solo Java): Segundo valor para rangos

Retorno:

Python: Lista de diccionarios

Java: List<VentaResultado>

Método eliminar_venta() / eliminarVenta()
Parámetros:

mes: Nombre o número del mes (1-12)

departamento: Nombre o número del departamento (1-3)

confirmar: Solicitar confirmación (True/False)

Método cargar_datos_ejemplo() / cargarDatosEjemplo()
Conjuntos disponibles:

completo: 36 ventas (todo el año)

basico: 3 ventas (prueba rápida)

estacional: 8 ventas (por temporadas)

aleatorio: 6 ventas (distribuidas)

⚠️ Manejo de Errores
Errores Comunes y Soluciones
Error	                                Causa	                            Solución
"Mes no válido"     	            Nombre mal escrito	                Usar nombres exactos o números 1-12
"Departamento no válido"	        Departamento incorrecto	            Usar "Ropa", "Deportes" o "Juguetería"
"Monto debe ser número"	            Formato incorrecto	                Usar números con punto decimal
"Fuera de rango"	                Números fuera de límites	        Meses: 1-12, Departamentos: 1-3


Validaciones Implementadas
Rangos numéricos: Verificación de meses (1-12) y departamentos (1-3)

Formatos monetarios: Validación de números decimales positivos

Existencia de datos: Verificación antes de eliminar

Confirmaciones: Pregunta antes de operaciones destructivas

Ejemplo de Flujo de Trabajo
Caso de Uso: Análisis Mensual
text
1. Cargar datos de ejemplo "completo"
2. Buscar ventas de "Diciembre"
3. Exportar resultados a "ventas_diciembre.txt"
4. Eliminar ventas menores a $10,000
5. Ver tabla actualizada
Caso de Uso: Limpieza de Datos
text
1. Cargar datos existentes
2. Buscar ventas por departamento "Juguetería"
3. Eliminar todas las ventas encontradas
4. Restaurar datos originales si es necesario
🔄 Comparación de Sintaxis
Creación de Matriz
python
# Python
self.ventas = [[0.0 for _ in range(3)] for _ in range(12)]
java
// Java
ventas = new double[12][3];
Búsqueda por Mes
python
# Python
if criterio_busqueda == 'mes':
    mes_idx = self.meses.index(valor)
java
// Java
if (criterioBusqueda.equals("mes")) {
    for (int i = 0; i < meses.length; i++) {
        if (meses[i].equalsIgnoreCase(valor)) {
            mesIdx = i;
            break;
        }
    }
}
Formato de Salida
python
# Python
print(f"{venta['mes']:<12} {venta['departamento']:<12} ${venta['monto']:<14,.2f}")
java
// Java
System.out.printf("%-12s %-12s $%-14,.2f\n", 
    venta.mes, venta.departamento, venta.monto);
🎯 Mejores Prácticas Implementadas
Python
Docstrings: Documentación completa de métodos

Manejo de excepciones: Try-except específicos

List comprehensions: Código más eficiente

Context managers: Manejo seguro de archivos

Java
Encapsulamiento: Atributos privados con métodos públicos

Tipado fuerte: Mayor seguridad en tiempo de compilación

Try-with-resources: Manejo automático de recursos

Formateo consistente: Uso de printf para salida

📚 Recursos Adicionales
Para la Versión Python
Módulos utilizados: time para timestamps

Estructuras de datos: Listas, diccionarios, tuplas

Características: F-strings, unpacking, métodos mágicos

Para la Versión Java
Paquetes utilizados: java.io, java.time, java.util

Estructuras de datos: ArrayList, HashMap, arrays

Características: Clases internas, formateo con String.format

🤝 Contribución
Mejoras Posibles
Interfaz gráfica: Versión con GUI usando Tkinter (Python) o Swing (Java)

Base de datos: Migración a SQLite o MySQL

Reportes PDF: Exportación a formatos PDF

API REST: Versión web con Flask (Python) o Spring (Java)

Análisis estadístico: Gráficos y tendencias

Estructura de Código
text
Ambas implementaciones siguen:
- Convenciones de nomenclatura del lenguaje
- Documentación en línea
- Modularidad y reusabilidad
- Manejo apropiado de errores

Licencia
Este proyecto es educativo y puede ser usado, modificado y distribuido libremente para fines de aprendizaje y enseñanza.

Nota: Ambos códigos son funcionalmente equivalentes pero aprovechan las características idiomáticas de cada lenguaje. Se recomienda elegir la implementación según el entorno de desarrollo y los requisitos específicos del proyecto.