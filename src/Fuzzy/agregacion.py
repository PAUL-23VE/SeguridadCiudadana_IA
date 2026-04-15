import math
import matplotlib
import importlib.util
if importlib.util.find_spec("_tkinter") is not None:
    matplotlib.use('TkAgg')
else:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_UNIVERSO = np.linspace(0, 100, 101)


def _triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    if x <= b:
        return (x - a) / (b - a) if (b - a) != 0 else 1.0
    return (c - x) / (c - b) if (c - b) != 0 else 1.0


def _cons_bajo(score):
    return _triangular(score, 0, 0, 40)


def _cons_medio(score):
    return _triangular(score, 25, 50, 75)


def _cons_alto(score):
    return _triangular(score, 60, 100, 100)


def agregar_consecuentes(activacion):
    """Trunca (MIN) cada consecuente con su grado de activacion y los une (MAX)."""
    mu_bajo  = activacion['bajo']
    mu_medio = activacion['medio']
    mu_alto  = activacion['alto']

    agregado = np.array([
        max(
            min(mu_bajo,  _cons_bajo(s)),
            min(mu_medio, _cons_medio(s)),
            min(mu_alto,  _cons_alto(s)),
        )
        for s in _UNIVERSO
    ])

    return {
        'universo':  _UNIVERSO,
        'agregado':  agregado,
        'mu_bajo':   mu_bajo,
        'mu_medio':  mu_medio,
        'mu_alto':   mu_alto,
        'cons_bajo':  np.array([_cons_bajo(s)  for s in _UNIVERSO]),
        'cons_medio': np.array([_cons_medio(s) for s in _UNIVERSO]),
        'cons_alto':  np.array([_cons_alto(s)  for s in _UNIVERSO]),
    }


def calcular_area_agregada(resultado_agregacion):
    return float(np.trapz(resultado_agregacion['agregado'],
                          resultado_agregacion['universo']))


def describir_agregacion():
    return (
        "  Agregacion de consecuentes:\n"
        "     Truncamiento : MIN(grado_activacion, funcion_consecuente)\n"
        "     Union        : MAX entre los tres consecuentes truncados\n"
        "     Salida       : funcion agregada sobre [0, 100]"
    )


def graficar_agregacion(activacion, nombre_zona=""):
    resultado = agregar_consecuentes(activacion)
    universo  = resultado['universo']
    colores   = {'bajo': '#4CAF50', 'medio': '#FF9800', 'alto': '#F44336'}

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.suptitle(f"Agregacion de Consecuentes\n{nombre_zona}", fontweight='bold')

    for nivel in ('bajo', 'medio', 'alto'):
        original = resultado[f'cons_{nivel}']
        truncado = np.minimum(resultado[f'mu_{nivel}'], original)
        ax.plot(universo, original, '--', color=colores[nivel], alpha=0.4, lw=1,
                label=f'{nivel.capitalize()} (original)')
        ax.fill_between(universo, truncado, alpha=0.5, color=colores[nivel],
                        label=f'{nivel.capitalize()} truncado (mu={resultado["mu_" + nivel]:.2f})')

    ax.plot(universo, resultado['agregado'], 'k-', lw=2.5, label='Agregacion (MAX)', zorder=10)
    ax.fill_between(universo, resultado['agregado'], alpha=0.12, color='black')

    ax.set_xlabel("Score de Riesgo")
    ax.set_ylabel("Grado de Membresia")
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.05, 1.1)
    ax.legend(fontsize=8, loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.ion()
    plt.show(block=False)
    plt.draw()
    plt.pause(0.1)
    print(f"     Grafica de agregacion generada")
