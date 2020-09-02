import numpy as np  
import matplotlib.pyplot as plt
import os

# importa configuraciones de juego
from configs import DIMENSION_PANTALLA, DIMENSION_SPRITE, DIMENSION_BORDE_AZUL, DIMENSION_FONDO_NEGRO, FPS, MOSTRAR_EJES, COLORES, PUNTOS_MAX
# importa configuraciones del algoritmo genetico y la red neuronal
from configs import NUMERO_GENERACIONES, POBLACION, PROB_MUTACION, ARQUITECTURA_RED

from configs import PANTALLA, FUENTE, pygame

from poblacion import Poblacion

class Juego():

    def __init__(self): 
        # titulo de ventana
        pygame.display.set_caption("OphidIA")

        # para manejar los fps
        self.framerate = pygame.time.Clock()

        pygame.display.update()
        self.framerate.tick(FPS)

        self.cargar_generacion = False
        self.guardar_generacion = False

        self.lista_generaciones = []
        self.lista_puntajes = []

    def actualizar_dibujos(self):
        pygame.display.update()
        self.framerate.tick(FPS)

    def actualizar_pantalla(self):
        dimension_bordes = [0, 0, DIMENSION_PANTALLA, DIMENSION_PANTALLA]
        # pinta el fondo negro (mas chiquito) sobre el azul
        pygame.draw.rect(PANTALLA, COLORES["bordes"], dimension_bordes)

        dimension_fondo_negro = [
            DIMENSION_SPRITE, DIMENSION_SPRITE, 
            DIMENSION_PANTALLA - DIMENSION_SPRITE*2, DIMENSION_PANTALLA - DIMENSION_SPRITE*2
        ]
        # pinta el fondo negro (mas chiquito) sobre el azul
        pygame.draw.rect(PANTALLA, COLORES["fondo_juego"], dimension_fondo_negro)

        # dibuja el texto del tamaño de la pantalla de juego
        texto_dim_pantalla = f"{DIMENSION_FONDO_NEGRO}x{DIMENSION_FONDO_NEGRO}"
        texto_render = FUENTE.render(texto_dim_pantalla, True, (0, 0, 0))
        posicion_texto = texto_render.get_rect()
        posicion_texto.x = DIMENSION_SPRITE
        posicion_texto.y = 0
        PANTALLA.blit(texto_render, posicion_texto)

        if self.guardar_generacion:
            texto_estado_generacion = "Guardando generacion..."

        if self.cargar_generacion:
            texto_estado_generacion = "Cargando generacion..."

        if self.guardar_generacion or self.cargar_generacion:
            texto_render = FUENTE.render(texto_estado_generacion, True, (0, 0, 0))
            posicion_texto = texto_render.get_rect()
            posicion_texto.x = DIMENSION_SPRITE
            posicion_texto.y = DIMENSION_PANTALLA - DIMENSION_SPRITE
            PANTALLA.blit(texto_render, posicion_texto)

    def actualizar_datos(self, num_generacion = None, mejor_puntaje = None, puntaje = 3):
        if num_generacion != None:
            pygame.draw.rect(PANTALLA, COLORES["fondo_juego"], [DIMENSION_SPRITE, DIMENSION_PANTALLA + DIMENSION_SPRITE, DIMENSION_PANTALLA - DIMENSION_SPRITE*2, DIMENSION_SPRITE*2])
            texto_num_generacion = f"Generación Nº[{num_generacion}]"
            num_gen_render = FUENTE.render(texto_num_generacion, True, COLORES["texto"])
            posision_num_gen = num_gen_render.get_rect()

            posision_num_gen.x = DIMENSION_SPRITE
            posision_num_gen.y = DIMENSION_PANTALLA + DIMENSION_SPRITE
            PANTALLA.blit(num_gen_render, posision_num_gen)

        if mejor_puntaje != None:
            texto_puntaje_alto = f"Mejor Puntaje: {mejor_puntaje}"
            puntaje_alto_render= FUENTE.render(texto_puntaje_alto, True, COLORES["texto"])
            posision_puntaje_alto = puntaje_alto_render.get_rect()

            posision_puntaje_alto.x =  DIMENSION_SPRITE
            posision_puntaje_alto.y = DIMENSION_PANTALLA + DIMENSION_SPRITE*2
            PANTALLA.blit(puntaje_alto_render, posision_puntaje_alto)
        
        pygame.draw.rect(PANTALLA, COLORES["fondo_juego"], [DIMENSION_SPRITE, DIMENSION_PANTALLA + DIMENSION_SPRITE*3, DIMENSION_PANTALLA - DIMENSION_SPRITE*2, DIMENSION_SPRITE])
        
        texto_puntaje = f"Puntaje: {puntaje}"
        puntaje_actual_render = FUENTE.render(texto_puntaje, True, COLORES["texto"])
        posision_puntaje_actual = puntaje_actual_render.get_rect()

        posision_puntaje_actual.x =  DIMENSION_SPRITE
        posision_puntaje_actual.y = DIMENSION_PANTALLA + DIMENSION_SPRITE*3
        PANTALLA.blit(puntaje_actual_render, posision_puntaje_actual)

    def actualizar_grafico(self, numero_generacion = 0, puntaje = 0):
        # listas para cada eje
        self.lista_generaciones.append(numero_generacion)
        self.lista_puntajes.append(puntaje)

        # el eje_X tiene las generaciones, y el eje_Y tiene los puntajes
        plt.plot(self.lista_generaciones, self.lista_puntajes, color="#27823f", marker=".")
                            
        # titulo del grafico y nombre de cada eje
        plt.title("Mejor Puntaje de Cada Generacion")
        plt.xlabel("Número de Generación")
        plt.ylabel("Mejor Puntaje")

        # dibuja una grilla
        plt.grid(True)

        try:
            # guarda el grafico en una imagen
            plt.savefig(f"grafico/datos_generacion.png")
        except FileNotFoundError:
            os.makedirs("grafico")
            plt.savefig(f"grafico/datos_generacion.png")

        # plt.show()
        plt.close()

        # # obtiene el directorio de la imagen
        # dir_imagen = str(os.path.dirname(os.path.abspath(__file__))) + r"\grafico\datos_generacion.png"
        # # carga la imagen a pygame desde el directorio
        # imagen = pygame.image.load(dir_imagen)

        # # reescala la imagen
        # imagen = pygame.transform.scale(imagen, (DIMENSION_PANTALLA * 2, DIMENSION_PANTALLA))

        # # posiciona la imagen
        # posicion_imagen = imagen.get_rect()
        # posicion_imagen.x = 0
        # posicion_imagen.y = DIMENSION_PANTALLA

        # PANTALLA.blit(imagen, posicion_imagen)

    def escuchar_evento_teclado(self):
        for event in pygame.event.get():
            # detecta si se apreta el boton de cerrar ventana
            if event.type == pygame.QUIT:
                # cierra la ventana pygame
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.cargar_generacion = True
                    break
                elif event.key == pygame.K_g:
                    self.guardar_generacion = True
                    break

def guardar_genes(generacion_entera):
    dir_archivo = str(os.path.dirname(os.path.abspath(__file__))) + r"\informacion_genetica\mejor_generacion.txt" 

    try:
        # intenta abrir el archivo en modo escritura
        archivo_genes = open(dir_archivo, "w")
    except FileNotFoundError:
        print("No se encontro el archivo o la carpeta! Creando carpeta si no existe...")
        os.makedirs("informacion_genetica")
        archivo_genes = open(dir_archivo, "w")

    for serpiente in generacion_entera:
        cromosomas = serpiente.cerebro.get_cromosomas()
        longitud_red = serpiente.cerebro.get_dimension_red()
        for n in range(1, longitud_red):
            for lista_genes in cromosomas[f"P{n}"]:
                # mete cada linea de pesos dentro del archivo
                archivo_genes.write(";".join(str(linea) for linea in lista_genes) + "\n")

    archivo_genes.close()

def cargar_genes(generacion_entera):
    dir_archivo = str(os.path.dirname(os.path.abspath(__file__))) + r"\informacion_genetica\mejor_generacion.txt"  

    try:
        # intenta abrir el archivo en modo lectura
        archivo_genes = open(dir_archivo, "r")
    except IOError:
        print("El archivo no existe! Debera activar el modo entrenamiento y esperar a que juegue al menos una generacion")
                
    lineas = archivo_genes.readlines()
    linea = 0

    for serpiente in generacion_entera:
        cerebro = serpiente.cerebro
        longitud_red = cerebro.get_dimension_red()
        for n in range(1, longitud_red):

            matriz_genes = np.empty(cerebro.get_cromosomas()[f"P{n}"].shape)
            for i in range(len(cerebro.get_cromosomas()[f"P{n}"])):
                # obtiene todos los valores de la linea en forma de lista float
                lista_valores = [float(valor) for valor in lineas[linea].split(";")]
                matriz_genes[i] = lista_valores
                linea += 1
            # le pasa la matriz formada a la serpiente
            cerebro.set_cromosomas_por_parametro(matriz_genes, f"P{n}")

    archivo_genes.close()

def alcanzo_limite_generaciones(numero_generacion):
    if NUMERO_GENERACIONES < 0:
        return False
    
    if numero_generacion > NUMERO_GENERACIONES:
        return True
    return False

juego = Juego()
poblacion = Poblacion(POBLACION)

# se setean los datos iniciales
juego.actualizar_datos(num_generacion=0, mejor_puntaje=3)

while not alcanzo_limite_generaciones(poblacion.generacion):
    juego.escuchar_evento_teclado()
    
    juego.actualizar_pantalla()

    if poblacion.termino_de_jugar() or juego.cargar_generacion:
        if juego.cargar_generacion:
            poblacion = Poblacion(POBLACION)

            # se cargan los genes guardados a la poblacion
            cargar_genes(poblacion.poblacion)
            juego.cargar_generacion = False
        else:
            poblacion.calcular_fitness()
            poblacion.seleccion_natural()

        num_generacion = poblacion.generacion
        mejor_puntaje = poblacion.mejor_puntaje
        
        juego.actualizar_datos(num_generacion, mejor_puntaje)
        juego.actualizar_grafico(num_generacion, mejor_puntaje)

        if juego.guardar_generacion:
            # una vez que juega la generacion, se guardan sus pesos
            guardar_genes(poblacion.poblacion)
            juego.guardar_generacion = False
    else:
        poblacion.mostrar()
        poblacion.actualizar()

    puntaje = poblacion.mejor_serpiente.puntaje

    juego.actualizar_datos(puntaje=puntaje)
    juego.actualizar_dibujos()