import random
import math
import numpy as np

from configs import DIMENSION_PANTALLA, DIMENSION_SPRITE, COLORES, DIMENSION_INICIAL_SERPIENTE, AUMENTO_POSICIONES, AJUSTE_CABEZA, AJUSTE_OBJETO, MOSTRAR_EJES, PANTALLA, pygame

from comida import Comida
from red_neuronal import Red_Neuronal

class Serpiente:

    def __init__(self, lista_comida = None):
        # cada serpiente contiene un "cerebro" (Red Neuronal) con sus propios pesos
        self.cerebro = Red_Neuronal()

        self.velocidad_x = 0
        self.velocidad_y = -DIMENSION_SPRITE

        self.posiciones = [
            # posiciona a la serpiente a la mitad de la pantalla (mitad_x, mitad_y), (mitad_x, mitad_y+1), (mitad_x, mitad_y+2)
            ((DIMENSION_PANTALLA - DIMENSION_SPRITE*2)//2, (DIMENSION_PANTALLA - DIMENSION_SPRITE*2)//2),
            ((DIMENSION_PANTALLA - DIMENSION_SPRITE*2)//2, ((DIMENSION_PANTALLA - DIMENSION_SPRITE*2)//2) + DIMENSION_SPRITE),
            ((DIMENSION_PANTALLA - DIMENSION_SPRITE*2)//2, ((DIMENSION_PANTALLA - DIMENSION_SPRITE*2)//2) + DIMENSION_SPRITE*2)
        ]

        self.puntaje = DIMENSION_INICIAL_SERPIENTE
        self.pasos = 0
        self.pasos_disponibles = 200
        self.fitness = 0

        self.muerta = False

        self.vision = []
        
        self.ite_comida = 0
        if lista_comida is None:
            self.replay = False
            self.lista_comida = []

            self.comida = Comida()
            while self.encontro_cuerpo(*self.comida.posicion):
                self.comida = Comida()

            self.lista_comida.append(self.comida)
        # para el replay
        else:
            self.replay = True
            self.lista_comida = [comida.clonar() for comida in lista_comida]
            
            self.comida = self.lista_comida[self.ite_comida]
            self.ite_comida += 1

    def mostrar(self):
        self.comida.mostrar()
        for posicion_serpiente in self.posiciones[1:]:
            pygame.draw.rect(PANTALLA, COLORES["cuerpo"], [*posicion_serpiente, DIMENSION_SPRITE, DIMENSION_SPRITE])
        if self.muerta:
            pygame.draw.rect(PANTALLA, COLORES["muerta"], [*self.posiciones[0], DIMENSION_SPRITE, DIMENSION_SPRITE])
        else:
            pygame.draw.rect(PANTALLA, COLORES["cuerpo"], [*self.posiciones[0], DIMENSION_SPRITE, DIMENSION_SPRITE])

    def clonar(self):
        clone = Serpiente()
        clone.cerebro = self.cerebro
        return clone

    def clonar_para_replay(self):
        clone = Serpiente(self.lista_comida)
        clone.cerebro = self.cerebro
        return clone

    def pensar(self):
        salida = self.cerebro.tomar_decision(self.vision)
        desicion = np.argmax(salida)

        # aplica el movimiento segun la desicion
        if desicion == 0:
            self.mover_arriba()
        elif desicion == 1:
            self.mover_abajo()
        elif desicion == 2:
            self.mover_izq()
        elif desicion == 3:
            self.mover_der()

    def mover_arriba(self):
        if self.velocidad_y != DIMENSION_SPRITE:
            self.velocidad_x = 0
            self.velocidad_y = -DIMENSION_SPRITE

    def mover_abajo(self):
        if self.velocidad_y != -DIMENSION_SPRITE:
            self.velocidad_x = 0
            self.velocidad_y = DIMENSION_SPRITE

    def mover_izq(self):
        if self.velocidad_x != DIMENSION_SPRITE:
            self.velocidad_x = -DIMENSION_SPRITE
            self.velocidad_y = 0

    def mover_der(self):
        if self.velocidad_x != -DIMENSION_SPRITE:
            self.velocidad_x = DIMENSION_SPRITE
            self.velocidad_y = 0

    def mover(self):
        self.pasos += 1
        self.pasos_disponibles -= 1

        # COMER
        if self.encontro_comida(*self.posiciones[0]):
            self.comer()

        # mueve las posiciones del cuerpo
        self.cambiar_posiciones()

        # COLISION
        if self.encontro_pared(*self.posiciones[0]):
            self.muerta = True
        elif self.encontro_cuerpo(*self.posiciones[0]):
            self.muerta = True
        # ATASCADA
        elif self.quedo_sin_pasos():
            self.muerta = True

    def cambiar_posiciones(self):
        nuevas_posiciones = []

        cabeza_x, cabeza_y = self.posiciones[0]
        cabeza_x += self.velocidad_x
        cabeza_y += self.velocidad_y
        # el primer valor
        nuevas_posiciones.append((cabeza_x, cabeza_y))
        
        # agrega las posiciones anteriores
        nuevas_posiciones.extend(self.posiciones)
        # menos la ultima
        nuevas_posiciones.pop()

        self.posiciones = nuevas_posiciones.copy()

    def comer(self):
        self.puntaje += 1
        
        if self.pasos_disponibles < 500:
            if self.pasos_disponibles > 400:
                self.pasos_disponibles = 500
            else:
                self.pasos_disponibles += 100
        
        # duplica la ultima posicion de la cola
        self.posiciones.append(self.posiciones[-1])

        if not self.replay:
            self.comida = Comida()
            while self.encontro_cuerpo(*self.comida.posicion):
                self.comida = Comida()

            self.lista_comida.append(self.comida)
        else:
            self.comida = self.lista_comida[self.ite_comida]
            self.ite_comida += 1

    def mirar(self):
        # se crea un array de 24 posiciones (entradas)
        self.vision = [0.0] * 24

        num_entrada = 0
        for eje in range(8):
            vision_en_eje = self.__mirar_direccion(*AUMENTO_POSICIONES[eje], *AJUSTE_CABEZA[eje], *AJUSTE_OBJETO[eje])
            for vision in vision_en_eje:
                self.vision[num_entrada] = vision
                num_entrada += 1

    def __mirar_direccion(self, pos_x, pos_y, ajuste_cabeza_x, ajuste_cabeza_y, ajuste_objeto_x, ajuste_objeto_y):
        valores_eje = [0.0] * 3

        comida_encontrada = False
        cuerpo_encontrado = False

        cabeza_x, cabeza_y = self.posiciones[0]
        centro_cabeza_x = cabeza_x + ajuste_cabeza_x
        centro_cabeza_y = cabeza_y + ajuste_cabeza_y

        cabeza_x += pos_x
        cabeza_y += pos_y
        distancia = 1

        # repite las iteraciones hasta que la vision llegue a la pared
        while not self.encontro_pared(cabeza_x, cabeza_y):
            # comprueba si se encontro comida a su cuerpo
            if not comida_encontrada and self.encontro_comida(cabeza_x, cabeza_y):
                comida_encontrada = True
                # se dibuja la linea hasta el centro de la comida encontrada
                valores_eje[0] = 1.0
                if MOSTRAR_EJES and self.replay:
                    pygame.draw.line(PANTALLA, COLORES["encontro_comida"], (centro_cabeza_x, centro_cabeza_y), (cabeza_x + ajuste_objeto_x, cabeza_y + ajuste_objeto_y), 5)

            if not cuerpo_encontrado and self.encontro_cuerpo(cabeza_x, cabeza_y):
                cuerpo_encontrado = True
                valores_eje[1] = 1.0
                # se dibuja la linea hasta el centro del cuerpo encontrado
                if MOSTRAR_EJES and self.replay:
                    pygame.draw.line(PANTALLA, COLORES["encontro_cuerpo"], (centro_cabeza_x, centro_cabeza_y), (cabeza_x + ajuste_objeto_x, cabeza_y + ajuste_objeto_y), 5)

            # itera cada sprite segun el eje
            cabeza_x += pos_x
            cabeza_y += pos_y
            # por cada sprite iterado, es uno mas de distancia desde la cabeza hasta la pared que se debe encontrar
            distancia += 1

        # una vez llego a la pared, se devuelve esa distancia
        valores_eje[2] = 1/distancia

        # solo dibuja el eje, si no hay nada, si lo hay, ya se dibujo previamente una linea de otro color y grosor
        if not comida_encontrada and not cuerpo_encontrado:
            # dibuja la linea del eje hasta el centro de la pared encontrada
            if MOSTRAR_EJES and self.replay:
                pygame.draw.line(PANTALLA, COLORES["ejes"], (centro_cabeza_x, centro_cabeza_y), (cabeza_x + ajuste_objeto_x, cabeza_y + ajuste_objeto_y), 2)

        return valores_eje

    def encontro_pared(self, cabeza_x, cabeza_y):
        if cabeza_x >= DIMENSION_PANTALLA - DIMENSION_SPRITE or cabeza_x < DIMENSION_SPRITE:
            return True
        if cabeza_y >= DIMENSION_PANTALLA - DIMENSION_SPRITE or cabeza_y < DIMENSION_SPRITE:
            return True
        return False

    def encontro_comida(self, cabeza_x, cabeza_y):
        if (cabeza_x, cabeza_y) == self.comida.posicion:
            return True
        return False

    def encontro_cuerpo(self, cabeza_x, cabeza_y):
        if (cabeza_x, cabeza_y) in self.posiciones[1:]:
            return True
        return False

    def quedo_sin_pasos(self):
        if self.pasos_disponibles <= 0:
            return True
        return False

    def calcular_fitness(self):
        if(self.puntaje < 10):
            self.fitness = math.floor(self.pasos * self.pasos) * pow(2, self.puntaje)
        else:
            self.fitness = math.floor(self.pasos * self.pasos) 
            self.fitness *= pow(2, 10) 
            self.fitness *= (self.puntaje - 9)