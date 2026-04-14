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
import importlib.util

import matplotlib
if importlib.util.find_spec("_tkinter") is not None:
    matplotlib.use('TkAgg')
else:
    matplotlib.use('Agg')
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


# ── Funciones de membresía del CONSECUENTE (Salida: Score de Riesgo 0-100) ───

def _membresia_consecuente_bajo(score):
    """Función de membresía del consecuente para RIESGO BAJO.
    Dominio de salida: [0, 100]
    """
    return _triangular(score, 0, 0, 40)  # Pico en 0, cae hasta 40


def _membresia_consecuente_medio(score):
    """Función de membresía del consecuente para RIESGO MEDIO.
    Dominio de salida: [0, 100]
    """
    return _triangular(score, 25, 50, 75)  # Pico en 50


def _membresia_consecuente_alto(score):
    """Función de membresía del consecuente para RIESGO ALTO.
    Dominio de salida: [0, 100]
    """
    return _triangular(score, 60, 100, 100)  # Sube desde 60, pico en 100


# ── Función principal ─────────────────────────────────────────────────────────

def clasificar_difuso(datos, metricas, pesos=None, mostrar_defuzzificacion=False, nombre_zona=""):
    """Clasifica el riesgo de una zona usando lógica difusa.

    Utiliza funciones de membresía TRIANGULARES (robos, vandalismo, accidentes)
    y SIGMA (microtráfico, llamadas_emergencias) para calcular el grado de
    pertenencia a los conjuntos Bajo / Medio / Alto.

    Args:
        datos: Diccionario con valores de las variables de entrada
        metricas: Métricas adicionales (no usado actualmente)
        pesos: Diccionario con pesos para cada variable
        mostrar_defuzzificacion: Si True, muestra gráfica del proceso de defuzzificación
        nombre_zona: Nombre descriptivo de la zona (para la gráfica)

    Retorna:
        nivel (str)  : 'Bajo' | 'Medio' | 'Alto'
        score (float): valor numérico de riesgo en [0, 100]
    """
    if pesos is None:
        pesos = {
            'robos': 0.3, 'microtrafico': 0.2,
            'vandalismo': 0.2, 'accidentes': 0.2,
            'llamadas_emergencias': 0.1,
        }    # Calcular grados de membresía ponderados para cada nivel
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

    # ═══════════════════════════════════════════════════════════════════════════
    # PASO 4: DEFUZZIFICACIÓN POR CENTROIDE (Método Correcto)
    # ═══════════════════════════════════════════════════════════════════════════
    # Usamos funciones de membresía del CONSECUENTE para calcular el centroide.
    # Se discretiza el universo de salida [0, 100] en 101 puntos.
    
    import numpy as np
    
    # Discretizar el universo de salida (score de 0 a 100)
    universo_salida = np.linspace(0, 100, 101)
    
    # Calcular la función de membresía AGREGADA para cada punto
    # Usamos el método MAX para agregar las salidas de las reglas
    agregado = np.zeros_like(universo_salida)
    
    for i, score_candidato in enumerate(universo_salida):
        # Para cada punto, calculamos el mínimo entre el grado de activación
        # de la regla y la función de membresía del consecuente
        contribucion_bajo  = min(mu_bajo,  _membresia_consecuente_bajo(score_candidato))
        contribucion_medio = min(mu_medio, _membresia_consecuente_medio(score_candidato))
        contribucion_alto  = min(mu_alto,  _membresia_consecuente_alto(score_candidato))
        
        # Agregación por MAX (unión difusa)
        agregado[i] = max(contribucion_bajo, contribucion_medio, contribucion_alto)
    
    # Calcular el CENTROIDE (centro de gravedad)
    numerador = np.sum(universo_salida * agregado)
    denominador = np.sum(agregado)
    
    if denominador == 0:
        # Si no hay área, usar defuzzificación por centros
        score = (mu_bajo * 16.5 + mu_medio * 50.0 + mu_alto * 83.5) / total
    else:
        # CENTROIDE CORRECTO
        score = numerador / denominador    # Clasificación por máximo grado de membresía
    max_mu = max(mu_bajo, mu_medio, mu_alto)
    if max_mu == mu_alto:
        nivel = 'Alto'
    elif max_mu == mu_medio:
        nivel = 'Medio'
    else:
        nivel = 'Bajo'

    # ═══════════════════════════════════════════════════════════════════════════
    # VISUALIZACIÓN DEL PROCESO DE DEFUZZIFICACIÓN (si se solicita)
    # ═══════════════════════════════════════════════════════════════════════════
    if mostrar_defuzzificacion:
        graficar_membresia_consecuente(
            mu_bajo=mu_bajo/total,  # Normalizar para visualización
            mu_medio=mu_medio/total,
            mu_alto=mu_alto/total,
            score_final=score,
            nombre_zona=nombre_zona
        )

    return nivel, round(score, 2)


def describir_membresia():
    lineas = ["  Funciones de membresia por variable:"]
    for var, tipo in TIPO_MEMBRESIA.items():
        simbolo = "[TRI]" if tipo == "triangular" else "[SIG]"
        lineas.append(f"     {simbolo}  {var:<28} -> {tipo.upper()}")
    return "\n".join(lineas)


def graficar_membresia_consecuente(mu_bajo=0.0, mu_medio=0.0, mu_alto=0.0, score_final=None, nombre_zona=""):
    """Genera y muestra la gráfica del CONSECUENTE (funciones de salida) con defuzzificación.
    
    Muestra:
    - Funciones de membresía del consecuente (Bajo, Medio, Alto)
    - Área agregada (cortada por los grados de activación)
    - Centroide calculado (línea vertical roja)
    """
    global _figuras_abiertas
    import numpy as np
    
    # Usar número de figura 2 para asegurar que se abra DESPUÉS de antecedentes
    fig = plt.figure(num=2, figsize=(10, 6))
    ax = fig.add_subplot(111)
    fig.suptitle(
        f"CONSECUENTE: Score de Riesgo [0-100]\nDefuzzificación por Centroide\n{nombre_zona}",
        fontsize=13, fontweight='bold'
    )
    
    # Universo de salida
    universo = np.linspace(0, 100, 200)
    
    # Funciones de membresía del consecuente
    mu_cons_bajo  = [_membresia_consecuente_bajo(x) for x in universo]
    mu_cons_medio = [_membresia_consecuente_medio(x) for x in universo]
    mu_cons_alto  = [_membresia_consecuente_alto(x) for x in universo]
    
    # Funciones cortadas por los grados de activación
    mu_cortado_bajo  = [min(mu_bajo, y) for y in mu_cons_bajo]
    mu_cortado_medio = [min(mu_medio, y) for y in mu_cons_medio]
    mu_cortado_alto  = [min(mu_alto, y) for y in mu_cons_alto]
    
    # Agregación (MAX)
    mu_agregado = [max(b, m, a) for b, m, a in zip(mu_cortado_bajo, mu_cortado_medio, mu_cortado_alto)]
    
    # Graficar funciones originales (líneas punteadas)
    ax.plot(universo, mu_cons_bajo, '--', color='#4CAF50', alpha=0.5, lw=1, label='Bajo (original)')
    ax.plot(universo, mu_cons_medio, '--', color='#FF9800', alpha=0.5, lw=1, label='Medio (original)')
    ax.plot(universo, mu_cons_alto, '--', color='#F44336', alpha=0.5, lw=1, label='Alto (original)')
    
    # Graficar funciones cortadas (áreas rellenas)
    ax.fill_between(universo, mu_cortado_bajo, alpha=0.4, color='#4CAF50', label=f'Bajo cortado (μ={mu_bajo:.2f})')
    ax.fill_between(universo, mu_cortado_medio, alpha=0.4, color='#FF9800', label=f'Medio cortado (μ={mu_medio:.2f})')
    ax.fill_between(universo, mu_cortado_alto, alpha=0.4, color='#F44336', label=f'Alto cortado (μ={mu_alto:.2f})')
    
    # Graficar agregación (línea negra gruesa)
    ax.plot(universo, mu_agregado, 'k-', lw=2.5, label='Agregación (MAX)', zorder=10)
    ax.fill_between(universo, mu_agregado, alpha=0.15, color='black')
    
    # Marcar el centroide
    if score_final is not None:
        ax.axvline(score_final, color='red', lw=3, linestyle='-', label=f'CENTROIDE = {score_final:.2f}', zorder=15)
        ax.scatter([score_final], [0], color='red', s=200, zorder=20, marker='^')
    
    ax.set_xlabel("Score de Riesgo", fontsize=11, fontweight='bold')
    ax.set_ylabel("Grado de Pertenencia", fontsize=11, fontweight='bold')
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.05, 1.1)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.ion()
    plt.show(block=False)
    
    _figuras_abiertas.append(plt.gcf())
    
    try:
        plt.gcf().canvas.manager.window.wm_attributes('-topmost', 1)
        plt.gcf().canvas.manager.window.wm_attributes('-topmost', 0)
    except Exception:
        pass
    
    plt.draw()
    plt.pause(0.1)
    
    print(f"     📊 Gráfica del CONSECUENTE abierta (Defuzzificación)")
    print(f"     🎯 Centroide calculado: {score_final:.2f}")


def graficar_membresia(datos_zona=None, nombre_zona=""):
    """Genera y muestra gráfica de funciones de membresía. La ventana permanece abierta."""
    global _figuras_abiertas
    import numpy as np

    variables = list(TIPO_MEMBRESIA.keys())
    n = len(variables)
    maximos = {'robos': 100, 'microtrafico': 50, 'vandalismo': 80,
               'accidentes': 60, 'llamadas_emergencias': 100}

    # Usar número de figura 1 para asegurar que se abra PRIMERO
    fig = plt.figure(num=1, figsize=(4 * n, 4))
    axes = fig.subplots(1, n)
    fig.suptitle(
        f"ANTECEDENTES: Funciones de Membresía - Lógica Difusa\n{nombre_zona}",
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
def graficar_defuzzificacion(mu_bajo, mu_medio, mu_alto, score_final, nombre_zona=""):
    """Genera gráfica del proceso de defuzzificación por centroide.
    
    Muestra:
    1. Funciones de membresía del consecuente (Bajo/Medio/Alto)
    2. Área agregada (MAX de las contribuciones)
    3. Centroide calculado (línea vertical)
    
    Args:
        mu_bajo: Grado de activación de la regla "Bajo"
        mu_medio: Grado de activación de la regla "Medio"
        mu_alto: Grado de activación de la regla "Alto"
        score_final: Score defuzzificado (resultado del centroide)
        nombre_zona: Nombre descriptivo de la zona
    """
    global _figuras_abiertas
    import numpy as np
    
    # Discretizar universo de salida
    universo = np.linspace(0, 100, 1001)
    
    # Calcular funciones de membresía del consecuente
    membresia_bajo  = np.array([_membresia_consecuente_bajo(x) for x in universo])
    membresia_medio = np.array([_membresia_consecuente_medio(x) for x in universo])
    membresia_alto  = np.array([_membresia_consecuente_alto(x) for x in universo])
    
    # Aplicar truncamiento (MIN con grado de activación)
    truncado_bajo  = np.minimum(mu_bajo, membresia_bajo)
    truncado_medio = np.minimum(mu_medio, membresia_medio)
    truncado_alto  = np.minimum(mu_alto, membresia_alto)
    
    # Agregación (MAX)
    agregado = np.maximum(np.maximum(truncado_bajo, truncado_medio), truncado_alto)
    
    # Crear figura
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    fig.suptitle(
        f"🧮 DEFUZZIFICACIÓN POR CENTROIDE - Lógica Difusa\n{nombre_zona}",
        fontsize=14, fontweight='bold', y=0.995
    )
    
    colores = {'Bajo': '#4CAF50', 'Medio': '#FF9800', 'Alto': '#F44336'}
    
    # ─── SUBPLOT 1: Funciones de Membresía del Consecuente ───
    ax1.set_title("Paso 3: AGREGACIÓN - Funciones de Membresía del Consecuente (Salida)", 
                  fontsize=11, fontweight='bold', pad=10)
    
    # Graficar funciones originales (semi-transparentes)
    ax1.plot(universo, membresia_bajo, '--', color=colores['Bajo'], 
             lw=1.5, alpha=0.4, label='Bajo (original)')
    ax1.plot(universo, membresia_medio, '--', color=colores['Medio'], 
             lw=1.5, alpha=0.4, label='Medio (original)')
    ax1.plot(universo, membresia_alto, '--', color=colores['Alto'], 
             lw=1.5, alpha=0.4, label='Alto (original)')
    
    # Graficar funciones truncadas (con MIN)
    ax1.fill_between(universo, truncado_bajo, alpha=0.6, color=colores['Bajo'], 
                     label=f'Bajo truncado (μ={mu_bajo:.2f})')
    ax1.fill_between(universo, truncado_medio, alpha=0.6, color=colores['Medio'], 
                     label=f'Medio truncado (μ={mu_medio:.2f})')
    ax1.fill_between(universo, truncado_alto, alpha=0.6, color=colores['Alto'], 
                     label=f'Alto truncado (μ={mu_alto:.2f})')
    
    ax1.set_xlabel("Score de Riesgo", fontsize=10)
    ax1.set_ylabel("Grado de Membresía", fontsize=10)
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 1.1)
    ax1.legend(fontsize=9, loc='upper right', framealpha=0.95)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # ─── SUBPLOT 2: Área Agregada + Centroide ───
    ax2.set_title("Paso 4: DEFUZZIFICACIÓN - Centroide del Área Agregada", 
                  fontsize=11, fontweight='bold', pad=10)
    
    # Área agregada (MAX)
    ax2.fill_between(universo, agregado, alpha=0.7, color='#2196F3', 
                     label='Área Agregada (MAX)')
    ax2.plot(universo, agregado, color='#1565C0', lw=2)
    
    # Centroide (resultado final)
    ax2.axvline(score_final, color='red', lw=3, linestyle='--', 
                label=f'CENTROIDE = {score_final:.2f}')
    ax2.axvspan(score_final - 1, score_final + 1, alpha=0.3, color='red')
    
    # Clasificación visual
    ax2.axvspan(0, 33, alpha=0.15, color=colores['Bajo'])
    ax2.axvspan(33, 66, alpha=0.15, color=colores['Medio'])
    ax2.axvspan(66, 100, alpha=0.15, color=colores['Alto'])
    
    ax2.text(16.5, 1.05, 'BAJO', ha='center', fontsize=9, fontweight='bold', 
             color=colores['Bajo'])
    ax2.text(49.5, 1.05, 'MEDIO', ha='center', fontsize=9, fontweight='bold', 
             color=colores['Medio'])
    ax2.text(83, 1.05, 'ALTO', ha='center', fontsize=9, fontweight='bold', 
             color=colores['Alto'])
    
    ax2.set_xlabel("Score de Riesgo", fontsize=10)
    ax2.set_ylabel("Grado de Membresía", fontsize=10)
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 1.15)
    ax2.legend(fontsize=9, loc='upper right', framealpha=0.95)
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    # Configurar para mantener abierta
    plt.ion()
    plt.show(block=False)
    _figuras_abiertas.append(plt.gcf())
    
    try:
        plt.gcf().canvas.manager.window.wm_attributes('-topmost', 1)
        plt.gcf().canvas.manager.window.wm_attributes('-topmost', 0)
    except Exception:
        pass
    
    plt.draw()
    plt.pause(0.1)
    
    print(f"     📊 Gráfica de defuzzificación abierta para: {nombre_zona}")
    print(f"     🎯 Centroide calculado: {score_final:.2f}")
    print(f"     📐 Grados de activación: Bajo={mu_bajo:.2f}, Medio={mu_medio:.2f}, Alto={mu_alto:.2f}")
