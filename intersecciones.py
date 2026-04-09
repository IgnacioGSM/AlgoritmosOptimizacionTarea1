import numpy as np

def interseccion(ecuacion1, ecuacion2):
    '''
    Calcula la interseccion de dos lineas usando la regla de Cramer.

    Parametros:
    ------------
    ecuacion1: tupla (a1, b1, c1), representa a1*x + b1*y = c1
    ecuacion2: tupla (a2, b2, c2), representa a2*x + b2*y = c2

    Retorna:
    ------------
    (x, y): punto de interseccion de las dos lineas, o None si las lineas son paralelas
    '''

    a1, b1, c1 = ecuacion1
    a2, b2, c2 = ecuacion2

    D = a1 * b2 - a2 * b1
    if D == 0:
        return None
    
    Dx = c1 * b2 - c2 * b1
    Dy = a1 * c2 - a2 * c1

    x = Dx / D
    y = Dy / D

    return (x, y)

def calcular_todas_intersecciones(ecuaciones: np.ndarray):
    '''
    Recorre todas las combinaciones de ecuaciones y calcula sus intersecciones.

    Parametros:
    ------------
    ecuaciones: np.ndarray de forma (n, 3), donde cada fila es una ecuacion de la forma ax + by = c 
                representada como (a, b, c)

    Retorna:
    ------------
    intersecciones: una lista de puntos (x, y) que son las intersecciones de todas las combinaciones de ecuaciones
    '''
    intersecciones = []
    for i in range(len(ecuaciones)):
        for j in range(i + 1, len(ecuaciones)):
            inter = interseccion(ecuaciones[i], ecuaciones[j])
            if inter is not None:
                intersecciones.append(inter)
    return intersecciones