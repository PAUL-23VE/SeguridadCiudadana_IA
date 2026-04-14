"""
Algoritmos de búsqueda en grafos: BFS, DFS, A*

Estos algoritmos exploran el grafo del mapa urbano OSM para encontrar
caminos entre dos puntos. Son útiles para análisis de rutas y conectividad.

Algoritmos implementados:
- BFS (Breadth-First Search): Búsqueda en anchura, encuentra el camino más corto en número de nodos
- DFS (Depth-First Search): Búsqueda en profundidad, explora exhaustivamente
- A* (A-Star): Búsqueda informada con heurística de Haversine, encuentra el camino óptimo en distancia
"""
import networkx as nx
import heapq
import math
from collections import deque


def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia real en metros entre dos puntos GPS usando la fórmula de Haversine.
    
    Parámetros
    ----------
    lat1, lon1 : float
        Latitud y longitud del punto 1 (en grados)
    lat2, lon2 : float
        Latitud y longitud del punto 2 (en grados)
    
    Retorna
    -------
    float : distancia en metros
    """
    R = 6371000  # Radio de la Tierra en metros
    
    # Convertir grados a radianes
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    # Fórmula de Haversine
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = R * c
    
    return distancia


def bfs(G, origen, destino, mostrar_mensajes=False):
    """
    Breadth-First Search (Búsqueda en Anchura)
    
    Explora el grafo nivel por nivel hasta encontrar el destino.
    Garantiza encontrar el camino más corto en número de nodos.
    
    Parámetros
    ----------
    G : networkx.Graph
        Grafo del mapa urbano
    origen : nodo
        Nodo de inicio
    destino : nodo
        Nodo objetivo
    mostrar_mensajes : bool
        Si True, imprime información del proceso en consola
    
    Retorna
    -------
    list : lista de nodos que forman el camino, o [] si no existe
    """
    if mostrar_mensajes:
        print("\n  [BFS] Iniciando búsqueda en anchura...")
    
    visitados = set()
    cola = deque([[origen]])
    nodos_explorados = 0
    
    while cola:
        camino = cola.popleft()
        nodo = camino[-1]
        nodos_explorados += 1
        
        if nodo == destino:
            if mostrar_mensajes:
                print(f"  [BFS] Camino encontrado! ({len(camino)} nodos, explorados: {nodos_explorados})")
            return camino
            
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in G.neighbors(nodo):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)
    
    if mostrar_mensajes:
        print(f"  [BFS] No existe camino (explorados: {nodos_explorados})")
    return []


def dfs(G, origen, destino, mostrar_mensajes=False):
    """
    Depth-First Search (Búsqueda en Profundidad)
    
    Explora el grafo en profundidad hasta encontrar el destino.
    No garantiza el camino más corto, pero explora exhaustivamente.
    
    Parámetros
    ----------
    G : networkx.Graph
        Grafo del mapa urbano
    origen : nodo
        Nodo de inicio
    destino : nodo
        Nodo objetivo
    mostrar_mensajes : bool
        Si True, imprime información del proceso en consola
    
    Retorna
    -------
    list : lista de nodos que forman el camino, o [] si no existe
    """
    if mostrar_mensajes:
        print("\n  [DFS] Iniciando búsqueda en profundidad...")
    
    visitados = set()
    pila = [[origen]]
    nodos_explorados = 0
    
    while pila:
        camino = pila.pop()
        nodo = camino[-1]
        nodos_explorados += 1
        
        if nodo == destino:
            if mostrar_mensajes:
                print(f"  [DFS] Camino encontrado! ({len(camino)} nodos, explorados: {nodos_explorados})")
            return camino
            
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in G.neighbors(nodo):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                pila.append(nuevo_camino)
    
    if mostrar_mensajes:
        print(f"  [DFS] No existe camino (explorados: {nodos_explorados})")
    return []


def heuristica_haversine(G, nodo1, nodo2):
    """
    Heurística de distancia real entre dos nodos (en km).
    
    Usa la fórmula de Haversine para calcular la distancia geodésica
    entre dos nodos del grafo. Esta es la heurística admisible para A*.
    
    Parámetros
    ----------
    G : networkx.Graph
        Grafo con nodos que tienen atributos 'x' (longitud) e 'y' (latitud)
    nodo1, nodo2 : nodo
        Nodos del grafo
    
    Retorna
    -------
    float : distancia en kilómetros
    """
    lat1 = G.nodes[nodo1]['y']
    lon1 = G.nodes[nodo1]['x']
    lat2 = G.nodes[nodo2]['y']
    lon2 = G.nodes[nodo2]['x']
    return calcular_distancia_haversine(lat1, lon1, lat2, lon2) / 1000  # Convertir a km


def a_estrella(G, origen, destino, mostrar_mensajes=False):
    """
    A* (A-Estrella) - Búsqueda Informada con Heurística de Haversine
    
    Usa la distancia geográfica real como heurística para encontrar
    el camino más corto en distancia (no en número de nodos).
    
    Parámetros
    ----------
    G : networkx.Graph
        Grafo del mapa urbano (debe tener atributos 'x' e 'y' en los nodos)
    origen : nodo
        Nodo de inicio
    destino : nodo
        Nodo objetivo
    mostrar_mensajes : bool
        Si True, imprime información del proceso en consola
      Retorna
    -------
    list : lista de nodos que forman el camino óptimo, o [] si no existe
    """
    if mostrar_mensajes:
        print("\n  [A*] Iniciando búsqueda informada con heurística Haversine...")
    
    frontera = [(0, [origen])]
    visitados = set()
    nodos_explorados = 0
    
    while frontera:
        costo, camino = heapq.heappop(frontera)
        nodo = camino[-1]
        nodos_explorados += 1
        
        if nodo == destino:
            distancia_total = sum(
                heuristica_haversine(G, camino[i], camino[i+1]) 
                for i in range(len(camino)-1)
            )
            if mostrar_mensajes:
                print(f"  [A*] ✅ Camino óptimo encontrado! ({len(camino)} nodos, {distancia_total:.2f} km, explorados: {nodos_explorados})")
            return camino
            
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in G.neighbors(nodo):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                heur = heuristica_haversine(G, vecino, destino)
                heapq.heappush(frontera, (costo + 1 + heur, nuevo_camino))
    
    if mostrar_mensajes:
        print(f"  [A*] ❌ No existe camino (explorados: {nodos_explorados})")
    return []


# Alias para compatibilidad con código existente
astar = a_estrella
