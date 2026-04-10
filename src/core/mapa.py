"""
mapa.py
=======
Módulo para descargar y procesar mapas reales de ciudades o países usando OSMnx.
"""
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

def cargar_mapa(ciudad):
    """Carga mapa desde OSM con configuración optimizada."""
    # Configurar OSMnx para ser más rápido y silencioso
    ox.settings.use_cache = True
    ox.settings.log_console = False
    ox.settings.timeout = 180  # Timeout de 3 minutos
    
    print(f"  📡 Descargando desde OpenStreetMap... (puede tardar 1-2 min)")
    
    # Descargar mapa con manejo de errores
    try:
        G = ox.graph_from_place(ciudad, network_type='drive')
        print(f"  ✅ Mapa descargado: {G.number_of_nodes()} intersecciones, {G.number_of_edges()} calles")
    except Exception as e:
        print(f"  ❌ Error descargando mapa: {e}")
        raise
    
    # Calcular bbox
    nodes = ox.graph_to_gdfs(G, edges=False)
    north = nodes.geometry.y.max()
    south = nodes.geometry.y.min()
    east = nodes.geometry.x.max()
    west = nodes.geometry.x.min()
    bbox = (north, south, east, west)
    
    return G, bbox

def visualizar_grafo(G, ciudad):
    """
    Visualiza el grafo del mapa real descargado desde OSM.
    Muestra nodos (intersecciones) y aristas (calles).
    """
    print(f"\n{'='*60}")
    print(f"  VISUALIZACIÓN DEL MAPA REAL - {ciudad.upper()}")
    print(f"{'='*60}")
    print(f"  📊 Estadísticas del grafo:")
    print(f"     • Nodos (intersecciones): {G.number_of_nodes()}")
    print(f"     • Aristas (calles): {G.number_of_edges()}")
    print(f"  📍 Fuente: OpenStreetMap (OSM)")
    print(f"  🔗 Tipo: Grafo dirigido de red vial urbana")
    print(f"{'='*60}\n")
    
    fig, ax = ox.plot_graph(
        G, 
        node_size=2, 
        node_color='#66ccff',
        edge_linewidth=0.5,
        edge_color='#888888',
        bgcolor='#0a0a0a',
        show=False,
        close=False
    )
    
    ax.set_title(f'Mapa Real de {ciudad}\n(Descargado desde OpenStreetMap)', 
                 color='white', fontsize=14, fontweight='bold', pad=20)
    
    # Agregar leyenda explicativa
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#66ccff', label='Intersecciones (nodos)'),
        Patch(facecolor='#888888', label='Calles (aristas)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', 
              facecolor='#1a1a1a', edgecolor='white', labelcolor='white')
    
    plt.tight_layout()
    plt.show()
    
    print("[Sistema] Grafo visualizado. Cierra la ventana para continuar...\n")

def _obtener_nombre_barrio(lat, lon):
    """
    Consulta Nominatim reverse-geocoding y devuelve el nombre más descriptivo
    disponible para la ubicación dada.

    Estrategia (de más a menos específico):
      1. neighbourhood / suburb / quarter / hamlet / village / city_district
      2. Compuesto "road, city_district"  (ej: "Av. Los Shyris, La Floresta")
      3. road solo                         (ej: "Calle Sucre")
      4. city_district / county / state_district
      5. "city, state"                     (ej: "Ambato, Tungurahua")
      6. Último recurso: "Sector [fila]"   — NUNCA coordenadas crudas
    """
    import urllib.request
    import json

    try:
        url = (
            "https://nominatim.openstreetmap.org/reverse"
            f"?lat={lat}&lon={lon}&format=json&zoom=17&addressdetails=1"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "SeguridadCiudadanaIA/1.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode())
    except Exception:
        return None   # Señal: no hay nombre → el llamador decide el fallback

    addr = data.get("address", {})

    # ── 1. Nombre de barrio / vecindario específico ───────────────────────────
    for campo in ("neighbourhood", "suburb", "quarter", "hamlet",
                  "village", "city_district"):
        val = addr.get(campo, "").strip()
        if val:
            return val

    # ── 2. Nombre compuesto: calle + barrio/distrito ──────────────────────────
    road    = addr.get("road", "").strip()
    distrit = (addr.get("city_district") or addr.get("suburb") or
               addr.get("county") or "").strip()
    if road and distrit:
        return f"{road}, {distrit}"

    # ── 3. Solo la calle ──────────────────────────────────────────────────────
    if road:
        return road

    # ── 4. Nivel superior: condado / sector administrativo ───────────────────
    for campo in ("county", "state_district", "state"):
        val = addr.get(campo, "").strip()
        if val:
            return val

    # ── 5. Ciudad + provincia ─────────────────────────────────────────────────
    city  = (addr.get("city") or addr.get("town") or addr.get("municipality") or "").strip()
    state = addr.get("state", "").strip()
    if city and state:
        return f"{city}, {state}"
    if city:
        return city

    # ── 6. Sin datos útiles → señal para el llamador ─────────────────────────
    return None


def construir_grid(G, bbox, filas=30, columnas=30):
    """
    Construye el grid de zonas con nombres de barrios.

    Optimización de velocidad:
      - Usa bloques de PASO×PASO celdas → solo (filas/PASO)*(cols/PASO) peticiones
      - Guarda el cache en disco (data/cache/nombres_<hash>.json) →
        la 2ª ejecución con el mismo bbox es INSTANTÁNEA (0 peticiones Nominatim)
    """
    import numpy as np
    import time
    import json
    import os
    import hashlib

    north, south, east, west = bbox
    lat_step = (north - south) / filas
    lon_step = (east - west) / columnas
    grid = np.zeros((filas, columnas), dtype=object)
    zonas = []

    # ── Cache en disco ────────────────────────────────────────────────────────
    # Clave única basada en bbox + tamaño de grid
    bbox_key  = f"{north:.5f},{south:.5f},{east:.5f},{west:.5f},{filas},{columnas}"
    cache_hash = hashlib.md5(bbox_key.encode()).hexdigest()[:12]
    # Guardar junto al cache de OSMnx (data/cache/)
    cache_dir  = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'cache')
    cache_dir  = os.path.normpath(cache_dir)
    cache_file = os.path.join(cache_dir, f"nombres_{cache_hash}.json")

    cache_nombres = {}

    if os.path.exists(cache_file):
        # ── Carga instantánea desde disco ────────────────────────────────────
        print("  ✅ Nombres de barrios cargados desde caché local (instantáneo)")
        with open(cache_file, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        # Las claves JSON son strings → convertir a tuplas (i, j)
        cache_nombres = {tuple(map(int, k.split(','))): v for k, v in raw.items()}
    else:
        # ── Geocodificación real con Nominatim ────────────────────────────────
        # PASO=6 → solo ~25 peticiones para un grid 30×30 (~4 segundos)
        PASO = 6
        puntos = [(i, j) for i in range(0, filas, PASO) for j in range(0, columnas, PASO)]
        total_pts = len(puntos)
        print(f"  🌐 Geocodificando {total_pts} puntos de referencia (Nominatim)...")

        for idx, (i, j) in enumerate(puntos, 1):
            lat_c = north - (i + 0.5) * lat_step
            lon_c = west  + (j + 0.5) * lon_step
            nombre = _obtener_nombre_barrio(lat_c, lon_c)   # None si falla
            cache_nombres[(i, j)] = nombre
            pct = int(idx / total_pts * 100)
            print(f"     [{idx:>2}/{total_pts}] {pct:>3}%  →  {nombre or '(sin nombre)'}", end='\r')
            time.sleep(0.15)   # Respetar rate-limit Nominatim (máx ~1 req/s)

        print(f"\n  ✅ Geocodificación completada")

        # Guardar en disco para próximas ejecuciones
        os.makedirs(cache_dir, exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({f"{k[0]},{k[1]}": v for k, v in cache_nombres.items()},
                      f, ensure_ascii=False, indent=2)
        print(f"  💾 Cache guardado → próxima vez será instantáneo")

    # ── Rellenar todas las celdas asignando el bloque de muestra más cercano ──
    for i in range(filas):
        for j in range(columnas):
            lat_c = north - (i + 0.5) * lat_step
            lon_c = west  + (j + 0.5) * lon_step

            # Buscar el punto de muestra más cercano que tenga nombre real
            nombre = None
            mejor_d = float('inf')
            for (si, sj), nom in cache_nombres.items():
                if nom:   # solo puntos con nombre válido
                    d = (i - si) ** 2 + (j - sj) ** 2
                    if d < mejor_d:
                        mejor_d = d
                        nombre  = nom

            # Fallback numérico limpio si ningún punto cercano tiene nombre
            if not nombre:
                bloque = (i // 6) * (columnas // 6 + 1) + (j // 6) + 1
                nombre = f"Sector {bloque}"

            grid[i, j] = {'lat': lat_c, 'lon': lon_c, 'nombre': nombre}
            zonas.append((i, j))

    return grid, zonas
