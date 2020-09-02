import numpy as np

def crossover_binario_en_un_punto(cromosomas_prog1, cromosomas_prog2):
    # se crea un array del mismo tamaño que el de los padres
    cromosomas_hijo = cromosomas_prog1.copy()

    # se elije un punto random divisorio para las filas y columnas
    punto_fila, punto_col = np.random.randint(0, cromosomas_prog1.shape)
    
    # se dividen las filas en la posicion elegida, obteniendo una tupla formada por las filas de un progenitor y las filas del otro
    nuevas_filas = (cromosomas_prog1[:punto_fila, :], cromosomas_prog2[punto_fila:, :])
    # despues se dividen las columnas
    nuevas_cols = (cromosomas_prog1[:, :punto_col], cromosomas_prog2[:, punto_col:])
    
    # se combinan las filas de cada progenitor
    cromosomas_hijo = np.vstack(nuevas_filas)
    # se combinan las columnas
    cromosomas_hijo = np.hstack(nuevas_cols)

    return cromosomas_hijo