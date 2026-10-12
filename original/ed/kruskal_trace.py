import networkx as nx
import matplotlib.pyplot as plt

class UnionFind:
    """
    Estructura Union-Find (DSU) con compresión de caminos y unión por rango.
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
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


def draw_graph(G, pos, current_edge=None, mst_edges=None, rejected_edge=None, fig=None, ax=None):
    """
    Dibuja el grafo completo, resaltando:
      - mst_edges en verde (aristas ya incluidas en el MST)
      - current_edge en rojo (arista en consideración)
      - rejected_edge en dashed rojo (arista descartada por ciclo)
    Además etiqueta cada arista con su peso.
    """
    if fig is None or ax is None:
        fig, ax = plt.subplots()
    ax.clear()
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, ax=ax)
    if mst_edges:
        nx.draw_networkx_edges(G, pos, edgelist=mst_edges, width=3, edge_color='green', ax=ax)
    if current_edge:
        nx.draw_networkx_edges(G, pos, edgelist=[current_edge], width=3, edge_color='red', ax=ax)
    if rejected_edge:
        nx.draw_networkx_edges(G, pos, edgelist=[rejected_edge], width=3, style='dashed', edge_color='red', ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    fig.canvas.draw()
    fig.canvas.flush_events()
    return fig, ax


def kruskal_manual(n, edges):
    """
    Versión manual de Kruskal: espera la confirmación del usuario en cada paso,
    detiene ciclos resaltándolos antes de descartar,
    y para al completar el MST.
    """
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    pos = nx.spring_layout(G)

    uf = UnionFind(n)
    mst = []

    plt.ion()
    fig, ax = plt.subplots()

    for (u, v, w) in sorted(edges, key=lambda x: x[2]):
        # 1) resaltar arista en consideración
        fig, ax = draw_graph(G, pos,
                             current_edge=(u, v),
                             mst_edges=mst,
                             rejected_edge=None,
                             fig=fig, ax=ax)
        print(f"Considerando arista {(u, v, w)} — pulsa tecla o click para evaluar...")
        fig.waitforbuttonpress()

        # 2) comprobar si forma ciclo
        if not uf.union(u, v):
            fig, ax = draw_graph(G, pos,
                                 current_edge=None,
                                 mst_edges=mst,
                                 rejected_edge=(u, v),
                                 fig=fig, ax=ax)
            print(f"Arista {(u, v, w)} forma ciclo y se descarta.")
            fig.waitforbuttonpress()
            continue

        # 3) si se une, añadir a MST y mostrar en verde
        mst.append((u, v))
        fig, ax = draw_graph(G, pos,
                             current_edge=None,
                             mst_edges=mst,
                             rejected_edge=None,
                             fig=fig, ax=ax)
        print(f"Arista {(u, v, w)} añadida al MST.")
        fig.waitforbuttonpress()

        # 4) condición de parada
        if len(mst) == n - 1:
            print("MST completado.")
            break

    plt.ioff()
    plt.show()
    return mst

if __name__ == "__main__":
    # Ejemplo de uso con grafo de 5 vértices y ciclos visibles
    n = 5
    edges = [
        (1, 2, 1),  # aceptada
        (0, 1, 2),  # aceptada
        (0, 2, 3),  # ciclo — descartada
        (1, 3, 4),  # aceptada
        (2, 4, 5),  # aceptada
        (3, 4, 6),  
        (2, 3, 1)
    ]
    mst = kruskal_manual(n, edges)
    print("MST resultante:", mst)