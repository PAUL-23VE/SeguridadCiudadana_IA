"""
visualizacion.py
===============
Módulo para visualizar el mapa y pintar las zonas según el nivel de riesgo.
"""
import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox
from matplotlib.patches import Circle
from matplotlib.widgets import Slider

def mostrar_mapa_interactivo(G, bbox, grid, resultados):
    """
    Muestra el mapa real con interacción: clic para seleccionar zona y slider para radio.
    """
    print("\n" + "="*60)
    print("MAPA INTERACTIVO - HAZ CLIC PARA SELECCIONAR UNA ZONA")
    print("="*60)
    print("📍 Haz clic en el mapa para seleccionar el centro de la zona")
    print("🔄 Usa el slider para ajustar el radio del área a diagnosticar")
    print("✅ Cierra la ventana para ver el diagnóstico detallado\n")
    
    fig, ax = ox.plot_graph(G, node_size=0, edge_color='#333333', edge_linewidth=0.5, 
                            bgcolor='white', show=False, close=False, figsize=(14, 10))
    ax.set_title('🗺️  HAZ CLIC EN EL MAPA PARA SELECCIONAR UNA ZONA', 
                 fontsize=14, weight='bold', pad=20)
    
    # Variables para almacenar la selección
    seleccion = {'lat': None, 'lon': None, 'radio': 2}
    circulo = None
    
    # Crear slider para el radio
    ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
    slider = Slider(ax_slider, 'Radio (zonas)', 1, 10, valinit=2, valstep=1)
    
    def on_click(event):
        nonlocal circulo
        if event.inaxes == ax and event.xdata and event.ydata:
            seleccion['lon'] = event.xdata
            seleccion['lat'] = event.ydata
            seleccion['radio'] = int(slider.val)
            
            # Eliminar círculo anterior
            if circulo:
                circulo.remove()
            
            # Dibujar nuevo círculo
            radio_grados = seleccion['radio'] * 0.003  # Aproximado
            circulo = Circle((seleccion['lon'], seleccion['lat']), radio_grados, 
                           color='red', alpha=0.3, linewidth=2, edgecolor='darkred')
            ax.add_patch(circulo)
            fig.canvas.draw()
            
            print(f"✅ Zona seleccionada: Lat {seleccion['lat']:.4f}, Lon {seleccion['lon']:.4f}, Radio: {seleccion['radio']}")
    
    def on_slider_change(val):
        seleccion['radio'] = int(val)
        if seleccion['lat'] and circulo:
            circulo.set_radius(seleccion['radio'] * 0.003)
            fig.canvas.draw()
    
    fig.canvas.mpl_connect('button_press_event', on_click)
    slider.on_changed(on_slider_change)
    
    plt.tight_layout()
    plt.show()
    
    return seleccion

def mostrar_mapa_real(G, bbox):
    """
    Muestra el mapa real de calles de la ciudad (vista desde arriba).
    """
    print("[Visualización] Mostrando mapa real de calles...")
    fig, ax = ox.plot_graph(G, node_size=0, edge_color='#333333', edge_linewidth=0.5, 
                            bgcolor='white', show=False, close=False, figsize=(12, 10))
    ax.set_title('Mapa Real de la Ciudad - Vista desde arriba', fontsize=16, weight='bold')
    plt.tight_layout()
    plt.show()
    print("[Visualización] Mapa mostrado. Puedes cerrar la ventana para continuar.\n")

def mostrar_mapa_coloreado(G, grid, resultados, bbox):
    filas, columnas = grid.shape
    matriz_riesgo = np.zeros((filas, columnas))
    for (i, j), diag in resultados.items():
        if diag['nivel'] == 'Alto':
            matriz_riesgo[i, j] = 2
        elif diag['nivel'] == 'Medio':
            matriz_riesgo[i, j] = 1
        else:
            matriz_riesgo[i, j] = 0
    colores = ['#27AE60', '#F39C12', '#E74C3C']  # verde, naranja, rojo
    cmap = plt.matplotlib.colors.ListedColormap(colores)
    plt.figure(figsize=(10, 8))
    plt.imshow(matriz_riesgo, cmap=cmap, origin='upper')
    plt.title('Mapa de Zonas de Riesgo')
    plt.xlabel('Longitud (columnas)')
    plt.ylabel('Latitud (filas)')
    cbar = plt.colorbar(ticks=[0, 1, 2])
    cbar.ax.set_yticklabels(['Bajo', 'Medio', 'Alto'])
    plt.show()
