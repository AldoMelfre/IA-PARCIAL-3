import heapq  # Importa el módulo heapq para usar colas de prioridad (min-heap)
import random  # Importa random para simular el tráfico con valores aleatorios
# ==========================================================
# GLOSARIO
# ----------------------------------------------------------
# Nodo:           Representa una ciudad o destino turístico.
# Arista:         Carretera o conexión entre dos nodos (ciudades).
# Grafo:          Estructura que almacena nodos y aristas.
# Peso:           Costo de recorrer una arista (distancia ajustada por tráfico).
# heapq:          Módulo de Python para colas de prioridad (min-heap).
# Dijkstra:       Algoritmo para encontrar la ruta más corta entre nodos.
# Tráfico:        Factor aleatorio que simula condiciones viales en tiempo real.
# Camino:         Secuencia de nodos desde el origen hasta el destino.
# Instrucción:    Indicación para conducir de una ciudad a otra.
# visitados:      Conjunto de nodos ya explorados en el algoritmo.
# Cola de prioridad: Estructura que permite extraer el nodo con menor costo acumulado.
# ==
# --- Módulo de adquisición de datos (simulación de tráfico en tiempo real) ---
def obtener_trafico_en_tiempo_real(origen, destino):
    # Simula el tráfico: retorna un factor aleatorio entre 1 (libre) y 3 (tráfico pesado)
    trafico = random.uniform(1, 3)
    return trafico  # Devuelve el factor de tráfico

# --- Módulo de grafo geoespacial (nodos: ciudades, aristas: carreteras) ---
class Grafo:
    def __init__(self):
        self.nodos = set()  # Conjunto de nodos (ciudades)
        self.aristas = {}   # Diccionario de aristas: clave=(origen, destino), valor=distancia base

    def agregar_nodo(self, nodo):
        self.nodos.add(nodo)  # Agrega un nodo (ciudad) al conjunto

    def agregar_arista(self, origen, destino, distancia):
        self.aristas[(origen, destino)] = distancia  # Agrega arista de origen a destino
        self.aristas[(destino, origen)] = distancia  # Agrega arista de destino a origen (bidireccional)

    def vecinos(self, nodo):
        # Devuelve una lista de nodos vecinos conectados al nodo dado
        return [dest for (ori, dest) in self.aristas if ori == nodo]

    def peso_actual(self, origen, destino):
        # Calcula el peso actual de la arista considerando el tráfico en tiempo real
        base = self.aristas[(origen, destino)]  # Distancia base entre origen y destino
        factor_trafico = obtener_trafico_en_tiempo_real(origen, destino)  # Factor de tráfico
        return base * factor_trafico  # Peso ajustado por tráfico

# --- Módulo de elección de ruta (Dijkstra adaptado) ---
def dijkstra_dinamico(grafo, inicio, destino):
    heap = [(0, inicio, [])]  # Cola de prioridad: (costo acumulado, nodo actual, camino recorrido)
    visitados = set()  # Conjunto de nodos ya visitados
    while heap:
        (costo, actual, camino) = heapq.heappop(heap)  # Extrae el nodo con menor costo
        if actual in visitados:
            continue  # Si ya fue visitado, lo ignora
        camino = camino + [actual]  # Agrega el nodo actual al camino
        if actual == destino:
            return (costo, camino)  # Si llegó al destino, retorna el costo y el camino
        visitados.add(actual)  # Marca el nodo como visitado
        for vecino in grafo.vecinos(actual):  # Itera sobre los vecinos del nodo actual
            if vecino not in visitados:
                peso = grafo.peso_actual(actual, vecino)  # Calcula el peso actual de la arista
                heapq.heappush(heap, (costo + peso, vecino, camino))  # Agrega el vecino a la cola de prioridad
    return (float('inf'), [])  # Si no hay ruta, retorna infinito y camino vacío

# --- Módulo de control del vehículo (traducción de ruta a instrucciones) ---
def traducir_ruta_a_instrucciones(ruta):
    instrucciones = []  # Lista para almacenar instrucciones
    for i in range(len(ruta)-1):
        # Genera una instrucción para ir de un nodo al siguiente
        instrucciones.append(f"Conduce de {ruta[i]} a {ruta[i+1]}")
    return instrucciones  # Devuelve la lista de instrucciones

# --- Ejemplo de uso con destinos turísticos de Jalisco ---
if __name__ == "__main__":
    grafo = Grafo()  # Crea una instancia del grafo
    lugares = [
        "Guadalajara", "Tequila", "Chapala", "Puerto Vallarta", "Tlaquepaque", "Mazamitla"
    ]
    for lugar in lugares:
        grafo.agregar_nodo(lugar)  # Agrega cada ciudad como nodo al grafo
    # Distancias aproximadas en km entre ciudades
    grafo.agregar_arista("Guadalajara", "Tequila", 60)
    grafo.agregar_arista("Guadalajara", "Chapala", 50)
    grafo.agregar_arista("Guadalajara", "Tlaquepaque", 10)
    grafo.agregar_arista("Guadalajara", "Mazamitla", 125)
    grafo.agregar_arista("Guadalajara", "Puerto Vallarta", 330)
    grafo.agregar_arista("Tequila", "Puerto Vallarta", 270)
    grafo.agregar_arista("Chapala", "Mazamitla", 75)

    ejemplos = [
        ("Guadalajara", "Puerto Vallarta"),  # Ejemplo 1: de Guadalajara a Puerto Vallarta
        ("Chapala", "Tequila"),              # Ejemplo 2: de Chapala a Tequila
        ("Mazamitla", "Tlaquepaque")         # Ejemplo 3: de Mazamitla a Tlaquepaque
    ]

    for origen, destino in ejemplos:
        costo, ruta = dijkstra_dinamico(grafo, origen, destino)  # Calcula la mejor ruta y su costo
        instrucciones = traducir_ruta_a_instrucciones(ruta)      # Traduce la ruta en instrucciones
        print(f"\nRuta óptima de {origen} a {destino}:")
        print(" -> ".join(ruta))  # Imprime la secuencia de ciudades
        print(f"Tiempo estimado (ponderado por tráfico): {costo:.2f} unidades")
        print("Instrucciones:")
        for instr in instrucciones:
            print(instr)  # Imprime cada instrucción de manejo