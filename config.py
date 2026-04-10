"""
config.py
=========
Configuración centralizada del Sistema de Diagnóstico de Zonas de Peligro Urbano

Este archivo contiene todos los parámetros configurables del sistema:
- Rutas de directorios
- Parámetros de algoritmos de IA
- Umbrales de clasificación
- Ciudades de Ecuador disponibles
"""
import os

# ============================================================================
# RUTAS DEL SISTEMA
# ============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CACHE_DIR = os.path.join(DATA_DIR, 'cache')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

# Crear directorios si no existen
for directory in [DATA_DIR, CACHE_DIR, OUTPUT_DIR, DOCS_DIR]:
    os.makedirs(directory, exist_ok=True)

# ============================================================================
# CIUDADES DE ECUADOR DISPONIBLES
# ============================================================================

CIUDADES_ECUADOR = [
    "Quito, Ecuador",
    "Guayaquil, Ecuador",
    "Cuenca, Ecuador",
    "Santo Domingo, Ecuador",
    "Machala, Ecuador",
    "Durán, Ecuador",
    "Manta, Ecuador",
    "Portoviejo, Ecuador",
    "Loja, Ecuador",
    "Ambato, Ecuador",
    "Esmeraldas, Ecuador",
    "Quevedo, Ecuador",
    "Riobamba, Ecuador",
    "Milagro, Ecuador",
    "Ibarra, Ecuador",
    "La Libertad, Ecuador"
]

# ============================================================================
# PARÁMETROS DEL GRID DE ANÁLISIS
# ============================================================================

GRID_SIZE = (30, 30)  # (Filas, Columnas) = 900 zonas por ciudad
RADIO_CONECTIVIDAD = 500  # Radio en metros para análisis BFS

# ============================================================================
# PARÁMETROS DEL ALGORITMO GENÉTICO
# ============================================================================

GENETICO_CONFIG = {
    'generaciones': 50,        # Número de generaciones
    'poblacion': 30,           # Tamaño de la población
    'tasa_mutacion': 0.1,      # Probabilidad de mutación (10%)
    'tasa_cruce': 0.7,         # Probabilidad de cruce (70%)
    'elitismo': 2,             # Mejores individuos a preservar
    'torneo_size': 3           # Tamaño del torneo para selección
}

# ============================================================================
# PARÁMETROS DE APRIORI (Reglas de Asociación)
# ============================================================================

APRIORI_CONFIG = {
    'min_soporte': 0.1,        # Soporte mínimo (10%)
    'min_confianza': 0.7       # Confianza mínima (70%)
}

# ============================================================================
# PARÁMETROS DE PRISM (Reglas de Clasificación)
# ============================================================================

PRISM_CONFIG = {
    'min_confianza': 0.5       # Confianza mínima (50%)
}

# ============================================================================
# PARÁMETROS DE LÓGICA DIFUSA
# ============================================================================

FUZZY_CONFIG = {
    # Rangos para densidad de edificios (edificios/km²)
    'densidad': {
        'baja': [0, 0, 50, 100],
        'media': [50, 100, 150, 200],
        'alta': [150, 200, 300, 300]
    },
    
    # Rangos para conectividad vial (índice 0-1)
    'conectividad': {
        'mala': [0, 0, 0.3, 0.5],
        'regular': [0.3, 0.5, 0.7],
        'buena': [0.5, 0.7, 1, 1]
    },
    
    # Rangos para comercios y servicios (cantidad)
    'comercios': {
        'pocos': [0, 0, 10, 20],
        'algunos': [10, 20, 30, 40],
        'muchos': [30, 40, 100, 100]
    },
    
    'servicios': {
        'pocos': [0, 0, 10, 20],
        'algunos': [10, 20, 30, 40],
        'muchos': [30, 40, 100, 100]
    }
}

# ============================================================================
# UMBRALES DE CLASIFICACIÓN DE RIESGO
# ============================================================================

UMBRALES_RIESGO = {
    'bajo': (0, 33),      # 0-33: Riesgo bajo 🟢
    'medio': (33, 66),    # 33-66: Riesgo medio 🟡
    'alto': (66, 100)     # 66-100: Riesgo alto 🔴
}

# ============================================================================
# CLASIFICACIÓN DE CONECTIVIDAD (nodos alcanzables)
# ============================================================================

CONECTIVIDAD_NIVELES = {
    'baja': (0, 10),           # 0-10 nodos
    'media': (10, 30),         # 10-30 nodos
    'alta': (30, float('inf')) # 30+ nodos
}

# ============================================================================
# COLORES PARA VISUALIZACIÓN DE MAPAS
# ============================================================================

COLORES_RIESGO = {
    'Bajo': '#2ecc71',    # Verde
    'Medio': '#f39c12',   # Amarillo/Naranja
    'Alto': '#e74c3c'     # Rojo
}

# ============================================================================
# CONFIGURACIÓN DE OpenStreetMap
# ============================================================================

OSM_CONFIG = {
    'network_type': 'drive',  # Tipo de red: 'drive', 'walk', 'bike', 'all'
    'timeout': 180,           # Timeout en segundos para descargas
    'max_query_area_size': 50000000  # Área máxima de consulta en m²
}

# ============================================================================
# CONFIGURACIÓN DE CACHÉ
# ============================================================================

CACHE_CONFIG = {
    'usar_cache': True,       # Usar mapas en caché
    'max_edad_dias': 30       # Edad máxima del caché en días
}

# ============================================================================
# MENSAJES DEL SISTEMA
# ============================================================================

MENSAJES = {
    'bienvenida': """
╔════════════════════════════════════════════════════════════════════╗
║  🚨 SISTEMA DE DIAGNÓSTICO DE ZONAS DE PELIGRO URBANO CON IA      ║
╚════════════════════════════════════════════════════════════════════╝
    """,
    'info': "📖 Documentación completa en README.md | Configuración en config.py"
}
