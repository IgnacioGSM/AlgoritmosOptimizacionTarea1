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

    a1, b1, c1 = float(ecuacion1[0]), float(ecuacion1[1]), float(ecuacion1[2])
    a2, b2, c2 = float(ecuacion2[0]), float(ecuacion2[1]), float(ecuacion2[2])

    D = a1 * b2 - a2 * b1
    if D == 0:
        return None
    
    Dx = c1 * b2 - c2 * b1
    Dy = a1 * c2 - a2 * c1

    x = Dx / D
    y = Dy / D

    return (x, y)

def evaluar_restriccion(a, b, c, inequality, x, y):
    '''
    Evalua si un punto (x, y) satisface una restriccion.

    Parametros:
    ------------
    a, b, c: coeficientes de la restriccion ax + by = c (desigualdad)
    inequality: '<=' o '>='
    x, y: coordenadas del punto

    Retorna:
    ------------
    True si el punto satisface la restriccion, False en caso contrario
    '''
    a, b, c = float(a), float(b), float(c)
    x, y = float(x), float(y)
    valor = a * x + b * y
    if inequality == '<=':
        return valor <= c + 1e-9
    else:
        return valor >= c - 1e-9

def es_punto_factible(punto, ecuaciones):
    '''
    Verifica si un punto satisface todas las restricciones.

    Parametros:
    ------------
    punto: tupla (x, y)
    ecuaciones: np.ndarray de forma (n, 4), donde cada fila es (a, b, c, inequality)
                inequality es '<=' o '>='

    Retorna:
    ------------
    True si el punto es factible, False en caso contrario
    '''
    x, y = float(punto[0]), float(punto[1])
    
    for eq in ecuaciones:
        a, b, c, inequality = float(eq[0]), float(eq[1]), float(eq[2]), eq[3]
        if not evaluar_restriccion(a, b, c, inequality, x, y):
            return False
    return True

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

def calcular_intersecciones_factibles(ecuaciones: np.ndarray):
    '''
    Calcula las intersecciones que son parte de la region factible.

    Parametros:
    ------------
    ecuaciones: np.ndarray de forma (n, 4), donde cada fila es (a, b, c, inequality)
                inequality es '<=' o '>='

    Retorna:
    ------------
    intersecciones_factibles: lista de puntos (x, y) que son validos para todas las restricciones
    '''
    restricciones = []
    for eq in ecuaciones:
        a, b, c, inequality = eq
        restricciones.append((a, b, c, inequality))
    
    #restricciones.extend([
    #    (1, 0, 0, '>='),
    #    (0, 1, 0, '>=')
    #])
    
    restricciones = np.array(restricciones, dtype=object)

    
    intersecciones = []
    for i in range(len(restricciones)):
        for j in range(i + 1, len(restricciones)):
            inter = interseccion(restricciones[i], restricciones[j])
            if inter is not None and es_punto_factible(inter, restricciones):
                intersecciones.append(inter)
    
    return intersecciones

def encontrar_punto_optimo(intersecciones_factibles, cx, cy, maximizar=True):
    '''
    Encuentra el punto optimo de la region factible evaluando la funcion objetivo.

    Parametros:
    ------------
    intersecciones_factibles: lista de puntos (x, y) que son las intersecciones factibles
    cx, cy: coeficientes de la funcion objetivo Z = cx*x + cy*y
    maximizar: True para maximizar, False para minimizar

    Retorna:
    ------------
    punto_optimo: tuple (x, y) con el valor optimo
    '''
    mejor_valor = -float('inf') if maximizar else float('inf')
    punto_optimo = None

    for punto in intersecciones_factibles:
        x, y = float(punto[0]), float(punto[1])
        valor = cx * x + cy * y

        if maximizar:
            if valor > mejor_valor:
                mejor_valor = valor
                punto_optimo = punto
        else:
            if valor < mejor_valor:
                mejor_valor = valor
                punto_optimo = punto

    return punto_optimo