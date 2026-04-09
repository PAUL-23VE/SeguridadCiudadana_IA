# 🔴 Sistema de Diagnóstico de Zonas Peligrosas con Inteligencia Artificial

**Proyecto Final de Inteligencia Artificial - Universidad**

Este proyecto determina si una zona urbana es peligrosa o no, usando algoritmos de inteligencia artificial sobre mapas reales de Ecuador. El sistema analiza factores urbanos, datos históricos y calcula el nivel de riesgo de forma automática y precisa.

---

## 📋 Objetivo del Proyecto

Desarrollar un sistema inteligente que:
- **Analice zonas urbanas** en mapas reales de ciudades de Ecuador usando OpenStreetMap
- **Determine el nivel de peligro** (Bajo, Medio, Alto) de cada zona
- **Explique el diagnóstico** mostrando factores principales y reglas encontradas
- **Visualice resultados** en un mapa interactivo con colores según el nivel de riesgo
- **Use múltiples algoritmos de IA** de forma integrada y justificada

---

## 🎯 Flujo Principal del Sistema

### 1. **Selección de Ciudad**
El usuario ingresa la ciudad o país a analizar (ej: "Ambato", "Quito", "Ecuador").

### 2. **Carga de Mapa Real**
El sistema descarga el mapa desde OpenStreetMap usando `osmnx` y lo guarda en caché para reutilización.

### 3. **Construcción del Grid**
El mapa se divide en una cuadrícula de 30×30 zonas para análisis detallado. Cada zona contiene:
- Coordenadas geográficas (latitud, longitud)
- Cantidad de nodos (intersecciones)
- Cantidad de calles
- Densidad urbana
- Conectividad

### 4. **Diagnóstico Masivo Automático**
El sistema analiza **todas las zonas** automáticamente usando:

#### **a) Lógica Difusa (scikit-fuzzy)**
- **Variables de entrada**: robos, vandalismo, microtráfico, accidentes, densidad de calles, densidad de intersecciones
- **Variables de salida**: nivel de riesgo (0-100)
- **Método**: Mamdani con defuzzificación por centroide
- **Funciones de membresía**: triangulares (bajo, medio, alto)
- **Reglas difusas**: 24 reglas que combinan factores delictivos y urbanos
- **Resultado**: Score de riesgo preciso entre 0 y 100

#### **b) Algoritmo Genético (optimización de pesos)**
- **Objetivo**: Optimizar los pesos de los factores para maximizar la precisión del diagnóstico
- **Población**: 30 individuos (conjuntos de pesos)
- **Generaciones**: 50 iteraciones
- **Operadores**: Selección por torneo, cruce de un punto, mutación gaussiana
- **Fitness**: Precisión de clasificación en dataset de prueba
- **Resultado**: Pesos óptimos para la lógica difusa

#### **c) Apriori (reglas de asociación)**
- **Objetivo**: Descubrir patrones frecuentes en los datos
- **Parámetros**: Soporte mínimo 0.10, confianza mínima 0.70
- **Dataset**: Zonas clasificadas con sus factores discretizados
- **Resultado**: Reglas como "SI robos=alto Y vandalismo=medio → riesgo=Alto (conf=0.95)"
- **Uso**: Explicar el diagnóstico con reglas comprensibles

#### **d) PRISM (inducción de reglas)**
- **Objetivo**: Generar reglas simples y precisas por clase
- **Método**: Covering algorithm (cubrir ejemplos clase por clase)
- **Parámetros**: Precisión mínima 0.85
- **Resultado**: 3-6 reglas simples por cada nivel de riesgo
- **Uso**: Proporcionar reglas alternativas y validar consistencia

### 5. **Visualización Interactiva**
El sistema muestra un mapa web interactivo (usando `folium`) donde:
- Cada zona está coloreada según su nivel de riesgo:
  - 🟢 **Verde**: Riesgo Bajo (score 0-30)
  - 🟠 **Naranja**: Riesgo Medio (score 30-60)
  - 🔴 **Rojo**: Riesgo Alto (score 60-100)
- El usuario puede hacer clic en una zona y seleccionar un radio
- Se muestran todas las zonas dentro del radio seleccionado

### 6. **Diagnóstico Detallado**
Para cada zona seleccionada, el sistema muestra:
- **Nombre del lugar** (barrio, calle) usando geocodificación inversa
- **Coordenadas** (latitud, longitud)
- **Nivel de riesgo**: Bajo / Medio / Alto
- **Factores principales**: Lista de variables que influyen más
- **Regla explicativa**: Regla Apriori o PRISM que justifica el diagnóstico
- **Emoji visual**: 🟢 🟠 🔴 según el nivel

---

## 🧠 Algoritmos de IA Implementados

### **1. Lógica Difusa (Fuzzy Logic)**
- **Módulo**: `difuso.py`
- **Librería**: `scikit-fuzzy`
- **Función**: `clasificar_zona_difusa(datos_zona)`
- **Justificación**: Permite manejar incertidumbre y valores imprecisos en los datos delictivos
- **Salida**: Score de riesgo [0-100] y nivel (Bajo/Medio/Alto)

### **2. Algoritmo Genético (Genetic Algorithm)**
- **Módulo**: `genetico.py`
- **Función**: `optimizar_pesos_genetico(dataset, poblacion=30, generaciones=50)`
- **Justificación**: Encuentra automáticamente los mejores pesos para maximizar la precisión de clasificación
- **Salida**: Diccionario de pesos óptimos para cada factor

### **3. Apriori (Association Rules)**
- **Módulo**: `reglas.py`
- **Librería**: `mlxtend`
- **Función**: `generar_reglas_apriori(dataset, min_support=0.10, min_confidence=0.70)`
- **Justificación**: Descubre patrones y relaciones entre factores de riesgo
- **Salida**: Lista de reglas con soporte, confianza y lift

### **4. PRISM (Rule Induction)**
- **Módulo**: `reglas.py`
- **Función**: `generar_reglas_prism(dataset, min_precision=0.85)`
- **Justificación**: Genera reglas simples y precisas para explicar cada nivel de riesgo
- **Salida**: Lista de reglas con precisión y cobertura

### **5. BFS (Breadth-First Search)**
- **Módulo**: `algoritmos.py`
- **Función**: `bfs(grafo, origen, destino)`
- **Justificación**: Búsqueda no informada para encontrar rutas entre zonas
- **Salida**: Lista de nodos en la ruta más corta (por cantidad de nodos)

### **6. DFS (Depth-First Search)**
- **Módulo**: `algoritmos.py`
- **Función**: `dfs(grafo, origen, destino)`
- **Justificación**: Búsqueda en profundidad para explorar conexiones entre zonas
- **Salida**: Lista de nodos en una ruta (puede no ser óptima)

### **7. A* (A-Star)**
- **Módulo**: `algoritmos.py`
- **Función**: `astar(grafo, origen, destino)`
- **Justificación**: Búsqueda informada con heurística de distancia Haversine
- **Salida**: Lista de nodos en la ruta óptima (distancia real)

### **8. Hill Climbing (Ascenso de Colinas)**
- **Módulo**: `algoritmos.py`
- **Función**: `hill_climbing(grafo, ruta_inicial, grid_riesgo)`
- **Justificación**: Optimización local para mejorar rutas evitando zonas peligrosas
- **Salida**: Ruta mejorada con menor riesgo promedio

---

## 📁 Estructura del Proyecto

```
SeguridadCiudadana_IA/
│
├── main.py                  # Flujo principal del sistema
├── mapa.py                  # Carga de mapas OSM y construcción de grid
├── datos.py                 # Generación de datos sintéticos y históricos
├── difuso.py                # Lógica difusa con scikit-fuzzy
├── genetico.py              # Algoritmo genético para optimización
├── reglas.py                # Apriori y PRISM para generación de reglas
├── algoritmos.py            # BFS, DFS, A*, Hill Climbing
├── diagnostico.py           # Lógica de diagnóstico y clasificación
├── visualizacion.py         # Mapas interactivos con folium
├── README.md                # Este archivo
├── cache/                   # Caché de mapas descargados
└── __pycache__/             # Archivos compilados de Python
```

---

## 🚀 Cómo Ejecutar el Proyecto

### **Requisitos Previos**
```bash
pip install osmnx networkx numpy pandas scikit-fuzzy mlxtend folium geopy matplotlib
```

### **Ejecución**
```bash
python main.py
```

### **Flujo de Uso**
1. Ingresa la ciudad (ej: "Ambato, Ecuador")
2. Espera a que se cargue el mapa y se realice el diagnóstico masivo
3. Se abrirá un mapa interactivo en tu navegador
4. Haz clic en una zona y selecciona el radio
5. El sistema mostrará el diagnóstico detallado de todas las zonas cercanas

---

## 📊 Resultados y Métricas

### **Precisión del Sistema**
- Lógica difusa baseline: ~68%
- Con pesos optimizados por algoritmo genético: ~83%
- Mejora: +15% de precisión

### **Reglas Generadas**
- Apriori: ~2490 reglas (soporte≥0.10, confianza≥0.70)
- PRISM: ~6 reglas (precisión≥0.85)

### **Ejemplo de Diagnóstico**
```
🔴 Parque Central, Ambato
   📍 Coordenadas: [12,15] - Lat: -1.2478, Lon: -78.6232
   ⚠️  Nivel de riesgo: Alto
   📊 Factores principales: robos, vandalismo, densidad_alta
   📜 Regla: SI robos=alto Y densidad_calles=alta → riesgo=Alto (conf=0.95)
```

---

## 🎓 Fundamentos Académicos

### **Por qué cada algoritmo**

1. **Lógica Difusa**: Maneja incertidumbre en datos delictivos imprecisos
2. **Algoritmo Genético**: Optimiza automáticamente los pesos del sistema
3. **Apriori**: Descubre patrones y relaciones ocultas en los datos
4. **PRISM**: Genera reglas explicativas simples y precisas
5. **BFS/DFS/A*/Hill Climbing**: Calculan rutas seguras y analizan conectividad urbana

### **Integración de Algoritmos**
- El algoritmo genético **optimiza** la lógica difusa
- Apriori y PRISM **explican** el diagnóstico generado por lógica difusa
- Los algoritmos de búsqueda **complementan** el análisis con rutas y conectividad

---

## 👨‍💻 Autor

**Proyecto Final de Inteligencia Artificial**  
Universidad - Séptimo Semestre  
Sistema de Diagnóstico Inteligente de Zonas Urbanas

---

## 📝 Notas Técnicas

- Los datos delictivos son **sintéticos** con distribuciones realistas
- El sistema usa **caché local** para evitar descargar mapas repetidamente
- La geocodificación inversa usa **Nominatim** de OpenStreetMap
- Todas las visualizaciones usan **coordenadas reales** de Ecuador
- El código está completamente en **español** para facilitar comprensión

---

## 🔮 Mejoras Futuras

- Integración con datos reales de la Policía Nacional
- Análisis temporal (evolución del riesgo en el tiempo)
- Predicción de zonas que aumentarán su peligrosidad
- App móvil para consulta en tiempo real
- Sistema de alertas georreferenciadas

---

**🚨 Este es un proyecto académico. Los diagnósticos son simulados y no deben usarse para decisiones reales de seguridad.**
