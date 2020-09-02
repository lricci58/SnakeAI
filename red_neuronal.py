import numpy as np

from configs import ARQUITECTURA_RED

class Red_Neuronal:

    def __init__(self):
        # seteamos el numero de nodos por capa
        # capa de entrada
        self.lista_capas = [ARQUITECTURA_RED["num_entradas"]]                          
        # capa oculta
        self.lista_capas.extend(ARQUITECTURA_RED["arquitectura_capa_oculta"])  
        # capa de salida: 4 salidas - arriba, abajo, izquierda y derecha
        self.lista_capas.append(4)

        self.parametros = {}

        # setea pesos y biases iniciales de cada fila en la capa oculta y la de salida
        for n in range(1, len(self.lista_capas)):
            # P[n] y b[n] guardan una lista de valores uniformes entre -1 y 1
            # la dimension de la lista de pesos, por ejemplo, va a ser de [self.lista_capas[n]] columnas y [self.lista_capas[n-1]] filas
            self.parametros[f"P{n}"] = np.random.uniform(-1, 1, (self.lista_capas[n], self.lista_capas[n-1]))
            # self.parametros[f"B{n}"] = np.ones(shape=(self.lista_capas[n], 1))
    
    def tomar_decision(self, lista_entradas):
        longitud_arquitectura = len(self.lista_capas) - 1

        # recorremos cada fila de la capa oculta
        for n in range(1, longitud_arquitectura):
            # obtenemos los pesos y biases
            pesos = self.parametros[f"P{n}"]
            # el output del nodo es la multipicacion del peso con cada input(lista) mas el bias
            resultado = np.dot(pesos, lista_entradas)
            # ejecutamos la func de activacion y esos seran los inputs de la siguiente capa
            lista_entradas = self.__reLU(resultado)

        # mismo proceso pero para el output
        pesos = self.parametros[f"P{longitud_arquitectura}"]
        resultado = np.dot(pesos, lista_entradas)
        salida = self.__reLU(resultado)

        return salida
    
    def __reLU(self, x):
        return np.maximum(0, x)

    def get_dimension_red(self):
        return len(self.lista_capas)

    def get_cromosomas(self):
        return self.parametros
    
    def set_cromosomas(self, nuevos_cromosomas):
        self.parametros = nuevos_cromosomas
    
    def set_cromosomas_por_parametro(self, nuevo_cromosoma, posicion):
        self.parametros[posicion] = nuevo_cromosoma