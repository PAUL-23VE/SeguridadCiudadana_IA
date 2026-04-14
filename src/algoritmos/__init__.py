"""
Módulos:
--------
- busqueda: Algoritmos de búsqueda en grafos (BFS, DFS, A*)
- conectividad: Análisis de conectividad urbana
- difuso: Lógica difusa para clasificación de riesgo
- genetico: Algoritmo genético para optimización de pesos
- reglas: Minería de reglas (Apriori, PRISM)
- montecarlo: Simulación Monte Carlo con datos históricos
"""

# Algoritmos de búsqueda en grafos
from .busqueda import bfs, dfs, a_estrella, astar, calcular_distancia_haversine, heuristica_haversine

# Análisis de conectividad urbana
from .conectividad import analizar_conectividad_zona

# Algoritmo genético para optimización
from .genetico import optimizar_pesos, calcular_fitness, crear_individuo

# Minería de reglas
from .reglas import (
    reglas_apriori, 
    reglas_prism, 
    obtener_regla_explicativa,
    discretizar_valor,
    apriori
)

# Lógica difusa
from .difuso import (
    clasificar_difuso, 
    mantener_graficas_abiertas,
    graficar_membresia,
    describir_membresia
)

# Monte Carlo
from .montecarlo import (
    generar_datos_zona,
    generar_datos_con_restricciones,
    generar_escenario_unico,
    visualizar_simulaciones_montecarlo,
    visualizar_scatter_montecarlo,
    visualizar_datos_historicos_reales
)

__all__ = [
    # Búsqueda
    'bfs', 'dfs', 'a_estrella', 'astar', 'calcular_distancia_haversine', 'heuristica_haversine',
    # Conectividad
    'analizar_conectividad_zona',# Genético
    'optimizar_pesos', 'calcular_fitness', 'crear_individuo',
    # Reglas
    'reglas_apriori', 'reglas_prism', 'obtener_regla_explicativa', 'discretizar_valor', 'apriori',
    # Difuso
    'clasificar_difuso', 'mantener_graficas_abiertas', 'graficar_membresia', 'describir_membresia',    # Monte Carlo
    'generar_datos_zona', 'generar_datos_con_restricciones', 'generar_escenario_unico',
    'visualizar_simulaciones_montecarlo', 'visualizar_scatter_montecarlo', 
    'visualizar_datos_historicos_reales'
]
