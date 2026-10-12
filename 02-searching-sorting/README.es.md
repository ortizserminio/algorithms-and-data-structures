# 02 · Búsqueda y ordenación: contar apariciones, ordenación por inserción

[English](README.md) · **Español**

Lenguaje: **C++14**. Origen: *Metodología de la Programación Avanzada*, prácticas 1 y 2.

Los vectores empiezan en **1** (posiciones `1..n`, la posición `0` no se usa) para coincidir con el pseudocódigo de la asignatura. Los tests comprueban que la posición 0 nunca se toca.

## Contar apariciones: [`count_occurrences.hpp`](count_occurrences.hpp)

**Problema.** Contar cuántos elementos de `v[1..n]` son iguales a `x`.

**Enfoque.** Recorrer el vector una vez e incrementar un contador en cada coincidencia.

**Análisis de complejidad (el objetivo de la práctica).** La demo construye tres vectores de entrada: todos los elementos iguales a `x`, ninguno igual, y la mitad iguales. Para este algoritmo los tres casos cuestan lo mismo, porque hay que mirar cada elemento sea cual sea su valor. Mejor, peor y caso medio son **Θ(n)** en tiempo, con **O(1)** de espacio adicional. Buscar la *primera* aparición sería distinto: ahí el mejor caso es O(1).

## Ordenación por inserción: [`insertion_sort.hpp`](insertion_sort.hpp)

**Problema.** Ordenar `v[1..n]` de menor a mayor, sobre el propio vector.

**Enfoque.**
1. Se considera que `v[1..i−1]` ya está ordenado, empezando con `i = 2`.
2. Se guarda `x = v[i]` y se desplaza una posición a la derecha cada elemento del prefijo que sea *mayor* que `x`.
3. Se coloca `x` en el hueco y se sigue con `i + 1`.

**Complejidad.**

| Entrada | Desplazamientos del bucle interno | Tiempo |
|---|---|---|
| Ya ordenada (mejor caso) | 0 por elemento | **Θ(n)** |
| Aleatoria (caso medio) | unos i/2 por elemento | **Θ(n²)** |
| Ordenada al revés (peor caso) | i − 1 por elemento | **Θ(n²)** |

El espacio adicional es **O(1)**. La ordenación es **estable**, porque solo se mueven los elementos estrictamente mayores.

**¿Por qué inserción, y cuándo no?** Es sencilla, trabaja sobre el propio vector, es estable y es *adaptativa*: es lineal con datos casi ordenados. Por eso ordenaciones reales como Timsort o introsort la usan para particiones pequeñas. Para entradas grandes y aleatorias lo adecuado es un algoritmo O(n log n) (mergesort, heapsort, quicksort). La demo mide el tiempo de los tres casos, y al duplicar `n` se ve claramente el crecimiento cuadrático.

## Ejecutar y probar

```bash
make test
make demos
./build/02-searching-sorting/count_occurrences_main
./build/02-searching-sorting/insertion_sort_main
```

Los tests cubren vectores vacíos y de un elemento, entradas de mejor, peor y caso medio, duplicados, números negativos y 200 vectores aleatorios comparados con `std::sort`.

> Un bug del `main()` de la práctica original (el vector del mejor caso nunca se imprimía) se corrigió en su propio commit. Puedes verlo en el historial de `count_occurrences_main.cpp`.
