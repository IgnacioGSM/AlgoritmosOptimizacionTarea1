import numpy as np

def orientacion(a, b, c):
    '''
    Calcula la orientación de tres puntos a, b, c en el plano (x, y) usando determinante.

    vector AB = (bx - ax, by - ay), 
    vector AC = (cx - ax, cy - ay), 
    se calcula el determinante de la matriz formada por los vectores AB y AC:

     | ABx ACx |
     | ABy ACy |

    Parametros:
    ------------
    a, b, c: tuplas (x, y) que representan puntos en el plano

    Retorna:
    ------------
    mayor que 0 si los puntos a, b, c están en sentido horario

    menor que 0 si los puntos a, b, c están en sentido antihorario

    igual a 0 si los puntos a, b, c son colineales

    '''
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def distancia(a, b):
    '''
    Parametros:
    ------------
    a, b: tuplas (x, y) que representan puntos en el plano

    Retorna:
    ------------
    La distancia euclidiana entre los puntos a y b
    '''
    return np.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

def marcha_jarvis(puntos:list):
    '''
    Algoritmo de Marcha de Jarvis (Gift Wrapping) para encontrar la envoltura convexa de un conjunto de puntos en el plano (x, y).

    Complejidad: O(n * h), donde n es el número de puntos y h es el número de puntos en la envoltura convexa.

    Parametros:
    ------------
    puntos: una lista de tuplas (x, y) que representan puntos en el plano

    Retorna:
    ------------
    Una lista de puntos que forman la envoltura convexa de los puntos
    
    Si hay menos de 3 puntos, retorna None
    '''
    
    if len(puntos) < 3:
        return None
    
    punto_inicio = min(puntos, key=lambda p: (p[0], p[1]))

    envoltura = []
    actual = punto_inicio
    while True:
        envoltura.append(actual)

        candidato = puntos[0] if puntos[0] != actual else puntos[1]

        for p in puntos:
            if p == actual:
                continue
            o = orientacion(actual, candidato, p)
            if o > 0:
                candidato = p
            elif o == 0:  
                if distancia(actual, p) > distancia(actual, candidato):
                    candidato = p
        
        actual = candidato

        if actual == punto_inicio:
            break
    
    envoltura.append(punto_inicio)
    
    return envoltura