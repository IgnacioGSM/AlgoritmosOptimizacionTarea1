import numpy as np

def orientacion(a, b, c):  #a, b y c son puntos (x,y)
    # (bx - ax)(cy - ay) - (by - ay)(cx - ax)
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    # > 0: c es a la izquierda de ab
    # < 0: c es a la derecha de ab
    # = 0: a, b y c son colineales

def distancia(a, b):
    return np.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2) # pitagoras

def marcha_jarvis(puntos:list):
    # solo funciona con 3 o mas puntos
    if len(puntos) < 3:
        return None
    
    punto_inicio = min(puntos, key=lambda p: (p[0], p[1]))  # punto con menor x y en caso de empate, menor y

    envoltura = []
    actual = punto_inicio
    while True:
        envoltura.append(actual)

        # se elige un candidato distinto al punto actual
        candidato = puntos[0] if puntos[0] != actual else puntos[1]

        for p in puntos:
            if p == actual:
                continue
            o = orientacion(actual, candidato, p)
            if o > 0:  # p es más a la izquierda que candidato (sentido antihorario)
                candidato = p
            elif o == 0:  # p es colineal con actual y candidato
                if distancia(actual, p) > distancia(actual, candidato):
                    candidato = p
        
        actual = candidato

        if actual == punto_inicio:  # termina cuando se vuelve al punto de inicio
            break
    
    envoltura.append(punto_inicio)  # de nuevo el punto de inicio para cerrar la envoltura
    
    return envoltura