import numpy as np
import random

def seleccion_ruleta_parcial(poblacion):
    # se crea la ruleta
    ruleta = sum(serpiente.fitness for serpiente in poblacion)

    resultado_ruleta = random.uniform(0, ruleta)
    puntero_fitness_serpiente = 0
    for serpiente in poblacion:
        # se define el puntero de la serpiente actual
        puntero_fitness_serpiente += abs(serpiente.fitness)
        # si el puntero alcanzo el valor de la ruleta, significa que la serpiente actual es la seleccionada
        if puntero_fitness_serpiente >= resultado_ruleta:
            return serpiente