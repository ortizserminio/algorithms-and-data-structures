"""Step-by-step visual trace of Kruskal's algorithm (ED practical 3, 2024/25).

Opens a matplotlib window and waits for a key press or click at each step:
the edge under consideration is drawn in red, a rejected edge (it would
close a cycle) in dashed red, and the edges already in the tree in green.

Requires: pip install networkx matplotlib
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from kruskal import Edge, UnionFind


def draw_graph(G, pos, current_edge=None, mst_edges=None, rejected_edge=None,
               fig=None, ax=None):
    """Draw the whole graph with edge weights and highlight the current step."""
    if fig is None or ax is None:
        fig, ax = plt.subplots()
    ax.clear()
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, ax=ax)
    if mst_edges:
        nx.draw_networkx_edges(G, pos, edgelist=mst_edges, width=3,
                               edge_color="green", ax=ax)
    if current_edge:
        nx.draw_networkx_edges(G, pos, edgelist=[current_edge], width=3,
                               edge_color="red", ax=ax)
    if rejected_edge:
        nx.draw_networkx_edges(G, pos, edgelist=[rejected_edge], width=3,
                               style="dashed", edge_color="red", ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"),
                                 ax=ax)
    fig.canvas.draw()
    fig.canvas.flush_events()
    return fig, ax


def kruskal_visual(n: int, edges: list[Edge]) -> list[tuple[int, int]]:
    """Run Kruskal, pausing for user input after every decision."""
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    pos = nx.spring_layout(G)

    uf = UnionFind(n)
    mst: list[tuple[int, int]] = []

    plt.ion()
    fig, ax = plt.subplots()

    for u, v, w in sorted(edges, key=lambda e: e[2]):
        fig, ax = draw_graph(G, pos, current_edge=(u, v), mst_edges=mst, fig=fig, ax=ax)
        print(f"Considering edge {(u, v, w)} - press a key or click to evaluate...")
        fig.waitforbuttonpress()

        if not uf.union(u, v):
            fig, ax = draw_graph(G, pos, mst_edges=mst, rejected_edge=(u, v), fig=fig, ax=ax)
            print(f"Edge {(u, v, w)} closes a cycle and is rejected.")
            fig.waitforbuttonpress()
            continue

        mst.append((u, v))
        fig, ax = draw_graph(G, pos, mst_edges=mst, fig=fig, ax=ax)
        print(f"Edge {(u, v, w)} added to the MST.")
        fig.waitforbuttonpress()

        if len(mst) == n - 1:
            print("MST complete.")
            break

    plt.ioff()
    plt.show()
    return mst


if __name__ == "__main__":
    kruskal_visual(5, [(1, 2, 1), (0, 1, 2), (0, 2, 3), (1, 3, 4),
                       (2, 4, 5), (3, 4, 6), (2, 3, 1)])
