"""
algoritmos.py
============
Módulo con algoritmos de búsqueda: BFS, DFS, A*, Hill Climbing sobre el grafo OSM.
"""
import networkx as nx
import heapq

def bfs(G, origen, destino):
    from collections import deque
    visitados = set()
    cola = deque([[origen]])
    while cola:
        camino = cola.popleft()
        nodo = camino[-1]
        if nodo == destino:
            return camino
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in G.neighbors(nodo):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)
    return []

def dfs(G, origen, destino):
    visitados = set()
    pila = [[origen]]
    while pila:
        camino = pila.pop()
        nodo = camino[-1]
        if nodo == destino:
            return camino
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in G.neighbors(nodo):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                pila.append(nuevo_camino)
    return []

def heuristica_haversine(G, nodo1, nodo2):
    import math
    lat1, lon1 = G.nodes[nodo1]['y'], G.nodes[nodo1]['x']
    lat2, lon2 = G.nodes[nodo2]['y'], G.nodes[nodo2]['x']
    R = 6371  # km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def astar(G, origen, destino):
    frontera = [(0, [origen])]
    visitados = set()
    while frontera:
        costo, camino = heapq.heappop(frontera)
        nodo = camino[-1]
        if nodo == destino:
            return camino
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in G.neighbors(nodo):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                heur = heuristica_haversine(G, vecino, destino)
                heapq.heappush(frontera, (costo + 1 + heur, nuevo_camino))
    return []

def hill_climbing(G, camino, grid, zonas):
    # Placeholder: retorna el mismo camino (puedes mejorar para evitar zonas de alto riesgo)
    return camino
