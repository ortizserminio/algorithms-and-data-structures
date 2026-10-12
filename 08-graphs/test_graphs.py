import itertools
import random

import pytest

from floyd import (INF, CostMatrixGraph, delivery_network, floyd,
                   negative_cycle_nodes, reconstruct_path, warshall)
from kruskal import UnionFind, kruskal


# ------------------------------------------------------------------ helpers
def brute_force_shortest(matrix, i, j):
    """Shortest simple-path cost by trying every ordering of intermediates
    (only for tiny graphs with non-negative weights)."""
    n = len(matrix)
    best = matrix[i][j]
    others = [k for k in range(n) if k not in (i, j)]
    for r in range(1, len(others) + 1):
        for mids in itertools.permutations(others, r):
            path = (i, *mids, j)
            if all(matrix[a][b] != INF for a, b in zip(path, path[1:])):
                best = min(best, sum(matrix[a][b] for a, b in zip(path, path[1:])))
    return best


def path_cost(matrix, names, path):
    idx = [names.index(p) for p in path]
    return sum(matrix[a][b] for a, b in zip(idx, idx[1:]))


# -------------------------------------------------------------------- Floyd
def test_floyd_on_delivery_network():
    g = delivery_network()
    nodes = g.nodes()
    dist, nxt, cycles = floyd(g)
    assert cycles == []
    a, h = nodes.index("A"), nodes.index("H")
    assert dist[a][h] == 19
    path = reconstruct_path(a, h, nxt, nodes)
    assert path[0] == "A" and path[-1] == "H"
    assert path_cost(g.matrix(), nodes, path) == 19


def test_floyd_unreachable_pair():
    g = delivery_network()
    nodes = g.nodes()
    dist, nxt, _ = floyd(g)
    h, a = nodes.index("H"), nodes.index("A")
    assert dist[h][a] == INF
    assert reconstruct_path(h, a, nxt, nodes) is None


def test_path_to_itself():
    g = delivery_network()
    _, nxt, _ = floyd(g)
    assert reconstruct_path(2, 2, nxt, g.nodes()) == ["C"]


def test_floyd_matches_brute_force_on_random_graphs():
    rng = random.Random(11)
    for _ in range(40):
        n = rng.randint(1, 6)
        m = [[0 if i == j else (rng.randint(1, 20) if rng.random() < 0.5 else INF)
              for j in range(n)] for i in range(n)]
        g = CostMatrixGraph([chr(65 + i) for i in range(n)], m)
        dist, nxt, _ = floyd(g)
        for i in range(n):
            for j in range(n):
                assert dist[i][j] == brute_force_shortest(m, i, j)
                path = reconstruct_path(i, j, nxt, g.nodes())
                if dist[i][j] == INF:
                    assert path is None
                else:
                    assert path_cost(m, g.nodes(), path) == dist[i][j]


def test_negative_edge_without_negative_cycle():
    g = CostMatrixGraph(["A", "B", "C"], [[0, 2, 10], [INF, 0, -4], [INF, INF, 0]])
    dist, nxt, cycles = floyd(g)
    assert cycles == []
    assert dist[0][2] == -2
    assert reconstruct_path(0, 2, nxt, g.nodes()) == ["A", "B", "C"]


def test_negative_cycle_is_detected():
    g = CostMatrixGraph(["A", "B", "C"], [[0, 2, INF], [INF, 0, -5], [1, INF, 0]])
    _, _, cycles = floyd(g)
    assert set(cycles) == {"A", "B", "C"}
    assert negative_cycle_nodes([[0, 1], [1, 0]], ["X", "Y"]) == []


def test_floyd_does_not_modify_the_graph():
    g = delivery_network()
    before = g.matrix()
    floyd(g)
    assert g.matrix() == before


def test_verbose_mode_prints_steps(capsys):
    floyd(CostMatrixGraph(["A", "B"], [[0, 1], [INF, 0]]), verbose=True,
          print_matrix_each_step=True)
    out = capsys.readouterr().out
    assert "INITIAL COST MATRIX" in out and "intermediate node" in out


@pytest.mark.parametrize("nodes, matrix", [
    ([], []),
    (["A"], []),
    (["A", "B"], [[0, 1]]),
    (["A", "B"], [[0, 1], [1]]),
    (["A"], [[5]]),
])
def test_invalid_graphs_are_rejected(nodes, matrix):
    with pytest.raises(ValueError):
        CostMatrixGraph(nodes, matrix)


def test_set_and_remove_edges():
    g = CostMatrixGraph(["A", "B"], [[0, INF], [INF, 0]])
    g.set_edge("a", "b", 7, bidirectional=True)   # names are case-insensitive
    assert g.matrix() == [[0, 7], [7, 0]]
    g.remove_edge("A", "B")
    assert g.matrix() == [[0, INF], [7, 0]]
    with pytest.raises(ValueError):
        g.set_edge("A", "A", 3)
    with pytest.raises(ValueError):
        g.set_edge("A", "Z", 1)


def test_bidirectional_network_is_symmetric():
    m = delivery_network(bidirectional=True).matrix()
    assert all(m[i][j] == m[j][i] for i in range(8) for j in range(8)
               if m[i][j] != INF and m[j][i] != INF)
    assert m[7][6] == 2  # H -> G now exists


# ----------------------------------------------------------------- Warshall
def test_warshall_matches_floyd_reachability():
    g = delivery_network()
    dist, _, _ = floyd(g)
    reach = warshall(g)
    for i in range(8):
        for j in range(8):
            assert reach[i][j] == (dist[i][j] != INF)


# --------------------------------------------------------------- Union-Find
def test_union_find_basic():
    uf = UnionFind(5)
    assert uf.union(0, 1) is True
    assert uf.union(1, 0) is False
    assert uf.union(3, 4) is True
    assert uf.find(0) == uf.find(1)
    assert uf.find(0) != uf.find(3)
    assert uf.union(1, 4) is True
    assert len({uf.find(i) for i in range(5)}) == 2   # {0,1,3,4} and {2}


def test_union_find_path_compression():
    uf = UnionFind(4)
    uf.parent = [0, 0, 1, 2]  # chain 3 -> 2 -> 1 -> 0
    assert uf.find(3) == 0
    assert uf.parent == [0, 0, 0, 0]


# ------------------------------------------------------------------ Kruskal
EXAMPLE = [(1, 2, 1), (0, 1, 2), (0, 2, 3), (1, 3, 4),
           (2, 4, 5), (3, 4, 6), (2, 3, 1)]


def test_kruskal_example_from_practical():
    tree = kruskal(5, EXAMPLE)
    assert len(tree) == 4
    assert sum(w for _, _, w in tree) == 9
    assert (0, 2, 3) not in tree       # would close the cycle 0-1-2


def brute_force_mst_weight(n, edges):
    best = None
    for subset in itertools.combinations(edges, n - 1):
        uf = UnionFind(n)
        if all(uf.union(u, v) for u, v, _ in subset):
            w = sum(e[2] for e in subset)
            best = w if best is None else min(best, w)
    return best


def test_kruskal_matches_brute_force_on_random_graphs():
    rng = random.Random(5)
    for _ in range(30):
        n = rng.randint(2, 6)
        edges = [(u, v, rng.randint(1, 9))
                 for u, v in itertools.combinations(range(n), 2) if rng.random() < 0.7]
        expected = brute_force_mst_weight(n, edges)
        tree = kruskal(n, edges)
        if expected is None:       # disconnected: spanning forest
            assert len(tree) < n - 1
        else:
            assert len(tree) == n - 1
            assert sum(w for _, _, w in tree) == expected


def test_kruskal_edge_cases():
    assert kruskal(1, []) == []
    assert kruskal(3, []) == []
    assert kruskal(2, [(0, 1, 5), (0, 1, 2)]) == [(0, 1, 2)]   # parallel edges
    assert kruskal(2, [(0, 0, 1), (0, 1, 3)]) == [(0, 1, 3)]   # self-loop ignored
