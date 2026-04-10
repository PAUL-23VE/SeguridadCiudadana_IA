"""
datos.py
========
Módulo para gestión de datos históricos o simulados para cada zona.
"""
import numpy as np

def obtener_datos_zona(fila, col):
    # Simulación de datos históricos (puedes conectar a una base real)
    return {
        'robos': np.random.randint(0, 100),
        'microtrafico': np.random.randint(0, 50),
        'vandalismo': np.random.randint(0, 80),
        'accidentes': np.random.randint(0, 60),
        'llamadas_emergencias': np.random.randint(0, 100)
    }

def obtener_metricas_zona(fila, col):
    # Simulación de métricas urbanas
    return {
        'densidad_calles': np.random.uniform(0, 500),
        'densidad_intersecciones': np.random.uniform(0, 300)
    }
