import random

from configs import DIMENSION_PANTALLA, DIMENSION_SPRITE, COLORES, PANTALLA, pygame

class Comida:

    def __init__(self):
        self.posicion = (
            random.randrange(DIMENSION_SPRITE, DIMENSION_PANTALLA - DIMENSION_SPRITE, DIMENSION_SPRITE),
            random.randrange(DIMENSION_SPRITE, DIMENSION_PANTALLA - DIMENSION_SPRITE, DIMENSION_SPRITE)
        )    
    
    def clonar(self):
        comida = Comida()
        clone_x, clone_y = self.posicion
        comida.posicion = (clone_x, clone_y)
        return comida

    def mostrar(self):
        pygame.draw.rect(PANTALLA, COLORES["comida"], [*self.posicion, DIMENSION_SPRITE, DIMENSION_SPRITE])