"""
genetico.py
===========
Módulo para optimización de pesos de la lógica difusa usando Algoritmo Genético.

Implementación siguiendo el proceso estándar:
1. Población inicial (N individuos)
2. Selección de padres
3. Crossover (cruce)
4. Mutación
5. Selección de N individuos
6. Criterio de detención
7. Solución (el mejor individuo)
"""
import numpy as np
import random


def generar_dataset_prueba(n=100):
    """
    Genera un dataset sintético para evaluar el fitness.
    
    Retorna
    -------
    list : Lista de ejemplos con datos y etiqueta real
    """
    dataset = []
    for _ in range(n):
        # Generar datos aleatorios
        robos = np.random.randint(0, 100)
        microtrafico = np.random.randint(0, 50)
        vandalismo = np.random.randint(0, 80)
        accidentes = np.random.randint(0, 60)
        llamadas = np.random.randint(0, 100)
        
        # Calcular score promedio para asignar etiqueta "real"
        score_avg = (robos * 0.35 + microtrafico * 0.15 + vandalismo * 0.25 + 
                     accidentes * 0.10 + llamadas * 0.15)
        
        if score_avg < 33:
            nivel = 'Bajo'
        elif score_avg < 66:
            nivel = 'Medio'
        else:
            nivel = 'Alto'
        
        dataset.append({
            'robos': robos,
            'microtrafico': microtrafico,
            'vandalismo': vandalismo,
            'accidentes': accidentes,
            'llamadas_emergencias': llamadas,
            'nivel_real': nivel
        })
    
    return dataset


def calcular_fitness(individuo, dataset):
    """
    Función Fitness: Evalúa la precisión de clasificación.
    
    Un individuo es un conjunto de pesos para cada variable.
    El fitness mide qué tan bien estos pesos clasifican el dataset.
    
    Parámetros
    ----------
    individuo : dict
        Diccionario con pesos para cada factor
    dataset : list
        Dataset de prueba con ejemplos etiquetados
    
    Retorna
    -------
    float : Precisión de clasificación (0.0 a 1.0)
    """
    correctos = 0
    total = len(dataset)
    
    for ejemplo in dataset:
        # Calcular score ponderado
        score = (
            ejemplo['robos'] * individuo['robos'] +
            ejemplo['microtrafico'] * individuo['microtrafico'] +
            ejemplo['vandalismo'] * individuo['vandalismo'] +
            ejemplo['accidentes'] * individuo['accidentes'] +
            ejemplo['llamadas_emergencias'] * individuo['llamadas_emergencias']
        )
        
        # Normalizar a escala 0-100
        score_normalizado = score / 100 * 100
        
        # Clasificar
        if score_normalizado < 33:
            prediccion = 'Bajo'
        elif score_normalizado < 66:
            prediccion = 'Medio'
        else:
            prediccion = 'Alto'
        
        # Comparar con etiqueta real
        if prediccion == ejemplo['nivel_real']:
            correctos += 1
    
    return correctos / total


def crear_individuo():
    """
    Crea un individuo (conjunto de pesos) aleatorio.
    Los pesos suman aproximadamente 1.0 para mantener normalización.
    
    Retorna
    -------
    dict : Individuo con pesos aleatorios
    """
    pesos = [random.random() for _ in range(5)]
    suma = sum(pesos)
    
    return {
        'robos': pesos[0] / suma,
        'microtrafico': pesos[1] / suma,
        'vandalismo': pesos[2] / suma,
        'accidentes': pesos[3] / suma,
        'llamadas_emergencias': pesos[4] / suma
    }


def crear_poblacion_inicial(n):
    """
    PASO 1: Crear población inicial de N individuos.
    
    Parámetros
    ----------
    n : int
        Tamaño de la población
    
    Retorna
    -------
    list : Lista de individuos (diccionarios de pesos)
    """
    return [crear_individuo() for _ in range(n)]

def seleccion_padres(poblacion, fitness_scores, n_padres):
    """
    PASO 2: Selección de padres por torneo.
    
    Selecciona los mejores individuos para reproducción.
    
    Parámetros
    ----------
    poblacion : list
        Lista de individuos
    fitness_scores : list
        Lista de scores de fitness de cada individuo
    n_padres : int
        Número de padres a seleccionar
    
    Retorna
    -------
    list : Lista de padres seleccionados
    """
    # Crear lista de tuplas (individuo, fitness)
    individuos_con_fitness = list(zip(poblacion, fitness_scores))
    
    # Ordenar por fitness (de mayor a menor)
    individuos_con_fitness.sort(key=lambda x: x[1], reverse=True)
    
    # Seleccionar los mejores n_padres
    padres = [ind for ind, fit in individuos_con_fitness[:n_padres]]
    
    return padres


def crossover(padre1, padre2):
    """
    PASO 3: Crossover (cruce) entre dos padres.
    
    Crea un hijo combinando genes (pesos) de ambos padres.
    Usa cruce promedio: hijo = (padre1 + padre2) / 2
    
    Parámetros
    ----------
    padre1, padre2 : dict
        Individuos padres
    
    Retorna
    -------
    dict : Nuevo individuo (hijo)
    """
    hijo = {}
    for key in padre1.keys():
        # Promedio de los pesos de ambos padres
        hijo[key] = (padre1[key] + padre2[key]) / 2
    
    return hijo


def mutacion(individuo, prob_mutacion=0.1, factor_mutacion=0.2):
    """
    PASO 4: Mutación de un individuo.
    
    Con cierta probabilidad, altera aleatoriamente algunos genes.
    
    Parámetros
    ----------
    individuo : dict
        Individuo a mutar
    prob_mutacion : float
        Probabilidad de mutación de cada gen (default: 0.1 = 10%)
    factor_mutacion : float
        Magnitud de la mutación (default: 0.2 = ±20%)
    
    Retorna
    -------
    dict : Individuo mutado
    """
    individuo_mutado = individuo.copy()
    
    for key in individuo_mutado.keys():
        if random.random() < prob_mutacion:
            # Aplicar mutación: agregar valor aleatorio
            cambio = random.uniform(-factor_mutacion, factor_mutacion)
            individuo_mutado[key] = max(0.0, individuo_mutado[key] + cambio)
    
    # Renormalizar para que los pesos sumen 1.0
    suma = sum(individuo_mutado.values())
    if suma > 0:
        for key in individuo_mutado.keys():
            individuo_mutado[key] /= suma
    
    return individuo_mutado


def optimizar_pesos(dataset=None, generaciones=50, tam_poblacion=30, silencioso=False):
    """
    Algoritmo Genético completo para optimización de pesos.
    
    Sigue el proceso:
    1. Población inicial
    2. Bucle de evolución (generaciones):
       a. Selección de padres
       b. Crossover
       c. Mutación
       d. Selección de N individuos (elitismo)
    3. Retornar el mejor individuo
    
    Parámetros
    ----------
    dataset : dict or None
        Datos de entrada (no usado, se genera dataset sintético)
    generaciones : int
        Número de generaciones a evolucionar (default: 50)
    tam_poblacion : int
        Tamaño de la población (default: 30)
    silencioso : bool
        Si True, no imprime información del proceso
    
    Retorna
    -------
    dict : Mejor conjunto de pesos encontrado
    """    # Leer configuración del AG desde config.py
    from config import GENETICO_CONFIG
    n_elite = GENETICO_CONFIG.get('elitismo', 2)

    # Generar dataset de prueba
    dataset_prueba = generar_dataset_prueba(100)
    
    if not silencioso:
        print(f"     → Población inicial: {tam_poblacion} individuos")
        print(f"     → Elitismo: {n_elite} individuos preservados por generación")
    
    # PASO 1: Crear población inicial
    poblacion = crear_poblacion_inicial(tam_poblacion)
    
    mejor_fitness_global = 0
    mejor_individuo_global = None
    
    # Evolución por generaciones
    for gen in range(generaciones):
        # Evaluar fitness de toda la población
        fitness_scores = [calcular_fitness(ind, dataset_prueba) for ind in poblacion]
        
        # Encontrar el mejor de esta generación
        mejor_fitness_gen = max(fitness_scores)
        idx_mejor = fitness_scores.index(mejor_fitness_gen)
        mejor_individuo_gen = poblacion[idx_mejor]
        
        # Actualizar mejor global
        if mejor_fitness_gen > mejor_fitness_global:
            mejor_fitness_global = mejor_fitness_gen
            mejor_individuo_global = mejor_individuo_gen
        
        if not silencioso and gen % 10 == 0:
            print(f"     → Generación {gen+1}/{generaciones}: Fitness = {mejor_fitness_gen:.3f} ({mejor_fitness_gen*100:.1f}%)")
        
        # PASO 2: Selección de padres (50% de la población)
        n_padres = tam_poblacion // 2
        padres = seleccion_padres(poblacion, fitness_scores, n_padres)
        
        # PASO 3 y 4: Crossover y Mutación para crear nueva generación
        nueva_poblacion = []
        
        # Elitismo: preservar los n_elite mejores individuos sin modificación
        individuos_ordenados = sorted(
            zip(poblacion, fitness_scores),
            key=lambda x: x[1],
            reverse=True
        )
        for ind, _ in individuos_ordenados[:n_elite]:
            nueva_poblacion.append(ind)
        
        while len(nueva_poblacion) < tam_poblacion:
            # Seleccionar dos padres aleatorios
            padre1 = random.choice(padres)
            padre2 = random.choice(padres)
            
            # PASO 3: Crossover
            hijo = crossover(padre1, padre2)
            
            # PASO 4: Mutación
            hijo = mutacion(hijo, prob_mutacion=0.1)
            
            nueva_poblacion.append(hijo)
        
        # PASO 5: Selección de N individuos (reemplazo generacional)
        poblacion = nueva_poblacion
    
    if not silencioso:
        print(f"     → Generación final {generaciones}/{generaciones}: Fitness = {mejor_fitness_global:.3f} ({mejor_fitness_global*100:.1f}%)")
    
    # PASO 6 y 7: Retornar la mejor solución
    return mejor_individuo_global
