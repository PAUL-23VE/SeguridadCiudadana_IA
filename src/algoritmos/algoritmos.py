"""
algoritmos.py
============
Módulo de compatibilidad - Re-exporta funciones de los nuevos módulos.

DEPRECADO: Este archivo se mantiene solo por compatibilidad con código antiguo.
Usa directamente los módulos especializados:
- busqueda.py: Algoritmos BFS, DFS, A*
- conectividad.py: Análisis de conectividad urbana

Importa desde este archivo solo si necesitas compatibilidad con código antiguo.
"""

# Re-exportar funciones de los nuevos módulos para compatibilidad
from .busqueda import (
    bfs, 
    dfs, 
    astar, 
    calcular_distancia_haversine, 
    heuristica_haversine
)
from .conectividad import analizar_conectividad_zona

# Lista de funciones públicas
__all__ = [
    'bfs',
    'dfs', 
    'astar',
    'calcular_distancia_haversine',
    'heuristica_haversine',
    'analizar_conectividad_zona'
]
