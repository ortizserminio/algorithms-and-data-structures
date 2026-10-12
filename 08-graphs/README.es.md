# 08 · Grafos: Floyd-Warshall, Warshall y Kruskal con Union-Find

[English](README.md) · **Español**

Lenguaje: **Python 3.10+**. Origen: *Estructuras de Datos*, práctica 3 (2024/25: Kruskal; 2025/26: Floyd, trabajo en equipo).

## Caminos mínimos entre todos los pares: [`floyd.py`](floyd.py)

**Caso de uso de la práctica:** un planificador de rutas para 8 puntos de reparto `A..H`, donde los pesos de las aristas son minutos de viaje. El grafo es dirigido y se guarda como matriz de costes, con `INF` cuando no hay carretera directa.

**Enfoque.**
1. Se empieza con `D = matriz de costes`. Para cada arista directa, `next_hop[i][j] = j`.
2. Para cada nodo `k`, se prueba como **parada intermedia** para cada par `(i, j)`. Si `D[i][k] + D[k][j] < D[i][j]`, se actualiza `D[i][j]` y se hace `next_hop[i][j] = next_hop[i][k]`.
3. Después de procesar `k`, `D[i][j]` es el camino más corto que solo usa los nodos `0..k` como intermedios. Después del último `k`, es el camino más corto real.
4. Para reconstruir una ruta se sigue `next_hop` desde `i` hasta llegar a `j`.
5. Si algún `D[i][i] < 0`, el nodo `i` está en un **ciclo negativo**: repetir el ciclo reduce el coste sin fin, así que no existe camino mínimo. La función devuelve esos nodos.

Ejemplo: la ruta más corta de A a H es `A → B → H`, 19 minutos.

**Complejidad.** Tres bucles anidados sobre `n` nodos: **Θ(n³)** de tiempo y **Θ(n²)** de espacio.

**¿Por qué Floyd-Warshall aquí?** El planificador responde a *cualquier* consulta origen–destino, así que hacen falta todos los pares.

| Alternativa | Coste para todos los pares | Cuándo es mejor |
|---|---|---|
| Dijkstra desde cada nodo (montículo binario) | O(n·(n+m) log n) | Grafos dispersos **sin** pesos negativos |
| Bellman-Ford desde cada nodo | O(n²·m) | Pocas veces; admite pesos negativos pero es más lento |
| **Floyd-Warshall** | **O(n³)** | Grafos pequeños o densos, admite pesos negativos, constante muy pequeña, el más sencillo de implementar |

**Warshall** es la versión booleana: `reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])`. Responde a "¿se puede llegar de i a j?", también en Θ(n³).

## Árbol de expansión mínima: [`kruskal.py`](kruskal.py)

**Problema.** Conectar todos los vértices de un grafo no dirigido con pesos, con el peso total mínimo. Por ejemplo, tender cable entre edificios.

**Enfoque (Kruskal).**
1. Se ordenan las aristas por peso.
2. Se toma cada arista en orden. Si sus extremos **ya están conectados**, cerraría un ciclo y se descarta; si no, se añade al árbol.
3. Se para cuando el árbol tiene `n − 1` aristas.

Esta elección voraz es segura por la propiedad del corte: la arista más ligera que cruza cualquier corte pertenece a algún árbol de expansión mínima.

La pregunta "¿ya están conectados?" la responde **Union-Find** (conjuntos disjuntos):
* `find(u)` sigue los punteros al padre hasta el representante del conjunto, con **compresión de caminos**: cada nodo visitado pasa a apuntar directamente a la raíz.
* `union(u, v)` cuelga el árbol más bajo debajo del más alto (**unión por rango**). Devuelve `False` si `u` y `v` ya estaban en el mismo conjunto.

Con las dos optimizaciones, cada operación cuesta **O(α(n))** amortizado, donde α es la inversa de la función de Ackermann (menor que 5 para cualquier n realista).

**Complejidad.** **O(E log E)** para ordenar, más O(E·α(V)) para las uniones; espacio O(V + E).
**Kruskal frente a Prim:** Prim hace crecer un único árbol desde un vértice con una cola de prioridad, en O(E log V), y es mejor en grafos densos dados como matriz de adyacencia. Kruskal es más sencillo sobre una lista de aristas y funciona directamente en grafos no conexos, donde devuelve un *bosque* de expansión mínima.

[`kruskal_visual.py`](kruskal_visual.py) es la traza paso a paso original. Dibuja el grafo con networkx y colorea en rojo la arista que se está evaluando, en rojo discontinuo las descartadas y en verde las aceptadas, esperando a que se pulse una tecla en cada paso. Para ejecutarlo hace falta `pip install networkx matplotlib`.

## Ejecutar y probar

```bash
python -m pytest 08-graphs
python 08-graphs/floyd.py          # planificador de rutas interactivo
python 08-graphs/kruskal.py
```

Hay 21 tests:
* **Floyd:** comparado con una búsqueda por fuerza bruta de todos los caminos en 40 grafos aleatorios, incluido el coste de los caminos. También cubre aristas negativas sin ciclo negativo, la detección de ciclos negativos y matrices no válidas, y comprueba que el grafo de entrada no se modifica.
* **Warshall:** tiene que coincidir con la alcanzabilidad de Floyd.
* **Union-Find:** operaciones básicas y compresión de caminos.
* **Kruskal:** comparado con un árbol de expansión mínima por fuerza bruta en 30 grafos aleatorios, más grafos no conexos, aristas paralelas y bucles.
