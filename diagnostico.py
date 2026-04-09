"""
diagnostico.py
==============
Módulo para diagnóstico de zonas usando lógica difusa, algoritmo genético, Apriori y PRISM.
"""
import numpy as np
from difuso import clasificar_difuso
from genetico import optimizar_pesos
from reglas import obtener_regla_explicativa

def diagnostico_masivo(grid, zonas):
    resultados = {}
    for (i, j) in zonas:
        resultados[(i, j)] = diagnosticar_zona(grid, i, j)
    return resultados

def diagnosticar_zona(grid, fila, col):
    # Simulación de datos: puedes reemplazar por datos reales o históricos
    datos = {
        'robos': np.random.randint(0, 100),
        'microtrafico': np.random.randint(0, 50),
        'vandalismo': np.random.randint(0, 80),
        'accidentes': np.random.randint(0, 60),
        'llamadas_emergencias': np.random.randint(0, 100)
    }
    metricas = {
        'densidad_calles': np.random.uniform(0, 500),
        'densidad_intersecciones': np.random.uniform(0, 300)
    }
    # Optimización de pesos con algoritmo genético
    pesos = optimizar_pesos(datos)
    # Diagnóstico con lógica difusa
    nivel, score = clasificar_difuso(datos, metricas, pesos)
    # Factores principales (top 2)
    factores = sorted(datos, key=datos.get, reverse=True)[:2]
    # Regla explicativa real (Apriori/PRISM)
    regla = obtener_regla_explicativa(datos, nivel)
    return {'nivel': nivel, 'factores': factores, 'regla': regla}