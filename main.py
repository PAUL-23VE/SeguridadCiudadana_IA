"""
main.py
=======
Flujo principal del sistema de diagnóstico de zonas peligrosas en mapas urbanos de Ecuador usando IA.
"""

from mapa import cargar_mapa, construir_grid
from diagnostico import diagnosticar_zona, diagnostico_masivo
from visualizacion import mostrar_mapa_interactivo
import osmnx as ox

# Paso 1: Selección de ciudad o país
print("="*60)
print("DIAGNÓSTICO DE ZONAS DE RIESGO EN ECUADOR")
print("="*60)
ciudad = input("Ingresa la ciudad a analizar (o 'Ecuador' para todo el país): ").strip()
if not ciudad:
    ciudad = "Ecuador"

# Paso 2: Cargar mapa y construir grid
G, bbox = cargar_mapa(ciudad)
grid, zonas = construir_grid(G, bbox, filas=30, columnas=30)

# Paso 3: Diagnóstico masivo de todas las zonas
print("\n[Sistema] Realizando diagnóstico masivo de todas las zonas...")
resultados = diagnostico_masivo(grid, zonas)
print("[Sistema] ✅ Diagnóstico completo.\n")

# Paso 4: Mapa interactivo - selección de zona
seleccion = mostrar_mapa_interactivo(G, bbox, grid, resultados)

if seleccion['lat'] and seleccion['lon']:
    # Encontrar la zona del grid más cercana
    lat_sel = seleccion['lat']
    lon_sel = seleccion['lon']
    radio = seleccion['radio']
    
    # Buscar zonas dentro del radio
    north, south, east, west = bbox
    lat_step = (north - south) / 30
    lon_step = (east - west) / 30
    
    zonas_seleccionadas = []
    for i in range(30):
        for j in range(30):
            zona_info = grid[i, j]
            dist_lat = abs(zona_info['lat'] - lat_sel)
            dist_lon = abs(zona_info['lon'] - lon_sel)
            dist = (dist_lat**2 + dist_lon**2)**0.5
            
            if dist <= radio * 0.003:  # Radio aproximado en grados
                zonas_seleccionadas.append((i, j))
    
    # Mostrar diagnóstico detallado
    print("\n" + "="*60)
    print(f"DIAGNÓSTICO DETALLADO - {len(zonas_seleccionadas)} ZONAS ENCONTRADAS")
    print("="*60 + "\n")
    
    for idx, (i, j) in enumerate(zonas_seleccionadas, 1):
        diag = resultados[(i, j)]
        zona_info = grid[i, j]
        
        # Obtener nombre del barrio/calle usando geocodificación inversa
        print(f"   Consultando nombre de zona {idx}/{len(zonas_seleccionadas)}...", end='\r')
        try:
            # Geocodificación inversa usando Nominatim
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(user_agent="diagnostico_zonas_ecuador")
            location = geolocator.reverse(f"{zona_info['lat']}, {zona_info['lon']}", language='es', timeout=10)
            
            if location and location.raw.get('address'):
                address = location.raw['address']
                # Extraer nombre más relevante (barrio, vecindario, ciudad)
                nombre_zona = (
                    address.get('neighbourhood') or 
                    address.get('suburb') or 
                    address.get('quarter') or 
                    address.get('hamlet') or 
                    address.get('road') or 
                    address.get('city') or 
                    f"Zona [{i},{j}]"
                )
                ciudad_zona = address.get('city', ciudad)
                nombre_completo = f"{nombre_zona}, {ciudad_zona}"
            else:
                nombre_completo = f"Zona [{i},{j}]"
        except Exception as e:
            nombre_completo = f"Zona [{i},{j}]"
        
        # Determinar emoji según nivel de riesgo
        emoji = "🔴" if diag['nivel'] == 'Alto' else "🟠" if diag['nivel'] == 'Medio' else "🟢"
        
        print(f"{emoji} {nombre_completo}")
        print(f"   📍 Coordenadas: [{i},{j}] - Lat: {zona_info['lat']:.4f}, Lon: {zona_info['lon']:.4f}")
        print(f"   ⚠️  Nivel de riesgo: {diag['nivel']}")
        print(f"   📊 Factores principales: {', '.join(diag['factores'])}")
        print(f"   📜 Regla: {diag['regla']}")
        print()
    
    print("="*60)
else:
    print("\n⚠️  No se seleccionó ninguna zona.")

print("\n✅ Gracias por usar el sistema de diagnóstico de zonas peligrosas.")
