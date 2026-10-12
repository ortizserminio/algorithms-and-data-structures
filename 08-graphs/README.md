# 08 · Graphs: Floyd-Warshall, Warshall and Kruskal with Union-Find

**English** · [Español](README.es.md)

Language: **Python 3.10+**. Source: *Estructuras de Datos*, practical 3 (2024/25: Kruskal; 2025/26: Floyd, team project).

## All-pairs shortest paths: [`floyd.py`](floyd.py)

**Use case from the practical:** a route planner for 8 delivery locations `A..H`, where edge weights are travel minutes. The graph is directed and stored as a cost matrix, with `INF` meaning no direct road.

**Approach.**
1. Start with `D = cost matrix`. Set `next_hop[i][j] = j` for every direct edge.
2. For each node `k`, try it as an **intermediate stop** for every pair `(i, j)`. If `D[i][k] + D[k][j] < D[i][j]`, update `D[i][j]` and set `next_hop[i][j] = next_hop[i][k]`.
3. After processing `k`, `D[i][j]` is the shortest path that only uses nodes `0..k` as intermediates. After the last `k`, it is the true shortest path.
4. Rebuild a route by following `next_hop` from `i` until reaching `j`.
5. If any `D[i][i] < 0`, node `i` is on a **negative cycle**: repeating the cycle lowers the cost forever, so no shortest path exists. The function reports those nodes.

Example: the shortest route from A to H is `A → B → H`, 19 minutes.

**Complexity.** Three nested loops over `n` nodes: **Θ(n³)** time and **Θ(n²)** space.

**Why Floyd-Warshall here?** The planner answers *any* origin–destination query, so we need all pairs.

| Alternative | Cost for all pairs | When it is better |
|---|---|---|
| Dijkstra from each node (binary heap) | O(n·(n+m) log n) | Sparse graphs **without** negative weights |
| Bellman-Ford from each node | O(n²·m) | Rarely; handles negative weights but is slower |
| **Floyd-Warshall** | **O(n³)** | Small or dense graphs, negative weights allowed, tiny constant, simplest to implement |

**Warshall** is the boolean version: `reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])`. It answers "can I get from i to j at all?", also in Θ(n³).

## Minimum spanning tree: [`kruskal.py`](kruskal.py)

**Problem.** Connect all vertices of a weighted undirected graph with minimum total weight. For example, laying cable between buildings.

**Approach (Kruskal).**
1. Sort the edges by weight.
2. Take each edge in order. If its endpoints are **already connected**, it would close a cycle, so skip it; otherwise add it to the tree.
3. Stop when the tree has `n − 1` edges.

This greedy choice is safe because of the cut property: the lightest edge crossing any cut belongs to some MST.

"Already connected?" is answered by **Union-Find** (disjoint sets):
* `find(u)` follows parent pointers to the set's representative, using **path compression**: every node visited is re-pointed straight at the root.
* `union(u, v)` hangs the shorter tree under the taller one (**union by rank**). It returns `False` if `u` and `v` were already in the same set.

With both optimisations each operation costs **O(α(n))** amortised, where α is the inverse Ackermann function (below 5 for any realistic n).

**Complexity.** **O(E log E)** to sort, plus O(E·α(V)) for the unions; space O(V + E).
**Kruskal vs Prim:** Prim grows a single tree from one vertex using a priority queue, in O(E log V). It is better on dense graphs given as adjacency matrices. Kruskal is simpler on an edge list and works directly on disconnected graphs, where it returns a minimum spanning *forest*.

[`kruskal_visual.py`](kruskal_visual.py) is the original step-by-step trace. It draws the graph with networkx and colours the edge under consideration red, rejected edges dashed red and accepted edges green, waiting for a key press at each step. Running it needs `pip install networkx matplotlib`.

## Run and test

```bash
python -m pytest 08-graphs
python 08-graphs/floyd.py          # interactive route planner
python 08-graphs/kruskal.py
```

There are 21 tests:
* **Floyd:** checked against a brute-force search over all paths on 40 random graphs, including path costs. Also covers negative edges without a negative cycle, negative-cycle detection, invalid matrices, and confirms the input graph is not modified.
* **Warshall:** must agree with Floyd's reachability.
* **Union-Find:** basic operations and path compression.
* **Kruskal:** checked against a brute-force MST on 30 random graphs, plus disconnected graphs, parallel edges and self-loops.
