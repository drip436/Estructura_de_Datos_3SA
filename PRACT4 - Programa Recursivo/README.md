
### COMPARATIVA DE SOLUCIONES #####

# Ventajas de la Solución Iterativa (Ciclos)
La principal fortaleza de este enfoque es su eficiencia y control de recursos.

- Velocidad de ejecución: Es extremadamente rápida porque calcula cada número de la serie una sola vez. En términos técnicos, tiene una complejidad de tiempo lineal, lo que significa que si quieres el número 100 de Fibonacci, el programa solo realiza unas 100 operaciones.

- Bajo consumo de memoria: Solo necesita guardar dos o tres variables en la memoria RAM (los números anteriores) para obtener el siguiente. No importa qué tan grande sea el número que busques, el espacio que ocupa en la memoria se mantiene constante y pequeño.

- Estabilidad: No corre el riesgo de "romper" el programa por falta de memoria (Stack Overflow), lo que la hace la opción ideal para software profesional o aplicaciones de alto rendimiento.

# Ventajas de la Solución Recursiva (Funciones que se llaman a sí mismas)
Aunque es menos eficiente en computadoras modernas, tiene un valor conceptual muy alto.

- Claridad y Elegancia: La solución recursiva es casi una copia fiel de la definición matemática de Fibonacci: F(n)=F(n−1)+F(n−2). Esto hace que el código sea muy breve, limpio y fácil de leer para un humano.

- Simplicidad en el Diseño: No requiere manejar variables de estado manuales (como "auxiliares" o contadores) dentro de un ciclo. El lenguaje de programación se encarga de gestionar la lógica a través de la "pila de llamadas".

- Valor Académico: Es la mejor forma de demostrar cómo funciona la recursividad y cómo un problema grande se puede dividir en subproblemas más pequeños, lo cual es la base de algoritmos mucho más complejos.