# ------------------------------
# Simulador de Árbol de Expansión Mínima y Máxima (Kruskal)
# Proyecto de gorras personalizadas: producción, marketing y administración
# ------------------------------

import networkx as nx                # Importa NetworkX para manipulación de grafos
import matplotlib.pyplot as plt      # Importa Matplotlib para graficar

def kruskal_mst(edges, reverse=False):
    """
    Algoritmo de Kruskal para Árbol de Expansión Mínima (reverse=False) o Máxima (reverse=True).
    edges: lista de tuplas (u, v, peso)
    reverse: False para mínimo, True para máximo
    Devuelve: lista de aristas del árbol
    """
    # Ordena las aristas por peso (ascendente para mínimo, descendente para máximo)
    edges = sorted(edges, key=lambda x: x[2], reverse=reverse)
    parent = {}  # Diccionario para el conjunto disjunto (union-find)
    def find(u):
        # Encuentra la raíz del conjunto de u
        while parent[u] != u:
            parent[u] = parent[parent[u]]  # Compresión de caminos
            u = parent[u]
        return u
    def union(u, v):
        # Une los conjuntos de u y v
        parent[find(u)] = find(v)
    # Inicializa conjuntos para cada nodo
    nodes = set()
    for u, v, _ in edges:
        nodes.add(u)
        nodes.add(v)
    for n in nodes:
        parent[n] = n
    mst = []  # Lista de aristas del árbol resultante
    for u, v, w in edges:
        if find(u) != find(v):      # Si u y v no están conectados aún
            mst.append((u, v, w))   # Añade la arista al árbol
            union(u, v)             # Une los conjuntos
        if len(mst) == len(nodes) - 1:  # Si ya tenemos n-1 aristas, termina
            break
    return mst

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

    # Convertir el grafo a lista de aristas (evitar duplicados)
    seen = set()  # Para no repetir aristas bidireccionales
    edges = []
    for u in tareas:
        for v, w in tareas[u].items():
            if (v, u) not in seen:      # Si la arista inversa no ha sido agregada
                edges.append((u, v, w)) # Agrega la arista
                seen.add((u, v))        # Marca como agregada

    # Árbol de mínimo coste (Kruskal)
    mst_min = kruskal_mst(edges, reverse=False)  # reverse=False para mínimo
    print("Árbol de Expansión Mínima (Kruskal):")
    for u, v, w in mst_min:
        print(f"{u} -> {v} (costo/tiempo: {w})")

    # Visualización del árbol mínimo
    T_min = nx.Graph()
    T_min.add_weighted_edges_from(mst_min)
    pos = nx.spring_layout(T_min)
    nx.draw(T_min, pos, with_labels=True, node_color='lightgreen', node_size=800)
    labels = nx.get_edge_attributes(T_min, 'weight')
    nx.draw_networkx_edge_labels(T_min, pos, edge_labels=labels)
    plt.title("Árbol de Expansión Mínima (Kruskal)")
    plt.axis('off')
    plt.show()

    # Árbol de máximo coste (Kruskal)
    mst_max = kruskal_mst(edges, reverse=True)  # reverse=True para máximo
    print("\nÁrbol de Expansión Máxima (Kruskal):")
    for u, v, w in mst_max:
        print(f"{u} -> {v} (costo/tiempo: {w})")

    # Visualización del árbol máximo
    T_max = nx.Graph()
    T_max.add_weighted_edges_from(mst_max)
    pos = nx.spring_layout(T_max)
    nx.draw(T_max, pos, with_labels=True, node_color='salmon', node_size=800)
    labels = nx.get_edge_attributes(T_max, 'weight')
    nx.draw_networkx_edge_labels(T_max, pos, edge_labels=labels)
    plt.title("Árbol de Expansión Máxima (Kruskal)")
    plt.axis('off')
    plt.show()