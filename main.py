"""
main.py
=======
Sistema de Diagnóstico de Zonas de Peligro Urbano con IA
Universidad Técnica de Ambato - Inteligencia Artificial

Este sistema utiliza 7 algoritmos de IA para clasificar zonas urbanas:
- BFS, DFS, A* (búsqueda y conectividad)
- Algoritmo Genético (optimización)
- Apriori, PRISM (reglas de clasificación)
- Lógica Difusa (clasificación fuzzy)
"""

import sys
import os
import folium
from config import GRID_SIZE, OUTPUT_DIR, COLORES_RIESGO

# Importar módulos del sistema
try:
    from src.core import cargar_mapa, construir_grid, diagnostico_masivo
    from src.core.diagnostico import diagnosticar_zona  # Para análisis individual
    from src.algoritmos.difuso import mantener_graficas_abiertas  # Para mantener gráficas
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    print("   Verifica que la estructura del proyecto esté correcta.")
    sys.exit(1)


def mostrar_banner():
    """Muestra el banner inicial del sistema."""
    print("\n" + "="*70)
    print("  🚨 SISTEMA DE DIAGNÓSTICO DE ZONAS DE PELIGRO URBANO CON IA")
    print("="*70)
    print("  📍 Universidad Técnica de Ambato")
    print("  🧠 7 Algoritmos de IA: BFS, DFS, A*, AG, Apriori, PRISM, Fuzzy")
    print("="*70 + "\n")


def solicitar_ciudad():
    """Solicita al usuario la ciudad a analizar."""
    ciudades = ["Quito", "Guayaquil", "Cuenca", "Ambato", "Riobamba", "Loja"]
    print("  Ciudades: " + " | ".join(ciudades))
    ciudad = input("\n  Ciudad a analizar: ").strip()
    
    if not ciudad:
        ciudad = "Ambato"  # Por defecto Ambato (UTA)
    
    if "Ecuador" not in ciudad and "ecuador" not in ciudad:
        ciudad = f"{ciudad}, Ecuador"
    
    return ciudad


def solicitar_modo_analisis():
    """Pregunta al usuario qué tipo de análisis desea."""
    print("\n  MODO DE ANÁLISIS:")
    print("  ─" * 35)
    print("  1️⃣  Análisis completo (todas las zonas)")
    print("  2️⃣  Análisis de zona específica (diagnóstico detallado)")
    print("  ─" * 35)
    
    opcion = input("\n  Selecciona opción (1/2): ").strip()
    return opcion if opcion in ['1', '2'] else '1'


def generar_mapa_grid(G, grid, grid_size, ciudad):
    """Genera un mapa HTML interactivo con círculo movible y slider de zoom."""
    filas, columnas = grid_size
    
    # Obtener centro del mapa y límites
    nodos = list(G.nodes(data=True))
    if not nodos:
        return None
    
    lats = [data['y'] for _, data in nodos]
    lons = [data['x'] for _, data in nodos]
    centro_lat = sum(lats) / len(lats)
    centro_lon = sum(lons) / len(lons)
    
    # Calcular límites del grid
    north = max(grid[i, j]['lat'] for i in range(filas) for j in range(columnas))
    south = min(grid[i, j]['lat'] for i in range(filas) for j in range(columnas))
    east = max(grid[i, j]['lon'] for i in range(filas) for j in range(columnas))
    west = min(grid[i, j]['lon'] for i in range(filas) for j in range(columnas))
    
    # Crear datos del grid en formato JSON para JavaScript
    import json
    grid_data = []
    for i in range(filas):
        for j in range(columnas):
            zona = grid[i, j]
            grid_data.append({
                'fila': i,
                'columna': j,
                'lat': zona['lat'],
                'lon': zona['lon']
            })
    
    # Crear HTML con mapa interactivo
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Selección de Zona - {ciudad}</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }}
        #map {{
            position: absolute;
            top: 0;
            bottom: 120px;
            left: 0;
            right: 0;
        }}
        #controls {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 120px;
            background: white;
            border-top: 2px solid #2196F3;
            padding: 15px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        }}
        #info {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: white;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
            min-width: 200px;
        }}
        .slider-container {{
            margin: 10px 0;
        }}
        .slider-label {{
            display: inline-block;
            width: 150px;
            font-weight: bold;
            color: #333;
        }}
        input[type="range"] {{
            width: 300px;
            vertical-align: middle;
        }}
        .value-display {{
            display: inline-block;
            width: 60px;
            text-align: right;
            font-weight: bold;
            color: #2196F3;
        }}
        button {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
            font-weight: bold;
        }}
        button:hover {{
            background: #45a049;
        }}
        .info-item {{
            margin: 8px 0;
            font-size: 14px;
        }}
        .info-label {{
            font-weight: bold;
            color: #666;
        }}
        .info-value {{
            color: #2196F3;
            font-weight: bold;
            font-size: 16px;
        }}
        #instructions {{
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
            max-width: 300px;
        }}
        #instructions h3 {{
            margin: 0 0 10px 0;
            color: #2196F3;
            font-size: 16px;
        }}
        #instructions ul {{
            margin: 5px 0;
            padding-left: 20px;
        }}
        #instructions li {{
            margin: 5px 0;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div id="instructions">
        <h3>📍 Cómo usar:</h3>
        <ul>
            <li>🖱️ <b>Click en el mapa</b> para mover el círculo</li>
            <li>🎚️ <b>Usa el slider</b> para ajustar el tamaño</li>
            <li>🔍 <b>Zoom</b> con la rueda o botones +/-</li>
            <li>✅ <b>Confirma</b> cuando estés listo</li>
        </ul>
    </div>
    
    <div id="info">
        <div class="info-item">
            <span class="info-label">Zona:</span>
            <span class="info-value" id="zona-coords">[?,?]</span>
        </div>
        <div class="info-item">
            <span class="info-label">Lat:</span>
            <span class="info-value" id="lat-display">-</span>
        </div>
        <div class="info-item">
            <span class="info-label">Lon:</span>
            <span class="info-value" id="lon-display">-</span>
        </div>
    </div>
    
    <div id="map"></div>
    
    <div id="controls">
        <div class="slider-container">
            <span class="slider-label">🎯 Tamaño del círculo:</span>
            <input type="range" id="radius-slider" min="50" max="500" value="150" step="10">
            <span class="value-display" id="radius-value">150m</span>
        </div>
        <div style="text-align: center; margin-top: 10px;">
            <button onclick="confirmarZona()">✅ Confirmar Zona Seleccionada</button>
            <button onclick="resetearCirculo()" style="background: #ff9800;">🔄 Resetear</button>
        </div>
    </div>

    <script>
        // Datos del grid
        const gridData = {json.dumps(grid_data)};
        const gridSize = {json.dumps([filas, columnas])};
        const bounds = [[{south}, {west}], [{north}, {east}]];
        
        // Crear mapa
        const map = L.map('map').setView([{centro_lat}, {centro_lon}], 13);
        
        // Agregar capa de OpenStreetMap
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18
        }}).addTo(map);
        
        // Dibujar grid de zonas (puntos pequeños)
        gridData.forEach(zona => {{
            L.circleMarker([zona.lat, zona.lon], {{
                radius: 2,
                color: '#999',
                fillColor: '#ddd',
                fillOpacity: 0.3,
                weight: 1
            }}).addTo(map);
        }});
        
        // Círculo de selección
        let circle = L.circle([{centro_lat}, {centro_lon}], {{
            color: '#FF5722',
            fillColor: '#FF5722',
            fillOpacity: 0.3,
            radius: 150,
            weight: 3
        }}).addTo(map);
        
        let selectedZona = null;
        
        // Función para encontrar la zona más cercana
        function encontrarZonaCercana(lat, lon) {{
            let minDist = Infinity;
            let zonaEncontrada = null;
            
            gridData.forEach(zona => {{
                const dist = Math.sqrt(
                    Math.pow(zona.lat - lat, 2) + 
                    Math.pow(zona.lon - lon, 2)
                );
                if (dist < minDist) {{
                    minDist = dist;
                    zonaEncontrada = zona;
                }}
            }});
            
            return zonaEncontrada;
        }}
        
        // Actualizar info de la zona
        function actualizarInfo(zona) {{
            if (zona) {{
                selectedZona = zona;
                document.getElementById('zona-coords').textContent = 
                    `[${{zona.fila}},${{zona.columna}}]`;
                document.getElementById('lat-display').textContent = 
                    zona.lat.toFixed(5);
                document.getElementById('lon-display').textContent = 
                    zona.lon.toFixed(5);
            }}
        }}
        
        // Click en el mapa
        map.on('click', function(e) {{
            const lat = e.latlng.lat;
            const lon = e.latlng.lng;
            
            // Mover círculo
            circle.setLatLng([lat, lon]);
            
            // Encontrar zona más cercana
            const zona = encontrarZonaCercana(lat, lon);
            actualizarInfo(zona);
        }});
        
        // Slider de radio
        const radiusSlider = document.getElementById('radius-slider');
        const radiusValue = document.getElementById('radius-value');
        
        radiusSlider.addEventListener('input', function() {{
            const radius = parseInt(this.value);
            circle.setRadius(radius);
            radiusValue.textContent = radius + 'm';
        }});
        
        // Función para confirmar zona
        function confirmarZona() {{
            if (selectedZona) {{
                // Mostrar coordenadas en alerta grande
                alert(`✅ ZONA SELECCIONADA\\n\\n` +
                      `Fila: ${{selectedZona.fila}}\\n` +
                      `Columna: ${{selectedZona.columna}}\\n\\n` +
                      `📍 Coordenadas:\\n` +
                      `Lat: ${{selectedZona.lat.toFixed(5)}}\\n` +
                      `Lon: ${{selectedZona.lon.toFixed(5)}}\\n\\n` +
                      `ANOTA ESTOS VALORES:\\n` +
                      `Fila: ${{selectedZona.fila}}\\n` +
                      `Columna: ${{selectedZona.columna}}\\n\\n` +
                      `Ahora vuelve a la consola y escríbelos.`);
            }} else {{
                alert('Por favor, haz click en el mapa para seleccionar una zona.');
            }}
        }}
        
        // Función para resetear
        function resetearCirculo() {{
            circle.setLatLng([{centro_lat}, {centro_lon}]);
            circle.setRadius(150);
            radiusSlider.value = 150;
            radiusValue.textContent = '150m';
            selectedZona = null;
            document.getElementById('zona-coords').textContent = '[?,?]';
            document.getElementById('lat-display').textContent = '-';
            document.getElementById('lon-display').textContent = '-';
        }}
        
        // Inicializar con la zona del centro
        const zonaInicial = encontrarZonaCercana({centro_lat}, {centro_lon});
        actualizarInfo(zonaInicial);
    </script>
</body>
</html>
"""
    
    # Guardar mapa interactivo
    ruta_mapa = os.path.join(OUTPUT_DIR, f"grid_{ciudad.replace(', ', '_').replace(' ', '_')}.html")
    with open(ruta_mapa, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return ruta_mapa


def solicitar_zona(grid_size, G, grid, ciudad):
    """
    Interfaz interactiva para seleccionar el CENTRO del círculo de análisis.
    Retorna: (fila_centro, columna_centro, lista_de_zonas_en_circulo, radio_metros)
    """
    import tkinter as tk
    from tkinter import ttk
    import math
    try:
        from tkintermapview import TkinterMapView
    except ImportError:
        print("  ⚠️  Instalando tkintermapview...")
        import subprocess
        subprocess.check_call([__import__('sys').executable, "-m", "pip", "install", "tkintermapview"])
        from tkintermapview import TkinterMapView

    filas, columnas = grid_size
    zona_seleccionada = {'fila': None, 'columna': None, 'lat': None, 'lon': None}
    radio_metros = {'valor': 150}
    zonas_en_circulo = {'lista': []}

    print(f"\n  🗺️  Abriendo mapa interactivo...")
    print(f"  💡 Mueve el mouse, ajusta el slider y haz click para confirmar")

    nodos = list(G.nodes(data=True))
    lats = [d['y'] for _, d in nodos]
    lons = [d['x'] for _, d in nodos]
    centro_lat = sum(lats) / len(lats)
    centro_lon = sum(lons) / len(lons)

    # ── Ventana ───────────────────────────────────────────────────────────────
    ventana = tk.Tk()
    ventana.title(f"Selección de Zona - {ciudad}")
    ventana.geometry("1200x800")
    ventana.configure(bg='#f5f5f5')

    # ── Panel lateral izquierdo ────────────────────────────────────────────────
    panel_izq = tk.Frame(ventana, bg='white', width=300, relief='raised', borderwidth=2)
    panel_izq.pack(side='left', fill='y')
    panel_izq.pack_propagate(False)

    hdr = tk.Frame(panel_izq, bg='#2196F3', height=60)
    hdr.pack(fill='x')
    hdr.pack_propagate(False)
    tk.Label(hdr, text="📊 INFORMACIÓN DE ZONA",
             font=('Arial', 12, 'bold'), bg='#2196F3', fg='white').pack(pady=18)

    info_box = tk.Frame(panel_izq, bg='white', pady=10)
    info_box.pack(fill='x', padx=15)

    tk.Label(info_box, text="Centro del círculo:", font=('Arial', 10),
             bg='white', fg='#666').pack(anchor='w')
    zona_label = tk.Label(info_box, text="[?,?]",
                          font=('Arial', 24, 'bold'), bg='white', fg='#2196F3')
    zona_label.pack(anchor='w', pady=(0, 4))

    zonas_count_label = tk.Label(info_box, text="0 zonas en el círculo",
                                 font=('Arial', 11, 'bold'), bg='white', fg='#FF5722')
    zonas_count_label.pack(anchor='w', pady=(0, 12))

    tk.Label(info_box, text="Coordenadas:", font=('Arial', 10),
             bg='white', fg='#666').pack(anchor='w')
    coords_label = tk.Label(info_box, text="Lat: -\nLon: -",
                            font=('Arial', 10), bg='white', fg='#333')
    coords_label.pack(anchor='w', pady=(0, 16))

    ttk.Separator(panel_izq, orient='horizontal').pack(fill='x', padx=15, pady=8)

    # Slider
    sl_box = tk.Frame(panel_izq, bg='white', pady=8)
    sl_box.pack(fill='x', padx=15)
    tk.Label(sl_box, text="🎯 Radio del círculo:",
             font=('Arial', 10, 'bold'), bg='white', fg='#333').pack(anchor='w')
    radio_label = tk.Label(sl_box, text="150 metros",
                           font=('Arial', 12, 'bold'), bg='white', fg='#FF5722')
    radio_label.pack(anchor='w', pady=(4, 8))
    slider = ttk.Scale(sl_box, from_=50, to=500, orient='horizontal', length=250, value=150)
    slider.pack(fill='x')
    sl_lims = tk.Frame(sl_box, bg='white')
    sl_lims.pack(fill='x')
    tk.Label(sl_lims, text="50m",  font=('Arial', 8), bg='white', fg='#999').pack(side='left')
    tk.Label(sl_lims, text="500m", font=('Arial', 8), bg='white', fg='#999').pack(side='right')

    ttk.Separator(panel_izq, orient='horizontal').pack(fill='x', padx=15, pady=16)    # Instrucciones
    inst_box = tk.Frame(panel_izq, bg='white')
    inst_box.pack(fill='x', padx=15)
    tk.Label(inst_box, text="💡 Cómo usar:",
             font=('Arial', 10, 'bold'), bg='white', fg='#333').pack(anchor='w')
    for txt in ["1. Mueve el mouse sobre el mapa",
                "2. Ajusta el radio con el slider",
                "3. Haz click para confirmar",
                "4. Se analizarán TODAS las zonas"]:
        tk.Label(inst_box, text=txt, font=('Arial', 9),
                 bg='white', fg='#666', justify='left').pack(anchor='w', pady=1)

    ttk.Separator(panel_izq, orient='horizontal').pack(fill='x', padx=15, pady=16)

    # Botón para iniciar análisis (se habilita al hacer click en el mapa)
    btn_iniciar = tk.Button(
        panel_izq,
        text="▶  INICIAR ANÁLISIS",
        font=('Arial', 12, 'bold'),
        bg='#4CAF50', fg='white',
        activebackground='#388E3C', activeforeground='white',
        relief='flat', cursor='hand2', pady=10,
        state='disabled',
        command=lambda: ventana.destroy()
    )
    btn_iniciar.pack(fill='x', padx=15, pady=(0, 10))

    # ── Header + mapa ──────────────────────────────────────────────────────────
    hdr_mapa = tk.Frame(ventana, bg='#2196F3', height=56)
    hdr_mapa.pack(side='top', fill='x')
    hdr_mapa.pack_propagate(False)
    titulo = tk.Label(hdr_mapa, text=f"🎯 Selecciona el centro del análisis - {ciudad}",
                      font=('Arial', 15, 'bold'), bg='#2196F3', fg='white')
    titulo.pack(pady=10)
    subtitulo = tk.Label(hdr_mapa, text="Mueve el mouse sobre el mapa",
                         font=('Arial', 10), bg='#2196F3', fg='#E3F2FD')
    subtitulo.pack()

    mapa_widget = TkinterMapView(ventana, corner_radius=0)
    mapa_widget.pack(side='top', fill='both', expand=True)
    mapa_widget.set_position(centro_lat, centro_lon)
    mapa_widget.set_zoom(14)

    circulo_hover = {'polygon': None}
    marcadores_zonas = []
    marcador_centro = {'marker': None}
    ultima_pos = {'lat': None, 'lon': None}

    # ── Funciones internas ────────────────────────────────────────────────────
    def calcular_dist_metros(lat1, lon1, lat2, lon2):
        R = 6371000
        p1, p2 = math.radians(lat1), math.radians(lat2)
        dp = math.radians(lat2 - lat1)
        dl = math.radians(lon2 - lon1)
        a = math.sin(dp/2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def zonas_en_radio(clat, clon, radio_m):
        resultado = []
        for i in range(filas):
            for j in range(columnas):
                z = grid[i, j]
                if calcular_dist_metros(clat, clon, z['lat'], z['lon']) <= radio_m:
                    resultado.append((i, j))
        return resultado

    def encontrar_zona_mas_cercana(lat, lon):
        min_d, cerca = float('inf'), (0, 0)
        for i in range(filas):
            for j in range(columnas):
                z = grid[i, j]
                d = (z['lat']-lat)**2 + (z['lon']-lon)**2
                if d < min_d:
                    min_d, cerca = d, (i, j)
        return cerca

    def dibujar_circulo(lat, lon, radio_m, color='#2196F3'):
        rad_deg = radio_m / 111000
        pts = []
        for k in range(64):
            ang = 2 * math.pi * k / 64
            pts.append((lat + rad_deg * math.cos(ang),
                        lon + rad_deg * math.sin(ang) / math.cos(math.radians(lat))))
        try:
            return mapa_widget.set_polygon(pts, fill_color=color,
                                           outline_color=color, border_width=2)
        except Exception:
            return None

    def actualizar_panel(fila, col, lat, lon, radio_m):
        zona_label.config(text=f"[{fila},{col}]")
        coords_label.config(text=f"Lat: {lat:.5f}\nLon: {lon:.5f}")
        subtitulo.config(text=f"Centro [{fila},{col}] - Click para confirmar")
        zonas = zonas_en_radio(lat, lon, radio_m)
        zonas_en_circulo['lista'] = zonas
        n = len(zonas)
        icono = '🔴' if n > 6 else '🟡' if n > 2 else '🟢'
        zonas_count_label.config(text=f"{icono} {n} zona{'s' if n != 1 else ''} en el círculo",
                                 fg='#4CAF50' if n > 0 else '#999')

    def hover_mapa(event):
        coords = mapa_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        if not coords:
            return
        lat, lon = coords
        if (ultima_pos['lat'] is not None and
                abs(lat - ultima_pos['lat']) < 0.0005 and
                abs(lon - ultima_pos['lon']) < 0.0005):
            return
        ultima_pos['lat'], ultima_pos['lon'] = lat, lon
        fila, col = encontrar_zona_mas_cercana(lat, lon)
        zi = grid[fila, col]
        if circulo_hover['polygon']:
            circulo_hover['polygon'].delete()
        circulo_hover['polygon'] = dibujar_circulo(zi['lat'], zi['lon'], radio_metros['valor'])
        actualizar_panel(fila, col, zi['lat'], zi['lon'], radio_metros['valor'])

    def click_mapa(coords):
        lat, lon = coords
        fila, col = encontrar_zona_mas_cercana(lat, lon)
        zi = grid[fila, col]
        radio_m = radio_metros['valor']
        zonas = zonas_en_radio(zi['lat'], zi['lon'], radio_m)

        zona_seleccionada.update({'fila': fila, 'columna': col,
                                   'lat': zi['lat'], 'lon': zi['lon']})
        zonas_en_circulo['lista'] = zonas

        # Limpiar marcadores anteriores
        for m in marcadores_zonas:
            try:
                m.delete()
            except Exception:
                pass
        marcadores_zonas.clear()

        # Marcadores verdes en TODAS las zonas del círculo
        for (fi, co) in zonas:
            z = grid[fi, co]
            barrio = z.get('nombre', '')
            label = f"{barrio} [{fi},{co}]" if barrio else f"[{fi},{co}]"
            mk = mapa_widget.set_marker(z['lat'], z['lon'],
                                        text=label,
                                        marker_color_circle="#4CAF50",
                                        marker_color_outside="#2E7D32")
            marcadores_zonas.append(mk)

        # Marcador amarillo en el centro
        if marcador_centro['marker']:
            try:
                marcador_centro['marker'].delete()
            except Exception:
                pass
        centro_barrio = zi.get('nombre', '')
        centro_label  = f"CENTRO: {centro_barrio} [{fila},{col}]" if centro_barrio else f"CENTRO [{fila},{col}]"
        marcador_centro['marker'] = mapa_widget.set_marker(
            zi['lat'], zi['lon'],
            text=centro_label,
            marker_color_circle="#FFC107",
            marker_color_outside="#FF6F00")

        n = len(zonas)
        subtitulo.config(text=f"✅ {n} zonas seleccionadas — presiona ▶ INICIAR ANÁLISIS para continuar")
        btn_iniciar.config(state='normal', bg='#4CAF50')

    def actualizar_radio(valor):
        nuevo = int(float(valor))
        radio_metros['valor'] = nuevo
        radio_label.config(text=f"{nuevo} metros")
        if ultima_pos['lat'] is not None:
            if circulo_hover['polygon']:
                circulo_hover['polygon'].delete()
            fila, col = encontrar_zona_mas_cercana(ultima_pos['lat'], ultima_pos['lon'])
            zi = grid[fila, col]
            circulo_hover['polygon'] = dibujar_circulo(zi['lat'], zi['lon'], nuevo)
            actualizar_panel(fila, col, zi['lat'], zi['lon'], nuevo)

    # ── Conectar eventos ──────────────────────────────────────────────────────
    slider.config(command=actualizar_radio)
    mapa_widget.add_left_click_map_command(click_mapa)
    mapa_widget.canvas.bind('<Motion>', hover_mapa)

    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth()  // 2) - (ventana.winfo_width()  // 2)
    y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
    ventana.geometry(f"+{x}+{y}")
    ventana.mainloop()

    # ── Resultado ─────────────────────────────────────────────────────────────
    if zona_seleccionada['fila'] is not None:
        fila   = zona_seleccionada['fila']
        col    = zona_seleccionada['columna']
        zonas  = zonas_en_circulo['lista']
        radio  = radio_metros['valor']
        print(f"\n  Centro: [{fila},{col}]  |  Radio: {radio}m  |  Zonas: {len(zonas)}")
        for z in zonas:
            barrio = grid[z[0], z[1]].get('nombre', '')
            etiq   = f"{barrio} [{z[0]},{z[1]}]" if barrio else f"[{z[0]},{z[1]}]"
            print(f"     * {etiq}")
        print(f"  Iniciando analisis de {len(zonas)} zonas...\n")
        return fila, col, zonas, radio
    else:
        print("\n  ⚠️  Sin selección. Usando centro [15,15] radio 150m")
        return 15, 15, [(15, 15)], 150


def generar_mapa_html(resultados, ciudad, G, grid, ruta_archivo):
    """Genera un mapa HTML interactivo con los resultados del diagnóstico."""
    # Obtener el centro del mapa
    nodos = list(G.nodes(data=True))
    if not nodos:
        print("  ⚠️ No hay nodos en el grafo")
        return
    
    lats = [data['y'] for _, data in nodos]
    lons = [data['x'] for _, data in nodos]
    centro_lat = sum(lats) / len(lats)
    centro_lon = sum(lons) / len(lons)
    
    # Crear mapa base
    mapa = folium.Map(
        location=[centro_lat, centro_lon],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Agregar marcadores de zonas
    for (i, j), diagnostico in resultados.items():
        zona_info = grid[i, j]
        lat = zona_info['lat']
        lon = zona_info['lon']
        
        # Color según nivel de riesgo
        color = COLORES_RIESGO.get(diagnostico['nivel'], '#gray')
        
        # Crear popup con información
        popup_html = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="margin: 0; color: {color};">
                {diagnostico['nivel'].upper()}
            </h4>
            <hr style="margin: 5px 0;">
            <p><b>📍 Zona:</b> [{i},{j}]</p>
            <p><b>📊 Factores:</b><br>{', '.join(diagnostico['factores'])}</p>
            <p><b>📜 Regla:</b><br>{diagnostico['regla']}</p>
        </div>
        """
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            popup=folium.Popup(popup_html, max_width=300),
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.6
        ).add_to(mapa)
    
    # Guardar mapa
    mapa.save(ruta_archivo)


def main():
    """Función principal del sistema."""
    try:
        # 1. Banner y solicitar ciudad
        mostrar_banner()
        ciudad = solicitar_ciudad()
        
        # 2. Seleccionar modo de análisis
        modo = solicitar_modo_analisis()
        
        # 3. Cargar mapa (puede tardar 1-2 min la primera vez)
        print(f"\n  🗺️  Iniciando análisis: {ciudad}")
        try:
            G, bbox = cargar_mapa(ciudad)
        except Exception as e:
            print(f"  ❌ Error descargando mapa: {e}")
            print("     Verifica tu conexión a internet.")
            return
        
        # 4. Construir grid
        print(f"  🔲 Generando grid {GRID_SIZE[0]}x{GRID_SIZE[1]}...")
        grid, zonas = construir_grid(G, bbox, filas=GRID_SIZE[0], columnas=GRID_SIZE[1])
        print(f"  ✅ {len(zonas)} zonas creadas")
        
        # 5. Ejecutar según el modo seleccionado
        if modo == '2':
            # MODO 2: Análisis de zona específica (con círculo)
            fila_centro, columna_centro, zonas_circulo, radio = solicitar_zona(GRID_SIZE, G, grid, ciudad)
            
            print(f"\n{'='*70}")
            print(f"  🔍 ANÁLISIS DE ZONA CIRCULAR")
            print(f"  📍 Centro: [{fila_centro},{columna_centro}]")
            print(f"  📏 Radio: {radio} metros")
            print(f"  📊 Total de zonas a analizar: {len(zonas_circulo)}")
            print(f"{'='*70}")
            resultados_circulo = {}
            for idx, (fi, co) in enumerate(zonas_circulo):
                print(f"\n  [{idx+1}/{len(zonas_circulo)}] Analizando zona [{fi},{co}]...")
                resultado = diagnosticar_zona(grid, fi, co, G, grid_shape=GRID_SIZE)
                resultados_circulo[(fi, co)] = resultado

            # Resumen del análisis circular
            print(f"\n{'='*70}")
            print(f"  ✅ DIAGNÓSTICO CIRCULAR COMPLETADO")
            print(f"{'='*70}")
            total = len(resultados_circulo)
            alto  = sum(1 for r in resultados_circulo.values() if r['nivel'].lower() == 'alto')
            medio = sum(1 for r in resultados_circulo.values() if r['nivel'].lower() == 'medio')
            bajo  = sum(1 for r in resultados_circulo.values() if r['nivel'].lower() == 'bajo')
            
            print(f"  📍 Centro del círculo: [{fila_centro},{columna_centro}]")
            print(f"  📏 Radio analizado: {radio} metros")
            print(f"  📊 {total} zonas analizadas:")
            print(f"     🔴 Alto riesgo:  {alto:>3} zonas ({alto/total*100:>5.1f}%)")
            print(f"     🟡 Medio riesgo: {medio:>3} zonas ({medio/total*100:>5.1f}%)")
            print(f"     🟢 Bajo riesgo:  {bajo:>3} zonas ({bajo/total*100:>5.1f}%)")
            print(f"\n  Detalle por zona:")
            print(f"  {'─'*72}")
            for (fi, co), r in sorted(resultados_circulo.items()):
                icono = '🔴' if r['nivel'].lower() == 'alto' else '🟡' if r['nivel'].lower() == 'medio' else '🟢'
                nombre_raw = r.get('nombre', '')
                # Filtrar fallbacks con coordenadas crudas que pudieran venir de caché antigua
                import re as _re
                if not nombre_raw or _re.match(r"^(Zona|Sector)\s*\[[-\d.]+,[-\d.]+\]", nombre_raw):
                    nombre = f"Sector [{fi},{co}]"
                else:
                    nombre = nombre_raw
                print(f"  {icono} {nombre:<40} → {r['nivel'].upper():<6}  ({', '.join(r['factores'][:2])})")
            print(f"{'='*70}\n")
            
        else:
            # MODO 1: Análisis completo de todas las zonas
            print(f"\n  🧠 Ejecutando algoritmos de IA...")
            resultados = diagnostico_masivo(grid, zonas, G)
            print(f"  ✅ Análisis completado")
            
            # Generar mapa HTML
            print(f"\n  🗺️  Generando mapa HTML...")
            nombre_archivo = f"mapa_{ciudad.replace(', ', '_').replace(' ', '_')}.html"
            ruta_mapa = os.path.join(OUTPUT_DIR, nombre_archivo)
            generar_mapa_html(resultados, ciudad, G, grid, ruta_mapa)
            
            # Mostrar resumen
            total = len(resultados)
            bajo = sum(1 for r in resultados.values() if r['nivel'].lower() == 'bajo')
            medio = sum(1 for r in resultados.values() if r['nivel'].lower() == 'medio')
            alto = sum(1 for r in resultados.values() if r['nivel'].lower() == 'alto')
            
            print(f"\n  📊 RESUMEN:")
            print(f"     🔴 Alto:  {alto:>3} zonas ({alto/total*100:>5.1f}%)")
            print(f"     🟡 Medio: {medio:>3} zonas ({medio/total*100:>5.1f}%)")
            print(f"     🟢 Bajo:  {bajo:>3} zonas ({bajo/total*100:>5.1f}%)")
            print(f"\n  🎉 Mapa guardado: {ruta_mapa}")
            print(f"  ✅ Análisis completado exitosamente!\n")
            
            # Mantener gráficas de membresía abiertas para la presentación
            mantener_graficas_abiertas()
        
    except KeyboardInterrupt:
        print("\n\n  ⚠️  Proceso interrumpido.\n")
    except Exception as e:
        print(f"\n  ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

