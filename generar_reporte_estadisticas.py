"""
generar_reporte_estadisticas.py
================================
Script para capturar las estadísticas mostradas en consola y generar un reporte HTML profesional.

Ejecuta el sistema y genera automáticamente un reporte visual con todas las estadísticas.
"""
import sys
import os
from datetime import datetime
from io import StringIO
import contextlib

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import OUTPUT_DIR
from src.utils.reporte import generar_reporte_html
from src.utils.historicos import obtener_gestor


class EstadisticasCapturador:
    """Captura estadísticas durante la ejecución del sistema."""
    
    def __init__(self):
        self.datos_reporte = {
            'ciudad': 'Ambato, Ecuador',
            'modo': 'Análisis Completo',
            'total_zonas': 0,
            'zonas_alto': 0,
            'zonas_medio': 0,
            'zonas_bajo': 0,
            'datos_historicos': {},
            'montecarlo': {},
            'detalles_zonas': [],
            'info_circulo': None
        }
    
    def cargar_datos_historicos(self):
        """Carga los datos históricos del gestor."""
        gestor = obtener_gestor()
        if gestor.datos is not None:
            self.datos_reporte['datos_historicos'] = gestor.estadisticas
            
            # Cargar datos de Monte Carlo
            for zona in ['Norte', 'Sur', 'Este', 'Oeste']:
                stats = gestor.obtener_estadisticas(zona)
                if stats and 'Robos' in stats:
                    from src.algoritmos.montecarlo import generar_datos_zona
                    import numpy as np
                    
                    try:
                        simulaciones = generar_datos_zona(zona, stats, 1000)
                        if simulaciones:
                            robos_vals = [s.get('robos', 0) for s in simulaciones]
                            self.datos_reporte['montecarlo'][zona] = {
                                'media_historica': stats['Robos'].get('media', 0),
                                'media_simulada': np.mean(robos_vals),
                                'std': np.std(robos_vals)
                            }
                    except Exception as e:
                        print(f"  ⚠️ Error al generar simulaciones para {zona}: {e}")
    
    def agregar_resultado(self, fila, col, resultado):
        """Agrega un resultado de diagnóstico."""
        self.datos_reporte['detalles_zonas'].append({
            'fila': fila,
            'columna': col,
            'nombre': resultado.get('nombre', f'Zona [{fila},{col}]'),
            'nivel': resultado['nivel'],
            'factores': resultado['factores']
        })
        
        # Actualizar contadores
        nivel = resultado['nivel'].lower()
        if nivel == 'alto':
            self.datos_reporte['zonas_alto'] += 1
        elif nivel == 'medio':
            self.datos_reporte['zonas_medio'] += 1
        else:
            self.datos_reporte['zonas_bajo'] += 1
        
        self.datos_reporte['total_zonas'] += 1
    
    def generar_reporte(self):
        """Genera el reporte HTML."""
        print(f"\n{'='*70}")
        print(f"  📄 GENERANDO REPORTE HTML CON ESTADÍSTICAS")
        print(f"{'='*70}")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_reporte = f"reporte_estadisticas_{timestamp}.html"
        ruta_reporte = os.path.join(OUTPUT_DIR, nombre_reporte)
        
        try:
            generar_reporte_html(self.datos_reporte, ruta_reporte)
            
            print(f"\n  ✅ REPORTE GENERADO EXITOSAMENTE!")
            print(f"  📁 Ubicación: {ruta_reporte}")
            print(f"\n  📊 Contenido del reporte:")
            print(f"     • Información general del análisis")
            print(f"     • Resumen de clasificación de riesgo")
            print(f"     • Datos históricos por macro-zona")
            print(f"     • Comparación Monte Carlo (1000 simulaciones)")
            print(f"     • Detalle de zonas analizadas")
            print(f"     • Gráficos y estadísticas visuales")
            print(f"{'='*70}\n")
            
            # Abrir automáticamente
            import webbrowser
            ruta_absoluta = os.path.abspath(ruta_reporte)
            webbrowser.open('file:///' + ruta_absoluta.replace('\\', '/'))
            print(f"  🌐 Reporte abierto en el navegador\n")
            
            return ruta_reporte
            
        except Exception as e:
            print(f"  ❌ Error al generar reporte: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """Genera un reporte con datos de ejemplo."""
    print("\n" + "="*70)
    print("  📊 GENERADOR DE REPORTE DE ESTADÍSTICAS")
    print("="*70)
    print("  Este script genera un reporte HTML profesional con todas las")
    print("  estadísticas del análisis de seguridad urbana.")
    print("="*70 + "\n")
    
    capturador = EstadisticasCapturador()
    
    # Cargar datos históricos
    print("  📈 Cargando datos históricos...")
    capturador.cargar_datos_historicos()
    
    # Simular algunos resultados de ejemplo para demostración
    print("  🔍 Generando datos de ejemplo...")
    
    import random
    niveles = ['Alto', 'Medio', 'Bajo']
    factores_disponibles = ['robos', 'microtrafico', 'vandalismo', 'accidentes', 'llamadas_emergencias']
    
    # Generar 30 zonas de ejemplo
    for i in range(5):
        for j in range(6):
            nivel = random.choice(niveles)
            factores = random.sample(factores_disponibles, k=random.randint(2, 4))
            
            capturador.agregar_resultado(i, j, {
                'nombre': f'Sector [{i},{j}]',
                'nivel': nivel,
                'factores': factores
            })
    
    # Generar reporte
    capturador.generar_reporte()
    
    print("  ✅ Proceso completado!")
    print("  💡 Para integrar con el sistema principal, las estadísticas")
    print("     se capturarán automáticamente durante la ejecución.\n")


if __name__ == "__main__":
    main()
