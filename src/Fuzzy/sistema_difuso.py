import matplotlib
import importlib.util
if importlib.util.find_spec("_tkinter") is not None:
    matplotlib.use("TkAgg")
else:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .fuzzificacion import fuzzificar_entrada, graficar_fuzzificacion, TIPO_MEMBRESIA, MAXIMOS, describir_fuzzificacion
from .evaluacion_reglas import evaluar_reglas, graficar_evaluacion_reglas, describir_reglas, PESOS_DEFAULT
from .agregacion import agregar_consecuentes, graficar_agregacion, describir_agregacion
from .defuzzificacion import defuzzificar_y_clasificar, graficar_defuzzificacion, describir_defuzzificacion

_figuras_abiertas = []


def clasificar_difuso(datos, metricas=None, pesos=None, mostrar_defuzzificacion=False, nombre_zona=""):
    if pesos is None:
        pesos = PESOS_DEFAULT.copy()
    grados = fuzzificar_entrada(datos)
    activacion = evaluar_reglas(grados, pesos)
    resultado = agregar_consecuentes(activacion)
    nivel, score = defuzzificar_y_clasificar(resultado)
    if mostrar_defuzzificacion:
        graficar_membresia_consecuente(activacion["bajo"], activacion["medio"], activacion["alto"], score, nombre_zona)
    return nivel, score


def clasificar_difuso_completo(datos, metricas=None, pesos=None, visualizar_pasos=False, nombre_zona=""):
    if pesos is None:
        pesos = PESOS_DEFAULT.copy()
    grados = fuzzificar_entrada(datos)
    if visualizar_pasos:
        graficar_fuzzificacion(datos, nombre_zona)
    activacion = evaluar_reglas(grados, pesos)
    if visualizar_pasos:
        graficar_evaluacion_reglas(grados, pesos, nombre_zona)
    resultado = agregar_consecuentes(activacion)
    if visualizar_pasos:
        graficar_agregacion(activacion, nombre_zona)
    nivel, score = defuzzificar_y_clasificar(resultado)
    if visualizar_pasos:
        graficar_defuzzificacion(resultado, score, nombre_zona)
    return {
        "nivel": nivel,
        "score": score,
        "grados_membresia": grados,
        "activacion": activacion,
        "resultado_agregacion": resultado,
    }


def graficar_membresia(datos_zona=None, nombre_zona=""):
    global _figuras_abiertas
    if datos_zona is None:
        datos_zona = {}
    graficar_fuzzificacion(datos_zona, nombre_zona)
    _figuras_abiertas.append(plt.gcf())
    try:
        plt.gcf().canvas.manager.window.wm_attributes("-topmost", 1)
        plt.gcf().canvas.manager.window.wm_attributes("-topmost", 0)
    except Exception:
        pass
    print(f"     Grafica de membresia abierta para: {nombre_zona}")


def graficar_membresia_consecuente(mu_bajo=0.0, mu_medio=0.0, mu_alto=0.0, score_final=None, nombre_zona=""):
    global _figuras_abiertas
    from .agregacion import agregar_consecuentes
    activacion = {"bajo": mu_bajo, "medio": mu_medio, "alto": mu_alto}
    resultado = agregar_consecuentes(activacion)
    graficar_defuzzificacion(resultado, score_final, nombre_zona)
    _figuras_abiertas.append(plt.gcf())
    try:
        plt.gcf().canvas.manager.window.wm_attributes("-topmost", 1)
        plt.gcf().canvas.manager.window.wm_attributes("-topmost", 0)
    except Exception:
        pass
    if score_final is not None:
        print(f"     Centroide calculado: {score_final:.2f}")


def mantener_graficas_abiertas():
    global _figuras_abiertas
    if _figuras_abiertas:
        print(f"\n  {len(_figuras_abiertas)} grafica(s) permanecen abiertas")
        print("  Cierra las ventanas manualmente cuando termines")
        for fig in _figuras_abiertas:
            try:
                fig.show()
            except Exception:
                pass
    else:
        print("\n  No hay graficas para mantener abiertas")


def describir_membresia():
    return describir_fuzzificacion()
