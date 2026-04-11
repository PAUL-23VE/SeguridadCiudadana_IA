"""
historicos.py
=============
Módulo para cargar y gestionar datos históricos de criminalidad por macro-zonas.

Este módulo maneja:
- Carga de datos históricos desde CSV
- Cálculo de estadísticas por zona (media, desv. estándar, min, max)
- Identificación de macro-zona según coordenadas
- Proporción de datos históricos para Monte Carlo
"""
import pandas as pd
import numpy as np
from pathlib import Path


class GestorHistoricos:
    """Gestor de datos históricos de criminalidad por macro-zonas."""
    
    def __init__(self, archivo_csv='data/historicos_zonas.csv'):
        """
        Inicializa el gestor cargando datos históricos.
        
        Parámetros
        ----------
        archivo_csv : str
            Ruta al archivo CSV con datos históricos
        """
        self.archivo = Path(archivo_csv)
        self.datos = None
        self.estadisticas = {}
        self.centro_mapa = None
        
        if self.archivo.exists():
            self._cargar_datos()
            self._calcular_estadisticas()
    
    def _cargar_datos(self):
        """Carga los datos históricos desde el CSV."""
        try:
            self.datos = pd.read_csv(self.archivo)
            print(f"  ✅ Datos históricos cargados: {len(self.datos)} registros")
        except Exception as e:
            print(f"  ⚠️  Error al cargar históricos: {e}")
            self.datos = None
    
    def _calcular_estadisticas(self):
        """Calcula estadísticas (media, std, min, max) por zona y variable."""
        if self.datos is None:
            return
        
        variables = ['Robos', 'Microtrafico', 'Vandalismo', 'Accidentes', 'Llamadas911']
        zonas = ['Norte', 'Sur', 'Este', 'Oeste']
        
        for zona in zonas:
            datos_zona = self.datos[self.datos['Zona'] == zona]
            self.estadisticas[zona] = {}
            
            for var in variables:
                valores = datos_zona[var].values
                self.estadisticas[zona][var] = {
                    'media': float(np.mean(valores)),
                    'std': float(np.std(valores)),
                    'min': float(np.min(valores)),
                    'max': float(np.max(valores)),
                    'historico': list(valores)
                }
    
    def configurar_centro_mapa(self, lat_centro, lon_centro):
        """
        Configura el centro del mapa para dividir en macro-zonas.
        
        Parámetros
        ----------
        lat_centro, lon_centro : float
            Coordenadas del centro del mapa
        """
        self.centro_mapa = (lat_centro, lon_centro)
    
    def identificar_zona(self, lat, lon):
        """
        Identifica a qué macro-zona pertenece una coordenada.
        
        Parámetros
        ----------
        lat, lon : float
            Coordenadas a clasificar
        
        Retorna
        -------
        str : 'Norte', 'Sur', 'Este', 'Oeste'
        """
        if self.centro_mapa is None:
            return 'Norte'  # Por defecto
        
        lat_centro, lon_centro = self.centro_mapa
        
        # Determinar cuadrante
        if lat >= lat_centro and lon >= lon_centro:
            return 'Norte'  # Noreste
        elif lat >= lat_centro and lon < lon_centro:
            return 'Oeste'  # Noroeste
        elif lat < lat_centro and lon >= lon_centro:
            return 'Este'   # Sureste
        else:
            return 'Sur'    # Suroeste
    
    def obtener_estadisticas(self, zona):
        """
        Obtiene las estadísticas de una macro-zona.
        
        Parámetros
        ----------
        zona : str
            Nombre de la zona ('Norte', 'Sur', 'Este', 'Oeste')
        
        Retorna
        -------
        dict : Estadísticas de la zona
        """
        return self.estadisticas.get(zona, {})
    
    def obtener_rangos(self, zona, variable):
        """
        Obtiene los rangos (min, max) de una variable en una zona.
        
        Parámetros
        ----------
        zona : str
            Nombre de la zona
        variable : str
            Nombre de la variable ('Robos', 'Microtrafico', etc.)
        
        Retorna
        -------
        tuple : (min, max)
        """
        stats = self.estadisticas.get(zona, {}).get(variable, {})
        return (stats.get('min', 0), stats.get('max', 100))
    
    def generar_resumen(self):
        """Genera un resumen de las estadísticas por zona."""
        if not self.estadisticas:
            return "No hay datos históricos cargados"
        
        lineas = ["\n  📊 RESUMEN DE DATOS HISTÓRICOS POR MACRO-ZONA:\n"]
        
        for zona in ['Sur', 'Norte', 'Este', 'Oeste']:
            stats = self.estadisticas.get(zona, {})
            if stats:
                lineas.append(f"  🔸 {zona.upper()}:")
                lineas.append(f"     Robos: {stats['Robos']['min']:.0f}-{stats['Robos']['max']:.0f} (μ={stats['Robos']['media']:.1f})")
                lineas.append(f"     Microtráfico: {stats['Microtrafico']['min']:.0f}-{stats['Microtrafico']['max']:.0f} (μ={stats['Microtrafico']['media']:.1f})")
                lineas.append(f"     Vandalismo: {stats['Vandalismo']['min']:.0f}-{stats['Vandalismo']['max']:.0f} (μ={stats['Vandalismo']['media']:.1f})")
                lineas.append("")
        
        return "\n".join(lineas)


# Instancia global del gestor (singleton)
_gestor_global = None


def obtener_gestor():
    """Obtiene la instancia global del gestor de históricos."""
    global _gestor_global
    if _gestor_global is None:
        _gestor_global = GestorHistoricos()
    return _gestor_global


def identificar_zona(lat, lon):
    """Atajo para identificar zona usando el gestor global."""
    return obtener_gestor().identificar_zona(lat, lon)


def obtener_estadisticas_zona(zona):
    """Atajo para obtener estadísticas usando el gestor global."""
    return obtener_gestor().obtener_estadisticas(zona)
