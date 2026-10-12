"""Minimum spanning tree with Kruskal's algorithm and Union-Find
(ED practical 3, 2024/25).

Kruskal sorts the edges by weight and adds each one unless it would close a
cycle. "Would it close a cycle?" is answered with a Union-Find (disjoint
set) structure: u and v are already connected exactly when they have the
same representative.

Union-Find uses path compression (``find`` makes every visited node point
straight to the root) and union by rank (the shorter tree goes under the
taller one). Together they make each operation run in O(alpha(n))
amortised time, where alpha is the inverse Ackermann function (< 5 for any
practical n).

Complexity of ``kruskal``: O(E log E) for sorting the edges, plus
O(E alpha(V)) for the Union-Find operations; O(V + E) space.

The original practical also drew every step with networkx/matplotlib
(see ``kruskal_visual.py``); this module keeps the algorithm free of any
plotting dependency so it can be tested.
"""
from __future__ import annotations

Edge = tuple[int, int, float]


class UnionFind:
    """Disjoint sets over the elements 0..n-1."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u: int) -> int:
        """Representative of u's set, compressing the path on the way back."""
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u: int, v: int) -> bool:
        """Merge the sets of u and v; False if they were already the same set."""
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u == root_v:
            return False
        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1
        return True


def kruskal(n: int, edges: list[Edge]) -> list[Edge]:
    """Return the edges of a minimum spanning tree of the graph with vertices
    0..n-1 (a minimum spanning forest if the graph is disconnected).

    Same steps as the original ``kruskal_manual``, without the drawing:
    take edges by increasing weight, discard the ones that close a cycle,
    and stop as soon as the tree has n - 1 edges.
    """
    uf = UnionFind(n)
    mst: list[Edge] = []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if not uf.union(u, v):
            continue  # u and v already connected: this edge closes a cycle
        mst.append((u, v, w))
        if len(mst) == n - 1:
            break
    return mst


if __name__ == "__main__":
    example = [(1, 2, 1), (0, 1, 2), (0, 2, 3), (1, 3, 4),
               (2, 4, 5), (3, 4, 6), (2, 3, 1)]
    tree = kruskal(5, example)
    print("MST edges:", tree)
    print("Total weight:", sum(w for _, _, w in tree))
