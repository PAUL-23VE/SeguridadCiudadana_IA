"""
conectividad.py
===============
Análisis de conectividad urbana usando BFS

Este módulo analiza la estructura de conectividad de zonas urbanas
para identificar áreas con baja conectividad que pueden ser más riesgosas.

La conectividad se mide contando cuántos nodos (intersecciones) son
alcanzables desde el centro de una zona dentro de un radio determinado.
"""
from collections import deque
from .busqueda import calcular_distancia_haversine


def analizar_conectividad_zona(G, zona_lat, zona_lon, radio_metros=500):
    """
    Analiza la conectividad de una zona específica usando BFS.
    
    Cuenta cuántos nodos (intersecciones) son alcanzables desde el centro
    de la zona dentro de un radio determinado. Una baja conectividad puede
    indicar mayor riesgo de inseguridad.
    
    Parámetros
    ----------
    G : networkx.Graph
        Grafo del mapa urbano
    zona_lat, zona_lon : float
        Coordenadas del centro de la zona (latitud, longitud)
    radio_metros : float
        Radio de análisis en metros (default: 500m)
    
    Retorna
    -------
    dict : {
        'nodos_alcanzables': int,
        'conectividad': str ('Baja', 'Media', 'Alta'),
        'factor_riesgo': float (0.0 - 1.0)
    }
    
    Ejemplo
    -------
    >>> resultado = analizar_conectividad_zona(G, 4.6097, -74.0817, 500)
    >>> print(resultado)
    {'nodos_alcanzables': 25, 'conectividad': 'Media', 'factor_riesgo': 0.5}
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
    
    # Clasificar conectividad según número de nodos alcanzables
    if nodos_alcanzables < 10:
        conectividad = 'Baja'
        factor_riesgo = 0.8  # Mayor riesgo en zonas poco conectadas
    elif nodos_alcanzables < 30:
        conectividad = 'Media'
        factor_riesgo = 0.5
    else:
        conectividad = 'Alta'
        factor_riesgo = 0.2  # Menor riesgo en zonas bien conectadas
    
    return {
        'nodos_alcanzables': nodos_alcanzables,
        'conectividad': conectividad,
        'factor_riesgo': factor_riesgo
    }
