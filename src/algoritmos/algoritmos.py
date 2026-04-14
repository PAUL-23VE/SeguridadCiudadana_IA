"""
Re-exporta funciones de los nuevos módulos.

Usa directamente los módulos especializados:
- busqueda.py: Algoritmos BFS, DFS, A*
- conectividad.py: Análisis de conectividad urbana
"""
from .busqueda import (
    bfs, 
    dfs, 
    a_estrella,
    astar, 
    calcular_distancia_haversine, 
    heuristica_haversine
)
from .conectividad import analizar_conectividad_zona

# Lista de funciones públicas
__all__ = [
    'bfs',
    'dfs', 
    'a_estrella',
    'astar',
    'calcular_distancia_haversine',
    'heuristica_haversine',
    'analizar_conectividad_zona'
]
