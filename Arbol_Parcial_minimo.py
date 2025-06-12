def prim_mst(graph, start):
    """
    Construye el Árbol de Expansión Mínima (AEM) usando Prim.
    Parámetros:
      - graph: dict de dict, adjacency list con pesos (tiempo/costo)
      - start: tarea inicial
    Devuelve:
      - mst_edges: lista de tuplas (u, v, peso) del AEM
    """
    visited = set()  # Conjunto de nodos visitados
    mst_edges = []   # Lista de aristas del árbol de expansión mínima
    edges = [(0, None, start)]  # Cola de prioridad: (peso, nodo_origen, nodo_destino)
    
    while edges:  # Mientras haya aristas por explorar
        weight, u, v = heapq.heappop(edges)  # Extrae la arista de menor peso
        if v in visited:  # Si el nodo destino ya fue visitado
            continue      # Salta a la siguiente iteración
        visited.add(v)    # Marca el nodo destino como visitado
        if u is not None: # Si no es el nodo inicial
            mst_edges.append((u, v, weight))  # Agrega la arista al árbol
        for w, w_weight in graph[v].items():  # Para cada vecino del nodo actual
            if w not in visited:              # Si el vecino no ha sido visitado
                heapq.heappush(edges, (w_weight, v, w))  # Agrega la arista a la cola
    return mst_edges  # Devuelve la lista de aristas del árbol
