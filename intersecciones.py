import numpy as np

# Entrada: dos ecuaciones de la forma ax + by = c, representadas como tuplas (a, b, c)
# Salida: un punto (x, y) que es la intersección de las dos líneas, o None si las líneas son paralelas
# Se utiliza la regla de Cramer para resolver el sistema de ecuaciones
def interseccion(ecuacion1, ecuacion2):
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

# Entrada: Matriz de ecuaciones, donde cada fila es una ecuación de la forma ax + by = c representada como (a, b, c)
# Salida: una lista de puntos (x, y) que son las intersecciones de todas las combinaciones de ecuaciones
def calcular_todas_intersecciones(ecuaciones: np.ndarray):
    intersecciones = []
    for i in range(len(ecuaciones)):
        for j in range(i + 1, len(ecuaciones)):
            inter = interseccion(ecuaciones[i], ecuaciones[j])
            if inter is not None:
                intersecciones.append(inter)
    return intersecciones