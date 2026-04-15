import matplotlib
import importlib.util
if importlib.util.find_spec("_tkinter") is not None:
    matplotlib.use('TkAgg')
else:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PESOS_DEFAULT = {
    'robos':                0.30,
    'microtrafico':         0.20,
    'vandalismo':           0.20,
    'accidentes':           0.20,
    'llamadas_emergencias': 0.10,
}


def evaluar_reglas(grados_membresia, pesos=None):
    """Aplica reglas IF-THEN ponderadas y retorna grados de activacion."""
    if pesos is None:
        pesos = PESOS_DEFAULT.copy()

    mu_bajo  = 0.0
    mu_medio = 0.0
    mu_alto  = 0.0

    for var, grados in grados_membresia.items():
        w = pesos.get(var, 0.2)
        mu_bajo  += w * grados['bajo']
        mu_medio += w * grados['medio']
        mu_alto  += w * grados['alto']

    return {
        'bajo':  mu_bajo,
        'medio': mu_medio,
        'alto':  mu_alto,
    }


def evaluar_reglas_detallado(grados_membresia, pesos=None):
    """Igual que evaluar_reglas pero con detalle por variable."""
    if pesos is None:
        pesos = PESOS_DEFAULT.copy()

    detalle = {}
    mu_bajo  = 0.0
    mu_medio = 0.0
    mu_alto  = 0.0

    for var, grados in grados_membresia.items():
        w = pesos.get(var, 0.2)
        cb = w * grados['bajo']
        cm = w * grados['medio']
        ca = w * grados['alto']
        mu_bajo  += cb
        mu_medio += cm
        mu_alto  += ca
        detalle[var] = {'bajo': cb, 'medio': cm, 'alto': ca, 'peso': w}

    return {
        'bajo':    mu_bajo,
        'medio':   mu_medio,
        'alto':    mu_alto,
        'detalle': detalle,
    }


def normalizar_activacion(activacion):
    total = activacion['bajo'] + activacion['medio'] + activacion['alto']
    if total == 0:
        return activacion.copy()
    return {
        'bajo':  activacion['bajo']  / total,
        'medio': activacion['medio'] / total,
        'alto':  activacion['alto']  / total,
    }


def describir_reglas():
    lineas = [
        "  Reglas IF-THEN con pesos:",
        f"     IF robos THEN riesgo                (peso={PESOS_DEFAULT['robos']})",
        f"     IF microtrafico THEN riesgo         (peso={PESOS_DEFAULT['microtrafico']})",
        f"     IF vandalismo THEN riesgo           (peso={PESOS_DEFAULT['vandalismo']})",
        f"     IF accidentes THEN riesgo           (peso={PESOS_DEFAULT['accidentes']})",
        f"     IF llamadas_emergencias THEN riesgo (peso={PESOS_DEFAULT['llamadas_emergencias']})",
    ]
    return "\n".join(lineas)


def graficar_evaluacion_reglas(grados_membresia, pesos=None, nombre_zona=""):
    if pesos is None:
        pesos = PESOS_DEFAULT.copy()

    resultado = evaluar_reglas_detallado(grados_membresia, pesos)
    variables = list(resultado['detalle'].keys())
    niveles   = ['bajo', 'medio', 'alto']
    colores   = {'bajo': '#4CAF50', 'medio': '#FF9800', 'alto': '#F44336'}

    x = np.arange(len(variables))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 5))
    for i, nivel in enumerate(niveles):
        valores = [resultado['detalle'][v][nivel] for v in variables]
        ax.bar(x + i * width, valores, width, label=nivel.capitalize(),
               color=colores[nivel], alpha=0.8)

    ax.set_title(f"Evaluacion de Reglas IF-THEN\n{nombre_zona}", fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(variables, rotation=15, ha='right', fontsize=8)
    ax.set_ylabel("Contribucion ponderada")
    ax.set_ylim(0, 0.35)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    ax.axhline(resultado['bajo'],  color=colores['bajo'],  lw=2, linestyle='--',
               label=f"Total Bajo={resultado['bajo']:.3f}")
    ax.axhline(resultado['medio'], color=colores['medio'], lw=2, linestyle='--',
               label=f"Total Medio={resultado['medio']:.3f}")
    ax.axhline(resultado['alto'],  color=colores['alto'],  lw=2, linestyle='--',
               label=f"Total Alto={resultado['alto']:.3f}")
    ax.legend(fontsize=8)

    plt.tight_layout()
    plt.ion()
    plt.show(block=False)
    plt.draw()
    plt.pause(0.1)
    print(f"     Grafica de evaluacion de reglas generada")
