"""
Algoritmos de busqueda en grafos: BFS, DFS, A*

Estos algoritmos exploran el grafo del mapa urbano OSM para encontrar
caminos entre dos puntos. Son utiles para analisis de rutas y conectividad.

Algoritmos implementados:
- BFS: Busqueda en anchura, camino mas corto en numero de nodos
- DFS: Busqueda en profundidad, explora exhaustivamente
- A*:  Busqueda informada con heuristica Haversine, camino optimo en km
"""
import networkx as nx
import heapq
import math
from collections import deque


def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """Distancia en metros entre dos puntos GPS (formula de Haversine)."""
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def heuristica_haversine(G, nodo1, nodo2):
    """Distancia geodesica en km entre dos nodos del grafo (heuristica admisible para A*)."""
    lat1 = G.nodes[nodo1]["y"]
    lon1 = G.nodes[nodo1]["x"]
    lat2 = G.nodes[nodo2]["y"]
    lon2 = G.nodes[nodo2]["x"]
    return calcular_distancia_haversine(lat1, lon1, lat2, lon2) / 1000


def bfs(G, origen, destino, mostrar_mensajes=False):
    """Breadth-First Search: camino mas corto en numero de nodos."""
    if mostrar_mensajes:
        print("\n  [BFS] Iniciando busqueda en anchura...")
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
    """Depth-First Search: explora exhaustivamente en profundidad."""
    if mostrar_mensajes:
        print("\n  [DFS] Iniciando busqueda en profundidad...")
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


def a_estrella(G, origen, destino, mostrar_mensajes=False):
    """
    A* con f(n) = g(n) + h(n).

    g(n): km reales acumulados desde origen hasta n
    h(n): km estimados por Haversine desde n hasta destino
    """
    if mostrar_mensajes:
        print("\n  [A*] Iniciando busqueda informada con heuristica Haversine...")
    frontera = [(0, [origen])]
    visitados = set()
    nodos_explorados = 0
    while frontera:
        costo, camino = heapq.heappop(frontera)
        nodo = camino[-1]
        nodos_explorados += 1
        if nodo == destino:
            distancia_total = sum(
                heuristica_haversine(G, camino[i], camino[i + 1])
                for i in range(len(camino) - 1)
            )
            if mostrar_mensajes:
                print(
                    f"  [A*] Camino optimo encontrado!"
                    f" ({len(camino)} nodos, {distancia_total:.2f} km,"
                    f" explorados: {nodos_explorados})"
                )
            return camino
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in G.neighbors(nodo):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                g = costo + heuristica_haversine(G, nodo, vecino)
                h = heuristica_haversine(G, vecino, destino)
                heapq.heappush(frontera, (g + h, nuevo_camino))
    if mostrar_mensajes:
        print(f"  [A*] No existe camino (explorados: {nodos_explorados})")
    return []


# Alias para compatibilidad con codigo existente
astar = a_estrella
