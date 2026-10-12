# 03 · Análisis de algoritmos: subsecuencia de suma máxima, O(n³) frente a O(n)

[English](README.md) · **Español**

Lenguaje: **C++14**. Origen: examen de *Metodología de la Programación Avanzada* (resuelto en equipo).

**Problema.** Dado `v[1..n]`, que puede tener valores negativos, encontrar las posiciones `i ≤ j` que maximizan `v[i] + … + v[j]`. Convenio: se permite la subsecuencia vacía, así que la respuesta nunca es negativa. Si todos los elementos son negativos, las dos funciones devuelven `0` con las posiciones `0..0`.

## Algoritmo 1: fuerza bruta, [`max_subarray_cubic`](max_subarray.hpp)

1. Para cada inicio `i` y cada final `j ≥ i`:
2. se suma `v[i..j]` desde cero con un tercer bucle, y
3. se guarda la mejor suma y sus posiciones.

**Complejidad.** El bucle más interno se ejecuta Σᵢ Σⱼ (j − i + 1) ≈ n³/6 veces, así que el tiempo es **Θ(n³)** y el espacio adicional **O(1)**.

## Algoritmo 2: una sola pasada, [`max_subarray_linear`](max_subarray.hpp)

1. Se mantiene `this_sum`, la suma de la subsecuencia candidata actual, que empieza en `i`.
2. Se suma `v[j]`. Si supera la mejor hasta ahora, se guarda `(i, j)`.
3. Si `this_sum` baja de 0, ese prefijo solo puede *reducir* cualquier subsecuencia que lo continúe. Así que se descarta: se reinicia con `i = j + 1` y `this_sum = 0`.

Es la idea del algoritmo de Kadane.

**Complejidad.** Cada elemento se visita una vez, así que el tiempo es **Θ(n)** y el espacio adicional **O(1)**.

## ¿Por qué el algoritmo lineal?

Existe una solución intermedia O(n²): fijar `i` y extender `j` con una suma acumulada. Divide y vencerás da O(n log n). La pasada única es óptima, porque cualquier algoritmo correcto tiene que leer todos los elementos, y además no necesita memoria extra. La fuerza bruta sigue siendo útil como **referencia** sencilla y claramente correcta para los tests.

La demo muestra la diferencia sobre el mismo vector aleatorio:

| n | O(n³) | O(n) |
|---|---|---|
| 3 000 | ~1,3 s | < 1 ms |
| 5 000 | ~5,4 s | < 1 ms |

(Medido en mi portátil con MinGW g++ 6.3 `-O2`. El tiempo cúbico crece unas 4,2 veces de 3 000 a 5 000, cerca del (5/3)³ ≈ 4,6 que predice la teoría.)

## Ejecutar y probar

```bash
make test
make demos
./build/03-algorithm-analysis/max_subarray_main
```

Los tests usan el ejemplo clásico `−2 1 −3 4 −1 2 1 −5 4`, cuya respuesta es 6 en las posiciones 4..7. Cubren el vector vacío, vectores todo negativos y todo positivos, y un solo elemento. También comparan 300 vectores aleatorios con una referencia O(n²) independiente y comprueban que las posiciones devueltas suman realmente la suma devuelta.

> Un bug del código original del examen (la medida de tiempo de O(n) usaba división entera y siempre mostraba 0 ms) se corrigió en su propio commit.
