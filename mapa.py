"""
mapa.py
=======
Módulo para descargar y procesar mapas reales de ciudades o países usando OSMnx.
"""
import osmnx as ox
import networkx as nx

def cargar_mapa(ciudad):
    print(f"[Mapa] Descargando mapa de: {ciudad} ...")
    G = ox.graph_from_place(ciudad, network_type='drive')
    nodes = ox.graph_to_gdfs(G, edges=False)
    north = nodes.geometry.y.max()
    south = nodes.geometry.y.min()
    east = nodes.geometry.x.max()
    west = nodes.geometry.x.min()
    bbox = (north, south, east, west)
    return G, bbox

def construir_grid(G, bbox, filas=30, columnas=30):
    import numpy as np
    north, south, east, west = bbox
    lat_step = (north - south) / filas
    lon_step = (east - west) / columnas
    grid = np.zeros((filas, columnas), dtype=object)
    zonas = []
    for i in range(filas):
        for j in range(columnas):
            lat_c = north - (i + 0.5) * lat_step
            lon_c = west + (j + 0.5) * lon_step
            grid[i, j] = {'lat': lat_c, 'lon': lon_c}
            zonas.append((i, j))
    return grid, zonas
