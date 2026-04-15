import math
import importlib.util
import matplotlib
if importlib.util.find_spec("_tkinter") is not None:
    matplotlib.use('TkAgg')
else:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

TIPO_MEMBRESIA = {
    'robos':                'triangular',
    'vandalismo':           'triangular',
    'accidentes':           'triangular',
    'microtrafico':         'sigma',
    'llamadas_emergencias': 'sigma',
}

MAXIMOS = {
    'robos':                100,
    'microtrafico':          50,
    'vandalismo':            80,
    'accidentes':            60,
    'llamadas_emergencias': 100,
}


def _triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    if x <= b:
        return (x - a) / (b - a) if (b - a) != 0 else 1.0
    return (c - x) / (c - b) if (c - b) != 0 else 1.0


def _sigma(x, a, b):
    return 1.0 / (1.0 + math.exp(-b * (x - a)))


def _grado_bajo(variable, valor, maximo):
    x = valor / maximo
    tipo = TIPO_MEMBRESIA.get(variable, 'triangular')
    if tipo == 'triangular':
        return _triangular(x, 0.0, 0.0, 0.4)
    else:
        return 1.0 - _sigma(x, 0.25, 12)


def _grado_medio(variable, valor, maximo):
    x = valor / maximo
    tipo = TIPO_MEMBRESIA.get(variable, 'triangular')
    if tipo == 'triangular':
        return _triangular(x, 0.25, 0.5, 0.75)
    else:
        return _sigma(x, 0.3, 12) - _sigma(x, 0.65, 12)


def _grado_alto(variable, valor, maximo):
    x = valor / maximo
    tipo = TIPO_MEMBRESIA.get(variable, 'triangular')
    if tipo == 'triangular':
        return _triangular(x, 0.6, 1.0, 1.0)
    else:
        return _sigma(x, 0.65, 12)


def fuzzificar_entrada(datos):
    grados = {}
    for var, valor in datos.items():
        if var not in MAXIMOS:
            continue
        maximo = MAXIMOS[var]
        grados[var] = {
            'bajo':   _grado_bajo(var, valor, maximo),
            'medio':  _grado_medio(var, valor, maximo),
            'alto':   _grado_alto(var, valor, maximo),
            'valor':  valor,
            'maximo': maximo,
        }
    return grados


def describir_fuzzificacion():
    lineas = ["  Funciones de membresia por variable:"]
    for var, tipo in TIPO_MEMBRESIA.items():
        simbolo = "[TRI]" if tipo == "triangular" else "[SIG]"
        lineas.append(f"     {simbolo}  {var:<28} -> {tipo.upper()}")
    return "\n".join(lineas)


def graficar_fuzzificacion(datos_zona=None, nombre_zona=""):
    if datos_zona is None:
        datos_zona = {}
    variables = list(TIPO_MEMBRESIA.keys())
    n = len(variables)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4))
    fig.suptitle(
        f"ANTECEDENTES: Funciones de Membresia - Logica Difusa\n{nombre_zona}",
        fontsize=13, fontweight='bold', y=1.01
    )
    colores = {'Bajo': '#4CAF50', 'Medio': '#FF9800', 'Alto': '#F44336'}
    for ax, var in zip(axes, variables):
        maximo = MAXIMOS[var]
        tipo = TIPO_MEMBRESIA[var]
        xs = np.linspace(0, maximo, 300)
        mu_b = [_grado_bajo(var, xv, maximo) for xv in xs]
        mu_m = [_grado_medio(var, xv, maximo) for xv in xs]
        mu_a = [_grado_alto(var, xv, maximo) for xv in xs]
        ax.plot(xs, mu_b, color=colores['Bajo'],  lw=2, label='Bajo')
        ax.plot(xs, mu_m, color=colores['Medio'], lw=2, label='Medio')
        ax.plot(xs, mu_a, color=colores['Alto'],  lw=2, label='Alto')
        ax.fill_between(xs, mu_b, alpha=0.10, color=colores['Bajo'])
        ax.fill_between(xs, mu_m, alpha=0.10, color=colores['Medio'])
        ax.fill_between(xs, mu_a, alpha=0.10, color=colores['Alto'])
        if datos_zona and var in datos_zona:
            val = datos_zona[var]
            ax.axvline(val, color='navy', lw=1.5, linestyle='--', label=f'Valor: {val}')
            ax.axvspan(val - maximo * 0.015, val + maximo * 0.015, alpha=0.25, color='navy')
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
    plt.ion()
    plt.show(block=False)
    try:
        plt.gcf().canvas.manager.window.wm_attributes('-topmost', 1)
        plt.gcf().canvas.manager.window.wm_attributes('-topmost', 0)
    except Exception:
        pass
    plt.draw()
    plt.pause(0.1)
    print(f"     Grafica de fuzzificacion generada para: {nombre_zona}")
