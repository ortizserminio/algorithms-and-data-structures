"""All-pairs shortest paths with Floyd-Warshall (ED practical 3, team project).

Use case from the practical: shortest delivery routes between 8 locations.
The graph is a cost matrix (``INF`` = no direct edge). Floyd-Warshall tries
every node ``k`` as an intermediate step:

    D[i][j] = min(D[i][j], D[i][k] + D[k][j])   for k = 0..n-1

and a ``next_hop`` matrix lets us rebuild the actual path. Negative edge
weights are allowed; a negative cycle shows up as D[i][i] < 0 at the end.
Warshall's algorithm is the boolean variant: it only answers "is there a
path from i to j?".

Complexity: Theta(n^3) time, Theta(n^2) space, for both algorithms.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

INF = 999999

Matrix = list[list[int]]


# --------------------------------------------------------------------------
# Graph interface and cost-matrix implementation
# --------------------------------------------------------------------------
class GraphInterface(ABC):
    """Minimal interface for a graph stored as a cost matrix."""

    @abstractmethod
    def nodes(self) -> list[str]: ...

    @abstractmethod
    def matrix(self) -> Matrix: ...

    @abstractmethod
    def set_edge(self, source: str, target: str, cost: int,
                 bidirectional: bool = False) -> None: ...

    @abstractmethod
    def remove_edge(self, source: str, target: str,
                    bidirectional: bool = False) -> None: ...


class CostMatrixGraph(GraphInterface):
    """Directed weighted graph; ``matrix[i][j]`` is the cost of edge i -> j."""

    def __init__(self, nodes: list[str], matrix: Matrix) -> None:
        self._nodes = list(nodes)
        self._matrix = [list(row) for row in matrix]
        self._validate()

    def _validate(self) -> None:
        if not self._nodes:
            raise ValueError("The graph cannot be empty.")
        if not self._matrix:
            raise ValueError("The cost matrix cannot be empty.")
        if len(self._matrix) != len(self._nodes):
            raise ValueError("The matrix must have one row per node.")
        for row in self._matrix:
            if len(row) != len(self._nodes):
                raise ValueError("The matrix must be square.")
        for i in range(len(self._nodes)):
            if self._matrix[i][i] != 0:
                raise ValueError("The diagonal of the matrix must be 0.")

    def nodes(self) -> list[str]:
        return list(self._nodes)

    def matrix(self) -> Matrix:
        """A copy of the cost matrix (callers cannot modify the graph)."""
        return [list(row) for row in self._matrix]

    def _index(self, node: str) -> int:
        node = node.upper()
        if node not in self._nodes:
            raise ValueError("The node does not exist.")
        return self._nodes.index(node)

    def set_edge(self, source: str, target: str, cost: int,
                 bidirectional: bool = False) -> None:
        i, j = self._index(source), self._index(target)
        if i == j and cost != 0:
            raise ValueError("The cost from a node to itself must be 0.")
        self._matrix[i][j] = cost
        if bidirectional:
            self._matrix[j][i] = cost

    def remove_edge(self, source: str, target: str,
                    bidirectional: bool = False) -> None:
        i, j = self._index(source), self._index(target)
        if i == j:
            self._matrix[i][j] = 0
        else:
            self._matrix[i][j] = INF
            if bidirectional:
                self._matrix[j][i] = INF


# --------------------------------------------------------------------------
# Algorithms
# --------------------------------------------------------------------------
def floyd(graph: GraphInterface, verbose: bool = False,
          print_matrix_each_step: bool = False
          ) -> tuple[Matrix, list[list[Optional[int]]], list[str]]:
    """Run Floyd-Warshall on ``graph``.

    Returns ``(distances, next_hop, negative_cycle_nodes)``.
    ``next_hop[i][j]`` is the node to go to first when travelling from i to
    j (None if j is unreachable). Paths are only replaced by strictly
    cheaper ones, so on ties the first path found is kept.
    """
    nodes = graph.nodes()
    dist = graph.matrix()
    n = len(nodes)

    next_hop: list[list[Optional[int]]] = [
        [j if dist[i][j] != INF and i != j else None for j in range(n)]
        for i in range(n)
    ]

    if verbose:
        print("\nINITIAL COST MATRIX:")
        print_matrix(dist, nodes)

    for k in range(n):  # k = intermediate node, i = source, j = target
        if verbose:
            print(f"--- Step using {nodes[k]} as intermediate node ---")
        changed = False

        for i in range(n):
            for j in range(n):
                # Never add up non-existent routes (INF + x).
                if dist[i][k] != INF and dist[k][j] != INF:
                    new_cost = dist[i][k] + dist[k][j]
                    if new_cost < dist[i][j]:
                        old = dist[i][j]
                        dist[i][j] = new_cost
                        next_hop[i][j] = next_hop[i][k]
                        changed = True
                        if verbose:
                            old_txt = "INF" if old == INF else old
                            print(f"  [!] Better: {nodes[i]} -> {nodes[j]} via "
                                  f"{nodes[k]} | before: {old_txt} | now: {new_cost}")

        if verbose and not changed:
            print("  No path improved in this step.")
        if verbose and print_matrix_each_step:
            print("Matrix after this step:")
            print_matrix(dist, nodes)

    cycles = negative_cycle_nodes(dist, nodes)
    if cycles and verbose:
        print("\nWARNING: the graph contains a negative cycle through",
              ", ".join(cycles), "- shortest paths are undefined.")
    return dist, next_hop, cycles


def reconstruct_path(source: int, target: int,
                     next_hop: list[list[Optional[int]]],
                     nodes: list[str]) -> Optional[list[str]]:
    """Follow ``next_hop`` from source to target; None if unreachable.

    Only valid when the graph has no negative cycle.
    """
    if source == target:
        return [nodes[source]]
    if next_hop[source][target] is None:
        return None
    path = [source]
    while source != target:
        source = next_hop[source][target]  # type: ignore[assignment]
        path.append(source)
    return [nodes[i] for i in path]


def negative_cycle_nodes(dist: Matrix, nodes: list[str]) -> list[str]:
    """After Floyd, D[i][i] < 0 means i lies on (or reaches) a negative cycle:
    the cycle could be repeated forever to keep lowering the cost."""
    return [nodes[i] for i in range(len(dist)) if dist[i][i] < 0]


def warshall(graph: GraphInterface) -> list[list[bool]]:
    """Transitive closure: ``reach[i][j]`` is True if some path i -> j exists."""
    m = graph.matrix()
    n = len(m)
    reach = [[i == j or m[i][j] != INF for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
    return reach


# --------------------------------------------------------------------------
# Printing helpers and example data
# --------------------------------------------------------------------------
def print_matrix(matrix: Matrix, nodes: list[str]) -> None:
    print("      " + "".join(f"{node:>8}" for node in nodes))
    for i, row in enumerate(matrix):
        cells = "".join(f"{'INF' if v == INF else v:>8}" for v in row)
        print(f"{nodes[i]:>6}{cells}")
    print()


def print_bool_matrix(matrix: list[list[bool]], nodes: list[str]) -> None:
    print("      " + "".join(f"{node:>8}" for node in nodes))
    for i, row in enumerate(matrix):
        print(f"{nodes[i]:>6}" + "".join(f"{'YES' if v else 'NO':>8}" for v in row))
    print()


def delivery_network(bidirectional: bool = False) -> CostMatrixGraph:
    """The 8-location delivery network used in the practical (minutes)."""
    nodes = ["A", "B", "C", "D", "E", "F", "G", "H"]
    matrix = [
        [0,   4,   8,   INF, INF, INF, INF, INF],
        [INF, 0,   INF, 5,   INF, INF, INF, 15],
        [INF, INF, 0,   2,   6,   INF, INF, INF],
        [INF, INF, INF, 0,   INF, 7,   INF, INF],
        [INF, INF, INF, INF, 0,   3,   INF, 8],
        [INF, INF, INF, INF, INF, 0,   4,   INF],
        [INF, INF, INF, INF, INF, INF, 0,   2],
        [INF, INF, INF, INF, INF, INF, INF, 0],
    ]
    graph = CostMatrixGraph(nodes, matrix)
    if bidirectional:
        edges = [("A", "B", 4), ("A", "C", 8), ("B", "D", 5), ("B", "H", 15),
                 ("C", "D", 2), ("C", "E", 6), ("D", "F", 7), ("E", "F", 3),
                 ("E", "H", 8), ("F", "G", 4), ("G", "H", 2)]
        for source, target, cost in edges:
            graph.set_edge(source, target, cost, bidirectional=True)
    return graph


def menu() -> None:
    """Interactive route planner, as presented in the practical."""
    graph = delivery_network()
    while True:
        print("\n" + "=" * 50)
        print(" ROUTE PLANNER - FLOYD'S ALGORITHM")
        print("=" * 50)
        print("1. Show cost matrix")
        print("2. Add, change or remove an edge")
        print("3. Shortest path with Floyd")
        print("4. Reachability with Warshall")
        print("5. Exit")
        option = input("\nOption (1-5): ")

        if option == "1":
            print_matrix(graph.matrix(), graph.nodes())
        elif option == "2":
            print("Nodes:", ", ".join(graph.nodes()))
            source = input("Source: ").upper()
            target = input("Target: ").upper()
            cost = input("New cost, or INF to remove the edge: ").upper()
            both = input("Also in the opposite direction? (Y/N): ").upper() == "Y"
            try:
                if cost == "INF":
                    graph.remove_edge(source, target, bidirectional=both)
                else:
                    graph.set_edge(source, target, int(cost), bidirectional=both)
                print("Done.")
            except ValueError as error:
                print("Error:", error)
        elif option == "3":
            nodes = graph.nodes()
            source = input("From: ").upper()
            target = input("To: ").upper()
            if source not in nodes or target not in nodes:
                print("Error: unknown node.")
                continue
            dist, next_hop, cycles = floyd(graph, verbose=True)
            if not cycles:
                i, j = nodes.index(source), nodes.index(target)
                path = reconstruct_path(i, j, next_hop, nodes)
                if path is None:
                    print(f"There is no path from {source} to {target}.")
                else:
                    print(f"Best route: {' -> '.join(path)}  ({dist[i][j]} minutes)")
        elif option == "4":
            print_bool_matrix(warshall(graph), graph.nodes())
        elif option == "5":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()
