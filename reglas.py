"""
reglas.py
=========
Módulo para minería de reglas Apriori y PRISM sobre el dataset de zonas.
"""
import numpy as np

def reglas_apriori(dataset):
    # Placeholder: retorna una regla simulada
    return ["SI robos > 50 Y vandalismo > 20 → riesgo alto"]

def reglas_prism(dataset):
    # Placeholder: retorna una regla simulada
    return ["SI microtrafico = medio Y accidentes = alto → riesgo medio"]
def obtener_regla_explicativa(datos, nivel):
    """
    Retorna una regla explicativa según el nivel de riesgo calculado.
    """
    if nivel == 'Alto':
        return reglas_apriori([datos])[0]
    elif nivel == 'Medio':
        return reglas_prism([datos])[0]
    else:
        return "Sin regla relevante para nivel de riesgo bajo"