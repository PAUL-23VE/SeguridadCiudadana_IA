# Sistema de Diagnóstico de Zonas de Riesgo Urbano

Proyecto académico de Inteligencia Artificial orientado al análisis de riesgo urbano en Ambato, Ecuador. El sistema combina datos históricos, lógica difusa, algoritmo genético, simulación Monte Carlo, reglas explicativas y análisis de conectividad sobre un grafo vial real obtenido desde OpenStreetMap.

## Información Académica

- Institución: Universidad Técnica de Ambato
- Carrera: Ingeniería de Software
- Asignatura: Inteligencia Artificial
- Autores: Paul Velastegui, David Manjarres

## Qué Hace el Sistema

- Carga datos históricos por macro-zona desde `data/historicos_zonas.csv`.
- Descarga el grafo vial de Ambato con OSMnx.
- Construye una grilla de análisis de `30 x 30` zonas.
- Genera escenarios sintéticos mediante Monte Carlo.
- Optimiza pesos con algoritmo genético.
- Clasifica el riesgo con lógica difusa.
- Ajusta el resultado según conectividad vial con BFS.
- Genera reglas explicativas con Apriori y PRISM.
- Exporta mapas HTML, gráficas PNG y reportes HTML.

## Algoritmos Utilizados

- BFS
- DFS
- A*
- Algoritmo Genético
- Apriori
- PRISM
- Lógica Difusa

## Requisitos

- Python 3.8 o superior
- Conexión a internet para descargar el mapa de OpenStreetMap
- Dependencias instaladas desde `requirements.txt`
- `tkinter/Tk` si se desea usar el modo detallado con interfaz gráfica

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

El programa trabaja sobre `Ambato, Ecuador` y ofrece dos modos:

- `Modo 1`: análisis completo de toda la grilla.
- `Modo 2`: análisis detallado de una zona específica con interfaz gráfica.

Si el entorno no dispone de `tkinter/Tk`, el sistema cambia automáticamente al modo 1.

## Salidas Generadas

Los archivos generados se guardan en `output/`:

- mapas HTML interactivos
- gráficas de datos históricos reales
- gráficas de simulación Monte Carlo
- reportes HTML consolidados

## Estructura del Proyecto

```text
.
├── main.py
├── config.py
├── requirements.txt
├── data/
├── output/
├── src/
│   ├── algoritmos/
│   │   ├── busqueda.py
│   │   ├── conectividad.py
│   │   ├── difuso.py
│   │   ├── genetico.py
│   │   ├── montecarlo.py
│   │   └── reglas.py
│   ├── core/
│   │   ├── diagnostico.py
│   │   ├── mapa.py
│   │   └── visualizacion.py
│   └── utils/
│       ├── datos.py
│       ├── historicos.py
│       └── reporte.py
└── APE1/
```

## Documentación

La documentación académica principal del proyecto se encuentra en:

- `APE1/FORMATO DE TRABAJO FINAL.tex`
- `APE1/FORMATO DE TRABAJO FINAL.pdf`

El `README` se mantiene breve y orientado al uso del repositorio; la explicación extensa del enfoque, metodología y resultados se desarrolla en el informe.

## Observaciones

- El proyecto es académico y no debe interpretarse como un sistema operativo de seguridad pública.
- Los resultados dependen de la calidad de los datos históricos y del comportamiento estocástico de Monte Carlo y del algoritmo genético.
- La carpeta `output/` contiene resultados generados y no forma parte del código fuente principal.
