import os

class ExternalSorting:
    """Librería especializada en métodos de ordenamiento externo."""

    @staticmethod
    def intercalacion(archivo_a, archivo_b, archivo_resultado):
        """
        1. INTERCALACIÓN
        Combina dos archivos que ya están previamente ordenados en un tercer archivo.
        """
        with open(archivo_a, 'r') as f_a, open(archivo_b, 'r') as f_b, open(archivo_resultado, 'w') as f_res:
            line_a = f_a.readline()
            line_b = f_b.readline()

            while line_a and line_b:
                if int(line_a) <= int(line_b):
                    f_res.write(line_a)
                    line_a = f_a.readline()
                else:
                    f_res.write(line_b)
                    line_b = f_b.readline()

            # Agregar los elementos restantes si un archivo termina antes que el otro
            while line_a:
                f_res.write(line_a)
                line_a = f_a.readline()
            while line_b:
                f_res.write(line_b)
                line_b = f_b.readline()

    @staticmethod
    def mezcla_directa(nombre_archivo):
        """
        2. MEZCLA DIRECTA
        Divide el archivo en secuencias de tamaño fijo (1, 2, 4, 8...) y las mezcla
        usando archivos auxiliares hasta que todo el archivo esté ordenado.
        """
        def contar_registros(n_archivo):
            with open(n_archivo, 'r') as f:
                return sum(1 for _ in f)

        n = contar_registros(nombre_archivo)
        distancia = 1
        
        while distancia < n:
            # Fase 1: Distribución en dos archivos auxiliares
            f = open(nombre_archivo, 'r')
            f1 = open('aux1.tmp', 'w')
            f2 = open('aux2.tmp', 'w')
            
            for i in range(n):
                linea = f.readline()
                if (i // distancia) % 2 == 0:
                    f1.write(linea)
                else:
                    f2.write(linea)
            f.close(); f1.close(); f2.close()

            # Fase 2: Mezcla de los archivos auxiliares de vuelta al original
            f = open(nombre_archivo, 'w')
            f1 = open('aux1.tmp', 'r')
            f2 = open('aux2.tmp', 'r')
            
            for _ in range(0, n, distancia * 2):
                c1, c2 = 0, 0
                val1 = f1.readline()
                val2 = f2.readline()
                
                while c1 < distancia and c2 < distancia and val1 and val2:
                    if int(val1) <= int(val2):
                        f.write(val1); val1 = f1.readline(); c1 += 1
                    else:
                        f.write(val2); val2 = f2.readline(); c2 += 1
                
                # Vaciar tramos restantes del bloque
                while c1 < distancia and val1:
                    f.write(val1); val1 = f1.readline(); c1 += 1
                while c2 < distancia and val2:
                    f.write(val2); val2 = f2.readline(); c2 += 1
            
            f.close(); f1.close(); f2.close()
            distancia *= 2

        # Limpiar temporales
        for tmp in ['aux1.tmp', 'aux2.tmp']:
            if os.path.exists(tmp): os.remove(tmp)

    @staticmethod
    def mezcla_equilibrada(nombre_archivo):
        """
        3. MEZCLA EQUILIBRADA (Natural Merge)
        A diferencia de la directa, aprovecha secuencias (runs) que ya vienen ordenadas.
        Utiliza un proceso de distribución y fusión basado en cambios de orden.
        """
        def hay_cambio_de_orden(actual, archivo):
            pos_actual = archivo.tell()
            proxima = archivo.readline()
            if not proxima:
                return True
            archivo.seek(pos_actual) # Retroceder para no perder el dato
            return int(actual) > int(proxima)

        ordenado = False
        while not ordenado:
            # Paso 1: Distribuir secuencias naturales en F1 y F2
            f = open(nombre_archivo, 'r')
            f1 = open('f1.tmp', 'w'); f2 = open('f2.tmp', 'w')
            
            dest = f1
            num_secuencias = 0
            linea = f.readline()
            while linea:
                dest.write(linea)
                if hay_cambio_de_orden(linea, f):
                    num_secuencias += 1
                    dest = f2 if dest == f1 else f1
                linea = f.readline()
            
            f.close(); f1.close(); f2.close()
            
            if num_secuencias <= 1:
                ordenado = True
                break

            # Paso 2: Fusionar las secuencias de vuelta
            f = open(nombre_archivo, 'w')
            f1 = open('f1.tmp', 'r'); f2 = open('f2.tmp', 'r')
            
            l1 = f1.readline(); l2 = f2.readline()
            while l1 or l2:
                while l1 and l2:
                    if int(l1) <= int(l2):
                        f.write(l1)
                        if hay_cambio_de_orden(l1, f1):
                            # Fin de secuencia en F1, vaciar secuencia de F2
                            l1 = f1.readline()
                            while l2 and not hay_cambio_de_orden(l2, f2):
                                f.write(l2); l2 = f2.readline()
                            if l2: f.write(l2); l2 = f2.readline()
                            break
                        l1 = f1.readline()
                    else:
                        f.write(l2)
                        if hay_cambio_de_orden(l2, f2):
                            # Fin de secuencia en F2, vaciar secuencia de F1
                            l2 = f2.readline()
                            while l1 and not hay_cambio_de_orden(l1, f1):
                                f.write(l1); l1 = f1.readline()
                            if l1: f.write(l1); l1 = f1.readline()
                            break
                        l2 = f2.readline()
                
                # Escribir restos de archivos si uno se agota antes
                if l1 and not l2: f.write(l1); l1 = f1.readline()
                if l2 and not l1: f.write(l2); l2 = f2.readline()

            f.close(); f1.close(); f2.close()

        # Limpiar temporales
        for tmp in ['f1.tmp', 'f2.tmp']:
            if os.path.exists(tmp): os.remove(tmp)