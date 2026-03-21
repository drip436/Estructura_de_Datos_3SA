# 📎 MyLinkedList

Implementación propia de una **Lista Enlazada Simple** (*Singly Linked List*) en Python, sin dependencias externas.

---

## 📁 Estructura del proyecto

```
MyLinkedList.py   ← Biblioteca principal (Node + MyLinkedList)
README.md         ← Este archivo
```

---

## 🚀 Instalación / Uso

No requiere instalación. Solo coloca `MyLinkedList.py` en tu proyecto e impórtalo:

```python
from MyLinkedList import MyLinkedList
```

---

## 🧩 Clases

### `Node`
Nodo interno de la lista. Normalmente no se usa directamente.

| Atributo | Descripción              |
|----------|--------------------------|
| `data`   | Valor almacenado         |
| `next`   | Referencia al siguiente nodo |

### `MyLinkedList`
La lista enlazada principal.

```
HEAD
 │
[10] ──► [20] ──► [30] ──► [40] ──► None
```

---

## 🛠️ Métodos disponibles

### Creación

```python
# Lista vacía
ll = MyLinkedList()

# Lista con valores iniciales (desde cualquier iterable)
ll = MyLinkedList([10, 20, 30, 40])
```

---

### ➕ Inserción

#### `append(data)` — Agrega al **final** · O(n)
```python
ll = MyLinkedList([10, 20])
ll.append(30)
# [10 -> 20 -> 30]
```

#### `prepend(data)` — Agrega al **inicio** · O(1)
```python
ll.prepend(0)
# [0 -> 10 -> 20 -> 30]
```

#### `insert(index, data)` — Inserta en una **posición específica** · O(n)
```python
ll.insert(2, 99)
# [0 -> 10 -> 99 -> 20 -> 30]
```
> ⚠️ Lanza `IndexError` si el índice está fuera de rango.

---

### ❌ Eliminación

#### `delete(data)` — Elimina el **primer** nodo con ese valor · O(n)
```python
ll.delete(99)
# [0 -> 10 -> 20 -> 30]
```
> ⚠️ Lanza `ValueError` si el valor no existe.

#### `delete_at(index)` — Elimina el nodo en una **posición** · O(n)
```python
ll.delete_at(0)
# [10 -> 20 -> 30]
```
> ⚠️ Lanza `IndexError` si el índice está fuera de rango.

---

### 🔍 Acceso y búsqueda

#### `get(index)` — Obtiene el valor en una posición · O(n)
```python
ll = MyLinkedList([10, 20, 30])
print(ll.get(1))   # → 20
```

#### `search(data)` — Busca un valor, devuelve su índice o `-1` · O(n)
```python
print(ll.search(30))   # → 2
print(ll.search(99))   # → -1
```

#### `update(index, data)` — Actualiza el valor en una posición · O(n)
```python
ll.update(1, 88)
# [10 -> 88 -> 30]
```

---

### 🔄 Operaciones sobre la lista

#### `reverse()` — Invierte la lista *in-place* · O(n)
```python
ll = MyLinkedList([1, 2, 3])
ll.reverse()
# [3 -> 2 -> 1]
```

#### `to_list()` — Convierte a lista de Python · O(n)
```python
ll.to_list()   # → [3, 2, 1]
```

#### `clear()` — Vacía la lista · O(1)
```python
ll.clear()
# []
```

#### `is_empty()` — Verifica si está vacía · O(1)
```python
ll.is_empty()   # → True / False
```

#### `size()` — Número de elementos · O(1)
```python
ll.size()   # → 3
```

---

### 🐍 Soporte nativo de Python

| Sintaxis            | Equivalente          | Ejemplo                         |
|---------------------|----------------------|---------------------------------|
| `len(ll)`           | `ll.size()`          | `len(ll)` → `3`                 |
| `for x in ll`       | iteración manual     | imprime cada elemento           |
| `20 in ll`          | `ll.search(20) != -1`| `True` / `False`                |
| `print(ll)`         | `__str__`            | `[10 -> 20 -> 30]`              |
| `ll1 == ll2`        | compara valores      | `True` si tienen los mismos elementos |

```python
ll = MyLinkedList([10, 20, 30])

print(len(ll))       # 3
print(20 in ll)      # True
print(99 in ll)      # False

for val in ll:
    print(val)       # 10, 20, 30

print(ll)            # [10 -> 20 -> 30]
```

---

## ⚠️ Manejo de errores

| Situación                          | Excepción     |
|------------------------------------|---------------|
| Índice fuera de rango              | `IndexError`  |
| Valor no encontrado en `delete()`  | `ValueError`  |
| Llamar `delete()` en lista vacía   | `ValueError`  |

```python
try:
    ll.get(100)
except IndexError as e:
    print(e)   # Índice 100 fuera de rango (tamaño: 3)

try:
    ll.delete(999)
except ValueError as e:
    print(e)   # Valor '999' no encontrado en la lista.
```

---

## 📊 Complejidad algorítmica

| Método         | Tiempo | Espacio |
|----------------|--------|---------|
| `append`       | O(n)   | O(1)    |
| `prepend`      | O(1)   | O(1)    |
| `insert`       | O(n)   | O(1)    |
| `delete`       | O(n)   | O(1)    |
| `delete_at`    | O(n)   | O(1)    |
| `get`          | O(n)   | O(1)    |
| `search`       | O(n)   | O(1)    |
| `update`       | O(n)   | O(1)    |
| `reverse`      | O(n)   | O(1)    |
| `to_list`      | O(n)   | O(n)    |
| `clear`        | O(1)   | O(1)    |
| `is_empty`     | O(1)   | O(1)    |
| `size` / `len` | O(1)   | O(1)    |

---

## 💡 Ejemplo completo

```python
from MyLinkedList import MyLinkedList

# Crear lista
ll = MyLinkedList([5, 10, 15, 20])
print(ll)            # [5 -> 10 -> 15 -> 20]

# Agregar elementos
ll.append(25)
ll.prepend(0)
print(ll)            # [0 -> 5 -> 10 -> 15 -> 20 -> 25]

# Insertar en posición 3
ll.insert(3, 99)
print(ll)            # [0 -> 5 -> 10 -> 99 -> 15 -> 20 -> 25]

# Buscar y actualizar
idx = ll.search(99)
ll.update(idx, 12)
print(ll)            # [0 -> 5 -> 10 -> 12 -> 15 -> 20 -> 25]

# Eliminar
ll.delete(0)
ll.delete_at(0)
print(ll)            # [10 -> 12 -> 15 -> 20 -> 25]

# Invertir
ll.reverse()
print(ll)            # [25 -> 20 -> 15 -> 12 -> 10]

# Convertir a lista de Python
print(ll.to_list())  # [25, 20, 15, 12, 10]

# Iterar
for val in ll:
    print(val, end=" ")  # 25 20 15 12 10

# Vaciar
ll.clear()
print(ll.is_empty()) # True
```