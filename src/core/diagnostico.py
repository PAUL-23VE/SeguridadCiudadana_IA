"""
diagnostico.py
==============
Modulo para diagnostico de zonas usando logica difusa, algoritmo genetico,
Apriori, PRISM y analisis de conectividad urbana.
"""
import numpy as np
from ..algoritmos.difuso import clasificar_difuso, describir_membresia, graficar_membresia, TIPO_MEMBRESIA
from ..algoritmos.genetico import optimizar_pesos
from ..algoritmos.reglas import obtener_regla_explicativa
from ..algoritmos.algoritmos import analizar_conectividad_zona


def _nombre_zona(fila, col, grid_shape=None, grid=None):
    nombre_raw = None
    if grid is not None:
        try:
            celda = grid[fila, col]
            nombre_raw = celda.get('nombre') if isinstance(celda, dict) else None
        except Exception:
            pass
    if nombre_raw:
        import re
        if re.match(r'^Zona\s*\[[-\d.]+,[-\d.]+\]$', nombre_raw.strip()):
            nombre_raw = None
    return nombre_raw or f'Sector {fila},{col}'


def diagnostico_masivo(grid, zonas, G=None):
    resultados = {}
    total = len(zonas)
    gs = grid.shape if hasattr(grid, 'shape') else (30, 30)
    for idx, (i, j) in enumerate(zonas):
        if total > 4 and idx % (total // 4) == 0 and idx > 0:
            print(f'     Progreso: {int(idx/total*100)}%...')
        resultados[(i, j)] = diagnosticar_zona_silencioso(grid, i, j, G, grid_shape=gs)
    return resultados


def diagnosticar_zona_silencioso(grid, fila, col, G=None, grid_shape=None):
    gs = grid_shape or (grid.shape if hasattr(grid, 'shape') else (30, 30))
    datos = {
        'robos':                np.random.randint(0, 100),
        'microtrafico':         np.random.randint(0, 50),
        'vandalismo':           np.random.randint(0, 80),
        'accidentes':           np.random.randint(0, 60),
        'llamadas_emergencias': np.random.randint(0, 100),
    }
    metricas = {
        'densidad_calles':         np.random.uniform(0, 500),
        'densidad_intersecciones': np.random.uniform(0, 300),
    }
    pesos        = optimizar_pesos(datos, silencioso=True)
    nivel, score = clasificar_difuso(datos, metricas, pesos)
    if G is not None:
        clat  = grid[fila, col]['lat']
        clon  = grid[fila, col]['lon']
        ci    = analizar_conectividad_zona(G, clat, clon)
        score = score * (1 + ci['factor_riesgo']) / 2
        nivel = 'Bajo' if score < 33 else 'Medio' if score < 66 else 'Alto'
    factores = sorted(datos, key=datos.get, reverse=True)[:2]
    regla    = obtener_regla_explicativa(datos, nivel)
    nombre   = _nombre_zona(fila, col, gs, grid)
    return {
        'nivel':    nivel,
        'factores': factores,
        'regla':    regla,
        'nombre':   f'{nombre} [{fila},{col}]',
    }


def diagnosticar_zona(grid, fila, col, G=None, grid_shape=None):
    gs     = grid_shape or (grid.shape if hasattr(grid, 'shape') else (30, 30))
    nombre = _nombre_zona(fila, col, gs, grid)
    sep    = chr(9472) * 60
    sep2   = chr(9472) * 56
    print(f'\n{sep}')
    print(f'  DIAGNOSTICO DE ZONA [{fila},{col}]')
    print(f'  Barrio/Sector: {nombre}')
    print(sep)
    datos = {
        'robos':                np.random.randint(0, 100),
        'microtrafico':         np.random.randint(0, 50),
        'vandalismo':           np.random.randint(0, 80),
        'accidentes':           np.random.randint(0, 60),
        'llamadas_emergencias': np.random.randint(0, 100),
    }
    metricas = {        'densidad_calles':         np.random.uniform(0, 500),
        'densidad_intersecciones': np.random.uniform(0, 300),
    }
    print(f'\n  PASO 1: DATOS DE ENTRADA')
    print(f'  {sep2}')
    for k, v in datos.items():
        tipo    = TIPO_MEMBRESIA.get(k, 'triangular')
        simbolo = '[TRI]' if tipo == 'triangular' else '[SIG]'
        print(f'     * {k:<28}: {v:>4}   {simbolo} {tipo}')
    for k, v in metricas.items():
        print(f'     * {k:<28}: {v:.2f}')
    print(f'\n  PASO 2: ALGORITMO GENETICO (optimizacion de pesos)')
    print(f'  {sep2}')
    print('     -> Generando poblacion inicial de 30 individuos...')
    print('     -> Evaluando fitness (precision de clasificacion)...')
    print('     -> Aplicando seleccion, cruce y mutacion...')
    pesos = optimizar_pesos(datos)
    print('     OK Pesos optimizados obtenidos')
    for k, v in pesos.items():
        print(f'        * {k}: {v:.3f}')
    print(f'\n  PASO 3: LOGICA DIFUSA (clasificacion)')
    print(f'  {sep2}')
    print(describir_membresia())
    print('     -> Evaluando grados de membresia Bajo / Medio / Alto...')
    print('     -> Defuzzificacion por centroide (centros: 16.5 / 50 / 83.5)...')
    nivel, score = clasificar_difuso(datos, metricas, pesos)
    print(f'     OK Score de riesgo : {score:.2f}/100')
    print(f'     OK Clasificacion   : {nivel}')
    fig_membresia = None
    try:
        fig_membresia = graficar_membresia(datos_zona=datos, nombre_zona=nombre)
    except Exception as e:
        print(f'     (grafica no disponible: {e})')
    factores = sorted(datos, key=datos.get, reverse=True)[:2]
    print(f'\n  PASO 4: ANALISIS DE FACTORES')
    print(f'  {sep2}')
    print('     -> Identificando variables con mayor influencia...')
    print(f'     OK Factores principales: {", ".join(factores)}')
    print(f'\n  PASO 5: GENERACION DE REGLAS (Apriori/PRISM)')
    print(f'  {sep2}')
    print('     -> Buscando patrones en dataset historico...')
    print('     -> Calculando soporte y confianza...')
    regla = obtener_regla_explicativa(datos, nivel)
    print(f'     OK Regla encontrada: {regla}')
    if G is not None:
        print(f'\n  PASO 6: ANALISIS DE CONECTIVIDAD URBANA (BFS/DFS/A*)')
        print(f'  {sep2}')
        clat = grid[fila, col]['lat']
        clon = grid[fila, col]['lon']
        print(f'     -> Analizando estructura urbana en ({clat:.5f}, {clon:.5f})...')
        print('     -> Aplicando BFS para explorar nodos alcanzables...')
        ci = analizar_conectividad_zona(G, clat, clon)
        print(f'     OK Nodos alcanzables (radio 500m): {ci["nodos_alcanzables"]}')
        print(f'     OK Conectividad urbana           : {ci["conectividad"]}')
        print(f'     OK Factor de ajuste de riesgo    : {ci["factor_riesgo"]:.2f}')
        score_o = score
        score   = score * (1 + ci['factor_riesgo']) / 2
        print(f'     -> Score original : {score_o:.2f}')
        print(f'     -> Score ajustado : {score:.2f}')
        nivel = 'Bajo' if score < 33 else 'Medio' if score < 66 else 'Alto'
        print(f'     OK Clasificacion final: {nivel}')
    print(f'{sep}\n')
    return {
        'nivel':    nivel,
        'factores': factores,
        'regla':    regla,
        'nombre':   f'{nombre} [{fila},{col}]',
    }
