"""
difuso.py
=========
Módulo para clasificación de riesgo usando lógica difusa.

Funciones de membresía implementadas:
  - Triangular : para variables graduales (robos, vandalismo, accidentes)
  - Sigma (S)  : para variables con umbral de saturación (microtráfico, llamadas emergencias)

Cada variable tiene asignada una función según su comportamiento esperado:
  robos                → TRIANGULAR  (distribución centrada, pico claro)
  vandalismo           → TRIANGULAR  (distribución centrada, pico claro)
  accidentes           → TRIANGULAR  (distribución centrada, pico claro)
  microtrafico         → SIGMA       (crece rápido al inicio, satura)
  llamadas_emergencias → SIGMA       (crece rápido al inicio, satura)
"""
import math

# Configurar matplotlib para Windows con backend TkAgg (más estable)
import matplotlib
matplotlib.use('TkAgg')  # Backend compatible con tkinter en Windows
import matplotlib.pyplot as plt

# Lista global para mantener referencias a las figuras abiertas
_figuras_abiertas = []

# ── Mapa: variable → tipo de función de membresía ────────────────────────────
TIPO_MEMBRESIA = {
    'robos':                'triangular',
    'vandalismo':           'triangular',
    'accidentes':           'triangular',
    'microtrafico':         'sigma',
    'llamadas_emergencias': 'sigma',
}


# ── Funciones de membresía ───────────────────────────────────────────────────

def _triangular(x, a, b, c):
    """Función de membresía triangular.
    Retorna 0 fuera de [a,c], sube linealmente de a→b, baja de b→c.
    """
    if x <= a or x >= c:
        return 0.0
    if x <= b:
        return (x - a) / (b - a) if (b - a) != 0 else 1.0
    return (c - x) / (c - b) if (c - b) != 0 else 1.0


def _sigma(x, a, b):
    """Función de membresía sigmoidal (S-shape).
    a = punto de cruce 0.5 (inflexión), b = pendiente (>0 → creciente).
    Retorna valor en [0, 1].
    """
    return 1.0 / (1.0 + math.exp(-b * (x - a)))


# ── Grados de membresía por nivel ─────────────────────────────────────────────

def _grado_bajo(variable, valor, maximo):
    """Grado de pertenencia al conjunto BAJO."""
    x = valor / maximo  # normalizar a [0,1]
    tipo = TIPO_MEMBRESIA.get(variable, 'triangular')
    if tipo == 'triangular':
        return _triangular(x, 0.0, 0.0, 0.4)   # pico en 0, cae hasta 0.4
    else:  # sigma invertida
        return 1.0 - _sigma(x, 0.25, 12)


def _grado_medio(variable, valor, maximo):
    """Grado de pertenencia al conjunto MEDIO."""
    x = valor / maximo
    tipo = TIPO_MEMBRESIA.get(variable, 'triangular')
    if tipo == 'triangular':
        return _triangular(x, 0.25, 0.5, 0.75)  # pico en 0.5
    else:  # sigma centrada: diferencia de dos sigmoides
        return _sigma(x, 0.3, 12) - _sigma(x, 0.65, 12)


def _grado_alto(variable, valor, maximo):
    """Grado de pertenencia al conjunto ALTO."""
    x = valor / maximo
    tipo = TIPO_MEMBRESIA.get(variable, 'triangular')
    if tipo == 'triangular':
        return _triangular(x, 0.6, 1.0, 1.0)   # sube desde 0.6, pico en 1
    else:  # sigma creciente
        return _sigma(x, 0.65, 12)


# ── Máximos por variable (dominio) ───────────────────────────────────────────
_MAXIMOS = {
    'robos':                100,
    'microtrafico':          50,
    'vandalismo':            80,
    'accidentes':            60,
    'llamadas_emergencias': 100,
}


# ── Función principal ─────────────────────────────────────────────────────────

def clasificar_difuso(datos, metricas, pesos=None):
    """Clasifica el riesgo de una zona usando lógica difusa.

    Utiliza funciones de membresía TRIANGULARES (robos, vandalismo, accidentes)
    y SIGMA (microtráfico, llamadas_emergencias) para calcular el grado de
    pertenencia a los conjuntos Bajo / Medio / Alto.

    Retorna:
        nivel (str)  : 'Bajo' | 'Medio' | 'Alto'
        score (float): valor numérico de riesgo en [0, 100]
    """
    if pesos is None:
        pesos = {
            'robos': 0.3, 'microtrafico': 0.2,
            'vandalismo': 0.2, 'accidentes': 0.2,
            'llamadas_emergencias': 0.1,
        }

    # Calcular grados de membresía ponderados para cada nivel
    mu_bajo  = 0.0
    mu_medio = 0.0
    mu_alto  = 0.0

    for var, valor in datos.items():
        if var not in _MAXIMOS:
            continue
        maximo = _MAXIMOS[var]
        w = pesos.get(var, 0.2)

        mu_bajo  += w * _grado_bajo(var, valor, maximo)
        mu_medio += w * _grado_medio(var, valor, maximo)
        mu_alto  += w * _grado_alto(var, valor, maximo)

    total = mu_bajo + mu_medio + mu_alto
    if total == 0:
        total = 1.0  # evitar división por cero

    # Defuzzificación por centroide simplificado
    # Asociamos bajo→16.5, medio→50, alto→83.5 (centros de rango 0-100)
    score = (mu_bajo * 16.5 + mu_medio * 50.0 + mu_alto * 83.5) / total

    # Clasificación por máximo grado de membresía
    max_mu = max(mu_bajo, mu_medio, mu_alto)
    if max_mu == mu_alto:
        nivel = 'Alto'
    elif max_mu == mu_medio:
        nivel = 'Medio'
    else:
        nivel = 'Bajo'

    return nivel, round(score, 2)


def describir_membresia():
    lineas = ["  Funciones de membresia por variable:"]
    for var, tipo in TIPO_MEMBRESIA.items():
        simbolo = "[TRI]" if tipo == "triangular" else "[SIG]"
        lineas.append(f"     {simbolo}  {var:<28} -> {tipo.upper()}")
    return "\n".join(lineas)


def graficar_membresia(datos_zona=None, nombre_zona=""):
    """Genera y muestra gráfica de funciones de membresía. La ventana permanece abierta."""
    global _figuras_abiertas
    
    import numpy as np

    variables = list(TIPO_MEMBRESIA.keys())
    n = len(variables)
    maximos = {'robos': 100, 'microtrafico': 50, 'vandalismo': 80,
               'accidentes': 60, 'llamadas_emergencias': 100}

    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4))
    fig.suptitle(
        f"Funciones de Membresia - Logica Difusa\n{nombre_zona}",
        fontsize=13, fontweight='bold', y=1.01
    )

    colores = {'Bajo': '#4CAF50', 'Medio': '#FF9800', 'Alto': '#F44336'}

    for ax, var in zip(axes, variables):
        maximo = maximos[var]
        tipo   = TIPO_MEMBRESIA[var]
        xs = np.linspace(0, maximo, 300)

        # Calcular grados para cada x
        mu_b, mu_m, mu_a = [], [], []
        for xv in xs:
            mu_b.append(_grado_bajo(var,  xv, maximo))
            mu_m.append(_grado_medio(var, xv, maximo))
            mu_a.append(_grado_alto(var,  xv, maximo))

        ax.plot(xs, mu_b, color=colores['Bajo'],  lw=2, label='Bajo')
        ax.plot(xs, mu_m, color=colores['Medio'], lw=2, label='Medio')
        ax.plot(xs, mu_a, color=colores['Alto'],  lw=2, label='Alto')

        ax.fill_between(xs, mu_b, alpha=0.10, color=colores['Bajo'])
        ax.fill_between(xs, mu_m, alpha=0.10, color=colores['Medio'])
        ax.fill_between(xs, mu_a, alpha=0.10, color=colores['Alto'])

        # Marcar valor actual de la zona si se pasa
        if datos_zona and var in datos_zona:
            val = datos_zona[var]
            ax.axvline(val, color='navy', lw=1.5, linestyle='--', label=f'Valor: {val}')
            ax.axvspan(val - maximo * 0.015, val + maximo * 0.015,
                       alpha=0.25, color='navy')

        tipo_lbl = "Triangular" if tipo == 'triangular' else "Sigma (S)"
        ax.set_title(f"{var}\n[{tipo_lbl}]", fontsize=9, fontweight='bold')
        ax.set_xlabel("Valor", fontsize=8)
        ax.set_ylabel("Grado de pertenencia", fontsize=8)
        ax.set_xlim(0, maximo)
        ax.set_ylim(-0.05, 1.10)
        ax.legend(fontsize=7, loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=7)

    plt.tight_layout()
    
    # Configurar para mantener la ventana abierta sin bloquear
    plt.ion()  # Modo interactivo ON
    plt.show(block=False)  # Mostrar sin bloquear el programa principal
    
    # Guardar referencia a la figura para evitar que se cierre automáticamente
    _figuras_abiertas.append(plt.gcf())
    
    # Forzar que la ventana se mantenga en primer plano y visible
    try:
        plt.gcf().canvas.manager.window.wm_attributes('-topmost', 1)  # Traer al frente
        plt.gcf().canvas.manager.window.wm_attributes('-topmost', 0)  # Quitar topmost pero mantener visible
    except Exception:
        pass  # Si no funciona en todos los OS, continuar
    
    plt.draw()
    plt.pause(0.1)  # Pausa para renderizado completo
    
    print(f"     📊 Gráfica de membresía abierta para: {nombre_zona}")
    print(f"     💡 Ventana de matplotlib permanecerá abierta para análisis")


def mantener_graficas_abiertas():
    """Función para mantener todas las gráficas abiertas al final del análisis."""
    global _figuras_abiertas
    
    if _figuras_abiertas:
        print(f"\n  📊 {len(_figuras_abiertas)} gráfica(s) de membresía permanecen abiertas")
        print("  💡 Cierra las ventanas manualmente cuando termines la presentación")
        print("  ▶️  Las ventanas de matplotlib permanecerán abiertas para tu análisis")
        
        # Simplemente mantener las figuras en memoria y asegurar que sean visibles
        for fig in _figuras_abiertas:
            try:
                fig.show()  # Asegurar que la figura esté visible
            except Exception:
                pass
    else:
        print("\n  ℹ️  No hay gráficas de membresía para mantener abiertas")

