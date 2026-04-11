# 🏙️ Sistema de Seguridad Ciudadana IA - Ambato

Sistema inteligente para análisis de seguridad ciudadana en Ambato, Ecuador, utilizando 7 algoritmos de Inteligencia Artificial y datos geográficos reales.

## 🎯 Características

- **Análisis completo** de todas las zonas de Ambato
- **Análisis específico** de zonas circulares con radio ajustable
- **7 algoritmos de IA** integrados para diagnóstico preciso
- **Mapas interactivos** HTML con visualización de resultados
- **Gráficas persistentes** para presentaciones

## 🧠 Algoritmos de IA Implementados

1. **Lógica Difusa** - Análisis de membresía y reglas difusas
2. **Algoritmo Genético** - Optimización evolutiva de parámetros  
3. **Redes Neuronales** - Clasificación y predicción avanzada
4. **Árboles de Decisión** - Análisis de factores de riesgo
5. **Análisis de Clustering** - Agrupación de zonas similares
6. **Regresión Logística** - Probabilidad de incidentes
7. **Sistema de Reglas** - Motor de inferencia y diagnosis

## 🎲 Simulación Monte Carlo

Sistema de generación de datos sintéticos basados en datos históricos de 4 macro-zonas:

- **📊 Datos históricos**: 240 registros (12 meses × 5 variables × 4 zonas)
- **🎯 Macro-zonas**: Norte, Sur, Este, Oeste (división automática)
- **🔢 Variables**: Robos, Microtráfico, Vandalismo, Accidentes, Llamadas 911
- **📈 Visualización**: Histogramas y scatter plots de simulaciones

### Visualización de Simulaciones

```python
from src.utils import obtener_gestor
from src.algoritmos.montecarlo import visualizar_simulaciones_montecarlo

# Cargar datos históricos
gestor = obtener_gestor()
stats = gestor.obtener_estadisticas('Norte')

# Generar visualización
resultado = visualizar_simulaciones_montecarlo(
    zona='Norte',
    estadisticas=stats,
    num_simulaciones=1000,
    guardar_path='simulacion.png'
)
```

**🎨 Elementos visualizados:**
- 📊 Histogramas de distribución
- 🟨 Área sombreada del rango histórico
- 🟢 Media histórica (línea verde)
- 🔵 Media simulada (línea azul)
- 🔴 Límites min/max históricos

**📁 Scripts de ejemplo:**
- `demo_visual.py` - Demostración rápida
- `ejemplo_visualizacion_montecarlo.py` - Ejemplos completos
- `test_visualizacion.py` - Tests automatizados

Ver documentación completa: `docs/VISUALIZACION_MONTECARLO.md`

## 📁 Estructura del Proyecto

```
SeguridadCiudadana_IA/
├── main.py                 # Programa principal
├── config.py              # Configuración
├── requirements.txt       # Dependencias
│
├── src/
│   ├── algoritmos/         # Algoritmos de IA
│   │   ├── algoritmos.py   # BFS, DFS, A*
│   │   ├── genetico.py     # Algoritmo genético
│   │   ├── reglas.py       # Sistemas de reglas
│   │   └── difuso.py       # Lógica difusa
│   │
│   ├── core/              # Núcleo del sistema
│   │   ├── diagnostico.py # Motor de diagnóstico
│   │   ├── mapa.py        # Procesamiento de mapas
│   │   └── visualizacion.py # Visualizaciones
│   │
│   └── utils/             # Utilidades
│       └── datos.py       # Generación de datos
│
├── data/                  # Datos y caché
├── output/               # Resultados generados
└── docs/                 # Documentación
```
│   └── mapa_*.html           # Mapas de calor con resultados
## 🚀 Instalación y Uso

### **Requisitos**
- Python 3.8+
- Internet (para descarga de mapas)

### **Instalación**
```cmd
# Clonar o descargar el proyecto
cd SeguridadCiudadana_IA

# Instalar dependencias
pip install -r requirements.txt
```

### **Ejecución**
```cmd
python main.py
```

### **Modos de Análisis**

**🔍 Modo 1: Análisis Completo**
- Analiza todas las zonas de Ambato
- Genera mapa HTML interactivo 
- Mantiene gráficas de matplotlib abiertas

**🎯 Modo 2: Análisis de Zona Específica**
- Abre mapa interactivo para seleccionar zona
- Permite ajustar radio de análisis (50-500m)
- Analiza solo zonas dentro del círculo seleccionado

## 📊 Niveles de Riesgo

- 🔴 **Alto**: Zonas con alta probabilidad de incidentes
- 🟡 **Medio**: Zonas con riesgo moderado  
- 🟢 **Bajo**: Zonas seguras con bajo riesgo

## 🛠️ Tecnologías

- **Python** - Lenguaje principal
- **OSMnx** - Descarga y análisis de mapas OpenStreetMap
- **NetworkX** - Procesamiento de grafos
- **Matplotlib** - Visualizaciones y gráficas
- **Folium** - Mapas interactivos HTML
- **Tkinter** - Interfaz de selección de zonas
- **NumPy/SciPy** - Cálculos científicos
- **Scikit-learn** - Algoritmos de machine learning

## 📝 Licencia

Proyecto académico para análisis de seguridad ciudadana.
- **Defuzzificación**: Centroide
- **Salida**: Valor de peligro [0-100] y clasificación (Bajo/Medio/Alto)

---

## 🔄 Flujo del Sistema

```
1. main.py
   ↓
2. Cargar mapa OSM de la ciudad (mapa.py)
   ↓
3. Crear grafo G de nodos urbanos
   ↓
4. diagnostico_masivo() → Para cada nodo:
   ↓
   4.1 Generar características sintéticas (datos.py)
   ↓
   4.2 Optimizar pesos con Algoritmo Genético (genetico.py)
   ↓
   4.3 Clasificar con Lógica Difusa (difuso.py)
   ↓
   4.4 Generar reglas Apriori y PRISM (reglas.py)
   ↓
   4.5 Analizar conectividad con BFS (algoritmos.py)
   ↓
5. Generar mapa HTML con visualización (visualizacion.py)
```

---

## 🚀 Instalación

### Requisitos
- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, Linux, macOS
- **RAM**: 4GB mínimo (8GB recomendado)
- **Conexión a Internet**: Para descargar mapas de OpenStreetMap

### Dependencias

Instala todas las dependencias con un solo comando:

```bash
pip install -r requirements.txt
```

Dependencias principales:
- `osmnx` - Descarga y análisis de mapas urbanos
- `networkx` - Procesamiento de grafos
- `folium` - Visualización de mapas interactivos
- `scikit-fuzzy` - Lógica difusa
- `numpy` - Computación numérica
- `scikit-learn` - Algoritmo Genético

### Instalación paso a paso

1. **Clonar el repositorio** (o descargar el proyecto):
   ```bash
   git clone <url-repositorio>
   cd SeguridadCiudadana_IA
   ```

2. **Crear entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv venv
   
   # Activar entorno virtual:
   # Windows:
   venv\Scripts\activate
   
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
   
   *Nota: La instalación puede tomar 2-5 minutos (osmnx es grande)*

4. **Ejecutar el sistema**:
   ```bash
   python main.py
   ```

---
## 💻 Uso

### Ejecución

```bash
python main.py
```

El sistema te guiará automáticamente a través del proceso:

1. ✅ Muestra el banner de bienvenida
2. ✅ Lista las ciudades disponibles de Ecuador
3. ✅ Solicita la ciudad a analizar
4. ✅ Descarga el mapa desde OpenStreetMap
5. ✅ Ejecuta los 7 algoritmos de IA
6. ✅ Genera el mapa HTML interactivo
7. ✅ Muestra el resumen de resultados

### Ejemplo de sesión

```
$ python main.py

======================================================================
  🚨 SISTEMA DE DIAGNÓSTICO DE ZONAS DE PELIGRO URBANO CON IA
======================================================================
  📍 Universidad Politécnica Salesiana
  🧠 7 Algoritmos de IA: BFS, DFS, A*, AG, Apriori, PRISM, Fuzzy
  🗺️  Mapas reales de Ecuador (OpenStreetMap)
======================================================================

  Ingresa la ciudad a analizar: Quito

  📥 CARGANDO MAPA...
  ✅ Mapa cargado: 15,342 nodos, 23,891 calles
  
  🧠 APLICANDO ALGORITMOS DE IA...
  ✅ 900 zonas analizadas
  
  🗺️  MAPA GENERADO: output/mapa_Quito_Ecuador.html
  
  📈 RESUMEN:
     🟢 Bajo:  300 zonas (33.3%)
     🟡 Medio: 400 zonas (44.4%)
     🔴 Alto:  200 zonas (22.2%)
```
7. Muestra el resumen de resultados

### Configuración personalizada

Editar `config.py`:

```python
# Ciudades a procesar
CIUDADES = [
    "Quito, Ecuador",
    "Guayaquil, Ecuador",
    # Agregar más ciudades...
]

# Tamaño de la grilla para análisis
GRID_SIZE = (30, 30)  # 30x30 = 900 zonas por ciudad
### Cambiar ciudad sin ejecutar interactivamente

Si quieres procesar una ciudad sin el modo interactivo, edita directamente `main.py` en la función `main()`:

```python
# En lugar de solicitar_ciudad(), usa directamente:
ciudad = "Cuenca, Ecuador"
``` 'tasa_cruce': 0.7
}

# Parámetros de Apriori
APRIORI_CONFIG = {
    'min_soporte': 0.1,
    'min_confianza': 0.7
}

# Parámetros de PRISM
PRISM_CONFIG = {
    'min_confianza': 0.5
}
```

### Procesar una ciudad específica

Modificar `main.py`:

```python
if __name__ == "__main__":
    ciudad = "Cuenca, Ecuador"
    resultado = diagnostico_masivo(ciudad)
    print(f"Mapa generado: output/mapa_{ciudad.replace(', ', '_')}.html")
```

---

## 📊 Salida del Sistema

### Mapas HTML interactivos

Cada mapa generado incluye:
- **Marcadores de zonas**: Coloreados según nivel de peligro
  - 🟢 **Verde**: Bajo
  - 🟡 **Amarillo**: Medio
  - 🔴 **Rojo**: Alto
- **Información emergente**: Click en cada zona para ver:
  - Clasificación (Bajo/Medio/Alto)
  - Puntaje de peligro (0-100)
  - Reglas aplicadas (Apriori/PRISM)
  - Conectividad (nodos alcanzables)
- **Mapa de calor**: Visualización de densidad de peligro

### Salida de consola

Ejemplo:
```
========================================
CIUDAD: Quito, Ecuador
========================================

Zona 1 (lat: -0.1807, lon: -78.4678):
  Clasificación: Alto
  Puntaje: 85.3
  Reglas aplicadas:
    - Apriori: SI densidad_baja Y pocos_comercios ENTONCES peligro_alto (conf: 0.85)
    - PRISM: SI densidad='Baja' ENTONCES clase_Alto (conf: 0.75)
  Conectividad: 12 nodos alcanzables en 500m

----------------------------------------

Mapa generado exitosamente en: output/mapa_Quito_Ecuador.html
```

---

## ⚙️ Configuración Técnica

### Parámetros del sistema

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `GRID_SIZE` | (30, 30) | Grilla de análisis (900 zonas) |
| `RADIO_CONECTIVIDAD` | 500 m | Radio de búsqueda BFS |
| `GENETICO.generaciones` | 50 | Iteraciones del AG |
| `GENETICO.poblacion` | 30 | Individuos por generación |
| `GENETICO.tasa_mutacion` | 0.1 | Probabilidad de mutación |
| `GENETICO.tasa_cruce` | 0.7 | Probabilidad de cruce |
| `APRIORI.min_soporte` | 0.1 | Soporte mínimo (10%) |
| `APRIORI.min_confianza` | 0.7 | Confianza mínima (70%) |
| `PRISM.min_confianza` | 0.5 | Confianza mínima (50%) |

### Funciones de membresía difusa

**Densidad de edificios** (edificios/km²):
- Baja: [0, 0, 50, 100]
- Media: [50, 100, 150, 200]
- Alta: [150, 200, 300, 300]

**Conectividad vial** (índice 0-1):
- Mala: [0, 0, 0.3, 0.5]
- Regular: [0.3, 0.5, 0.7]
- Buena: [0.5, 0.7, 1, 1]

**Comercios y Servicios** (cantidad):
- Pocos: [0, 0, 10, 20]
- Algunos: [10, 20, 30, 40]
- Muchos: [30, 40, 100, 100]

---

## 🏙️ Ciudades de Ecuador Incluidas

El sistema está configurado para procesar 16 ciudades principales:

1. Quito
2. Guayaquil
3. Cuenca
4. Santo Domingo
5. Machala
6. Durán
7. Manta
8. Portoviejo
9. Loja
10. Ambato
11. Esmeraldas
12. Quevedo
13. Riobamba
14. Milagro
15. Ibarra
16. La Libertad

Los mapas se descargan automáticamente de OpenStreetMap y se cachean en `data/cache/`.

---

## 📖 Documentación Técnica

### Módulo: `src/algoritmos/algoritmos.py`

**Funciones principales**:

```python
def bfs(G, nodo_inicio, max_distancia=500):
    """Búsqueda en anchura desde un nodo.
    
    Args:
        G: Grafo NetworkX
        nodo_inicio: Nodo de inicio
        max_distancia: Distancia máxima en metros
        
    Returns:
        set: Nodos alcanzables
    """

def dfs(G, nodo_inicio, visitados=None):
    """Búsqueda en profundidad.
    
    Args:
        G: Grafo NetworkX
        nodo_inicio: Nodo de inicio
        visitados: Set de nodos visitados
        
    Returns:
        set: Nodos alcanzables
    """

def astar(G, nodo_inicio, nodo_fin):
    """Búsqueda A* de camino óptimo.
    
    Args:
        G: Grafo NetworkX
        nodo_inicio: Nodo de inicio
        nodo_fin: Nodo destino
        
    Returns:
        list: Camino óptimo
    """

def analizar_conectividad_zona(G, nodos_zona, radio=500):
    """Analiza conectividad de una zona usando BFS.
    
    Args:
        G: Grafo NetworkX
        nodos_zona: Lista de nodos de la zona
        radio: Radio de búsqueda en metros
        
    Returns:
        dict: {
            'nodos_alcanzables': int,
            'nodos_cercanos': list
        }
    """
```

### Módulo: `src/algoritmos/genetico.py`

**Función principal**:

```python
def optimizar_pesos(ejemplos, generaciones=50, poblacion=30):
    """Optimiza pesos usando Algoritmo Genético.
    
    Args:
        ejemplos: Lista de tuplas (caracteristicas, clase)
        generaciones: Número de generaciones
        poblacion: Tamaño de la población
        
    Returns:
        list: Pesos optimizados [w1, w2, w3, w4]
    """
```

### Módulo: `src/algoritmos/reglas.py`

**Funciones principales**:

```python
def reglas_apriori(dataset=None, min_soporte=0.1, min_confianza=0.7):
    """Genera reglas de asociación con Apriori.
    
    Args:
        dataset: Lista de transacciones
        min_soporte: Soporte mínimo
        min_confianza: Confianza mínima
        
    Returns:
        list: Reglas generadas
    """

def reglas_prism(dataset=None, min_confianza=0.5):
    """Genera reglas de clasificación con PRISM.
    
    Args:
        dataset: Lista de ejemplos (caracteristicas, clase)
        min_confianza: Confianza mínima
        
    Returns:
        list: Reglas por clase
    """

def obtener_regla_explicativa(caracteristicas, clasificacion, reglas_apriori, reglas_prism):
    """Obtiene la mejor regla que explica la clasificación.
    
    Args:
        caracteristicas: Dict con características de la zona
        clasificacion: Clase asignada
        reglas_apriori: Reglas de Apriori
        reglas_prism: Reglas de PRISM
        
    Returns:
        str: Regla explicativa
    """
```

### Módulo: `src/algoritmos/difuso.py`

**Función principal**:

```python
def clasificar_difuso(densidad, conectividad, comercios, servicios):
    """Clasifica zona usando lógica difusa.
    
    Args:
        densidad: Densidad de edificios (0-300)
        conectividad: Índice de conectividad (0-1)
        comercios: Número de comercios (0-100)
        servicios: Número de servicios (0-100)
        
    Returns:
        tuple: (clasificacion, puntaje)
            clasificacion: 'Bajo', 'Medio', 'Alto'
            puntaje: Valor numérico 0-100
    """
```

### Módulo: `src/core/diagnostico.py`

**Funciones principales**:

```python
def diagnosticar_zona(lat, lon, G):
    """Diagnostica una zona específica.
    
    Args:
        lat: Latitud
        lon: Longitud
        G: Grafo NetworkX de la ciudad
        
    Returns:
        dict: {
            'coordenadas': (lat, lon),
            'clasificacion': str,
            'puntaje': float,
            'regla': str,
            'conectividad': int
        }
    """

def diagnostico_masivo(ciudad):
    """Procesa una ciudad completa.
    
    Args:
        ciudad: Nombre de la ciudad (ej: "Quito, Ecuador")
        
    Returns:
        dict: Resultados del diagnóstico
    """
```

### Módulo: `src/core/mapa.py`

**Función principal**:

```python
def cargar_mapa(ciudad, usar_cache=True):
    """Carga mapa de OpenStreetMap.
    
    Args:
        ciudad: Nombre de la ciudad
        usar_cache: Si usar caché local
        
    Returns:
        networkx.Graph: Grafo de calles de la ciudad
    """
```

### Módulo: `src/core/visualizacion.py`

**Función principal**:

```python
def generar_mapa_html(resultados, ciudad, G):
    """Genera mapa HTML interactivo.
    
    Args:
        resultados: Lista de diagnósticos
        ciudad: Nombre de la ciudad
        G: Grafo NetworkX
        
    Returns:
        str: Ruta del archivo HTML generado
    """
```

---

## 🛠️ Solución de Problemas

### Error: "NetworkXNoPath"
**Causa**: No existe camino entre dos nodos en A*.  
**Solución**: El sistema maneja la excepción automáticamente.

### Error: "No se encontró el mapa en caché"
**Causa**: Primera ejecución o caché eliminado.  
**Solución**: El sistema descarga automáticamente de OSM.

### Error: "MemoryError" al procesar ciudades grandes
**Causa**: Grid demasiado grande o RAM insuficiente.  
**Solución**: Reducir `GRID_SIZE` en `config.py` (ej: (20, 20)).

### Mapas HTML no se generan
**Causa**: Carpeta `output/` no existe.  
**Solución**: El sistema crea la carpeta automáticamente.

### Rendimiento lento
**Solución**:
- Reducir número de generaciones del AG
- Disminuir tamaño de población
- Usar grilla más pequeña

---

## 📚 Referencias

### Algoritmos implementados
- **BFS/DFS**: Cormen, T. H., et al. "Introduction to Algorithms" (4th ed., 2022)
- **A\***: Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"
- **Algoritmo Genético**: Holland, J. H. (1975). "Adaptation in Natural and Artificial Systems"
- **Apriori**: Agrawal, R., & Srikant, R. (1994). "Fast Algorithms for Mining Association Rules"
- **PRISM**: Cendrowska, J. (1987). "PRISM: An Algorithm for Inducing Modular Rules"
- **Lógica Difusa**: Zadeh, L. A. (1965). "Fuzzy Sets"

### Bibliotecas utilizadas
- **OSMnx**: Boeing, G. (2017). "OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks"
- **NetworkX**: Hagberg, A. A., et al. (2008). "Exploring Network Structure, Dynamics, and Function using NetworkX"
- **Folium**: Python bindings for Leaflet.js
- **scikit-fuzzy**: Fuzzy logic toolkit for Python

---

## 👨‍💻 Desarrollo

### Estructura de paquetes

El proyecto sigue una arquitectura modular:

- **`src/algoritmos/`**: Lógica de IA (independiente del dominio)
- **`src/core/`**: Lógica de negocio (dominio urbano)
- **`src/utils/`**: Utilidades comunes

### Agregar nuevas ciudades

Editar `config.py`:

```python
CIUDADES = [
    "Quito, Ecuador",
    "Guayaquil, Ecuador",
    "NuevaCiudad, Ecuador"  # Agregar aquí
]
```

### Agregar nuevos algoritmos

1. Crear archivo en `src/algoritmos/`
2. Implementar función principal
3. Exportar en `src/algoritmos/__init__.py`
4. Integrar en `src/core/diagnostico.py`

---

## 📄 Licencia

Este proyecto fue desarrollado con fines académicos para el curso de Inteligencia Artificial.

**Institución**: Universidad Politécnica Salesiana  
**Curso**: Inteligencia Artificial  
**Semestre**: Séptimo  
**Año**: 2024

---

## 🤝 Contribuciones

Proyecto académico. Para sugerencias o mejoras, contactar a los autores.

---

## 📞 Contacto

**Autor**: Paul Vacacela  
**Proyecto**: Sistema de Diagnóstico de Zonas de Peligro Urbano  
**Universidad**: Universidad Politécnica Salesiana

---

## 🎯 Funcionalidades Destacadas

✅ **7 algoritmos de IA integrados** (BFS, DFS, A*, AG, Apriori, PRISM, Fuzzy)  
✅ **Mapas reales** de 16 ciudades de Ecuador  
✅ **Visualizaciones interactivas** con Folium  
✅ **Sistema de caché** para mapas OSM  
✅ **Configuración centralizada** en `config.py`  
✅ **Arquitectura modular** y escalable  
✅ **Reglas explicativas** para cada clasificación  
✅ **Análisis de conectividad** urbana  
✅ **Optimización automática** de parámetros con AG  

---

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~2000
- **Módulos**: 10
- **Algoritmos**: 7
- **Ciudades procesables**: 16
- **Zonas por ciudad**: 900 (30x30)
- **Tiempo de procesamiento**: ~30-60 seg/ciudad
- **Formato de salida**: HTML interactivo

---

**¡Sistema listo para uso académico y demostración! 🚀**
