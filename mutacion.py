import numpy as np

def mutacion_gaussiana(cromosomas, prob_mutacion):
    # crea un array con valores random entre [0.00, 1.00) con la forma dada que representan la probabilidad de mutacion
    # si el valor es menor a [prob_mutacion], la posicion contiene un False; tiene True en caso contrario
    # luego, se asigna el array de booleanos dentro de lista_mutaciones
    lista_mutaciones = np.random.random(cromosomas.shape) < prob_mutacion
    
    mutacion_gaussiana = np.random.normal(size=cromosomas.shape)
    
    mutacion_gaussiana[lista_mutaciones] /= 5

    # se actualizan los genes que "deben mutar" (segun el array lista_mutaciones) de cada cromosoma
    cromosomas[lista_mutaciones] += mutacion_gaussiana[lista_mutaciones]
    return cromosomas