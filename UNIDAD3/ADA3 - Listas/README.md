# Gestion de Postres con Listas Enlazadas

---

## Descripcion

Programa en Python que implementa un arreglo llamado POSTRES donde cada elemento es un nodo que apunta a una lista enlazada de ingredientes. La estructura refleja el diagrama de listas enlazadas visto en clase, donde cada nodo contiene un dato y un apuntador al siguiente nodo, siendo NIL (None en Python) el fin de cada lista.

---

## Estructura de datos

```
POSTRES
  |
  |--> [Arroz con leche] --> [arroz] --> [leche] --> [azucar] --> [canela] --> NIL
  |
  |--> [Flan] --> [huevo] --> [leche] --> [azucar] --> [vainilla] --> NIL
  |
  |--> [Gelatina] --> [grenetina] --> [agua] --> [azucar] --> NIL
  |
  |--> [Pay de limon] --> [galleta] --> [mantequilla] --> [limon] --> NIL
```

Se definen dos clases:

- `NodoIngrediente` — almacena el nombre del ingrediente y un apuntador `siguiente` (NIL si es el ultimo).
- `NodoPostre` — almacena el nombre del postre y un apuntador `ingredientes` al primer nodo de su lista enlazada (NIL si no tiene ingredientes).

---

## Funcionalidades

### a) Imprimir ingredientes de un postre
Recorre la lista enlazada del postre indicado e imprime cada nodo con el formato:
```
[huevo] --> [leche] --> [azucar] --> NIL
```

### b) Insertar ingredientes a un postre
Agrega uno o varios ingredientes al final de la lista enlazada del postre. No permite duplicados dentro de la misma lista.

### c) Eliminar un ingrediente
Desconecta el nodo del ingrediente de la lista enlazada usando un apuntador anterior, reconectando los nodos vecinos para mantener la cadena.

### d) Alta de postre
Crea un nuevo NodoPostre con su lista enlazada de ingredientes y lo inserta en el arreglo POSTRES manteniendo el orden alfabetico.

### e) Baja de postre
Libera nodo por nodo la lista enlazada de ingredientes antes de eliminar el NodoPostre del arreglo, dejando todos los apuntadores en NIL.

---

## Ejercicio 2 — Eliminar postres repetidos

La funcion recorre el arreglo POSTRES usando un conjunto para detectar nombres duplicados. Al encontrar un duplicado lo elimina del arreglo.

### Por que se manda advertencia

Al eliminar un NodoPostre duplicado, su lista enlazada de ingredientes tambien se pierde porque ningun apuntador llega a ella. Si el duplicado tenia ingredientes distintos al original, esa informacion es irrecuperable.

### Conclusion

Esta operacion debe usarse con cuidado. Se recomienda revisar manualmente los duplicados o respaldar la informacion antes de ejecutarla.

---

## Como ejecutar

Requiere Python 3. No usa librerias externas.

```bash
python postres.py
```

Al iniciar, el programa carga cuatro postres de prueba y muestra el siguiente menu:

```
====================================================
      GESTION DE POSTRES - Listas Enlazadas
====================================================
  1. (a) Imprimir ingredientes de un postre
  2. (b) Insertar ingredientes a un postre
  3. (c) Eliminar un ingrediente de un postre
  4. (d) Dar de alta un postre
  5. (e) Dar de baja un postre
  6.     Mostrar todos los postres
  7.     Eliminar postres repetidos (Ejercicio 2)
  0.     Salir
====================================================
```

---

## Ejemplo de uso

```
Elige una opcion: 1
Nombre del postre: Flan

  Ingredientes de 'Flan':
  [huevo] --> [leche] --> [azucar] --> [vainilla] --> NIL
```

```
Elige una opcion: 4
Nombre del nuevo postre: Nieve de guanabana
Ingredientes (separados por coma): leche, guanabana, azucar

  [OK] 'Nieve de guanabana' dado de alta y ordenado alfabeticamente.
```

---

## Notas tecnicas

- El arreglo POSTRES se mantiene en orden alfabetico en todo momento.
- La busqueda de postres e ingredientes es case-insensitive.
- Al insertar ingredientes se pueden escribir varios separados por coma: `canela, nuez, pasas`
- NIL equivale a `None` en Python. Es la forma en que el lenguaje representa un apuntador vacio o sin siguiente nodo.
