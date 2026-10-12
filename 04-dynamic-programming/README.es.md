# 04 · Programación dinámica: número de combinaciones C(n, k)

[English](README.md) · **Español**

Lenguaje: **C++14**. Origen: *Metodología de la Programación Avanzada*, práctica 3.2 y examen.

**Problema.** Contar las formas de elegir `k` elementos de entre `n`, con `0 ≤ k ≤ n`.

## Recursividad simple: `binomial_recursive`

Regla de Pascal: `C(n, k) = 1` si `k = 0` o `k = n`; si no, `C(n−1, k−1) + C(n−1, k)`.

Es corta y claramente correcta, pero recalcula los mismos subproblemas una y otra vez: a `C(n−2, k−1)`, por ejemplo, se llega desde dos padres distintos. Cada hoja del árbol de llamadas devuelve 1, así que hay exactamente `C(n, k)` hojas y **`2·C(n, k) − 1` llamadas** en total. Los tests comprueban este número para todo `n ≤ 16`. Para `k = n/2` eso es **Θ(2ⁿ/√n)**, exponencial en `n`. La profundidad de pila es O(n).

`binomial_trace` imprime el árbol de llamadas con sangría, y así se ve el trabajo repetido. Para `C(4, 2)`, `combinaciones_traza(2,1)` aparece dos veces.

## Programación dinámica: `binomial_dp`

1. Se construye una tabla `M[0..n][0..k]`.
2. Se rellenan los bordes: `M[i][0] = 1` y `M[i][i] = 1`.
3. Fila a fila, para `i = 2..n`, se calcula `M[i][j] = M[i−1][j−1] + M[i−1][j]` con `1 ≤ j < i` y `j ≤ k`.
4. La respuesta es `M[n][k]`.

Cada celda se calcula **una sola vez**, a partir de dos celdas de la fila anterior, así que el tiempo es **Θ(n·k)** y el espacio **Θ(n·k)**.

## Por qué programación dinámica, y posibles mejoras

El problema tiene los dos ingredientes que necesita la programación dinámica: **subestructura óptima** (la respuesta se construye con respuestas a instancias más pequeñas) y **subproblemas solapados** (la recursividad los repite). La tabla sustituye un tiempo exponencial por uno polinómico.

Mejoras que no necesité para el ejercicio:
- Cada fila solo usa la anterior, así que el espacio puede bajar a **O(k)** guardando una sola fila y rellenándola de derecha a izquierda.
- `C(n, k) = n! / (k!(n−k)!)` se puede calcular con O(k) multiplicaciones usando la fórmula multiplicativa, pero los valores intermedios desbordan un `int` enseguida.

Con `int` de 32 bits, los resultados se desbordan a partir de `C(33, 16)` más o menos. Los tests se quedan por debajo.

## Ejecutar y probar

```bash
make test
make demos
./build/04-dynamic-programming/binomial_main     # imprime la traza si n <= 6
```

Los tests comprueban valores conocidos (`C(0,0)`, `C(10,5) = 252`, `C(30,15) = 155117520`). También comprueban que recursividad y programación dinámica coinciden para todo `n ≤ 18`, la simetría `C(n,k) = C(n,n−k)`, la fórmula del número de llamadas y el formato de la traza.
