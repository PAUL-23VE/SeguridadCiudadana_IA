"""
difuso.py
=========
Módulo para clasificación de riesgo usando lógica difusa (scikit-fuzzy).
"""
def clasificar_difuso(datos, metricas, pesos=None):
    # Placeholder: score ponderado simple
    score = (
        datos['robos'] * (pesos['robos'] if pesos else 0.3) +
        datos['microtrafico'] * (pesos['microtrafico'] if pesos else 0.2) +
        datos['vandalismo'] * (pesos['vandalismo'] if pesos else 0.2) +
        datos['accidentes'] * (pesos['accidentes'] if pesos else 0.2) +
        datos['llamadas_emergencias'] * (pesos['llamadas_emergencias'] if pesos else 0.1)
    )
    if score >= 100:
        return 'Alto', score
    elif score >= 50:
        return 'Medio', score
    else:
        return 'Bajo', score
