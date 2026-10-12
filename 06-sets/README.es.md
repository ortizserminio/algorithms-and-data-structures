# 06 · Conjuntos como vectores de bits

[English](README.md) · **Español**

Lenguaje: **Python 3.10+**. Origen: *Estructuras de Datos*, ejercicio del tema 4 ("TAD Conjunto").

**Problema.** Representar subconjuntos de un universo pequeño `{0, …, size−1}` e implementar unión, intersección, diferencia, diferencia simétrica, pertenencia, inserción y borrado.

## Enfoque

Todo el conjunto se guarda en **un solo entero**: el elemento `i` pertenece al conjunto cuando el bit `i` vale 1. Por ejemplo, `{1, 2, 4}` sobre 8 elementos es `0b00010110`.

La asignatura pedía escribir las operaciones **bit a bit**, como se manejaría un conjunto de indicadores 0/1 en pseudocódigo. Para cada posición `i` se leen `a = (A >> i) & 1` y `b = (B >> i) & 1`, y se combinan:

| Operación | Regla para el bit `i` |
|---|---|
| Unión | `max(a, b)` |
| Intersección | `a · b` |
| Diferencia A − B | `a and not b` |
| Diferencia simétrica | `a xor b` |

`add(i)` suma `2^i` solo si el bit `i` vale 0, y `remove(i)` lo resta solo si vale 1, así que las dos operaciones son idempotentes.

## Complejidad, y por qué un vector de bits

| | Vector de bits (este) | Conjunto hash (`set`) | Lista ordenada |
|---|---|---|---|
| Pertenencia / añadir / borrar | **O(1)** | O(1) en media | O(log n) / O(n) |
| Unión, intersección… | **O(tamaño)** con el bucle bit a bit, una instrucción por palabra con `\|`, `&`, `^` | O(len A + len B) | O(len A + len B) |
| Espacio | **tamaño bits** | decenas de bytes por elemento | una posición por elemento |

Los vectores de bits ganan cuando el universo es pequeño y denso: permisos, indicadores, tableros de ajedrez, filtros de Bloom. Pierden cuando el universo es enorme y el conjunto disperso (por ejemplo, identificadores arbitrarios de 64 bits); ahí lo adecuado es un conjunto hash.

## Correcciones sobre el ejercicio original

El `Conjuntos.py` original no se podía ejecutar. La corrección está en un único commit que enumera cada problema:
1. Todos los métodos estaban sangrados *dentro* de `__init__`, así que los objetos no tenían ninguno.
2. Una errata, `max_elemetos`, lanzaba `AttributeError` en todas las operaciones.
3. `contains` y `add` aceptaban `num == size`, uno más allá del universo. Ahora los límites son `0 ≤ num < size`.

## Ejecutar y probar

```bash
python -m pytest 06-sets
python 06-sets/bitset.py
```

Los 14 tests comparan las cuatro operaciones con el `set` de Python sobre 200 pares aleatorios, y cubren conjuntos vacíos y llenos, valores fuera del universo, `add` idempotente, otros tamaños de universo y la identidad `A − B = A ∩ (U − B)`.
