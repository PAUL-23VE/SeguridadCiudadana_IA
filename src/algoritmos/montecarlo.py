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
from scipy.stats import norm


def generar_datos_zona(zona, estadisticas, num_simulaciones=1):
    """
    Genera datos sintéticos basados en estadísticas históricas usando Monte Carlo.
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

            media   = stats.get('media', 50)
            std     = stats.get('std', 10)
            min_val = stats.get('min', 0)
            max_val = stats.get('max', 100)

            valor = np.random.normal(media, std)
            valor = np.clip(valor, min_val, max_val)

            nombre_var = mapeo_variables.get(var, var.lower())
            datos_simulados[nombre_var] = int(round(valor))

        simulaciones.append(datos_simulados)

    return simulaciones


def generar_datos_con_restricciones(zona, estadisticas, num_simulaciones=100, percentil_confianza=95):
    """
    Genera datos Monte Carlo con intervalo de confianza.
    """
    todas_simulaciones = generar_datos_zona(zona, estadisticas, num_simulaciones * 2)

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

    estadisticas_agregadas = {}
    for var in ['robos', 'microtrafico', 'vandalismo', 'accidentes', 'llamadas_emergencias']:
        valores = [s[var] for s in simulaciones_filtradas if var in s]
        if valores:
            estadisticas_agregadas[var] = {
                'media': np.mean(valores),
                'std':   np.std(valores),
                'min':   np.min(valores),
                'max':   np.max(valores)
            }

    return {
        'simulaciones': simulaciones_filtradas[:num_simulaciones],
        'estadisticas_agregadas': estadisticas_agregadas
    }


def generar_escenario_unico(zona, estadisticas):
    """
    Genera un único escenario de datos para una zona.
    """
    simulaciones = generar_datos_zona(zona, estadisticas, num_simulaciones=1)
    return simulaciones[0] if simulaciones else {}


def visualizar_simulaciones_montecarlo(zona, estadisticas, num_simulaciones=1000, mostrar=True, guardar_path=None):
    """
    Visualiza las simulaciones Monte Carlo con curvas de distribución (masa).

    Genera una figura con 5 subplots (uno por variable) mostrando:
    - Curva de densidad de las simulaciones Monte Carlo
    - Curva de densidad histórica
    - Media histórica y simulada
    - Zona ±1σ de las simulaciones
    """
    simulaciones = generar_datos_zona(zona, estadisticas, num_simulaciones)

    variables = [
        ('robos',                'Robos'),
        ('microtrafico',         'Microtráfico'),
        ('vandalismo',           'Vandalismo'),
        ('accidentes',           'Accidentes'),
        ('llamadas_emergencias', 'Llamadas 911')
    ]

    fig, axes = plt.subplots(1, 5, figsize=(22, 5))
    fig.suptitle(
        f'Validación Monte Carlo - Zona {zona} ({num_simulaciones} simulaciones)\n'
        f'Distribución: Datos Históricos vs Simulaciones',
        fontsize=14, fontweight='bold', y=1.02
    )

    resumen = {}

    for idx, (var_sistema, var_display) in enumerate(variables):
        ax = axes[idx]

        valores = [sim[var_sistema] for sim in simulaciones if var_sistema in sim]

        if not valores:
            ax.text(0.5, 0.5, f'Sin datos\npara\n{var_display}',
                    ha='center', va='center', fontsize=11, color='red')
            ax.set_title(var_display, fontsize=11, fontweight='bold')
            ax.set_xticks([])
            ax.set_yticks([])
            continue

        var_original = {
            'robos':                'Robos',
            'microtrafico':         'Microtrafico',
            'vandalismo':           'Vandalismo',
            'accidentes':           'Accidentes',
            'llamadas_emergencias': 'Llamadas911'
        }[var_sistema]

        stats_hist = estadisticas.get(var_original, {})
        media_hist = stats_hist.get('media', np.mean(valores))
        std_hist   = stats_hist.get('std',   np.std(valores))
        min_hist   = stats_hist.get('min',   np.min(valores))
        max_hist   = stats_hist.get('max',   np.max(valores))

        media_sim = np.mean(valores)
        std_sim   = np.std(valores)
        min_sim   = np.min(valores)
        max_sim   = np.max(valores)

        resumen[var_sistema] = {
            'media_simulacion': media_sim,
            'std_simulacion':   std_sim,
            'min_simulacion':   min_sim,
            'max_simulacion':   max_sim,
            'media_historica':  media_hist,
            'min_historico':    min_hist,
            'max_historico':    max_hist
        }

        # Rango común para las curvas
        x_min = min(min_hist, min_sim) - std_hist * 0.8
        x_max = max(max_hist, max_sim) + std_hist * 0.8
        x_range = np.linspace(x_min, x_max, 300)

        # Curva histórica
        densidad_hist = norm.pdf(x_range, media_hist, std_hist) if std_hist > 0 else np.zeros_like(x_range)
        frecuencia_hist = densidad_hist * len(valores) * std_hist * 2.5

        # Curva simulada
        densidad_sim = norm.pdf(x_range, media_sim, std_sim) if std_sim > 0 else np.zeros_like(x_range)
        frecuencia_sim = densidad_sim * len(valores) * std_sim * 2.5

        # Área histórica (azul)
        ax.fill_between(x_range, frecuencia_hist,
                        alpha=0.4, color='#2E86AB',
                        label='Histórico', edgecolor='#1A5276', linewidth=2)
        ax.plot(x_range, frecuencia_hist, color='#1A5276', linewidth=2)

        # Área simulada (magenta)
        ax.fill_between(x_range, frecuencia_sim,
                        alpha=0.4, color='#A23B72',
                        label=f'Simulado (MC)', edgecolor='#6C2449', linewidth=2)
        ax.plot(x_range, frecuencia_sim, color='#6C2449', linewidth=2)

        # Media histórica (línea roja)
        ax.axvline(media_hist, color='#E74C3C', linestyle='-', linewidth=2.5,
                   label=f'Media hist: {media_hist:.1f}', zorder=10)

        # Media simulada (línea verde)
        ax.axvline(media_sim, color='#27AE60', linestyle='--', linewidth=2,
                   label=f'Media sim: {media_sim:.1f}', zorder=10)

        # Zona ±1σ simulada (verde claro)
        ax.axvspan(media_sim - std_sim, media_sim + std_sim,
                   alpha=0.12, color='#27AE60', label='±1σ sim', zorder=1)

        # Etiquetas y configuración
        ax.set_xlabel('Valor del Indicador', fontsize=10, fontweight='bold')
        ax.set_ylabel('Frecuencia Estimada', fontsize=10, fontweight='bold')
        ax.set_title(f'{var_display}\n(σ sim={std_sim:.1f})', fontsize=11, fontweight='bold')
        ax.legend(fontsize=7.5, loc='upper right', framealpha=0.95)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_facecolor('#FFFFFF')
        ax.set_xlim(x_min, x_max)

        # Indicador de n
        ax.text(0.98, 0.02, f'n={num_simulaciones}', transform=ax.transAxes,
                fontsize=7, ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='gray'))

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])

    if guardar_path:
        plt.savefig(guardar_path, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfica guardada en: {guardar_path}")

    if mostrar:
        plt.show()

    return {
        'figura':      fig,
        'simulaciones': simulaciones,
        'resumen':     resumen
    }


def visualizar_datos_historicos_reales(zona, estadisticas, mostrar=True, guardar_path=None):
    """
    Visualiza los datos históricos REALES (12 meses del CSV) con CURVA SUAVE.

    Genera curvas de distribución mostrando:
    - Curva continua suave (sin barras)
    - Eje X: Valor del indicador
    - Eje Y: Frecuencia estimada
    - Área rellena azul bajo la curva
    - Media histórica (línea roja vertical)
    - Rango min-max (líneas naranja)
    - Zona ±1σ (área verde sombreada)
    """
    variables = ['Robos', 'Microtrafico', 'Vandalismo', 'Accidentes', 'Llamadas911']
    nombres_display = {
        'Robos':       'Robos',
        'Microtrafico':'Microtráfico',
        'Vandalismo':  'Vandalismo',
        'Accidentes':  'Accidentes de Tránsito',
        'Llamadas911': 'Llamadas de Emergencia'
    }

    fig, axes = plt.subplots(1, 5, figsize=(22, 5))
    fig.suptitle(
        f'Datos Historicos REALES - Zona {zona} (12 meses del CSV)\n'
        f'Curvas muestran la distribucion de valores historicos',
        fontsize=13, fontweight='bold', y=1.03
    )

    datos_reales = {}

    for idx, var in enumerate(variables):
        ax = axes[idx]

        stats = estadisticas.get(var, {})
        valores_reales = stats.get('historico', [])

        if not valores_reales:
            ax.text(0.5, 0.5, f'Sin datos\nhistóricos', ha='center', va='center',
                    fontsize=11, color='red')
            ax.set_title(nombres_display[var], fontsize=11, fontweight='bold')
            ax.set_xticks([])
            ax.set_yticks([])
            continue

        datos_reales[var] = valores_reales

        media   = stats.get('media', np.mean(valores_reales))
        std     = stats.get('std',   np.std(valores_reales))
        min_val = stats.get('min',   min(valores_reales))
        max_val = stats.get('max',   max(valores_reales))

        x_range   = np.linspace(min_val - std * 0.8, max_val + std * 0.8, 300)
        densidad  = norm.pdf(x_range, media, std)
        frecuencia = densidad * len(valores_reales) * std * 2.5

        # Área rellena (azul claro)
        ax.fill_between(x_range, frecuencia,
                        alpha=0.5, color='#4A90E2',
                        label=f'Distribución (n={len(valores_reales)})',
                        edgecolor='#2E5C8A', linewidth=2.5)
        ax.plot(x_range, frecuencia, color='#1E3A5F', linewidth=3, zorder=5)

        # Media (roja)
        ax.axvline(media, color='#E74C3C', linestyle='-', linewidth=3.5,
                   label=f'Media: {media:.1f}', zorder=10, alpha=0.9)

        # Min / Max (naranja)
        ax.axvline(min_val, color='#F39C12', linestyle='--', linewidth=2.5,
                   label=f'Min: {min_val:.0f}', alpha=0.8, zorder=9)
        ax.axvline(max_val, color='#F39C12', linestyle='--', linewidth=2.5,
                   label=f'Max: {max_val:.0f}', alpha=0.8, zorder=9)

        # Zona ±1σ (verde)
        ax.axvspan(media - std, media + std, alpha=0.18, color='#27AE60',
                   label='±1σ', zorder=1)

        ax.set_xlabel('Valor del Indicador', fontsize=10, fontweight='bold')
        ax.set_ylabel('Frecuencia Estimada', fontsize=10, fontweight='bold')
        ax.set_title(f'{nombres_display[var]}\n(μ={media:.1f}, σ={std:.1f})',
                     fontsize=11, fontweight='bold')
        ax.legend(fontsize=7.5, loc='upper right', framealpha=0.95)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_facecolor('#FFFFFF')
        ax.set_xlim(min_val - std * 0.8, max_val + std * 0.8)
        ax.set_ylim(0, np.max(frecuencia) * 1.15)

        texto_stats = f'n = {len(valores_reales)} meses\nRango: [{min_val:.0f}, {max_val:.0f}]'
        ax.text(0.03, 0.97, texto_stats, transform=ax.transAxes,
                fontsize=8, verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9,
                          edgecolor='#34495E', linewidth=1.5))

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])

    if guardar_path:
        plt.savefig(guardar_path, dpi=300, bbox_inches='tight')
        print(f"✓ Visualización de datos reales guardada en: {guardar_path}")

    if mostrar:
        plt.show()
    else:
        plt.close(fig)

    return {
        'figura':          fig,
        'datos_historicos': datos_reales
    }