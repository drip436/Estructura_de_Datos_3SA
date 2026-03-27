# Torre de Hanoi — Visualizador Gráfico

Implementación interactiva del clásico puzzle matemático **Torre de Hanoi** con interfaz gráfica, cronómetro en tiempo real y soporte desde 2 hasta 64 discos.

---

## Requisitos

- Python 3.7 o superior
- `tkinter` (incluido en la instalación estándar de Python)

> En Linux puede requerirse instalación manual:
> ```bash
> sudo apt install python3-tk
> ```

---

## ▶Ejecución

```bash
python hanoi.py
```

---

## Cómo jugar

1. Haz clic en la torre que contiene el disco que quieres mover — aparecerá un anillo punteado indicando la selección.
2. Haz clic en la torre de destino para colocar el disco.
3. Si el movimiento es inválido (disco grande sobre disco pequeño), se mostrará un aviso en rojo.
4. El objetivo es mover **todos los discos** de la torre **ORIGEN** a la torre **DESTINO**.

**Reglas:**
- Solo se puede mover un disco a la vez.
- Solo se puede tomar el disco que está en el tope de cada torre.
- No se puede colocar un disco grande sobre uno más pequeño.

---

## Controles

| Botón | Función |
|-------|---------|
| `↺ REINICIAR` | Reinicia la partida manteniendo el número de discos actual |
| `⬆ +DISCO` | Agrega un disco y reinicia la partida |
| `⬇ −DISCO` | Quita un disco y reinicia la partida |
| `AUTO` | El algoritmo resuelve el puzzle animado paso a paso (hasta 20 discos) |
| ` INSTANTÁNEO` | Calcula y muestra la solución final al instante (ideal para n grande) |
| `✕ PARAR` | Detiene la resolución automática en cualquier momento |

---

## Cronómetro ###

- Se inicia automáticamente con el **primer movimiento manual**.
- Se detiene al completar el puzzle.
- Formato: `MM:SS.mmm`
- En el modo **AUTO**, mide el tiempo total de animación.
- En el modo **INSTANTÁNEO**, mide el tiempo de cálculo en milisegundos.
- Al ganar, el banner de victoria muestra el tiempo final, los movimientos realizados y si se logró la solución óptima.

---

## Presets de discos

| Discos | Movimientos mínimos          | Modo AUTO       | Observación |
|--------|------------------------------|-----------------|-------------|
| 2 – 8  | 3 – 255                      | Animado     | Jugable manualmente |
| 10     | 1,023                        | Animado     | Rápido |
| 30     | 1,073,741,823                | Instantáneo | ~1 mil millones de movimientos |
| 64     | 18,446,744,073,709,551,615   | Instantáneo | ≈ 585,000 millones de años a 1 mov/seg |

> Para **30 y 64 discos**, el botón AUTO redirige automáticamente al modo instantáneo, ya que una animación real sería físicamente imposible de completar.

---

## Algoritmo

La solución se calcula con el algoritmo recursivo clásico:

```
hanoi(n, origen, destino, auxiliar):
    si n == 1:
        mover disco de origen a destino
    sino:
        hanoi(n-1, origen, auxiliar, destino)
        mover disco de origen a destino
        hanoi(n-1, auxiliar, destino, origen)
```

Para valores grandes de `n`, se utiliza una versión **iterativa con pila explícita** para evitar errores de recursión en Python.

El modo **instantáneo** no simula los movimientos uno a uno — calcula directamente el estado final (todos los discos en la torre DESTINO) y actualiza los contadores matemáticamente.

---

## Estructura del código

```
hanoi.py
├── Hanoi              # Lógica del juego (torres, movimientos, validaciones)
│   ├── seleccionar()  # Manejo de selección y movimiento interactivo
│   ├── pasos_solucion() # Genera la secuencia de movimientos (iterativo)
│   └── resolver_instantaneo() # Aplica el estado final directamente
│
├── Cronometro         # Medición de tiempo con precisión de milisegundos
│   ├── iniciar() / detener() / reset()
│   └── formato()      # Retorna string MM:SS.mmm
│
└── HanoiGUI           # Interfaz gráfica (tkinter Canvas)
    ├── _build_ui()    # Construcción del layout
    ├── _redraw()      # Renderizado adaptativo del canvas
    ├── _auto_step()   # Animación paso a paso
    └── _on_instant()  # Resolución instantánea
```

---

## Características visuales

- Estilo visual de **templo antiguo** con paleta de colores oscuros y dorados.
- Discos coloreados individualmente (8 colores cíclicos) con efecto de profundidad 3D.
- Torres con base grabada en numeración romana (I, II, III).
- Visualización adaptativa: los discos se redimensionan automáticamente según `n` para siempre caber en el canvas.
- Para `n` muy grande, se muestra un indicador `+N` cuando hay discos fuera del área visible.
- Banner de victoria con tiempo, movimientos y calificación de eficiencia.

---

## Fórmula del mínimo de movimientos

El número mínimo de movimientos para resolver la Torre de Hanoi con `n` discos es:

```
movimientos_mínimos = 2ⁿ − 1
```

| n  | Mínimo       |
|----|--------------|
| 3  | 7            |
| 5  | 31           |
| 8  | 255          |
| 10 | 1,023        |
| 20 | 1,048,575    |
| 30 | 1,073,741,823 |
| 64 | 1.844 × 10¹⁹ |