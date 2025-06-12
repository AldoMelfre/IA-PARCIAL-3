import heapq                 # Importa el módulo heapq para usar colas de prioridad (min-heap)
import networkx as nx        # Importa NetworkX para crear y manipular grafos
import matplotlib.pyplot as plt  # Importa matplotlib para graficar

def prim_mst(graph, start):
    """
    Construye el Árbol de Expansión Mínima (AEM) usando Prim.
    Parámetros:
      - graph: dict de dict, adjacency list con pesos (tiempo/costo)
      - start: tarea inicial
    Devuelve:
      - mst_edges: lista de tuplas (u, v, peso) del AEM
    """
    visited = set()              # Conjunto de nodos ya visitados
    mst_edges = []               # Lista de aristas del árbol de expansión mínima
    edges = [(0, None, start)]   # Cola de prioridad: (peso, nodo_origen, nodo_destino)
    
    while edges:                 # Mientras haya aristas por explorar
        weight, u, v = heapq.heappop(edges)  # Extrae la arista de menor peso
        if v in visited:         # Si el nodo destino ya fue visitado, ignora
            continue
        visited.add(v)           # Marca el nodo como visitado
        if u is not None:        # Si no es el nodo inicial
            mst_edges.append((u, v, weight))  # Agrega la arista al árbol
        for w, w_weight in graph[v].items():  # Explora vecinos del nodo actual
            if w not in visited:              # Si el vecino no ha sido visitado
                heapq.heappush(edges, (w_weight, v, w))  # Agrega la arista a la cola
    return mst_edges             # Devuelve las aristas del árbol mínimo

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
    mst = prim_mst(tareas, 'Diseño')   # Calcula el árbol de expansión mínima
    print("Secuencia de tareas óptima (AEM):")
    for u, v, w in mst:                # Imprime cada arista del árbol
        print(f"{u} -> {v} (costo/tiempo: {w})")
    
    # Visualización del árbol de tareas
    T = nx.Graph()                     # Crea un grafo vacío
    T.add_weighted_edges_from(mst)     # Agrega las aristas del árbol mínimo
    pos = nx.spring_layout(T)          # Calcula posiciones para los nodos
    nx.draw(T, pos, with_labels=True, node_color='lightgreen', node_size=800)  # Dibuja nodos y aristas
    labels = nx.get_edge_attributes(T, 'weight')   # Obtiene etiquetas de pesos
    nx.draw_networkx_edge_labels(T, pos, edge_labels=labels)  # Dibuja etiquetas de aristas
    plt.title("Árbol de tareas para proyecto de gorras personalizadas")  # Título del gráfico
    plt.axis('off')                    # Oculta los ejes
    plt.show()                         # Muestra el gráfico
