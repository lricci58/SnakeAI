# OphidIA

Proyecto de IA hecho con python, el codigo esta en español.

## Instalacion

Debera tener python3 y el package manager [pip](https://pip.pypa.io/en/stable/) para instalar las librerias necesarias:
```bash
pip3 install -r requirements.txt
```

## Uso

Una vez instaladas las librerías, usted ya es libre de correr el programa y dejar que las serpientes aprendan.
Sin embargo, desde el archivo 'configs.py' se pueden realizar cambios, tanto visuales como funcionales, al codigo.

1. DIMENSION_PANTALLA: para cambiar el tamaño de la pantalla, teniendo en cuenta que los sprites son de 20x20 pixels, puede hacer los calculos del tamaño de pantalla que necesita, sin embargo, la pantalla siempre sera de un tamaño cuadrado (base = altura)
2. DIMENSION_SPRITE: esto indica el tamaño de cada bloque que se dibuja en el juego. Se recomienda no cambiar
3. MOSTRAR_TODAS: este es un booleano que, al estar activado, permite mostrar TODAS las serpientes que juegan a la vez (en vez de solo la mejor)
4. MOSTRAR_EJES: las serpientes cuentan con ejes por donde detectan la comida, usted puede activar o desactivar esta funcion para poder o no verlos
5. COLORES: este es un array asociativo con colores en formato rgb, usted puede cambiar estos colores para darle su propio toque visual
6. POBLACION: este valor indica cuantas serpientes juegan en cada generacion
7. PROB_MUTACION: esta constante permite valores entre [0, 1) representando porcentajes de probabilidad de que muten los genes de una serpiente hija al ser creada
8. NUMERO_GENERACIONES: este valor declara cuantas generaciones de serpientes van a jugar hasta que termine el programa (para generaciones infinitas usar -1)
9. ARQUITECTURA_RED: este es un array asociativo que contiene el numero de entradas (no tocar), y el numero de nodos en cada capa oculta

## Guardar y cargar serpientes

El programa trae la posibilidad de guardar y cargar serpientes cuando se necesite.
Durante la ejecucion del programa:
- apretar la tecla 'g' para guardar la generacion actual de serpientes que esta jugando (deberá esperar a que terminen  de jugar todas para que se guarde)
- apretar la tecla 'c' para cargar alguna generacion guardada (al hacer esto, la generacion que esta jugando en el momento, dejará de hacerlo para cargar la nueva)

## Especificaciones

El programa esta hecho con el lenguaje python. La librería usada para la parte gráfica es pygame.
Dentro de la carpeta del programa se encuentra otra con el nombre de 'grafico' donde se puede encontrar un grafico del avance de las serpientes en cada generacion.

## Estado del proyecto

El proyecto no es completamente mio, formo parte de un grupo con el que se creo este programa. 
El proyecto final puede estar sujeto a cambios, sin embargo, este repositorio no se actualizará con esos cambios.
El link al repositorio donde se mantendrá el proyecto final: [gitlab](https://gitlab.com/pablo30/openroxy/-/tree/neural-network/OphidIA/SnakeGame)