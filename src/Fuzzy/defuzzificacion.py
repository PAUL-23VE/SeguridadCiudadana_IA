import matplotlib
import importlib.util
if importlib.util.find_spec("_tkinter") is not None:
    matplotlib.use('TkAgg')
else:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def clasificar_score(score):
    if score >= 66:
        return 'Alto'
    elif score >= 33:
        return 'Medio'
    return 'Bajo'


def defuzzificar(resultado_agregacion):
    """Calcula el centroide del area agregada."""
    universo = resultado_agregacion['universo']
    agregado = resultado_agregacion['agregado']
    denominador = float(np.sum(agregado))
    if denominador == 0:
        mu_bajo  = resultado_agregacion['mu_bajo']
        mu_medio = resultado_agregacion['mu_medio']
        mu_alto  = resultado_agregacion['mu_alto']
        total    = mu_bajo + mu_medio + mu_alto or 1.0
        return float((mu_bajo * 16.5 + mu_medio * 50.0 + mu_alto * 83.5) / total)
    return float(np.sum(universo * agregado) / denominador)


def defuzzificar_y_clasificar(resultado_agregacion):
    """Retorna (nivel, score) a partir del resultado de agregacion."""
    score = defuzzificar(resultado_agregacion)
    nivel = clasificar_score(score)
    # Usar max de activaciones como desempate de nivel
    mu_bajo  = resultado_agregacion['mu_bajo']
    mu_medio = resultado_agregacion['mu_medio']
    mu_alto  = resultado_agregacion['mu_alto']
    max_mu   = max(mu_bajo, mu_medio, mu_alto)
    if max_mu == mu_alto:
        nivel = 'Alto'
    elif max_mu == mu_medio:
        nivel = 'Medio'
    else:
        nivel = 'Bajo'
    return nivel, round(score, 2)


def comparar_metodos_defuzzificacion(resultado_agregacion):
    """Compara centroide vs centros de masa."""
    score_centroide = defuzzificar(resultado_agregacion)
    mu_bajo  = resultado_agregacion['mu_bajo']
    mu_medio = resultado_agregacion['mu_medio']
    mu_alto  = resultado_agregacion['mu_alto']
    total    = mu_bajo + mu_medio + mu_alto or 1.0
    score_centros = (mu_bajo * 16.5 + mu_medio * 50.0 + mu_alto * 83.5) / total
    return {
        'centroide':     round(score_centroide, 2),
        'centros_masa':  round(score_centros, 2),
    }


def describir_defuzzificacion():
    return (
        "  Defuzzificacion:\n"
        "     Metodo  : Centroide (Centro de Gravedad)\n"
        "     Universo: [0, 100]\n"
        "     Formula : sum(x * mu(x)) / sum(mu(x))"
    )


def graficar_defuzzificacion(resultado_agregacion, score_final=None, nombre_zona=""):
    universo = resultado_agregacion['universo']
    agregado = resultado_agregacion['agregado']
    colores  = {'bajo': '#4CAF50', 'medio': '#FF9800', 'alto': '#F44336'}

    if score_final is None:
        score_final = defuzzificar(resultado_agregacion)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 9))
    fig.suptitle(f"Defuzzificacion por Centroide - Logica Difusa\n{nombre_zona}",
                 fontsize=13, fontweight='bold')

    # Subplot 1: consecuentes truncados
    ax1.set_title("Paso 3: Agregacion - Consecuentes Truncados", fontweight='bold')
    for nivel in ('bajo', 'medio', 'alto'):
        original = resultado_agregacion[f'cons_{nivel}']
        mu       = resultado_agregacion[f'mu_{nivel}']
        truncado = np.minimum(mu, original)
        ax1.plot(universo, original, '--', color=colores[nivel], alpha=0.4, lw=1)
        ax1.fill_between(universo, truncado, alpha=0.55, color=colores[nivel],
                         label=f'{nivel.capitalize()} (mu={mu:.2f})')
    ax1.set_xlim(0, 100); ax1.set_ylim(0, 1.1)
    ax1.set_ylabel("Grado de Membresia")
    ax1.legend(fontsize=9, loc='upper right'); ax1.grid(True, alpha=0.3)

    # Subplot 2: area agregada + centroide
    ax2.set_title("Paso 4: Defuzzificacion - Centroide", fontweight='bold')
    ax2.fill_between(universo, agregado, alpha=0.65, color='#2196F3', label='Area Agregada (MAX)')
    ax2.plot(universo, agregado, color='#1565C0', lw=2)
    ax2.axvline(score_final, color='red', lw=3, linestyle='--',
                label=f'CENTROIDE = {score_final:.2f}')
    ax2.axvspan(0, 33,   alpha=0.10, color=colores['bajo'])
    ax2.axvspan(33, 66,  alpha=0.10, color=colores['medio'])
    ax2.axvspan(66, 100, alpha=0.10, color=colores['alto'])
    ax2.text(16.5, 1.05, 'BAJO',  ha='center', fontsize=9, fontweight='bold', color=colores['bajo'])
    ax2.text(49.5, 1.05, 'MEDIO', ha='center', fontsize=9, fontweight='bold', color=colores['medio'])
    ax2.text(83.0, 1.05, 'ALTO',  ha='center', fontsize=9, fontweight='bold', color=colores['alto'])
    ax2.set_xlim(0, 100); ax2.set_ylim(0, 1.15)
    ax2.set_xlabel("Score de Riesgo"); ax2.set_ylabel("Grado de Membresia")
    ax2.legend(fontsize=9, loc='upper right'); ax2.grid(True, alpha=0.3)

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
    print(f"     Grafica de defuzzificacion generada")
    print(f"     Centroide calculado: {score_final:.2f}")
