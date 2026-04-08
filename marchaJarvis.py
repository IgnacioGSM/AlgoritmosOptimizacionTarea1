import numpy as np

# Entrada: tres puntos (a, b, c) en el plano (x, y)
# Salida: un valor que indica la orientación de los puntos
# Mediante el producto cruz de los vectores ab y ac se puede determinar la orientación de los puntos:
# - Si el resultado es positivo, entonces c está a la izquierda de ab (sentido antihorario).
# - Si el resultado es negativo, entonces c está a la derecha de ab (sentido horario).
# - Si el resultado es cero, entonces a, b y c son colineales
def orientacion(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

# Entrada: dos puntos (a, b) en el plano (x, y)
# Salida: la distancia euclidiana entre los puntos a y b
def distancia(a, b):
    return np.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

# Entrada: una lista de puntos en el plano (x, y)
# Salida: una lista de puntos que forman la envoltura convexa de los puntos
# O(n * h), n = número de puntos, h = número de puntos en la envoltura convexa
# Elige el punto mas a la izquierda, el siguiente punto es el que este mas a la izquierda en relacion al punto actual
def marcha_jarvis(puntos:list):
    
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