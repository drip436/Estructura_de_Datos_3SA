import java.io.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

public class VentasDepartamentos {
    
    private String[] meses = {
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    };
    
    private String[] departamentos = {"Ropa", "Deportes", "Juguetería"};
    private double[][] ventas;
    private double[][] datosOriginales;
    private Scanner scanner;
    
    // Clase interna para representar una venta encontrada
    private class VentaResultado {
        String mes;
        String departamento;
        double monto;
        int[] indices;
        
        VentaResultado(String mes, String departamento, double monto, int i, int j) {
            this.mes = mes;
            this.departamento = departamento;
            this.monto = monto;
            this.indices = new int[]{i, j};
        }
    }
    
    public VentasDepartamentos() {
        ventas = new double[12][3];
        scanner = new Scanner(System.in);
    }
    
    // -----------------------------------------------------------------
    // 4. MÉTODO PARA BUSCAR VENTAS
    // -----------------------------------------------------------------
    public List<VentaResultado> buscarVentas(String criterioBusqueda, String valor) {
        return buscarVentas(criterioBusqueda, valor, null);
    }
    
    public List<VentaResultado> buscarVentas(String criterioBusqueda, String valor, String valor2) {
        try {
            List<VentaResultado> resultados = new ArrayList<>();
            
            if (criterioBusqueda == null) {
                // Buscar todas las ventas (distintas de 0)
                System.out.println("BUSCANDO TODAS LAS VENTAS REGISTRADAS...");
                for (int i = 0; i < meses.length; i++) {
                    for (int j = 0; j < departamentos.length; j++) {
                        if (ventas[i][j] > 0) {
                            resultados.add(new VentaResultado(meses[i], departamentos[j], ventas[i][j], i, j));
                        }
                    }
                }
                return resultados;
            }
            
            criterioBusqueda = criterioBusqueda.toLowerCase();
            
            if (criterioBusqueda.equals("mes")) {
                // Buscar por mes específico
                int mesIdx = -1;
                for (int i = 0; i < meses.length; i++) {
                    if (meses[i].equalsIgnoreCase(valor)) {
                        mesIdx = i;
                        break;
                    }
                }
                
                if (mesIdx == -1) {
                    System.out.println("❌ Error: Mes '" + valor + "' no válido");
                    return resultados;
                }
                
                System.out.println("🔍 BUSCANDO VENTAS EN " + valor.toUpperCase() + "...");
                
                for (int j = 0; j < departamentos.length; j++) {
                    if (ventas[mesIdx][j] > 0) {
                        resultados.add(new VentaResultado(valor, departamentos[j], ventas[mesIdx][j], mesIdx, j));
                    }
                }
            }
            else if (criterioBusqueda.equals("departamento")) {
                // Buscar por departamento específico
                int deptIdx = -1;
                for (int i = 0; i < departamentos.length; i++) {
                    if (departamentos[i].equalsIgnoreCase(valor)) {
                        deptIdx = i;
                        break;
                    }
                }
                
                if (deptIdx == -1) {
                    System.out.println("❌ Error: Departamento '" + valor + "' no válido");
                    return resultados;
                }
                
                System.out.println("🔍 BUSCANDO VENTAS EN " + valor.toUpperCase() + "...");
                
                for (int i = 0; i < meses.length; i++) {
                    if (ventas[i][deptIdx] > 0) {
                        resultados.add(new VentaResultado(meses[i], valor, ventas[i][deptIdx], i, deptIdx));
                    }
                }
            }
            else if (criterioBusqueda.equals("monto")) {
                // Buscar por monto exacto
                try {
                    double montoBuscar = Double.parseDouble(valor);
                    System.out.printf("🔍 BUSCANDO VENTAS CON MONTO EXACTO $%,.2f...\n", montoBuscar);
                    
                    for (int i = 0; i < meses.length; i++) {
                        for (int j = 0; j < departamentos.length; j++) {
                            if (Math.abs(ventas[i][j] - montoBuscar) < 0.01) {
                                resultados.add(new VentaResultado(meses[i], departamentos[j], ventas[i][j], i, j));
                            }
                        }
                    }
                } catch (NumberFormatException e) {
                    System.out.println("❌ Error: El monto debe ser un número válido");
                    return resultados;
                }
            }
            else if (criterioBusqueda.equals("rango")) {
                // Buscar por rango de montos
                try {
                    double minMonto = Double.parseDouble(valor);
                    double maxMonto = Double.parseDouble(valor2);
                    
                    System.out.printf("🔍 BUSCANDO VENTAS ENTRE $%,.2f Y $%,.2f...\n", minMonto, maxMonto);
                    
                    for (int i = 0; i < meses.length; i++) {
                        for (int j = 0; j < departamentos.length; j++) {
                            if (minMonto <= ventas[i][j] && ventas[i][j] <= maxMonto) {
                                resultados.add(new VentaResultado(meses[i], departamentos[j], ventas[i][j], i, j));
                            }
                        }
                    }
                } catch (NumberFormatException e) {
                    System.out.println("❌ Error: Los valores del rango deben ser números");
                    return resultados;
                }
            }
            else if (criterioBusqueda.equals("mayor")) {
                // Buscar ventas mayores a un valor
                try {
                    double montoMin = Double.parseDouble(valor);
                    System.out.printf("🔍 BUSCANDO VENTAS MAYORES A $%,.2f...\n", montoMin);
                    
                    for (int i = 0; i < meses.length; i++) {
                        for (int j = 0; j < departamentos.length; j++) {
                            if (ventas[i][j] > montoMin) {
                                resultados.add(new VentaResultado(meses[i], departamentos[j], ventas[i][j], i, j));
                            }
                        }
                    }
                } catch (NumberFormatException e) {
                    System.out.println("❌ Error: El monto debe ser un número válido");
                    return resultados;
                }
            }
            else if (criterioBusqueda.equals("menor")) {
                // Buscar ventas menores a un valor
                try {
                    double montoMax = Double.parseDouble(valor);
                    System.out.printf("🔍 BUSCANDO VENTAS MENORES A $%,.2f...\n", montoMax);
                    
                    for (int i = 0; i < meses.length; i++) {
                        for (int j = 0; j < departamentos.length; j++) {
                            if (ventas[i][j] > 0 && ventas[i][j] < montoMax) {
                                resultados.add(new VentaResultado(meses[i], departamentos[j], ventas[i][j], i, j));
                            }
                        }
                    }
                } catch (NumberFormatException e) {
                    System.out.println("❌ Error: El monto debe ser un número válido");
                    return resultados;
                }
            }
            else {
                System.out.println("❌ Error: Criterio de búsqueda no válido");
                return resultados;
            }
            
            return resultados;
            
        } catch (Exception e) {
            System.out.println("❌ Error en búsqueda: " + e.getMessage());
            return new ArrayList<>();
        }
    }
    
    public void buscarVentasInteractivo() {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("🔍 BUSQUEDA DE VENTAS - MODO INTERACTIVO");
        System.out.println("=".repeat(60));
        
        while (true) {
            System.out.println("\n📊 CRITERIOS DE BÚSQUEDA DISPONIBLES:");
            System.out.println("1. Por mes específico");
            System.out.println("2. Por departamento específico");
            System.out.println("3. Por monto exacto");
            System.out.println("4. Por rango de montos");
            System.out.println("5. Mayores a un monto");
            System.out.println("6. Menores a un monto");
            System.out.println("7. Todas las ventas registradas");
            System.out.println("8. Volver al menú principal");
            
            try {
                System.out.print("\nSeleccione criterio (1-8): ");
                String opcion = scanner.nextLine().trim();
                
                if (opcion.equals("8")) {
                    System.out.println("\n👋 Regresando al menú principal...");
                    break;
                }
                
                List<VentaResultado> resultados = new ArrayList<>();
                
                switch (opcion) {
                    case "1":
                        System.out.println("\n📅 MESES DISPONIBLES:");
                        for (int i = 0; i < meses.length; i++) {
                            System.out.printf("  %2d. %s\n", i + 1, meses[i]);
                        }
                        
                        System.out.print("\nIngrese nombre o número del mes: ");
                        String entrada = scanner.nextLine().trim();
                        String mes;
                        
                        if (entrada.matches("\\d+") && Integer.parseInt(entrada) >= 1 && Integer.parseInt(entrada) <= 12) {
                            mes = meses[Integer.parseInt(entrada) - 1];
                        } else {
                            mes = entrada.substring(0, 1).toUpperCase() + entrada.substring(1).toLowerCase();
                        }
                        
                        resultados = buscarVentas("mes", mes);
                        break;
                        
                    case "2":
                        System.out.println("\n🏬 DEPARTAMENTOS DISPONIBLES:");
                        for (int i = 0; i < departamentos.length; i++) {
                            System.out.printf("  %d. %s\n", i + 1, departamentos[i]);
                        }
                        
                        System.out.print("\nIngrese nombre o número del departamento: ");
                        entrada = scanner.nextLine().trim();
                        String departamento;
                        
                        if (entrada.matches("\\d+") && Integer.parseInt(entrada) >= 1 && Integer.parseInt(entrada) <= 3) {
                            departamento = departamentos[Integer.parseInt(entrada) - 1];
                        } else {
                            departamento = entrada.substring(0, 1).toUpperCase() + entrada.substring(1).toLowerCase();
                        }
                        
                        resultados = buscarVentas("departamento", departamento);
                        break;
                        
                    case "3":
                        System.out.print("\nIngrese el monto exacto a buscar: $");
                        String monto = scanner.nextLine().trim();
                        resultados = buscarVentas("monto", monto);
                        break;
                        
                    case "4":
                        System.out.println("\n📈 BUSCAR POR RANGO DE MONTOS");
                        System.out.print("Monto mínimo: $");
                        String minMonto = scanner.nextLine().trim();
                        System.out.print("Monto máximo: $");
                        String maxMonto = scanner.nextLine().trim();
                        resultados = buscarVentas("rango", minMonto, maxMonto);
                        break;
                        
                    case "5":
                        System.out.print("\nIngrese monto mínimo: $");
                        monto = scanner.nextLine().trim();
                        resultados = buscarVentas("mayor", monto);
                        break;
                        
                    case "6":
                        System.out.print("\nIngrese monto máximo: $");
                        monto = scanner.nextLine().trim();
                        resultados = buscarVentas("menor", monto);
                        break;
                        
                    case "7":
                        resultados = buscarVentas(null, null);
                        break;
                        
                    default:
                        System.out.println("❌ Opción inválida");
                        continue;
                }
                
                // Mostrar resultados
                if (!resultados.isEmpty()) {
                    System.out.printf("\n✅ ENCONTRADAS %d VENTAS:\n", resultados.size());
                    System.out.println("-".repeat(60));
                    System.out.printf("%-12s %-12s %-15s\n", "MES", "DEPARTAMENTO", "MONTO");
                    System.out.println("-".repeat(60));
                    
                    double total = 0;
                    for (VentaResultado venta : resultados) {
                        System.out.printf("%-12s %-12s $%-14,.2f\n", 
                                venta.mes, venta.departamento, venta.monto);
                        total += venta.monto;
                    }
                    
                    System.out.println("-".repeat(60));
                    System.out.printf("%-24s $%,.2f\n", "TOTAL", total);
                    System.out.println("=".repeat(60));
                    
                    // Exportar opciones
                    System.out.print("\n¿Exportar resultados a archivo? (s/n): ");
                    String exportar = scanner.nextLine().trim().toLowerCase();
                    if (exportar.equals("s")) {
                        exportarResultados(resultados, "resultados_busqueda.txt");
                    }
                } else {
                    System.out.println("\n❌ No se encontraron ventas con los criterios especificados");
                }
                
                // Preguntar por otra búsqueda
                System.out.print("\n¿Realizar otra búsqueda? (s/n): ");
                String otra = scanner.nextLine().trim().toLowerCase();
                if (!otra.equals("s")) {
                    break;
                }
                    
            } catch (Exception e) {
                System.out.println("\n❌ Error: " + e.getMessage());
            }
        }
    }
    
    public void exportarResultados(List<VentaResultado> resultados, String nombreArchivo) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(nombreArchivo))) {
            writer.write("=".repeat(60) + "\n");
            writer.write("RESULTADOS DE BÚSQUEDA DE VENTAS\n");
            writer.write("Fecha: " + LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")) + "\n");
            writer.write("Total de ventas encontradas: " + resultados.size() + "\n");
            writer.write("=".repeat(60) + "\n\n");
            
            writer.write(String.format("%-12s %-12s %-15s\n", "MES", "DEPARTAMENTO", "MONTO"));
            writer.write("-".repeat(60) + "\n");
            
            double total = 0;
            for (VentaResultado venta : resultados) {
                writer.write(String.format("%-12s %-12s $%-14,.2f\n", 
                        venta.mes, venta.departamento, venta.monto));
                total += venta.monto;
            }
            
            writer.write("-".repeat(60) + "\n");
            writer.write(String.format("%-24s $%,.2f\n", "TOTAL", total));
            writer.write("=".repeat(60) + "\n");
            
            System.out.println("✅ Resultados exportados a '" + nombreArchivo + "'");
            
        } catch (Exception e) {
            System.out.println("❌ Error al exportar: " + e.getMessage());
        }
    }
    
    // -----------------------------------------------------------------
    // 5. MÉTODO PARA ELIMINAR VENTA
    // -----------------------------------------------------------------
    public boolean eliminarVenta(String mes, String departamento, boolean confirmar) {
        try {
            // Si no se proporcionan parámetros, modo interactivo
            if (mes == null || departamento == null) {
                eliminarVentaInteractivo();
                return true;
            }
            
            // Procesar mes
            int mesIdx;
            String mesNombre;
            
            if (mes.matches("\\d+")) {
                int mesNum = Integer.parseInt(mes);
                if (mesNum >= 1 && mesNum <= 12) {
                    mesNombre = meses[mesNum - 1];
                    mesIdx = mesNum - 1;
                } else {
                    System.out.println("❌ Error: Número de mes " + mesNum + " fuera de rango (1-12)");
                    return false;
                }
            } else {
                mesIdx = -1;
                for (int i = 0; i < meses.length; i++) {
                    if (meses[i].equalsIgnoreCase(mes)) {
                        mesIdx = i;
                        mesNombre = meses[i];
                        break;
                    }
                }
                if (mesIdx == -1) {
                    System.out.println("❌ Error: Mes '" + mes + "' no válido");
                    return false;
                }
                mesNombre = meses[mesIdx];
            }
            
            // Procesar departamento
            int deptIdx;
            String deptNombre;
            
            if (departamento.matches("\\d+")) {
                int deptNum = Integer.parseInt(departamento);
                if (deptNum >= 1 && deptNum <= 3) {
                    deptNombre = departamentos[deptNum - 1];
                    deptIdx = deptNum - 1;
                } else {
                    System.out.println("❌ Error: Número de departamento " + deptNum + " fuera de rango (1-3)");
                    return false;
                }
            } else {
                deptIdx = -1;
                for (int i = 0; i < departamentos.length; i++) {
                    if (departamentos[i].equalsIgnoreCase(departamento)) {
                        deptIdx = i;
                        deptNombre = departamentos[i];
                        break;
                    }
                }
                if (deptIdx == -1) {
                    System.out.println("❌ Error: Departamento '" + departamento + "' no válido");
                    return false;
                }
                deptNombre = departamentos[deptIdx];
            }
            
            // Verificar si existe venta
            double ventaActual = ventas[mesIdx][deptIdx];
            if (ventaActual == 0) {
                System.out.println("❌ No hay venta registrada en " + mesNombre + " - " + deptNombre);
                return false;
            }
            
            // Confirmar eliminación
            if (confirmar) {
                System.out.println("\n⚠️  CONFIRMAR ELIMINACIÓN");
                System.out.println("   Mes: " + mesNombre);
                System.out.println("   Departamento: " + deptNombre);
                System.out.printf("   Monto a eliminar: $%,.2f\n", ventaActual);
                
                System.out.print("\n¿Está seguro de eliminar esta venta? (s/n): ");
                String respuesta = scanner.nextLine().trim().toLowerCase();
                if (!respuesta.equals("s")) {
                    System.out.println("❌ Eliminación cancelada");
                    return false;
                }
            }
            
            // Eliminar venta
            ventas[mesIdx][deptIdx] = 0.0;
            
            System.out.printf("✅ VENTA ELIMINADA: %s - %s: $%,.2f\n", mesNombre, deptNombre, ventaActual);
            return true;
            
        } catch (Exception e) {
            System.out.println("❌ Error al eliminar venta: " + e.getMessage());
            return false;
        }
    }
    
    public void eliminarVentaInteractivo() {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("🗑️  ELIMINACIÓN DE VENTAS - MODO INTERACTIVO");
        System.out.println("=".repeat(60));
        
        while (true) {
            try {
                // Mostrar meses
                System.out.println("\n📅 MESES DISPONIBLES:");
                for (int i = 0; i < meses.length; i++) {
                    System.out.printf("  %2d. %s\n", i + 1, meses[i]);
                }
                
                // Solicitar mes
                System.out.print("\nIngrese número o nombre del mes: ");
                String entradaMes = scanner.nextLine().trim();
                
                // Mostrar departamentos
                System.out.println("\n🏬 DEPARTAMENTOS DISPONIBLES:");
                for (int i = 0; i < departamentos.length; i++) {
                    System.out.printf("  %d. %s\n", i + 1, departamentos[i]);
                }
                
                // Solicitar departamento
                System.out.print("\nIngrese número o nombre del departamento: ");
                String entradaDept = scanner.nextLine().trim();
                
                // Eliminar venta
                if (eliminarVenta(entradaMes, entradaDept, true)) {
                    System.out.println("\n✅ Venta eliminada exitosamente!");
                } else {
                    System.out.println("\n❌ No se pudo eliminar la venta");
                }
                
                // Preguntar si continuar
                System.out.print("\n¿Eliminar otra venta? (s/n): ");
                String continuar = scanner.nextLine().trim().toLowerCase();
                if (!continuar.equals("s")) {
                    System.out.println("\n👋 Regresando al menú principal...");
                    break;
                }
                    
            } catch (Exception e) {
                System.out.println("\n❌ Error: " + e.getMessage());
            }
        }
    }
    
    public Map<String, Object> eliminarVentasPorCriterio(String criterio, String valor) {
        Map<String, Object> estadisticas = new HashMap<>();
        estadisticas.put("eliminadas", 0);
        estadisticas.put("total", 0);
        
        try {
            // Primero buscar las ventas que coinciden
            List<VentaResultado> resultados = buscarVentas(criterio, valor);
            
            if (resultados.isEmpty()) {
                System.out.println("❌ No se encontraron ventas con el criterio especificado");
                return estadisticas;
            }
            
            System.out.printf("\n⚠️  SE ELIMINARÁN %d VENTAS:\n", resultados.size());
            double totalMonto = 0;
            for (VentaResultado v : resultados) {
                totalMonto += v.monto;
            }
            System.out.printf("   Monto total a eliminar: $%,.2f\n", totalMonto);
            
            // Confirmar
            System.out.print("\n¿Está seguro de eliminar todas estas ventas? (s/n): ");
            String confirmar = scanner.nextLine().trim().toLowerCase();
            if (!confirmar.equals("s")) {
                System.out.println("❌ Eliminación masiva cancelada");
                estadisticas.put("total", resultados.size());
                return estadisticas;
            }
            
            // Eliminar cada venta
            int eliminadas = 0;
            for (VentaResultado venta : resultados) {
                int i = venta.indices[0];
                int j = venta.indices[1];
                ventas[i][j] = 0.0;
                eliminadas++;
            }
            
            System.out.printf("\n✅ ELIMINADAS %d VENTAS\n", eliminadas);
            System.out.printf("   Monto eliminado: $%,.2f\n", totalMonto);
            
            estadisticas.put("eliminadas", eliminadas);
            estadisticas.put("total", resultados.size());
            estadisticas.put("monto", totalMonto);
            
            return estadisticas;
            
        } catch (Exception e) {
            System.out.println("❌ Error en eliminación masiva: " + e.getMessage());
            return estadisticas;
        }
    }
    
    // -----------------------------------------------------------------
    // 6. MÉTODO PARA CARGAR DATOS DE EJEMPLO
    // -----------------------------------------------------------------
    public Map<String, Object> cargarDatosEjemplo(String conjunto) {
        Map<String, Object> estadisticas = new HashMap<>();
        estadisticas.put("exitosos", 0);
        estadisticas.put("fallidos", 0);
        estadisticas.put("total", 0);
        
        try {
            System.out.printf("\n📂 CARGANDO DATOS DE EJEMPLO (%s)...\n", conjunto.toUpperCase());
            
            // Guardar datos originales para posible restauración
            datosOriginales = new double[12][3];
            for (int i = 0; i < 12; i++) {
                System.arraycopy(ventas[i], 0, datosOriginales[i], 0, 3);
            }
            
            // Definir conjuntos de datos de ejemplo
            List<String[]> datos = new ArrayList<>();
            
            switch (conjunto.toLowerCase()) {
                case "basico":
                    datos.add(new String[]{"Enero", "Ropa", "12000"});
                    datos.add(new String[]{"Febrero", "Deportes", "8500"});
                    datos.add(new String[]{"Marzo", "Juguetería", "9600"});
                    break;
                    
                case "completo":
                    // Enero
                    datos.add(new String[]{"Enero", "Ropa", "12500"});
                    datos.add(new String[]{"Enero", "Deportes", "8200"});
                    datos.add(new String[]{"Enero", "Juguetería", "11300"});
                    // Febrero
                    datos.add(new String[]{"Febrero", "Ropa", "9800"});
                    datos.add(new String[]{"Febrero", "Deportes", "10500"});
                    datos.add(new String[]{"Febrero", "Juguetería", "7600"});
                    // Marzo
                    datos.add(new String[]{"Marzo", "Ropa", "13200"});
                    datos.add(new String[]{"Marzo", "Deportes", "7400"});
                    datos.add(new String[]{"Marzo", "Juguetería", "8900"});
                    // Abril
                    datos.add(new String[]{"Abril", "Ropa", "11500"});
                    datos.add(new String[]{"Abril", "Deportes", "9200"});
                    datos.add(new String[]{"Abril", "Juguetería", "10100"});
                    // Mayo
                    datos.add(new String[]{"Mayo", "Ropa", "14200"});
                    datos.add(new String[]{"Mayo", "Deportes", "11300"});
                    datos.add(new String[]{"Mayo", "Juguetería", "12500"});
                    // Junio
                    datos.add(new String[]{"Junio", "Ropa", "16200"});
                    datos.add(new String[]{"Junio", "Deportes", "14500"});
                    datos.add(new String[]{"Junio", "Juguetería", "18300"});
                    // Julio
                    datos.add(new String[]{"Julio", "Ropa", "15200"});
                    datos.add(new String[]{"Julio", "Deportes", "13800"});
                    datos.add(new String[]{"Julio", "Juguetería", "17200"});
                    // Agosto
                    datos.add(new String[]{"Agosto", "Ropa", "14800"});
                    datos.add(new String[]{"Agosto", "Deportes", "12600"});
                    datos.add(new String[]{"Agosto", "Juguetería", "16500"});
                    // Septiembre
                    datos.add(new String[]{"Septiembre", "Ropa", "13500"});
                    datos.add(new String[]{"Septiembre", "Deportes", "11800"});
                    datos.add(new String[]{"Septiembre", "Juguetería", "14200"});
                    // Octubre
                    datos.add(new String[]{"Octubre", "Ropa", "12800"});
                    datos.add(new String[]{"Octubre", "Deportes", "11200"});
                    datos.add(new String[]{"Octubre", "Juguetería", "13600"});
                    // Noviembre
                    datos.add(new String[]{"Noviembre", "Ropa", "17500"});
                    datos.add(new String[]{"Noviembre", "Deportes", "14200"});
                    datos.add(new String[]{"Noviembre", "Juguetería", "19800"});
                    // Diciembre
                    datos.add(new String[]{"Diciembre", "Ropa", "23800"});
                    datos.add(new String[]{"Diciembre", "Deportes", "18500"});
                    datos.add(new String[]{"Diciembre", "Juguetería", "31200"});
                    break;
                    
                case "estacional":
                    datos.add(new String[]{"Noviembre", "Juguetería", "25000"});
                    datos.add(new String[]{"Noviembre", "Ropa", "22000"});
                    datos.add(new String[]{"Diciembre", "Juguetería", "45000"});
                    datos.add(new String[]{"Diciembre", "Ropa", "32000"});
                    datos.add(new String[]{"Enero", "Deportes", "18000"});
                    datos.add(new String[]{"Febrero", "Deportes", "16500"});
                    datos.add(new String[]{"Abril", "Ropa", "9500"});
                    datos.add(new String[]{"Mayo", "Juguetería", "8500"});
                    break;
                    
                case "aleatorio":
                    datos.add(new String[]{"Enero", "Ropa", "15000"});
                    datos.add(new String[]{"Marzo", "Deportes", "12000"});
                    datos.add(new String[]{"Mayo", "Juguetería", "18000"});
                    datos.add(new String[]{"Julio", "Ropa", "14000"});
                    datos.add(new String[]{"Septiembre", "Deportes", "11000"});
                    datos.add(new String[]{"Noviembre", "Juguetería", "22000"});
                    break;
                    
                default:
                    System.out.printf("❌ Conjunto '%s' no disponible. Usando 'completo'\n", conjunto);
                    return cargarDatosEjemplo("completo");
            }
            
            // Preguntar si limpiar datos existentes
            boolean tieneDatos = false;
            for (int i = 0; i < 12; i++) {
                for (int j = 0; j < 3; j++) {
                    if (ventas[i][j] > 0) {
                        tieneDatos = true;
                        break;
                    }
                }
                if (tieneDatos) break;
            }
            
            if (tieneDatos) {
                System.out.println("\n⚠️  ADVERTENCIA: Ya existen datos en el sistema");
                System.out.print("¿Desea limpiar datos existentes antes de cargar? (s/n): ");
                String opcion = scanner.nextLine().trim().toLowerCase();
                
                if (opcion.equals("s")) {
                    // Limpiar todos los datos
                    ventas = new double[12][3];
                    System.out.println("✅ Datos existentes limpiados");
                } else {
                    System.out.println("⚠️  Los nuevos datos se agregarán a los existentes");
                }
            }
            
            // Cargar datos
            int exitosos = 0;
            int fallidos = 0;
            double totalMonto = 0;
            
            for (String[] dato : datos) {
                String mes = dato[0];
                String dept = dato[1];
                double monto = Double.parseDouble(dato[2]);
                
                System.out.printf("  Cargando: %s - %s: $%,.2f\n", mes, dept, monto);
                
                if (escribirMonto(mes, dept, monto, false)) {
                    exitosos++;
                    totalMonto += monto;
                } else {
                    fallidos++;
                }
            }
            
            // Mostrar resumen
            System.out.printf("\n📊 RESUMEN DE CARGA (%s):\n", conjunto.toUpperCase());
            System.out.printf("   ✅ Éxitos: %d\n", exitosos);
            System.out.printf("   ❌ Fallos: %d\n", fallidos);
            System.out.printf("   💰 Monto total cargado: $%,.2f\n", totalMonto);
            if (exitosos > 0) {
                System.out.printf("   📈 Promedio por venta: $%,.2f\n", totalMonto / exitosos);
            }
            
            estadisticas.put("conjunto", conjunto);
            estadisticas.put("exitosos", exitosos);
            estadisticas.put("fallidos", fallidos);
            estadisticas.put("total", datos.size());
            estadisticas.put("monto_total", totalMonto);
            
            return estadisticas;
            
        } catch (Exception e) {
            System.out.println("❌ Error al cargar datos de ejemplo: " + e.getMessage());
            return estadisticas;
        }
    }
    
    public boolean restaurarDatosOriginales() {
        try {
            if (datosOriginales != null) {
                for (int i = 0; i < 12; i++) {
                    System.arraycopy(datosOriginales[i], 0, ventas[i], 0, 3);
                }
                System.out.println("✅ Datos originales restaurados");
                return true;
            } else {
                System.out.println("❌ No hay datos originales guardados");
                return false;
            }
        } catch (Exception e) {
            System.out.println("❌ Error al restaurar datos: " + e.getMessage());
            return false;
        }
    }
    
    // -----------------------------------------------------------------
    // MÉTODOS AUXILIARES
    // -----------------------------------------------------------------
    public boolean escribirMonto(String mes, String departamento, double monto, boolean mostrarMensaje) {
        try {
            int mesIdx = -1;
            for (int i = 0; i < meses.length; i++) {
                if (meses[i].equalsIgnoreCase(mes)) {
                    mesIdx = i;
                    break;
                }
            }
            
            int deptIdx = -1;
            for (int i = 0; i < departamentos.length; i++) {
                if (departamentos[i].equalsIgnoreCase(departamento)) {
                    deptIdx = i;
                    break;
                }
            }
            
            if (mesIdx == -1 || deptIdx == -1) {
                if (mostrarMensaje) {
                    System.out.println("❌ Error: Mes o departamento no válido");
                }
                return false;
            }
            
            if (monto < 0) {
                if (mostrarMensaje) {
                    System.out.println("❌ Error: El monto no puede ser negativo");
                }
                return false;
            }
            
            ventas[mesIdx][deptIdx] = monto;
            
            if (mostrarMensaje) {
                System.out.printf("✅ MONTO REGISTRADO: %s - %s: $%,.2f\n", mes, departamento, monto);
            }
            
            return true;
            
        } catch (Exception e) {
            if (mostrarMensaje) {
                System.out.println("❌ Error al escribir monto: " + e.getMessage());
            }
            return false;
        }
    }
    
    public void escribirMontoInteractivo() {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("📝 REGISTRO DE VENTA INDIVIDUAL");
        System.out.println("=".repeat(60));
        
        System.out.println("\n📅 MESES DISPONIBLES:");
        for (int i = 0; i < meses.length; i++) {
            System.out.printf("  %2d. %s\n", i + 1, meses[i]);
        }
        
        System.out.println("\n🏬 DEPARTAMENTOS DISPONIBLES:");
        for (int i = 0; i < departamentos.length; i++) {
            System.out.printf("  %d. %s\n", i + 1, departamentos[i]);
        }
        
        System.out.print("\nIngrese número o nombre del mes: ");
        String mes = scanner.nextLine().trim();
        
        System.out.print("Ingrese número o nombre del departamento: ");
        String departamento = scanner.nextLine().trim();
        
        System.out.print("Ingrese el monto de la venta: $");
        try {
            double monto = Double.parseDouble(scanner.nextLine().trim());
            escribirMonto(mes, departamento, monto, true);
        } catch (NumberFormatException e) {
            System.out.println("❌ Error: El monto debe ser un número válido");
        }
    }
    
    public void escribirMontosPorLote(List<String[]> lote) {
        int exitosos = 0;
        int fallidos = 0;
        double total = 0;
        
        System.out.println("\n📦 PROCESANDO LOTE DE DATOS...");
        
        for (String[] datos : lote) {
            if (datos.length != 3) {
                System.out.println("❌ Formato incorrecto: " + Arrays.toString(datos));
                fallidos++;
                continue;
            }
            
            try {
                String mes = datos[0];
                String dept = datos[1];
                double monto = Double.parseDouble(datos[2]);
                
                if (escribirMonto(mes, dept, monto, false)) {
                    exitosos++;
                    total += monto;
                    System.out.printf("  ✅ %s - %s: $%,.2f\n", mes, dept, monto);
                } else {
                    fallidos++;
                    System.out.printf("  ❌ %s - %s: $%,.2f (Error)\n", mes, dept, monto);
                }
            } catch (NumberFormatException e) {
                System.out.println("❌ Error en monto: " + Arrays.toString(datos));
                fallidos++;
            }
        }
        
        System.out.printf("\n📊 RESUMEN DEL LOTE:\n");
        System.out.printf("   ✅ Éxitos: %d\n", exitosos);
        System.out.printf("   ❌ Fallos: %d\n", fallidos);
        System.out.printf("   💰 Total registrado: $%,.2f\n", total);
    }
    
    public void mostrarTablaCompleta() {
        System.out.println("\n" + "=".repeat(70));
        System.out.println("📊 TABLA COMPLETA DE VENTAS");
        System.out.println("=".repeat(70));
        
        System.out.printf("%-12s", "");
        for (String dept : departamentos) {
            System.out.printf(" %-15s", dept);
        }
        System.out.println("   TOTAL");
        System.out.println("-".repeat(70));
        
        double totalGeneral = 0;
        double[] totalesDepartamentos = new double[departamentos.length];
        
        for (int i = 0; i < meses.length; i++) {
            System.out.printf("%-12s", meses[i]);
            double totalMes = 0;
            
            for (int j = 0; j < departamentos.length; j++) {
                System.out.printf(" $%-14,.2f", ventas[i][j]);
                totalMes += ventas[i][j];
                totalesDepartamentos[j] += ventas[i][j];
            }
            
            System.out.printf(" $%-14,.2f\n", totalMes);
            totalGeneral += totalMes;
        }
        
        System.out.println("-".repeat(70));
        System.out.printf("%-12s", "TOTAL");
        for (double totalDept : totalesDepartamentos) {
            System.out.printf(" $%-14,.2f", totalDept);
        }
        System.out.printf(" $%-14,.2f\n", totalGeneral);
        System.out.println("=".repeat(70));
    }
    
    public void exportarTablaCompleta(String nombreArchivo) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(nombreArchivo))) {
            writer.write("=".repeat(70) + "\n");
            writer.write("TABLA COMPLETA DE VENTAS\n");
            writer.write("Fecha: " + LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")) + "\n");
            writer.write("=".repeat(70) + "\n\n");
            
            writer.write(String.format("%-12s", ""));
            for (String dept : departamentos) {
                writer.write(String.format(" %-15s", dept));
            }
            writer.write("   TOTAL\n");
            writer.write("-".repeat(70) + "\n");
            
            double totalGeneral = 0;
            double[] totalesDepartamentos = new double[departamentos.length];
            
            for (int i = 0; i < meses.length; i++) {
                writer.write(String.format("%-12s", meses[i]));
                double totalMes = 0;
                
                for (int j = 0; j < departamentos.length; j++) {
                    writer.write(String.format(" $%-14,.2f", ventas[i][j]));
                    totalMes += ventas[i][j];
                    totalesDepartamentos[j] += ventas[i][j];
                }
                
                writer.write(String.format(" $%-14,.2f\n", totalMes));
                totalGeneral += totalMes;
            }
            
            writer.write("-".repeat(70) + "\n");
            writer.write(String.format("%-12s", "TOTAL"));
            for (double totalDept : totalesDepartamentos) {
                writer.write(String.format(" $%-14,.2f", totalDept));
            }
            writer.write(String.format(" $%-14,.2f\n", totalGeneral));
            writer.write("=".repeat(70) + "\n");
            
            System.out.println("✅ Tabla exportada a '" + nombreArchivo + "'");
            
        } catch (Exception e) {
            System.out.println("❌ Error al exportar tabla: " + e.getMessage());
        }
    }
    
    // -----------------------------------------------------------------
    // MENÚ PRINCIPAL COMPLETO
    // -----------------------------------------------------------------
    public void menuPrincipal() {
        while (true) {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("🏬 SISTEMA DE GESTIÓN DE VENTAS - MENÚ PRINCIPAL");
            System.out.println("=".repeat(60));
            System.out.println("1. 📝 Escribir monto (individual)");
            System.out.println("2. 📦 Escribir montos (por lote)");
            System.out.println("3. 📊 Mostrar tabla completa");
            System.out.println("4. 🔍 Buscar ventas");
            System.out.println("5. 🗑️  Eliminar venta");
            System.out.println("6. 📂 Cargar datos de ejemplo");
            System.out.println("7. 🔄 Restaurar datos originales");
            System.out.println("8. 💾 Exportar datos a archivo");
            System.out.println("9. 🚪 Salir del sistema");
            System.out.println("=".repeat(60));
            
            try {
                System.out.print("\nSeleccione opción (1-9): ");
                String opcion = scanner.nextLine().trim();
                
                switch (opcion) {
                    case "1":
                        escribirMontoInteractivo();
                        break;
                        
                    case "2":
                        System.out.println("\n📦 ESCRITURA POR LOTE");
                        System.out.println("Formato: mes,departamento,monto");
                        System.out.println("Ejemplo: Enero,Ropa,1500.50");
                        System.out.println("Deje línea vacía para terminar\n");
                        
                        List<String[]> lote = new ArrayList<>();
                        while (true) {
                            System.out.print("Dato: ");
                            String entrada = scanner.nextLine().trim();
                            if (entrada.isEmpty()) {
                                break;
                            }
                            
                            String[] partes = entrada.split(",");
                            if (partes.length == 3) {
                                lote.add(new String[]{
                                    partes[0].trim(),
                                    partes[1].trim(),
                                    partes[2].trim()
                                });
                            } else {
                                System.out.println("❌ Formato incorrecto");
                            }
                        }
                        
                        if (!lote.isEmpty()) {
                            escribirMontosPorLote(lote);
                        }
                        break;
                        
                    case "3":
                        mostrarTablaCompleta();
                        break;
                        
                    case "4":
                        buscarVentasInteractivo();
                        break;
                        
                    case "5":
                        System.out.println("\n🗑️  ELIMINAR VENTAS");
                        System.out.println("1. Eliminar venta específica");
                        System.out.println("2. Eliminar por criterio (masivo)");
                        
                        System.out.print("\nSeleccione (1-2): ");
                        String subOpcion = scanner.nextLine().trim();
                        
                        if (subOpcion.equals("1")) {
                            eliminarVentaInteractivo();
                        } else if (subOpcion.equals("2")) {
                            System.out.println("\n📊 CRITERIOS PARA ELIMINACIÓN MASIVA:");
                            System.out.println("1. Por mes");
                            System.out.println("2. Por departamento");
                            System.out.println("3. Mayores a un monto");
                            System.out.println("4. Menores a un monto");
                            
                            System.out.print("\nSeleccione criterio (1-4): ");
                            String criterioOpc = scanner.nextLine().trim();
                            
                            Map<String, String> criteriosMap = new HashMap<>();
                            criteriosMap.put("1", "mes");
                            criteriosMap.put("2", "departamento");
                            criteriosMap.put("3", "mayor");
                            criteriosMap.put("4", "menor");
                            
                            if (criteriosMap.containsKey(criterioOpc)) {
                                System.out.print("\nIngrese valor para '" + criteriosMap.get(criterioOpc) + "': ");
                                String valor = scanner.nextLine().trim();
                                eliminarVentasPorCriterio(criteriosMap.get(criterioOpc), valor);
                            } else {
                                System.out.println("❌ Opción inválida");
                            }
                        } else {
                            System.out.println("❌ Opción inválida");
                        }
                        break;
                        
                    case "6":
                        System.out.println("\n📂 CONJUNTOS DE DATOS DE EJEMPLO:");
                        System.out.println("1. Completo (datos anuales completos)");
                        System.out.println("2. Básico (solo 3 meses)");
                        System.out.println("3. Estacional (ventas por temporada)");
                        System.out.println("4. Aleatorio (datos variados)");
                        
                        System.out.print("\nSeleccione conjunto (1-4): ");
                        String conjuntoOpc = scanner.nextLine().trim();
                        
                        Map<String, String> conjuntosMap = new HashMap<>();
                        conjuntosMap.put("1", "completo");
                        conjuntosMap.put("2", "basico");
                        conjuntosMap.put("3", "estacional");
                        conjuntosMap.put("4", "aleatorio");
                        
                        if (conjuntosMap.containsKey(conjuntoOpc)) {
                            cargarDatosEjemplo(conjuntosMap.get(conjuntoOpc));
                        } else {
                            System.out.println("❌ Opción inválida");
                        }
                        break;
                        
                    case "7":
                        restaurarDatosOriginales();
                        break;
                        
                    case "8":
                        System.out.println("\n💾 EXPORTAR DATOS");
                        System.out.println("1. Exportar tabla completa");
                        System.out.println("2. Exportar resultados de búsqueda");
                        
                        System.out.print("\nSeleccione (1-2): ");
                        String exportOpc = scanner.nextLine().trim();
                        
                        if (exportOpc.equals("1")) {
                            System.out.print("Nombre del archivo (ej: ventas_completas.txt): ");
                            String nombreArchivo = scanner.nextLine().trim();
                            if (nombreArchivo.isEmpty()) {
                                nombreArchivo = "ventas_completas.txt";
                            }
                            exportarTablaCompleta(nombreArchivo);
                        } else if (exportOpc.equals("2")) {
                            System.out.println("⚠️  Primero realice una búsqueda para exportar resultados");
                        } else {
                            System.out.println("❌ Opción inválida");
                        }
                        break;
                        
                    case "9":
                        System.out.println("\n" + "=".repeat(60));
                        System.out.println("👋 ¡GRACIAS POR USAR EL SISTEMA DE GESTIÓN DE VENTAS!");
                        System.out.println("=".repeat(60));
                        scanner.close();
                        return;
                        
                    default:
                        System.out.println("\n❌ Opción inválida");
                }
                
            } catch (Exception e) {
                System.out.println("\n❌ Error: " + e.getMessage());
            }
        }
    }
    
    // Método main para ejecutar el programa
    public static void main(String[] args) {
        VentasDepartamentos sistema = new VentasDepartamentos();
        
        System.out.println("=".repeat(60));
        System.out.println("🏬 SISTEMA DE GESTIÓN DE VENTAS POR DEPARTAMENTO");
        System.out.println("=".repeat(60));
        System.out.println("📅 Meses: Enero a Diciembre");
        System.out.println("🏬 Departamentos: Ropa, Deportes, Juguetería");
        System.out.println("=".repeat(60));
        
        // Cargar datos de ejemplo automáticamente
        System.out.print("\n¿Cargar datos de ejemplo automáticamente? (s/n): ");
        String cargarEjemplo = sistema.scanner.nextLine().trim().toLowerCase();
        if (cargarEjemplo.equals("s")) {
            sistema.cargarDatosEjemplo("basico");
        }
        
        // Ejecutar menú principal
        sistema.menuPrincipal();
    }
}