"""
Paquete utils - Utilidades y funciones auxiliares
"""
from .historicos import (
    GestorHistoricos,
    obtener_gestor,
    identificar_zona,
    obtener_estadisticas_zona
)

__all__ = [
    'GestorHistoricos',
    'obtener_gestor',
    'identificar_zona',
    'obtener_estadisticas_zona'
]
