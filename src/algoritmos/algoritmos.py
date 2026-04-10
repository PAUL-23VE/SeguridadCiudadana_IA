"""
algoritmos.py
============
Módulo con algoritmos de búsqueda: BFS, DFS, A* sobre el grafo OSM.
Estos algoritmos analizan la estructura urbana del mapa real.
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


def bfs(G, origen, destino, verbose=False):
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
    verbose : bool
        Si True, imprime información del proceso
    
    Retorna
    -------
    list : lista de nodos que forman el camino, o [] si no existe
    """
    if verbose:
        print("\n  [BFS] Iniciando búsqueda en anchura...")
    
    visitados = set()
    cola = deque([[origen]])
    nodos_explorados = 0
    
    while cola:
        camino = cola.popleft()
        nodo = camino[-1]
        nodos_explorados += 1
        
        if nodo == destino:
            if verbose:
                print(f"  [BFS] ✅ Camino encontrado! ({len(camino)} nodos, explorados: {nodos_explorados})")
            return camino
            
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in G.neighbors(nodo):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)
    
    if verbose:
        print(f"  [BFS] ❌ No existe camino (explorados: {nodos_explorados})")
    return []


def dfs(G, origen, destino, verbose=False):
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
    verbose : bool
        Si True, imprime información del proceso
    
    Retorna
    -------
    list : lista de nodos que forman el camino, o [] si no existe
    """
    if verbose:
        print("\n  [DFS] Iniciando búsqueda en profundidad...")
    
    visitados = set()
    pila = [[origen]]
    nodos_explorados = 0
    
    while pila:
        camino = pila.pop()
        nodo = camino[-1]
        nodos_explorados += 1
        
        if nodo == destino:
            if verbose:
                print(f"  [DFS] ✅ Camino encontrado! ({len(camino)} nodos, explorados: {nodos_explorados})")
            return camino
            
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in G.neighbors(nodo):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                pila.append(nuevo_camino)
    
    if verbose:
        print(f"  [DFS] ❌ No existe camino (explorados: {nodos_explorados})")
    return []


def heuristica_haversine(G, nodo1, nodo2):
    """Heurística de distancia real entre dos nodos (en km)"""
    lat1, lon1 = G.nodes[nodo1]['y'], G.nodes[nodo1]['x']
    lat2, lon2 = G.nodes[nodo2]['y'], G.nodes[nodo2]['x']
    return calcular_distancia_haversine(lat1, lon1, lat2, lon2) / 1000  # Convertir a km


def astar(G, origen, destino, verbose=False):
    """
    A* (A-Star) - Búsqueda Informada con Heurística de Haversine
    
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
    verbose : bool
        Si True, imprime información del proceso
    
    Retorna
    -------
    list : lista de nodos que forman el camino óptimo, o [] si no existe
    """
    if verbose:
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
            if verbose:
                print(f"  [A*] ✅ Camino óptimo encontrado! ({len(camino)} nodos, {distancia_total:.2f} km, explorados: {nodos_explorados})")
            return camino
            
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in G.neighbors(nodo):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                heur = heuristica_haversine(G, vecino, destino)
                heapq.heappush(frontera, (costo + 1 + heur, nuevo_camino))
    
    if verbose:
        print(f"  [A*] ❌ No existe camino (explorados: {nodos_explorados})")
    return []


def analizar_conectividad_zona(G, zona_lat, zona_lon, radio_metros=500):
    """
    Analiza la conectividad de una zona específica usando BFS.
    
    Cuenta cuántos nodos (intersecciones) son alcanzables desde el centro
    de la zona dentro de un radio determinado.
    
    Parámetros
    ----------
    G : networkx.Graph
        Grafo del mapa urbano
    zona_lat, zona_lon : float
        Coordenadas del centro de la zona
    radio_metros : float
        Radio de análisis en metros
    
    Retorna
    -------
    dict : {
        'nodos_alcanzables': int,
        'conectividad': str ('Baja', 'Media', 'Alta'),
        'factor_riesgo': float (0.0 - 1.0)
    }
    """
    # Encontrar el nodo más cercano al centro de la zona
    nodo_centro = None
    distancia_minima = float('inf')
    
    for nodo, datos in G.nodes(data=True):
        if 'x' in datos and 'y' in datos:
            dist = calcular_distancia_haversine(
                zona_lat, zona_lon,
                datos['y'], datos['x']
            )
            if dist < distancia_minima:
                distancia_minima = dist
                nodo_centro = nodo
    
    if nodo_centro is None:
        return {
            'nodos_alcanzables': 0,
            'conectividad': 'Desconocida',
            'factor_riesgo': 0.5
        }
    
    # BFS desde el nodo centro, contando nodos dentro del radio
    visitados = {nodo_centro}
    cola = deque([nodo_centro])
    nodos_alcanzables = 0
    
    while cola:
        nodo_actual = cola.popleft()
        nodos_alcanzables += 1
        
        for vecino in G.neighbors(nodo_actual):
            if vecino not in visitados:
                # Verificar si está dentro del radio
                lat = G.nodes[vecino]['y']
                lon = G.nodes[vecino]['x']
                dist = calcular_distancia_haversine(zona_lat, zona_lon, lat, lon)
                
                if dist <= radio_metros:
                    visitados.add(vecino)
                    cola.append(vecino)
    
    # Clasificar conectividad
    if nodos_alcanzables < 10:
        conectividad = 'Baja'
        factor_riesgo = 0.8  # Mayor riesgo
    elif nodos_alcanzables < 30:
        conectividad = 'Media'
        factor_riesgo = 0.5
    else:
        conectividad = 'Alta'
        factor_riesgo = 0.2  # Menor riesgo
    
    return {
        'nodos_alcanzables': nodos_alcanzables,
        'conectividad': conectividad,
        'factor_riesgo': factor_riesgo
    }
