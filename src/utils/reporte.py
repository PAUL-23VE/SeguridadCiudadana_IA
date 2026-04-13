"""
reporte.py
==========
Generador de reportes HTML profesionales con todas las estadísticas del sistema
"""
import os
from datetime import datetime


def generar_reporte_html(datos_reporte, ruta_salida):
    """
    Genera un reporte HTML profesional con todas las estadísticas del sistema.
    
    Parámetros
    ----------
    datos_reporte : dict
        Diccionario con toda la información del análisis
    ruta_salida : str
        Ruta donde se guardará el archivo HTML
    """
    
    # Extraer datos
    ciudad = datos_reporte.get('ciudad', 'Desconocida')
    modo = datos_reporte.get('modo', 'Completo')
    total_zonas = datos_reporte.get('total_zonas', 0)
    zonas_alto = datos_reporte.get('zonas_alto', 0)
    zonas_medio = datos_reporte.get('zonas_medio', 0)
    zonas_bajo = datos_reporte.get('zonas_bajo', 0)
    
    # Datos históricos
    datos_historicos = datos_reporte.get('datos_historicos', {})
    
    # Datos de simulación Monte Carlo
    datos_montecarlo = datos_reporte.get('montecarlo', {})
    
    # Detalles de zonas analizadas
    detalles_zonas = datos_reporte.get('detalles_zonas', [])
    
    # Información del círculo (si es modo 2)
    info_circulo = datos_reporte.get('info_circulo', None)
    
    # Calcular porcentajes
    pct_alto = (zonas_alto / total_zonas * 100) if total_zonas > 0 else 0
    pct_medio = (zonas_medio / total_zonas * 100) if total_zonas > 0 else 0
    pct_bajo = (zonas_bajo / total_zonas * 100) if total_zonas > 0 else 0
    
    # Generar HTML
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Análisis - {ciudad}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f0f2f5;
            padding: 0;
            min-height: 100vh;
            color: #1a1a1a;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 50px 60px;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 500px;
            height: 500px;
            background: rgba(255,255,255,0.05);
            border-radius: 50%;
        }}
        
        .header h1 {{
            font-size: 2.8em;
            font-weight: 800;
            margin-bottom: 12px;
            position: relative;
            z-index: 1;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            font-weight: 300;
            opacity: 0.95;
            position: relative;
            z-index: 1;
        }}
        
        .header .fecha {{
            margin-top: 20px;
            font-size: 0.95em;
            opacity: 0.85;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }}
        
        .content {{
            padding: 60px;
            background: #ffffff;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section-title {{
            font-size: 1.6em;
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 25px;
            padding-bottom: 12px;
            border-bottom: 3px solid #3b82f6;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 35px;
        }}
        
        .info-card {{
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 28px;
            border-radius: 16px;
            border-left: 5px solid #3b82f6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: all 0.3s ease;
        }}
        
        .info-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }}
        
        .info-card .label {{
            font-size: 0.85em;
            color: #64748b;
            margin-bottom: 8px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .info-card .value {{
            font-size: 1.8em;
            font-weight: 700;
            color: #1e293b;
        }}
        
        .stats-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin: 30px 0;
        }}
        
        .stat-card {{
            background: white;
            padding: 35px 30px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 6px;
            transition: height 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.12);
        }}
        
        .stat-card.alto::before {{
            background: linear-gradient(90deg, #dc2626, #ef4444);
        }}
        
        .stat-card.medio::before {{
            background: linear-gradient(90deg, #f59e0b, #fbbf24);
        }}
        
        .stat-card.bajo::before {{
            background: linear-gradient(90deg, #10b981, #34d399);
        }}
        
        .stat-card .icon {{
            font-size: 3.5em;
            margin-bottom: 15px;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
        }}
        
        .stat-card .numero {{
            font-size: 3em;
            font-weight: 800;
            margin: 15px 0;
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .stat-card .label {{
            font-size: 1em;
            color: #64748b;
            margin-bottom: 8px;
            font-weight: 600;
        }}
        
        .stat-card .porcentaje {{
            font-size: 1.4em;
            color: #94a3b8;
            font-weight: 600;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 12px;
            background: #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
            margin: 12px 0;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .progress-fill {{
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-weight: 700;
            font-size: 0.75em;
            transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 25px 0;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }}
        
        table thead {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
        }}
        
        table th {{
            padding: 18px 20px;
            text-align: left;
            font-weight: 700;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        table td {{
            padding: 16px 20px;
            border-bottom: 1px solid #f1f5f9;
            font-size: 0.95em;
        }}
        
        table tbody tr {{
            transition: background 0.2s ease;
        }}
        
        table tbody tr:hover {{
            background: #f8fafc;
        }}
        
        table tbody tr:last-child td {{
            border-bottom: none;
        }}
        
        .badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .badge.alto {{
            background: linear-gradient(135deg, #fee2e2, #fecaca);
            color: #991b1b;
        }}
        
        .badge.medio {{
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            color: #92400e;
        }}
        
        .badge.bajo {{
            background: linear-gradient(135deg, #d1fae5, #a7f3d0);
            color: #065f46;
        }}
        
        .historico-table {{
            background: #f8fafc;
            padding: 30px;
            border-radius: 16px;
            margin: 25px 0;
            border: 1px solid #e2e8f0;
        }}
        
        .historico-table h3 {{
            color: #1e3a8a;
            margin-bottom: 20px;
            font-size: 1.3em;
            font-weight: 700;
        }}
        
        .montecarlo-comparison {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }}
        
        .comparison-card {{
            background: white;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.06);
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }}
        
        .comparison-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        }}
        
        .comparison-card h3 {{
            color: #1e3a8a;
            margin-bottom: 20px;
            font-size: 1.4em;
            font-weight: 700;
            padding-bottom: 12px;
            border-bottom: 2px solid #3b82f6;
        }}
        
        .comparison-row {{
            display: flex;
            justify-content: space-between;
            padding: 14px 0;
            border-bottom: 1px solid #f1f5f9;
        }}
        
        .comparison-row:last-child {{
            border-bottom: none;
        }}
        
        .comparison-label {{
            color: #64748b;
            font-weight: 600;
            font-size: 0.9em;
        }}
        
        .comparison-value {{
            font-weight: 700;
            color: #1e293b;
            font-size: 1.1em;
        }}
        
        .algoritmos-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .algoritmo-item {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            font-weight: 700;
            font-size: 0.95em;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            transition: all 0.3s ease;
        }}
        
        .algoritmo-item:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
            
            .stat-card:hover {{
                transform: none;
            }}
        }}
        
        @media (max-width: 768px) {{
            .content {{
                padding: 30px 20px;
            }}
            
            .header {{
                padding: 30px 20px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .stats-cards {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>📊 Reporte de Análisis de Seguridad Urbana</h1>
            <div class="subtitle">Sistema de Diagnóstico con Inteligencia Artificial</div>
            <div class="fecha">📅 {datetime.now().strftime('%d de %B de %Y • %H:%M:%S')}</div>
        </div>
        
        <!-- CONTENT -->
        <div class="content">
            
            <!-- INFORMACIÓN GENERAL -->
            <div class="section">
                <div class="section-title">
                    📍 Información General
                </div>
                <div class="info-grid">
                    <div class="info-card">
                        <div class="label">Ciudad Analizada</div>
                        <div class="value">{ciudad}</div>
                    </div>
                    <div class="info-card">
                        <div class="label">Modo de Análisis</div>
                        <div class="value">{modo}</div>
                    </div>
                    <div class="info-card">
                        <div class="label">Total de Zonas</div>
                        <div class="value">{total_zonas}</div>
                    </div>
"""
    
    # Si es modo circular, agregar información del círculo
    if info_circulo:
        html += f"""
                    <div class="info-card">
                        <div class="label">Centro del Círculo</div>
                        <div class="value">[{info_circulo['fila']}, {info_circulo['columna']}]</div>
                    </div>
                    <div class="info-card">
                        <div class="label">Radio Analizado</div>
                        <div class="value">{info_circulo['radio']} metros</div>
                    </div>
"""
    
    html += """
                </div>
            </div>
            
            <!-- RESUMEN DE CLASIFICACIÓN -->
            <div class="section">
                <div class="section-title">
                    📊 Resumen de Clasificación de Riesgo
                </div>
                <div class="stats-cards">
                    <div class="stat-card alto">
                        <div class="icon">🔴</div>
                        <div class="label">Riesgo Alto</div>
                        <div class="numero">{}</div>
                        <div class="porcentaje">{}%</div>
                    </div>
                    <div class="stat-card medio">
                        <div class="icon">🟡</div>
                        <div class="label">Riesgo Medio</div>
                        <div class="numero">{}</div>
                        <div class="porcentaje">{}%</div>
                    </div>
                    <div class="stat-card bajo">
                        <div class="icon">🟢</div>
                        <div class="label">Riesgo Bajo</div>
                        <div class="numero">{}</div>
                        <div class="porcentaje">{}%</div>
                    </div>
                </div>
                
                <!-- Barras de progreso -->
                <div style="margin-top: 40px;">
                    <div style="margin-bottom: 25px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span style="color: #64748b; font-weight: 700; font-size: 0.9em;">RIESGO ALTO</span>
                            <span style="color: #64748b; font-weight: 700;">{:.1f}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {}%; background: linear-gradient(90deg, #dc2626, #ef4444);"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 25px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span style="color: #64748b; font-weight: 700; font-size: 0.9em;">RIESGO MEDIO</span>
                            <span style="color: #64748b; font-weight: 700;">{:.1f}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {}%; background: linear-gradient(90deg, #f59e0b, #fbbf24);"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span style="color: #64748b; font-weight: 700; font-size: 0.9em;">RIESGO BAJO</span>
                            <span style="color: #64748b; font-weight: 700;">{:.1f}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {}%; background: linear-gradient(90deg, #10b981, #34d399);"></div>
                        </div>
                    </div>
                </div>
            </div>
""".format(
        zonas_alto, pct_alto,
        zonas_medio, pct_medio,
        zonas_bajo, pct_bajo,
        pct_alto, pct_alto,
        pct_medio, pct_medio,
        pct_bajo, pct_bajo
    )
    
    # Algoritmos utilizados
    html += """
            <!-- ALGORITMOS UTILIZADOS -->
            <div class="section">
                <div class="section-title">
                    🧠 Algoritmos de Inteligencia Artificial Utilizados
                </div>
                <div class="algoritmos-grid">
                    <div class="algoritmo-item">BFS (Búsqueda en Anchura)</div>
                    <div class="algoritmo-item">DFS (Búsqueda en Profundidad)</div>
                    <div class="algoritmo-item">A* (Búsqueda Óptima)</div>
                    <div class="algoritmo-item">Algoritmo Genético</div>
                    <div class="algoritmo-item">Apriori (Reglas)</div>
                    <div class="algoritmo-item">PRISM (Reglas)</div>
                    <div class="algoritmo-item">Lógica Difusa</div>
                    <div class="algoritmo-item">Monte Carlo</div>
                </div>
            </div>
"""
    
    # Datos históricos
    if datos_historicos:
        html += """
            <!-- DATOS HISTÓRICOS -->
            <div class="section">
                <div class="section-title">
                    📈 Datos Históricos por Macro-Zona
                </div>
"""
        
        for zona, stats in datos_historicos.items():
            if stats:
                html += f"""
                <div class="historico-table">
                    <h3 style="color: #667eea; margin-bottom: 15px;">🔸 Zona {zona}</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Variable</th>
                                <th>Mínimo</th>
                                <th>Máximo</th>
                                <th>Media (μ)</th>
                                <th>Desv. Std (σ)</th>
                            </tr>
                        </thead>
                        <tbody>
"""
                
                variables = ['Robos', 'Microtrafico', 'Vandalismo', 'Accidentes', 'Llamadas911']
                nombres_display = {
                    'Robos': 'Robos',
                    'Microtrafico': 'Microtráfico',
                    'Vandalismo': 'Vandalismo',
                    'Accidentes': 'Accidentes de Tránsito',
                    'Llamadas911': 'Llamadas 911'
                }
                
                for var in variables:
                    if var in stats:
                        st = stats[var]
                        html += f"""
                            <tr>
                                <td><strong>{nombres_display[var]}</strong></td>
                                <td>{st.get('min', 0):.0f}</td>
                                <td>{st.get('max', 0):.0f}</td>
                                <td>{st.get('media', 0):.1f}</td>
                                <td>{st.get('std', 0):.1f}</td>
                            </tr>
"""
                
                html += """
                        </tbody>
                    </table>
                </div>
"""
        
        html += """
            </div>
"""
    
    # Comparación Monte Carlo
    if datos_montecarlo:
        html += """
            <!-- SIMULACIÓN MONTE CARLO -->
            <div class="section">
                <div class="section-title">
                    🎲 Simulación Monte Carlo (1000 escenarios)
                </div>
                <p style="color: #666; margin-bottom: 20px;">
                    Comparación entre datos históricos reales y simulaciones probabilísticas
                </p>
                <div class="montecarlo-comparison">
"""
        
        for zona, datos in datos_montecarlo.items():
            html += f"""
                    <div class="comparison-card">
                        <h3>Zona {zona}</h3>
                        <div class="comparison-row">
                            <span class="comparison-label">Media Histórica (Robos)</span>
                            <span class="comparison-value">{datos.get('media_historica', 0):.1f}</span>
                        </div>
                        <div class="comparison-row">
                            <span class="comparison-label">Media Simulada (Robos)</span>
                            <span class="comparison-value">{datos.get('media_simulada', 0):.1f}</span>
                        </div>
                        <div class="comparison-row">
                            <span class="comparison-label">Desviación Estándar</span>
                            <span class="comparison-value">{datos.get('std', 0):.1f}</span>
                        </div>
                        <div class="comparison-row">
                            <span class="comparison-label">Diferencia</span>
                            <span class="comparison-value">{abs(datos.get('media_simulada', 0) - datos.get('media_historica', 0)):.1f}</span>
                        </div>
                    </div>
"""
        
        html += """
                </div>
            </div>
"""
    
    # Detalle de zonas analizadas
    if detalles_zonas:
        html += """
            <!-- DETALLE DE ZONAS -->
            <div class="section">
                <div class="section-title">
                    📋 Detalle de Zonas Analizadas
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Zona</th>
                            <th>Coordenadas</th>
                            <th>Nivel de Riesgo</th>
                            <th>Factores Principales</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        
        for detalle in detalles_zonas:
            nivel = detalle.get('nivel', 'Bajo').lower()
            badge_class = 'alto' if nivel == 'alto' else 'medio' if nivel == 'medio' else 'bajo'
            icono = '🔴' if nivel == 'alto' else '🟡' if nivel == 'medio' else '🟢'
            
            html += f"""
                        <tr>
                            <td>{detalle.get('nombre', 'Desconocido')}</td>
                            <td>[{detalle.get('fila', '?')}, {detalle.get('columna', '?')}]</td>
                            <td><span class="badge {badge_class}">{icono} {detalle.get('nivel', 'Bajo').upper()}</span></td>
                            <td>{', '.join(detalle.get('factores', [])[:3])}</td>
                        </tr>
"""
        
        html += """
                    </tbody>
                </table>
            </div>
"""
    
    # Footer eliminado - Terminar el HTML
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    # Guardar archivo
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return ruta_salida
