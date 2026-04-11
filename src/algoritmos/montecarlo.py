"""
montecarlo.py
=============
Módulo de simulación Monte Carlo para generación de datos sintéticos
basados en distribuciones históricas.

Este módulo genera datos aleatorios que respetan los límites y
distribuciones de los datos históricos de cada macro-zona.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def generar_datos_zona(zona, estadisticas, num_simulaciones=1):
    """
    Genera datos sintéticos basados en estadísticas históricas usando Monte Carlo.
    
    Método:
    1. Genera valores con distribución normal (media, desv. estándar)
    2. Aplica restricción: solo acepta valores dentro de [min, max] histórico
    3. Retorna valores que cumplen las restricciones
    
    Parámetros
    ----------
    zona : str
        Nombre de la zona ('Norte', 'Sur', 'Este', 'Oeste')
    estadisticas : dict
        Estadísticas históricas de la zona
    num_simulaciones : int
        Número de escenarios a generar (default: 1)
    
    Retorna
    -------
    list : Lista de diccionarios con datos generados
    
    Ejemplo
    -------
    >>> stats = {'Robos': {'media': 50, 'std': 5, 'min': 40, 'max': 60}}
    >>> datos = generar_datos_zona('Norte', stats, num_simulaciones=100)
    >>> len(datos)
    100
    """
    variables = ['Robos', 'Microtrafico', 'Vandalismo', 'Accidentes', 'Llamadas911']
    mapeo_variables = {
        'Robos': 'robos',
        'Microtrafico': 'microtrafico',
        'Vandalismo': 'vandalismo',
        'Accidentes': 'accidentes',
        'Llamadas911': 'llamadas_emergencias'
    }
    
    simulaciones = []
    
    for _ in range(num_simulaciones):
        datos_simulados = {}
        
        for var in variables:
            stats = estadisticas.get(var, {})
            if not stats:
                continue
            
            media = stats.get('media', 50)
            std = stats.get('std', 10)
            min_val = stats.get('min', 0)
            max_val = stats.get('max', 100)
            
            # Generar valor con distribución normal
            valor = np.random.normal(media, std)
            
            # Aplicar restricción: mantener dentro de límites históricos
            valor = np.clip(valor, min_val, max_val)
            
            # Guardar con el nombre de variable que usa el sistema
            nombre_var = mapeo_variables.get(var, var.lower())
            datos_simulados[nombre_var] = int(round(valor))
        
        simulaciones.append(datos_simulados)
    
    return simulaciones


def generar_datos_con_restricciones(zona, estadisticas, num_simulaciones=100, percentil_confianza=95):
    """
    Genera datos Monte Carlo con intervalo de confianza.
    
    Solo retorna simulaciones que caen dentro del percentil de confianza
    de la distribución histórica.
    
    Parámetros
    ----------
    zona : str
        Nombre de la zona
    estadisticas : dict
        Estadísticas históricas
    num_simulaciones : int
        Número de simulaciones a generar
    percentil_confianza : int
        Percentil de confianza (ej: 95 para 95%)
    
    Retorna
    -------
    dict : {
        'simulaciones': list de datos generados,
        'estadisticas_agregadas': estadísticas de las simulaciones
    }
    """
    # Generar más simulaciones de las necesarias
    todas_simulaciones = generar_datos_zona(zona, estadisticas, num_simulaciones * 2)
    
    # Calcular límites de confianza para cada variable
    limites_inferior = {}
    limites_superior = {}
    
    for var_original, var_sistema in [
        ('Robos', 'robos'),
        ('Microtrafico', 'microtrafico'),
        ('Vandalismo', 'vandalismo'),
        ('Accidentes', 'accidentes'),
        ('Llamadas911', 'llamadas_emergencias')
    ]:
        valores = [s[var_sistema] for s in todas_simulaciones if var_sistema in s]
        if valores:
            percentil_bajo = (100 - percentil_confianza) / 2
            percentil_alto = 100 - percentil_bajo
            limites_inferior[var_sistema] = np.percentile(valores, percentil_bajo)
            limites_superior[var_sistema] = np.percentile(valores, percentil_alto)
    
    # Filtrar simulaciones dentro del intervalo de confianza
    simulaciones_filtradas = []
    for sim in todas_simulaciones:
        dentro_intervalo = all(
            limites_inferior.get(var, -np.inf) <= sim.get(var, 0) <= limites_superior.get(var, np.inf)
            for var in ['robos', 'microtrafico', 'vandalismo', 'accidentes', 'llamadas_emergencias']
        )
        if dentro_intervalo:
            simulaciones_filtradas.append(sim)
            if len(simulaciones_filtradas) >= num_simulaciones:
                break
    
    # Calcular estadísticas agregadas
    estadisticas_agregadas = {}
    for var in ['robos', 'microtrafico', 'vandalismo', 'accidentes', 'llamadas_emergencias']:
        valores = [s[var] for s in simulaciones_filtradas if var in s]
        if valores:
            estadisticas_agregadas[var] = {
                'media': np.mean(valores),
                'std': np.std(valores),
                'min': np.min(valores),
                'max': np.max(valores)
            }
    
    return {
        'simulaciones': simulaciones_filtradas[:num_simulaciones],
        'estadisticas_agregadas': estadisticas_agregadas
    }


def generar_escenario_unico(zona, estadisticas):
    """
    Genera un único escenario de datos para una zona.
    
    Útil para análisis de zona individual con datos históricos.
    
    Parámetros
    ----------
    zona : str
        Nombre de la zona
    estadisticas : dict
        Estadísticas históricas
    
    Retorna
    -------
    dict : Datos generados para un escenario
    """
    simulaciones = generar_datos_zona(zona, estadisticas, num_simulaciones=1)
    return simulaciones[0] if simulaciones else {}


def visualizar_simulaciones_montecarlo(zona, estadisticas, num_simulaciones=1000, mostrar=True, guardar_path=None):
    """
    Visualiza las simulaciones Monte Carlo con histogramas y scatter plots.
    
    Genera una figura con 5 subplots (uno por variable) mostrando:
    - Histograma de la distribución de valores generados
    - Puntos individuales (scatter) de cada valor aleatorio
    - Líneas de referencia: media (verde), min (rojo), max (rojo)
    - Área sombreada del rango histórico válido
    
    Parámetros
    ----------
    zona : str
        Nombre de la zona ('Norte', 'Sur', 'Este', 'Oeste')
    estadisticas : dict
        Estadísticas históricas de la zona
    num_simulaciones : int
        Número de simulaciones a generar (default: 1000)
    mostrar : bool
        Si True, muestra la gráfica en pantalla (default: True)
    guardar_path : str, optional
        Si se proporciona, guarda la gráfica en este path
    
    Retorna
    -------
    dict : {
        'figura': objeto Figure de matplotlib,
        'simulaciones': datos generados,
        'resumen': estadísticas de las simulaciones
    }
    
    Ejemplo
    -------
    >>> from src.utils import obtener_gestor
    >>> gestor = obtener_gestor()
    >>> stats = gestor.obtener_estadisticas('Norte')
    >>> resultado = visualizar_simulaciones_montecarlo('Norte', stats, 1000)
    >>> plt.show()
    """
    # Generar simulaciones
    simulaciones = generar_datos_zona(zona, estadisticas, num_simulaciones)
    
    # Mapeo de variables
    variables = [
        ('robos', 'Robos'),
        ('microtrafico', 'Microtráfico'),
        ('vandalismo', 'Vandalismo'),
        ('accidentes', 'Accidentes'),
        ('llamadas_emergencias', 'Llamadas 911')
    ]
    
    # Crear figura con 5 subplots (uno por variable)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle(f'Simulación Monte Carlo - Zona {zona}\n{num_simulaciones} simulaciones', 
                 fontsize=16, fontweight='bold')
    
    # Aplanar axes para iterar fácilmente
    axes_flat = axes.flatten()
    
    # Calcular resumen estadístico
    resumen = {}
    
    for idx, (var_sistema, var_display) in enumerate(variables):
        ax = axes_flat[idx]
        
        # Extraer valores de las simulaciones
        valores = [sim[var_sistema] for sim in simulaciones if var_sistema in sim]
        
        if not valores:
            ax.text(0.5, 0.5, f'Sin datos para {var_display}', 
                   ha='center', va='center', fontsize=12)
            ax.set_title(var_display, fontsize=12, fontweight='bold')
            continue
        
        # Obtener estadísticas históricas
        var_original = {
            'robos': 'Robos',
            'microtrafico': 'Microtrafico',
            'vandalismo': 'Vandalismo',
            'accidentes': 'Accidentes',
            'llamadas_emergencias': 'Llamadas911'
        }[var_sistema]
        
        stats_hist = estadisticas.get(var_original, {})
        media_hist = stats_hist.get('media', np.mean(valores))
        min_hist = stats_hist.get('min', np.min(valores))
        max_hist = stats_hist.get('max', np.max(valores))
        
        # Calcular estadísticas de las simulaciones
        media_sim = np.mean(valores)
        std_sim = np.std(valores)
        min_sim = np.min(valores)
        max_sim = np.max(valores)
        
        resumen[var_sistema] = {
            'media_simulacion': media_sim,
            'std_simulacion': std_sim,
            'min_simulacion': min_sim,
            'max_simulacion': max_sim,
            'media_historica': media_hist,
            'min_historico': min_hist,
            'max_historico': max_hist
        }
        
        # --- GRÁFICA 1: Histograma + Referencias ---
        
        # Crear histograma
        n, bins, patches = ax.hist(valores, bins=30, alpha=0.6, color='steelblue', 
                                   edgecolor='black', label='Distribución generada')
        
        # Área sombreada del rango histórico
        ax.axvspan(min_hist, max_hist, alpha=0.15, color='yellow', 
                  label=f'Rango histórico [{min_hist:.0f}-{max_hist:.0f}]')
        
        # Líneas de referencia
        ax.axvline(media_hist, color='green', linestyle='--', linewidth=2, 
                  label=f'Media histórica ({media_hist:.1f})')
        ax.axvline(min_hist, color='red', linestyle=':', linewidth=1.5, 
                  label=f'Min histórico ({min_hist:.0f})')
        ax.axvline(max_hist, color='red', linestyle=':', linewidth=1.5, 
                  label=f'Max histórico ({max_hist:.0f})')
        
        # Línea de media simulada
        ax.axvline(media_sim, color='blue', linestyle='-', linewidth=2, 
                  label=f'Media simulada ({media_sim:.1f})')
        
        # Configurar gráfica
        ax.set_xlabel('Valor', fontsize=10)
        ax.set_ylabel('Frecuencia', fontsize=10)
        ax.set_title(f'{var_display}\nμ={media_sim:.1f}, σ={std_sim:.1f}', 
                    fontsize=12, fontweight='bold')
        ax.legend(fontsize=7, loc='upper right')
        ax.grid(True, alpha=0.3)
        
        # Añadir texto con estadísticas
        textstr = f'n={num_simulaciones}\nRango: [{min_sim:.0f}, {max_sim:.0f}]'
        ax.text(0.02, 0.98, textstr, transform=ax.transAxes, 
               fontsize=8, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Ocultar el subplot extra (tenemos 5 variables en grid 2x3)
    axes_flat[5].axis('off')
    
    # Ajustar layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    # Guardar si se especifica path
    if guardar_path:
        plt.savefig(guardar_path, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfica guardada en: {guardar_path}")
    
    # Mostrar si se solicita
    if mostrar:
        plt.show()
    
    return {
        'figura': fig,
        'simulaciones': simulaciones,
        'resumen': resumen
    }


def visualizar_scatter_montecarlo(zona, estadisticas, num_simulaciones=1000, mostrar=True, guardar_path=None):
    """
    Visualiza puntos individuales de simulaciones Monte Carlo con scatter plots.
    
    Genera una figura con 5 subplots mostrando cada valor generado como un punto,
    permitiendo ver la dispersión individual de las simulaciones.
    
    Parámetros
    ----------
    zona : str
        Nombre de la zona
    estadisticas : dict
        Estadísticas históricas
    num_simulaciones : int
        Número de simulaciones (default: 1000)
    mostrar : bool
        Si True, muestra la gráfica (default: True)
    guardar_path : str, optional
        Path para guardar la imagen
    
    Retorna
    -------
    dict : {
        'figura': objeto Figure,
        'simulaciones': datos generados
    }
    """
    # Generar simulaciones
    simulaciones = generar_datos_zona(zona, estadisticas, num_simulaciones)
    
    # Variables
    variables = [
        ('robos', 'Robos'),
        ('microtrafico', 'Microtráfico'),
        ('vandalismo', 'Vandalismo'),
        ('accidentes', 'Accidentes'),
        ('llamadas_emergencias', 'Llamadas 911')
    ]
    
    # Crear figura
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle(f'Scatter Plot - Simulación Monte Carlo (Zona {zona})\n{num_simulaciones} puntos generados', 
                 fontsize=16, fontweight='bold')
    
    axes_flat = axes.flatten()
    
    for idx, (var_sistema, var_display) in enumerate(variables):
        ax = axes_flat[idx]
        
        # Extraer valores
        valores = [sim[var_sistema] for sim in simulaciones if var_sistema in sim]
        
        if not valores:
            ax.text(0.5, 0.5, f'Sin datos para {var_display}', 
                   ha='center', va='center', fontsize=12)
            ax.set_title(var_display, fontsize=12, fontweight='bold')
            continue
        
        # Estadísticas históricas
        var_original = {
            'robos': 'Robos',
            'microtrafico': 'Microtrafico',
            'vandalismo': 'Vandalismo',
            'accidentes': 'Accidentes',
            'llamadas_emergencias': 'Llamadas911'
        }[var_sistema]
        
        stats_hist = estadisticas.get(var_original, {})
        media_hist = stats_hist.get('media', np.mean(valores))
        min_hist = stats_hist.get('min', np.min(valores))
        max_hist = stats_hist.get('max', np.max(valores))
        
        # Crear índices para el eje X
        indices = np.arange(len(valores))
        
        # Scatter plot con puntos individuales
        ax.scatter(indices, valores, alpha=0.5, s=10, color='steelblue', 
                  label='Valores generados')
        
        # Área sombreada del rango histórico
        ax.axhspan(min_hist, max_hist, alpha=0.15, color='yellow', 
                  label=f'Rango histórico')
        
        # Líneas de referencia
        ax.axhline(media_hist, color='green', linestyle='--', linewidth=2, 
                  label=f'Media histórica ({media_hist:.1f})')
        ax.axhline(min_hist, color='red', linestyle=':', linewidth=1.5)
        ax.axhline(max_hist, color='red', linestyle=':', linewidth=1.5)
        
        # Configurar
        ax.set_xlabel('Número de Simulación', fontsize=10)
        ax.set_ylabel('Valor', fontsize=10)
        ax.set_title(f'{var_display}', fontsize=12, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        
        # Límites del eje Y
        y_margin = (max_hist - min_hist) * 0.1
        ax.set_ylim(min_hist - y_margin, max_hist + y_margin)
    
    # Ocultar subplot extra
    axes_flat[5].axis('off')
    
    # Ajustar layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    # Guardar
    if guardar_path:
        plt.savefig(guardar_path, dpi=300, bbox_inches='tight')
        print(f"✓ Scatter plot guardado en: {guardar_path}")
    
    # Mostrar
    if mostrar:
        plt.show()
    
    return {
        'figura': fig,
        'simulaciones': simulaciones
    }


def visualizar_datos_historicos_reales(zona, estadisticas, mostrar=True, guardar_path=None):
    """
    Visualiza los datos históricos REALES (12 meses del CSV) sin simulaciones Monte Carlo.
    
    Crea histogramas mostrando la distribución de los valores reales históricos
    para cada variable de criminalidad en una zona específica.
    
    Parámetros
    ----------
    zona : str
        Nombre de la zona ('Norte', 'Sur', 'Este', 'Oeste')
    estadisticas : dict
        Diccionario con estadísticas que incluyen campo 'historico' con los 12 valores mensuales
    mostrar : bool
        Si mostrar la figura (default: True)
    guardar_path : str, optional
        Ruta para guardar la figura
    
    Retorna
    -------
    dict : Diccionario con 'figura' y 'datos_historicos'
    
    Ejemplo
    -------
    >>> from src.utils.historicos import GestorHistoricos
    >>> gestor = GestorHistoricos()
    >>> resultado = visualizar_datos_historicos_reales(
    ...     zona='Norte',
    ...     estadisticas=gestor.estadisticas['Norte'],
    ...     guardar_path='output/norte_reales.png'
    ... )
    """
    # Variables a graficar
    variables = ['Robos', 'Microtrafico', 'Vandalismo', 'Accidentes', 'Llamadas911']
    nombres_display = {
        'Robos': 'Robos',
        'Microtrafico': 'Microtráfico',
        'Vandalismo': 'Vandalismo',
        'Accidentes': 'Accidentes de Tránsito',
        'Llamadas911': 'Llamadas de Emergencia'
    }
    
    # Crear figura con 5 subplots (2x3 grid)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle(f'Datos Históricos REALES - Zona {zona}\n(12 meses del CSV)', 
                 fontsize=16, fontweight='bold')
    
    axes_flat = axes.flatten()
    datos_reales = {}
    
    for idx, var in enumerate(variables):
        ax = axes_flat[idx]
        
        # Obtener datos históricos reales
        stats = estadisticas.get(var, {})
        valores_reales = stats.get('historico', [])
        
        if not valores_reales:
            ax.text(0.5, 0.5, 'Sin datos históricos', ha='center', va='center')
            ax.set_title(nombres_display[var])
            continue
        
        datos_reales[var] = valores_reales
        
        # Estadísticas
        media = stats.get('media', np.mean(valores_reales))
        std = stats.get('std', np.std(valores_reales))
        min_val = stats.get('min', min(valores_reales))
        max_val = stats.get('max', max(valores_reales))
        
        # HISTOGRAMA de datos reales
        ax.hist(valores_reales, bins=min(len(valores_reales), 12), 
                alpha=0.7, color='steelblue', edgecolor='black', linewidth=1.2,
                label=f'Datos reales (n={len(valores_reales)})')
        
        # Línea de media
        ax.axvline(media, color='red', linestyle='--', linewidth=2, 
                   label=f'Media: {media:.1f}')
        
        # Líneas de desviación estándar
        ax.axvline(media - std, color='orange', linestyle=':', linewidth=1.5, 
                   label=f'±1σ: [{media-std:.1f}, {media+std:.1f}]')
        ax.axvline(media + std, color='orange', linestyle=':', linewidth=1.5)
        
        # Configurar
        ax.set_xlabel('Valor', fontsize=10)
        ax.set_ylabel('Frecuencia', fontsize=10)
        ax.set_title(f'{nombres_display[var]}', fontsize=12, fontweight='bold')
        ax.legend(fontsize=8, loc='best')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Anotaciones con estadísticas
        texto_stats = f'Min: {min_val:.0f}\nMax: {max_val:.0f}\nσ: {std:.1f}'
        ax.text(0.02, 0.98, texto_stats, transform=ax.transAxes,
                fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Ocultar subplot extra
    axes_flat[5].axis('off')
    
    # Ajustar layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    # Guardar
    if guardar_path:
        plt.savefig(guardar_path, dpi=300, bbox_inches='tight')
        print(f"✓ Visualización de datos reales guardada en: {guardar_path}")
    
    # Mostrar
    if mostrar:
        plt.show()
    else:
        plt.close(fig)
    
    return {
        'figura': fig,
        'datos_historicos': datos_reales
    }
