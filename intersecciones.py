import numpy as np

# Calculo del sistema de ecuaciones usando determinantes (Regla de Cramer)
def interseccion(ecuacion1, ecuacion2):     # Ecuaciones formato [a b c] representa ax + by = c
    a1, b1, c1 = ecuacion1
    a2, b2, c2 = ecuacion2

    D = a1 * b2 - a2 * b1
    if D == 0:
        return None  # No hay solución o infinitas soluciones
    
    Dx = c1 * b2 - c2 * b1
    Dy = a1 * c2 - a2 * c1

    x = Dx / D
    y = Dy / D

    return (x, y)

def calcular_todas_intersecciones(ecuaciones: np.ndarray):  # recibe la matriz de ecuaciones
    intersecciones = []
    for i in range(len(ecuaciones)):
        for j in range(i + 1, len(ecuaciones)):
            inter = interseccion(ecuaciones[i], ecuaciones[j])
            if inter is not None:
                intersecciones.append(inter)
    return intersecciones