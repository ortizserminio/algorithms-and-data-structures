# Algoritmos y estructuras de datos

[English](README.md) · **Español**

[![CI](https://github.com/ortizserminio/algorithms-and-data-structures/actions/workflows/ci.yml/badge.svg)](https://github.com/ortizserminio/algorithms-and-data-structures/actions/workflows/ci.yml)

Algoritmos y estructuras de datos que implementé durante el grado en Ingeniería Informática en la Universidad Miguel Hernández (UMH, España), en **C++** y **Python**. Cada carpeta de tema tiene su propio README con el problema, el enfoque paso a paso, por qué se eligió ese algoritmo frente a las alternativas y un análisis Big-O justificado. Todas las implementaciones tienen tests que se ejecutan en CI.

## Índice

| # | Problema | Técnica | Tiempo | Espacio | Lenguaje | Enlace |
|---|---|---|---|---|---|---|
| 01 | Decimal → binario | Recursividad | O(log n) | O(log n) de pila | C++ | [01-recursion](01-recursion/README.es.md) |
| 01 | Potencia rápida xⁿ | Divide y vencerás; recursivo → iterativo con pila explícita | O(log n) | O(log n) | C++ | [01-recursion](01-recursion/README.es.md) |
| 02 | Contar apariciones | Recorrido lineal; análisis de casos mejor/peor/medio | Θ(n) | O(1) | C++ | [02-searching-sorting](02-searching-sorting/README.es.md) |
| 02 | Ordenación | Inserción (estable, adaptativa) | Θ(n) mejor, Θ(n²) peor | O(1) | C++ | [02-searching-sorting](02-searching-sorting/README.es.md) |
| 03 | Subsecuencia de suma máxima | Fuerza bruta frente a una pasada (Kadane) | Θ(n³) frente a **Θ(n)** | O(1) | C++ | [03-algorithm-analysis](03-algorithm-analysis/README.es.md) |
| 04 | Combinaciones C(n, k) | Recursividad simple frente a **programación dinámica** | Θ(C(n,k)) llamadas frente a **Θ(n·k)** | O(n) frente a Θ(n·k) | C++ | [04-dynamic-programming](04-dynamic-programming/README.es.md) |
| 05 | Pila | Array de capacidad fija | O(1) por operación | O(capacidad) | Python | [05-linear-adts](05-linear-adts/README.es.md) |
| 05 | Cola, pila | Lista enlazada con punteros a cabeza y cola; concatenación O(1) | O(1) por operación | O(n) | Python | [05-linear-adts](05-linear-adts/README.es.md) |
| 05 | Lista en memoria estática | Array contiguo; lista enlazada por índices con huecos libres | O(n) insertar/borrar | O(capacidad) | Python | [05-linear-adts](05-linear-adts/README.es.md) |
| 06 | Operaciones de conjuntos | Vector de bits | O(1) pertenencia, O(tamaño) unión/∩/− | tamaño bits | Python | [06-sets](06-sets/README.es.md) |
| 07 | Diccionario ordenado | Árbol binario de búsqueda | O(h), O(n) peor caso | O(n) | Python | [07-trees](07-trees/README.es.md) |
| 07 | Diccionario ordenado | **Árbol AVL** (autoequilibrado, 4 casos de rotación) | **O(log n) peor caso** | O(n) | Python | [07-trees](07-trees/README.es.md) |
| 08 | Caminos mínimos entre todos los pares | **Floyd-Warshall**, reconstrucción de caminos, detección de ciclos negativos | Θ(n³) | Θ(n²) | Python | [08-graphs](08-graphs/README.es.md) |
| 08 | Alcanzabilidad | Warshall (cierre transitivo) | Θ(n³) | Θ(n²) | Python | [08-graphs](08-graphs/README.es.md) |
| 08 | Árbol de expansión mínima | **Kruskal + Union-Find** (compresión de caminos, unión por rango) | O(E log E) | O(V + E) | Python | [08-graphs](08-graphs/README.es.md) |

## Cómo se prueba

* **Python:** 77 tests de `pytest`. Además de los casos normales y límite (vacío, lleno, un solo elemento, duplicados, valores negativos, entrada no válida), los algoritmos se comparan con una referencia independiente sobre entradas aleatorias: el `set` de Python, `sorted`, caminos mínimos por fuerza bruta y árboles de expansión mínima por fuerza bruta. El árbol AVL se comprueba contra sus invariantes después de cada inserción y cada borrado.
* **C++:** 4 programas de test con unas 2 400 comprobaciones, usando una macro `CHECK` mínima (`common/check.hpp`), así que no hace falta ningún framework externo. Las versiones recursiva e iterativa se comparan sobre rejillas de entradas, y los algoritmos O(n³) y O(n) se comparan con una referencia O(n²).
* **CI** ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) se ejecuta en cada push: pytest en Python 3.10 y 3.12, y los tests de C++ con g++ y clang++, usando `-Werror` y AddressSanitizer/UndefinedBehaviorSanitizer.

## Cómo ejecutarlo

```bash
# Python (3.10+)
pip install -r requirements-dev.txt
python -m pytest

# C++ (cualquier compilador C++14 + make)
make test     # compila y ejecuta todos los tests de C++
make demos    # compila las demos interactivas en build/
```

Cada módulo de Python también funciona como una pequeña demo (`python 07-trees/avl.py`), y `08-graphs/floyd.py` abre el planificador de rutas interactivo de la práctica original.

## Sobre este código

* Los algoritmos son mis prácticas de *Metodología de la Programación Avanzada* (C++) y *Estructuras de Datos* (Python), 2024–2026. El examen de la subsecuencia de suma máxima y el planificador de rutas con Floyd fueron trabajo en equipo.
* Los originales sin modificar están en el primer commit, [`26c3ed7`](https://github.com/ortizserminio/algorithms-and-data-structures/commit/26c3ed7) (sin los nombres de mis compañeros, por privacidad). Después, el historial muestra cada paso por separado: reestructuración, tests y **cada corrección de bugs** con su motivo (por ejemplo, un borrado del ABB que fallaba en nodos con dos hijos, y un método de borrado del AVL al que nunca se llegaba por una errata).
* La limpieza, los tests, el CI y la documentación se prepararon con ayuda de un asistente de IA. Yo los he revisado, y los algoritmos y su lógica son mis prácticas.

## Licencia

[MIT](LICENSE)
