# ------------------------------
# Árbol de tareas para proyecto de gorras personalizadas (usando Prim)
# Incluye ramas de producción, marketing y administración
# ------------------------------

import heapq
import networkx as nx
import matplotlib.pyplot as plt

def prim_mst(graph, start):
    """
    Construye el Árbol de Expansión Mínima (AEM) usando Prim.
    Parámetros:
      - graph: dict de dict, adjacency list con pesos (tiempo/costo)
      - start: tarea inicial
    Devuelve:
      - mst_edges: lista de tuplas (u, v, peso) del AEM
    """
    visited = set()
    mst_edges = []
    edges = [(0, None, start)]
    
    while edges:
        weight, u, v = heapq.heappop(edges)
        if v in visited:
            continue
        visited.add(v)
        if u is not None:
            mst_edges.append((u, v, weight))
        for w, w_weight in graph[v].items():
            if w not in visited:
                heapq.heappush(edges, (w_weight, v, w))
    return mst_edges

if __name__ == "__main__":
    # Grafo de tareas (nodos = tareas, pesos = tiempo estimado en horas)
    tareas = {
        # Producción
        'Diseño': {'Compra Materiales': 2, 'Corte Tela': 4, 'Plan Marketing': 3, 'Admin General': 2},
        'Compra Materiales': {'Diseño': 2, 'Corte Tela': 1, 'Confección': 3},
        'Corte Tela': {'Diseño': 4, 'Compra Materiales': 1, 'Confección': 2},
        'Confección': {'Compra Materiales': 3, 'Corte Tela': 2, 'Bordado': 3},
        'Bordado': {'Confección': 3, 'Empaque': 2},
        'Empaque': {'Bordado': 2, 'Entrega': 1},
        'Entrega': {'Empaque': 1},

        # Marketing
        'Plan Marketing': {'Diseño': 3, 'Redes Sociales': 2, 'Publicidad': 4},
        'Redes Sociales': {'Plan Marketing': 2, 'Publicidad': 1, 'Atención Cliente': 2},
        'Publicidad': {'Plan Marketing': 4, 'Redes Sociales': 1},
        'Atención Cliente': {'Redes Sociales': 2},

        # Administración
        'Admin General': {'Diseño': 2, 'Finanzas': 2, 'Inventario': 3, 'Facturación': 4},
        'Finanzas': {'Admin General': 2, 'Facturación': 2},
        'Inventario': {'Admin General': 3},
        'Facturación': {'Admin General': 4, 'Finanzas': 2}
    }
    
    # Ejecutamos Prim desde la tarea inicial 'Diseño'
    mst = prim_mst(tareas, 'Diseño')
    print("Secuencia de tareas óptima (AEM):")
    for u, v, w in mst:
        print(f"{u} -> {v} (costo/tiempo: {w})")
    
    # Visualización del árbol de tareas
    T = nx.Graph()
    T.add_weighted_edges_from(mst)
    pos = nx.spring_layout(T)
    nx.draw(T, pos, with_labels=True, node_color='lightgreen', node_size=800)
    labels = nx.get_edge_attributes(T, 'weight')
    nx.draw_networkx_edge_labels(T, pos, edge_labels=labels)
    plt.title("Árbol de tareas para proyecto de gorras personalizadas")
    plt.axis('off')
    plt.show()
