import numpy as np
import random

from configs import PROB_MUTACION, MOSTRAR_TODAS

from seleccion import seleccion_ruleta_parcial
from crossover import crossover_binario_en_un_punto
from mutacion import mutacion_gaussiana

from serpiente import Serpiente

class Poblacion:
    
    def __init__(self, dimension_poblacion):
        # su mitad tiene que ser par
        self.dimension_poblacion = dimension_poblacion

        self.padre1 = None
        self.padre2 = None
        self.hijo = None

        self.prob_mutacion = PROB_MUTACION
        self.prob_mutacion_default = self.prob_mutacion

        self.generacion = 0

        # crea la lista de serpientes que juegan
        self.poblacion = []
        for _ in range(dimension_poblacion):
            self.poblacion.append(Serpiente())

        self.mejor_serpiente = Serpiente()
        self.mejor_puntaje = self.mejor_serpiente.puntaje
        # self.misma_mejor = 0

    def termino_de_jugar(self):
        # retorna True si todas las serpientes estan muertas
        estados_serpientes = [serpiente.muerta for serpiente in self.poblacion]
        return all(estados_serpientes)

    def actualizar(self):
        if not self.mejor_serpiente.muerta:
            self.mejor_serpiente.mirar()
            self.mejor_serpiente.pensar()
            self.mejor_serpiente.mover()

        for serpiente in self.poblacion:
            if not serpiente.muerta:
                serpiente.mirar()
                serpiente.pensar()
                serpiente.mover()

    def mostrar(self):
        if not MOSTRAR_TODAS:
            self.mejor_serpiente.mostrar()
        else:
            for serpiente in self.poblacion:
                serpiente.mostrar()

    def calcular_fitness(self):
        # se guarda el mejor puntaje
        if self.mejor_serpiente.puntaje > self.mejor_puntaje:
            self.mejor_puntaje = self.mejor_serpiente.puntaje

        # se calcula el fitness de cada serpiente
        for serpiente in self.poblacion:
            serpiente.calcular_fitness()

    def set_mejor_serpiente(self):
        # crea una lista de fitnesses
        lista_fitness = [serpiente.fitness for serpiente in self.poblacion]
        maxIndex = np.argmax(lista_fitness)
        # si la mejor serpiente elegida es igual a la anterior se clona esa
        if self.mejor_serpiente == self.poblacion[maxIndex].clonar_para_replay():
            self.mejor_serpiente = self.mejor_serpiente.clonar_para_replay()
            
            # self.misma_mejor += 1
            # if self.misma_mejor > 2:
            #     self.prob_mutacion *= 2
            #     self.misma_mejor = 0
            
        else:
            self.mejor_serpiente = self.poblacion[maxIndex].clonar_para_replay()
            self.puntaje_mejor_serpiente = self.poblacion[maxIndex].puntaje

            # self.misma_mejor = 0
            # self.prob_mutacion = self.prob_mutacion_default

    def seleccion_natural(self):
        poblacion_hijos = []
        
        # calcula cual es la mejor serpiente
        self.set_mejor_serpiente()
        
        # pasa la mejor serpiente a la siguiente generacion
        poblacion_hijos.append(self.mejor_serpiente.clonar())
        # reproduce hasta tener todos los hijos
        for _ in range(self.dimension_poblacion - 1):
            # se seleccionan 2 padres
            self.seleccion()
            # se crean 2 hijos a partir de ellos
            self.crossover()
            # se mutan algunos pesos segun la probabilidad
            self.mutacion()

            # se añaden los hijos a una lista temporal
            poblacion_hijos.append(self.hijo)
        
        # guardamos a los hijos (y la mejor serpiente) en la poblacion
        self.poblacion = poblacion_hijos.copy()

        # mezcla la poblacion (no afecta al aprendizaje)
        random.shuffle(self.poblacion)

        self.generacion += 1

    def seleccion(self):
        # elije a un progenitor1
        self.padre1 = seleccion_ruleta_parcial(self.poblacion)
        # elije a un progenitor2
        self.padre2 = seleccion_ruleta_parcial(self.poblacion)

    def crossover(self):
        self.hijo = Serpiente()

        cerebro_padre1 = self.padre1.cerebro
        cerebro_padre2 = self.padre2.cerebro
        cerebro_hijo = self.hijo.cerebro

        # se obtienen los cromosomas de los progenitores
        cromosomas_padre1 = cerebro_padre1.get_cromosomas()
        cromosomas_padre2 = cerebro_padre2.get_cromosomas()
        cromosomas_hijo = {}

        num_capas = cerebro_padre1.get_dimension_red()
        for n in range(1, num_capas):
            # se realiza el crossover de cromosomas de cada progenitor
            cromosomas_hijo[f"P{n}"] = crossover_binario_en_un_punto(cromosomas_padre1[f"P{n}"], cromosomas_padre2[f"P{n}"])

        # se setean los cromosomas de cada hijo
        cerebro_hijo.set_cromosomas(cromosomas_hijo)

    def mutacion(self):
        cerebro_hijo = self.hijo.cerebro
        cromosomas_hijo = cerebro_hijo.get_cromosomas()

        num_capas = cerebro_hijo.get_dimension_red()
        for n in range(1, num_capas):
            # muta los pesos del hijo
            pesos_hijo_mutados = mutacion_gaussiana(cromosomas_hijo[f"P{n}"], self.prob_mutacion)

            # actualiza los pesos del hijo
            cerebro_hijo.set_cromosomas_por_parametro(pesos_hijo_mutados, f"P{n}")