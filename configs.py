import pygame

# ----- Configuraciones de Juego ----- #
DIMENSION_PANTALLA = 440
# dimension (en pixeles) cuadrada de la pantalla de juego
# dimension real: 440px - 20x20 sprites

# tamaño de cada sprite
DIMENSION_SPRITE = 20

# velocidad del juego (fps)
FPS = 20

# por el momento no se recomienda cambiar
DIMENSION_INICIAL_SERPIENTE = 3

# calcula el maximo de puntos que la serpiente puede alcanzar
DIMENSION_BORDE_AZUL = (DIMENSION_SPRITE * 2)
DIMENSION_FONDO_NEGRO = ((DIMENSION_PANTALLA - DIMENSION_BORDE_AZUL) // DIMENSION_SPRITE) 
PUNTOS_MAX = DIMENSION_FONDO_NEGRO ** 2 - DIMENSION_INICIAL_SERPIENTE

MOSTRAR_TODAS = False
MOSTRAR_EJES = True

# setea los posibles colores en rgb
COLORES = {
    "fondo_ventana": (13, 110, 103),
    "fondo_juego": (0, 0, 0),
    "bordes": (169, 173, 94),
    "texto": (158, 40, 40),

    "comida": (125, 27, 27),
    "cuerpo": (76, 158, 41),
    "muerta": (61, 128, 33),

    "ejes": (150, 150, 150),
    "encontro_comida": (94, 38, 38),
    "encontro_cuerpo": (83, 145, 144)
}

# los ejes se recorren en este orden:
# sup-izq, sup, sup-der, der, inf-der, inf, inf-izq, izq
AUMENTO_POSICIONES = [
    (-DIMENSION_SPRITE, -DIMENSION_SPRITE),
    (0, -DIMENSION_SPRITE),
    (DIMENSION_SPRITE, -DIMENSION_SPRITE),
    (DIMENSION_SPRITE, 0),
    (DIMENSION_SPRITE, DIMENSION_SPRITE),
    (0, DIMENSION_SPRITE),
    (-DIMENSION_SPRITE, DIMENSION_SPRITE),
    (-DIMENSION_SPRITE, 0)
]

AJUSTE_CABEZA = [
    (0, 0),
    (DIMENSION_SPRITE//2, 0),
    (DIMENSION_SPRITE, 0),
    (DIMENSION_SPRITE, DIMENSION_SPRITE//2),
    (DIMENSION_SPRITE, DIMENSION_SPRITE),
    (DIMENSION_SPRITE//2, DIMENSION_SPRITE),
    (0, DIMENSION_SPRITE),
    (0, DIMENSION_SPRITE//2)
]

AJUSTE_OBJETO = [
    (DIMENSION_SPRITE, DIMENSION_SPRITE),
    (DIMENSION_SPRITE//2, DIMENSION_SPRITE),
    (0, DIMENSION_SPRITE),
    (0, DIMENSION_SPRITE//2),
    (0, 0),
    (DIMENSION_SPRITE//2, 0),
    (DIMENSION_SPRITE, 0),
    (DIMENSION_SPRITE, DIMENSION_SPRITE//2)
]

# ----- Configuraciones de Algoritmo Genetico ----- #
POBLACION = 2000

# config mutacion:
# valores pueden estar entre [0.00, 1.00)
PROB_MUTACION = 0.05

# para infinitas generaciones usar numero menores a 0
NUMERO_GENERACIONES = -1

# ----- Configuraciones de la Red Neuronal ----- #
ARQUITECTURA_RED = {"num_entradas": 24, "arquitectura_capa_oculta": [18, 18]}
# entradas posibles
# distancia de la pared en 8 ejes
# vision binaria de la comida en 8 ejes
# vision binaria del cuerpo en 8 ejes

# ----- Inicia Pygame ----- #
pygame.init()

# setea la fuente y el tamaño del texto
FUENTE = pygame.font.Font('agencyfb-bold.ttf', 15)

# crea una pantalla con las dimensiones dadas
PANTALLA = pygame.display.set_mode([DIMENSION_PANTALLA, DIMENSION_PANTALLA + DIMENSION_SPRITE*5])