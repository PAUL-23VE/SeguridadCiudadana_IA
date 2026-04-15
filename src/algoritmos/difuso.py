"""
difuso.py
=========
Modulo de compatibilidad - redirige a src.Fuzzy donde esta implementada
la logica difusa completa en 4 modulos separados:

  Paso 1 - src/Fuzzy/fuzzificacion.py     -> funciones de membresia
  Paso 2 - src/Fuzzy/evaluacion_reglas.py -> reglas IF-THEN ponderadas
  Paso 3 - src/Fuzzy/agregacion.py        -> truncamiento MIN + union MAX
  Paso 4 - src/Fuzzy/defuzzificacion.py   -> centroide
           src/Fuzzy/sistema_difuso.py    -> integracion de los 4 pasos
"""
from src.Fuzzy.fuzzificacion import (
    TIPO_MEMBRESIA,
    MAXIMOS as _MAXIMOS,
    _triangular,
    _sigma,
    _grado_bajo,
    _grado_medio,
    _grado_alto,
)

from src.Fuzzy.agregacion import (
    _cons_bajo  as _membresia_consecuente_bajo,
    _cons_medio as _membresia_consecuente_medio,
    _cons_alto  as _membresia_consecuente_alto,
)

from src.Fuzzy.sistema_difuso import (
    clasificar_difuso,
    describir_membresia,
    graficar_membresia,
    graficar_membresia_consecuente,
    mantener_graficas_abiertas,
    PESOS_DEFAULT,
)

from src.Fuzzy.defuzzificacion import (
    graficar_defuzzificacion,
)

__all__ = [
    'TIPO_MEMBRESIA',
    '_MAXIMOS',
    '_triangular',
    '_sigma',
    '_grado_bajo',
    '_grado_medio',
    '_grado_alto',
    '_membresia_consecuente_bajo',
    '_membresia_consecuente_medio',
    '_membresia_consecuente_alto',
    'clasificar_difuso',
    'describir_membresia',
    'graficar_membresia',
    'graficar_membresia_consecuente',
    'graficar_defuzzificacion',
    'mantener_graficas_abiertas',
    'PESOS_DEFAULT',
]

