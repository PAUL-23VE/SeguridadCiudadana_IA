"""
reglas.py
=========
Módulo para minería de reglas Apriori y PRISM sobre el dataset de zonas.

Implementación completa siguiendo el proceso del ingeniero:
1. Discretizar datos (convertir a categorías)
2. Encontrar items frecuentes (PASO 1 - Frecuencia)
3. Reducir por soporte mínimo (PASO 2 - Filtrar)
4. Generar combinaciones (PASO 3 - Combinar)
5. Calcular confianza y soporte
6. Filtrar reglas por confianza mínima
"""
import numpy as np
from itertools import combinations
from collections import defaultdict


def discretizar_valor(valor, variable):
    """
    Discretiza un valor continuo a categorías (bajo/medio/alto).
    Siguiendo el proceso de la imagen: X₁(1), X₂(0), etc.
    
    Parámetros
    ----------
    valor : float
        Valor numérico a discretizar
    variable : str
        Nombre de la variable
    
    Retorna
    -------
    str : Categoría ('bajo', 'medio', 'alto')
    """
    if variable in ['robos', 'vandalismo', 'llamadas_emergencias']:
        # Variables de 0-100
        if valor < 33:
            return 'bajo'
        elif valor < 66:
            return 'medio'
        else:
            return 'alto'
    elif variable in ['microtrafico', 'accidentes']:
        # Variables de 0-50 o 0-60
        if valor < 20:
            return 'bajo'
        elif valor < 40:
            return 'medio'
        else:
            return 'alto'
    else:
        # Por defecto
        if valor < 33:
            return 'bajo'
        elif valor < 66:
            return 'medio'
        else:
            return 'alto'


def generar_dataset_transaccional():
    """
    Genera un dataset transaccional para Apriori.
    Cada transacción = zona con sus atributos discretizados.
    
    Retorna
    -------
    list : Lista de transacciones (sets de items)
    list : Lista de niveles de riesgo correspondientes
    """
    transacciones = []
    niveles = []
    
    # Generar 100 zonas sintéticas
    for _ in range(100):
        zona = {
            'robos': np.random.randint(0, 100),
            'microtrafico': np.random.randint(0, 50),
            'vandalismo': np.random.randint(0, 80),
            'accidentes': np.random.randint(0, 60),
            'llamadas_emergencias': np.random.randint(0, 100)
        }
        
        # Discretizar cada atributo
        items = set()
        for variable, valor in zona.items():
            categoria = discretizar_valor(valor, variable)
            items.add(f"{variable}={categoria}")  # Ejemplo: "robos=alto"
        
        # Calcular nivel de riesgo
        score = (zona['robos'] * 0.35 + zona['microtrafico'] * 0.15 + 
                 zona['vandalismo'] * 0.25 + zona['accidentes'] * 0.10 +
                 zona['llamadas_emergencias'] * 0.15)
        
        if score < 33:
            nivel = 'Bajo'
        elif score < 66:
            nivel = 'Medio'
        else:
            nivel = 'Alto'
        
        # Agregar nivel como item especial
        items.add(f"riesgo={nivel}")
        
        transacciones.append(items)
        niveles.append(nivel)
    
    return transacciones, niveles


def calcular_soporte(itemset, transacciones):
    """
    PASO 1: Calcula el soporte de un itemset.
    
    Soporte = frecuencia del itemset / total de transacciones
    Ejemplo de la imagen: P(B∧A) = 3/6 = 0.6
    
    Parámetros
    ----------
    itemset : frozenset
        Conjunto de items
    transacciones : list
        Lista de transacciones
    
    Retorna
    -------
    float : Soporte (0.0 - 1.0)
    """
    count = sum(1 for trans in transacciones if itemset.issubset(trans))
    return count / len(transacciones)


def obtener_items_frecuentes_1(transacciones, min_soporte):
    """
    PASO 1: Encuentra items individuales frecuentes.
    Ejemplo de la imagen: X₁(1)=4, X₂(1)=6
    
    Parámetros
    ----------
    transacciones : list
        Lista de transacciones
    min_soporte : float
        Soporte mínimo (ej: 0.1 = 10%)
    
    Retorna
    -------
    list : Items frecuentes con soporte >= min_soporte
    """
    # Contar frecuencia de cada item
    item_counts = defaultdict(int)
    for trans in transacciones:
        for item in trans:
            item_counts[item] += 1
    
    # Filtrar por soporte mínimo (PASO 2 - Reducir)
    total = len(transacciones)
    items_frecuentes = []
    
    for item, count in item_counts.items():
        soporte = count / total
        if soporte >= min_soporte:
            items_frecuentes.append((frozenset([item]), soporte))
    
    return items_frecuentes


def generar_candidatos_k(items_frecuentes_k_minus_1, k):
    """
    PASO 3: Genera combinaciones de k items.
    Ejemplo de la imagen: Combinar X₁(1) con X₂(1)
    
    Parámetros
    ----------
    items_frecuentes_k_minus_1 : list
        Items frecuentes de tamaño k-1
    k : int
        Tamaño de los candidatos a generar
    
    Retorna
    -------
    list : Candidatos de tamaño k
    """
    candidatos = []
    n = len(items_frecuentes_k_minus_1)
    
    for i in range(n):
        for j in range(i + 1, n):
            # Unir dos itemsets de tamaño k-1
            union = items_frecuentes_k_minus_1[i][0] | items_frecuentes_k_minus_1[j][0]
            if len(union) == k:
                candidatos.append(union)
    
    return candidatos


def apriori(transacciones, min_soporte=0.1):
    """
    Algoritmo Apriori completo siguiendo el proceso del ingeniero.
    
    Proceso:
    1. Encontrar items frecuentes de tamaño 1
    2. Reducir por soporte mínimo
    3. Generar candidatos de tamaño k (k=2,3,...)
    4. Filtrar candidatos por soporte
    5. Repetir hasta que no haya más candidatos
    
    Parámetros
    ----------
    transacciones : list
        Lista de transacciones (sets de items)
    min_soporte : float
        Soporte mínimo (default: 0.1 = 10%)
    
    Retorna
    -------
    list : Items frecuentes con su soporte
    """
    # PASO 1 y 2: Items frecuentes de tamaño 1
    items_frecuentes = obtener_items_frecuentes_1(transacciones, min_soporte)
    todos_frecuentes = items_frecuentes.copy()
    
    k = 2
    while items_frecuentes:
        # PASO 3: Generar candidatos de tamaño k
        candidatos = generar_candidatos_k(items_frecuentes, k)
        
        if not candidatos:
            break
        
        # Calcular soporte de cada candidato
        items_frecuentes = []
        for candidato in candidatos:
            soporte = calcular_soporte(candidato, transacciones)
            if soporte >= min_soporte:
                items_frecuentes.append((candidato, soporte))
                todos_frecuentes.append((candidato, soporte))
        
        k += 1
    
    return todos_frecuentes


def generar_reglas_apriori(items_frecuentes, transacciones, min_confianza=0.7):
    """
    Genera reglas de asociación a partir de items frecuentes.
    
    Calcula confianza siguiendo la imagen: P(B/A) = frecuencia/total
    Ejemplo: Si robos=alto → riesgo=Alto, confianza = 3/4 = 0.75
    
    Parámetros
    ----------
    items_frecuentes : list
        Items frecuentes del algoritmo Apriori
    transacciones : list
        Transacciones originales
    min_confianza : float
        Confianza mínima (default: 0.7 = 70%)
    
    Retorna
    -------
    list : Reglas con formato (antecedente, consecuente, soporte, confianza)
    """
    reglas = []
    
    for itemset, soporte in items_frecuentes:
        if len(itemset) < 2:
            continue
        
        # Generar todas las posibles divisiones antecedente → consecuente
        for i in range(1, len(itemset)):
            for antecedente in combinations(itemset, i):
                antecedente = frozenset(antecedente)
                consecuente = itemset - antecedente
                
                # Filtrar: solo reglas que concluyan en "riesgo="
                tiene_riesgo = any('riesgo=' in item for item in consecuente)
                if not tiene_riesgo:
                    continue
                
                # Calcular confianza: P(B/A) = P(A∧B) / P(A)
                soporte_antecedente = calcular_soporte(antecedente, transacciones)
                if soporte_antecedente == 0:
                    continue
                
                confianza = soporte / soporte_antecedente
                
                # Filtrar por confianza mínima
                if confianza >= min_confianza:
                    reglas.append({
                        'antecedente': antecedente,
                        'consecuente': consecuente,
                        'soporte': soporte,
                        'confianza': confianza
                    })
    
    return reglas


def reglas_apriori(dataset=None, min_soporte=0.1, min_confianza=0.7, silencioso=True):
    """
    Función principal de Apriori (SILENCIOSO).
    
    Parámetros
    ----------
    dataset : cualquier cosa (no se usa, se genera sintético)
    min_soporte : float
        Soporte mínimo (default: 0.1 = 10%)
    min_confianza : float
        Confianza mínima (default: 0.7 = 70%)
    silencioso : bool
        Si True, no imprime nada (default: True)
    
    Retorna
    -------
    list : Lista de reglas en formato string
    """
    # Generar dataset transaccional
    transacciones, _ = generar_dataset_transaccional()
    
    # Aplicar Apriori
    items_frecuentes = apriori(transacciones, min_soporte)
    
    # Generar reglas
    reglas = generar_reglas_apriori(items_frecuentes, transacciones, min_confianza)
    
    # Formatear reglas como strings
    reglas_str = []
    for regla in reglas[:10]:  # Top 10 reglas
        ant_str = " Y ".join(sorted(regla['antecedente']))
        cons_str = " Y ".join(sorted(regla['consecuente']))
        reglas_str.append(
            f"SI {ant_str} → {cons_str} "
            f"(soporte={regla['soporte']:.2f}, conf={regla['confianza']:.2f})"
        )
    
    return reglas_str if reglas_str else ["No se encontraron reglas con los criterios dados"]


def reglas_prism(dataset=None, min_confianza=0.5, silencioso=True):
    """
    Algoritmo PRISM para generación de reglas de clasificación (SILENCIOSO).
    
    Parámetros
    ----------
    dataset : cualquier cosa (se genera sintético)
    min_confianza : float
        Confianza mínima requerida para una regla (default: 0.5)
    silencioso : bool
        Si True, no imprime nada (default: True)
    
    Retorna
    -------
    list : reglas generadas en formato texto
    """
    # Generar dataset transaccional
    transacciones, niveles = generar_dataset_transaccional()
    
    # Convertir a formato tabla
    ejemplos = []
    for trans, nivel in zip(transacciones, niveles):
        ejemplo = {}
        for item in trans:
            if 'riesgo=' not in item:
                variable, valor = item.split('=')
                ejemplo[variable] = valor
        ejemplo['riesgo'] = nivel
        ejemplos.append(ejemplo)
    
    # Clases disponibles
    clases = ['Alto', 'Medio', 'Bajo']
    
    # Reglas generadas
    todas_reglas = []
    
    # PRISM: Para cada clase
    for clase_objetivo in clases:
        ejemplos_disponibles = ejemplos.copy()
        iteracion = 1
        
        # Mientras haya ejemplos sin cubrir de esta clase
        while ejemplos_disponibles:
            # Ejemplos de esta clase que aún no están cubiertos
            ejemplos_clase = [e for e in ejemplos_disponibles if e['riesgo'] == clase_objetivo]
            
            if not ejemplos_clase or len(ejemplos_clase) < 2:
                break
            
            mejor_condicion = None
            mejor_confianza = 0
            mejor_variable = None
            mejor_valor = None
            mejor_ejemplos_cumplen = []
            
            # Probar todas las condiciones posibles
            variables = ['robos', 'microtrafico', 'vandalismo', 'accidentes', 'llamadas_emergencias']
            valores = ['bajo', 'medio', 'alto']
            
            for var in variables:
                for val in valores:
                    # Contar ejemplos que cumplen la condición
                    ejemplos_cumplen = [e for e in ejemplos_disponibles if e.get(var) == val]
                    
                    if not ejemplos_cumplen:
                        continue
                    
                    # CÁLCULO DE CONFIANZA
                    correctos = sum(1 for e in ejemplos_cumplen if e['riesgo'] == clase_objetivo)
                    confianza = correctos / len(ejemplos_cumplen)
                    
                    # Seleccionar la mejor condición
                    if confianza > mejor_confianza:
                        mejor_confianza = confianza
                        mejor_condicion = (var, val)
                        mejor_variable = var
                        mejor_valor = val
                        mejor_ejemplos_cumplen = ejemplos_cumplen
            
            # Si encontramos una condición con confianza suficiente
            if mejor_confianza >= min_confianza and mejor_condicion:
                correctos = sum(1 for e in mejor_ejemplos_cumplen if e['riesgo'] == clase_objetivo)
                total_cumplen = len(mejor_ejemplos_cumplen)
                
                regla_texto = f"SI {mejor_variable}={mejor_valor} ENTONCES riesgo={clase_objetivo}"
                todas_reglas.append({
                    'regla': regla_texto,
                    'confianza': mejor_confianza,
                    'soporte': total_cumplen / len(ejemplos),
                    'ejemplos_cubiertos': total_cumplen
                })
                
                # Eliminar ejemplos cubiertos
                ejemplos_disponibles = [e for e in ejemplos_disponibles if e not in mejor_ejemplos_cumplen]
                iteracion += 1
            else:
                # No hay más condiciones útiles para esta clase
                break
    
    # Formatear reglas como strings
    reglas_str = []
    for regla in todas_reglas:
        reglas_str.append(
            f"{regla['regla']} "
            f"(confianza={regla['confianza']:.2f}, soporte={regla['soporte']:.2f})"
        )
    
    return reglas_str if reglas_str else ["No se encontraron reglas PRISM"]

def obtener_regla_explicativa(datos, nivel):
    """
    Retorna una regla explicativa según el nivel de riesgo calculado.
    """
    if nivel == 'Alto':
        reglas = reglas_apriori([datos], silencioso=True)
        return reglas[0] if reglas else "Sin regla disponible"
    elif nivel == 'Medio':
        return reglas_prism([datos], silencioso=True)[0]
    else:
        return "Sin regla relevante para nivel de riesgo bajo"