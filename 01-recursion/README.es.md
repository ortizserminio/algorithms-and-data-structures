# 01 · Recursividad y paso de recursivo a iterativo

[English](README.md) · **Español**

Lenguaje: **C++14**. Origen: *Metodología de la Programación Avanzada*, prácticas 3.1 y 4.

| Archivo | Qué hace |
|---|---|
| [`binary.hpp`](binary.hpp) | Convierte un número natural a binario de forma recursiva; una segunda versión imprime la traza de llamadas. |
| [`recursion_to_iteration.hpp`](recursion_to_iteration.hpp) | Potencia rápida y una recursividad lineal no final, cada una en versión recursiva y en versión iterativa con una pila explícita. |
| [`test_recursion.cpp`](test_recursion.cpp) | Tests de ambas cabeceras. |

## 1. Decimal a binario

**Problema.** Imprimir la representación binaria de `n ≥ 0`.

**Enfoque.**
1. Si `n < 2`, el dígito binario es el propio `n` (caso base).
2. Si no, primero se imprime la forma binaria de `n div 2` y después `n mod 2`.

Como la llamada recursiva va *antes* de imprimir, el dígito más significativo sale primero y no hace falta invertir nada.

**¿Por qué recursividad aquí?** La alternativa iterativa genera los dígitos al revés (primero el menos significativo), así que necesita un búfer o una pila para imprimirlos. La pila de llamadas hace ese trabajo gratis. Con un `int` la profundidad es como mucho de unas 31 llamadas, así que el desbordamiento de pila no es un problema.

**Complejidad.** Cada llamada divide `n` entre 2, lo que da ⌊log₂ n⌋ + 1 llamadas. El tiempo es **O(log n)** y el espacio de pila **O(log n)**.

`binary_trace` ejecuta el mismo algoritmo y escribe una línea numerada antes de cada llamada. Por ejemplo, para `n = 10`:

```
1.- binario_traza(10)
2.- binario_traza(5)
3.- binario_traza(2)
4.- binario_traza(1)
1010
```

## 2. Potencia rápida: de recursivo a iterativo

**Problema.** Calcular `xⁿ` para `n ≥ 0`.

**Enfoque (recursivo).** Si `n = 0`, se devuelve 1. Si `n` es impar, se devuelve `x · xⁿ⁻¹`. Si `n` es par, se calcula `y = x^(n/2)` y se devuelve `y²`.

**Enfoque (iterativo).** La función tiene *dos ramas recursivas distintas*, así que un bucle simple no puede sustituirla directamente. La versión iterativa simula la pila de llamadas:
1. **Al bajar**, mientras `n ≠ 0`, se apila `'I'` y se hace `n -= 1` si `n` es impar; si no, se apila `'P'` y se hace `n /= 2`.
2. Se empieza con `r = 1`, el caso base.
3. **Al subir**, se desapila cada marca: `'I'` significa `r *= x` y `'P'` significa `r = r²`.

**¿Por qué este algoritmo?** El bucle ingenuo `r *= x` repetido `n` veces es O(n). Elevar al cuadrado divide el exponente al menos a la mitad cada dos pasos.

**Complejidad.** **O(log n)** de tiempo, más **O(log n)** de espacio, ya sea en la pila de llamadas o en la pila explícita.

## 3. Recursividad lineal no final → iterativa

`f(x, y) = x + y` si `x ≤ 4`; si no, `f(x−4, y/3) + (x−4)·(y/3)`.

Queda trabajo *después* de la llamada recursiva (sumar `x·y`), así que no es recursividad final. La versión iterativa apila el par `(x, y)` ya actualizado de cada nivel al bajar, y al subir suma `x·y` por cada par desapilado. Ambas versiones son **O(x)** en tiempo y **O(x)** en espacio.

## Ejecutar y probar

Desde la raíz del repositorio:

```bash
make test                       # compila y ejecuta todos los tests de C++
make demos                      # compila las demos interactivas en build/
./build/01-recursion/binary_main
./build/01-recursion/recursion_to_iteration_main
```

Los tests comprueban casos límite (`0`, `1`, `n = 0`, bases negativas). También comprueban que las versiones recursiva e iterativa coinciden sobre una rejilla de entradas.
