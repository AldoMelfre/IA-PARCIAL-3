# Algoritmo de Dijkstra para optimización de rutas de entrega en KREA Work

# GLOSARIO:
# Nodo:           Ubicación (taller o cliente)
# Arista:         Conexión entre dos ubicaciones (camino posible)
# Peso:           Distancia, tiempo o costo entre dos ubicaciones
# Grafo:          Diccionario que representa las conexiones y pesos
# Dijkstra:       Algoritmo para encontrar el camino de menor costo
# dist:           Diccionario con el costo mínimo desde el origen a cada nodo
# previo:         Diccionario para reconstruir la ruta óptima

import heapq

def dijkstra(grafo, origen):
    # Inicializa las distancias a infinito y el previo a None
    dist = {nodo: float('inf') for nodo in grafo}
    dist[origen] = 0
    previo = {nodo: None for nodo in grafo}
    heap = [(0, origen)]  # Cola de prioridad: (costo acumulado, nodo actual)

    while heap:
        costo_actual, nodo = heapq.heappop(heap)
        if costo_actual > dist[nodo]:
            continue  # Si ya se encontró un camino mejor, ignora
        for vecino, peso in grafo[nodo].items():
            nueva_dist = costo_actual + peso
            if nueva_dist < dist[vecino]:
                dist[vecino] = nueva_dist
                previo[vecino] = nodo
                heapq.heappush(heap, (nueva_dist, vecino))
    return dist, previo

# Ejemplo de grafo: clientes en diferentes zonas de Guadalajara y alrededores
grafo = {
    'Guadalajara Centro': {
        'Zapopan': 10,
        'Tlaquepaque': 12,
        'Tonala': 16,
        'Tlajomulco': 30,
        'Chapala': 50,
        'Zapotlanejo': 35,
        'Etzatlan': 65  # Conexión directa, pero más cara que por Zapopan
    },
    'Zapopan': {
        'Guadalajara Centro': 10,
        'Tlaquepaque': 22,
        'Tonala': 28,
        'Chapala': 65,
        'Zapotlanejo': 55,
        'Etzatlan': 20  # HAZ ESTE PESO BAJO para forzar el paso por aquí
    },
    'Tlaquepaque': {
        'Guadalajara Centro': 12,
        'Tonala': 10,
        'Tlajomulco': 18,
        'Chapala': 45,
        'Zapotlanejo': 30,
        'Etzatlan': 80
    },
    'Tonala': {
        'Guadalajara Centro': 16,
        'Tlaquepaque': 10,
        'Zapopan': 28,
        'Tlajomulco': 25,
        'Chapala': 60,
        'Zapotlanejo': 20,
        'Etzatlan': 90
    },
    'Tlajomulco': {
        'Tlaquepaque': 18,
        'Tonala': 25,
        'Chapala': 35,
        'Zapotlanejo': 60,
        'Etzatlan': 100
    },
    'Chapala': {
        'Zapopan': 65,
        'Tlaquepaque': 45,
        'Guadalajara Centro': 50,
        'Tonala': 60,
        'Tlajomulco': 35,
        'Zapotlanejo': 70,
        'Etzatlan': 120,
        'Ajijic': 10  # Solo Chapala conecta con Ajijic
    },
    'Ajijic': {
        'Chapala': 10  # Solo Ajijic conecta con Chapala
    },
    'Zapotlanejo': {
        'Zapopan': 55,
        'Tlaquepaque': 30,
        'Guadalajara Centro': 35,
        'Tonala': 20,
        'Tlajomulco': 60,
        'Chapala': 70,
        'Etzatlan': 110
    },
    'Etzatlan': {
        'Zapopan': 60,
        'Tlaquepaque': 80,
        'Guadalajara Centro': 65,
        'Tonala': 90,
        'Tlajomulco': 100,
        'Chapala': 120,
        'Zapotlanejo': 110
    }
}

origen = 'Guadalajara Centro'
distancias, previos = dijkstra(grafo, origen)

# Mostrar la distancia mínima y la ruta a cada cliente
for destino in grafo:
    if destino == origen:
        continue
    # Reconstruir la ruta óptima
    ruta = []
    actual = destino
    while actual:
        ruta.insert(0, actual)
        actual = previos[actual]
    print(f"Ruta óptima a {destino}: {' -> '.join([origen] + ruta[1:])}")
    print(f"  Costo total: {distancias[destino]} unidades\n")