import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Configura el backend de Matplotlib para Tkinter (salia error FigureCanvasAgg is non-interactive)
import matplotlib.pyplot as plt
from intersecciones import calcular_todas_intersecciones
from graficacion import graficar
from marchaJarvis import marcha_jarvis

# Matriz de ecuaciones lineales, fila en formato [a b c] representa ax + by = c
num_ecuaciones = 5
ecuaciones = np.random.randint(-10, 10, (num_ecuaciones, 3))


intersecciones = calcular_todas_intersecciones(ecuaciones)

# para la visualizacion, limites del grafico
minx, maxx = 0, 0
miny, maxy = 0, 0

for inter in intersecciones:
    x, y = inter
    minx = min(minx, x)
    maxx = max(maxx, x)
    miny = min(miny, y)
    maxy = max(maxy, y)

# ajuste de limites para mejor visualizacion
padding = 1
minx -= padding
maxx += padding
miny -= padding
maxy += padding


print("Limites del gráfico: x=[{:.2f}, {:.2f}], y=[{:.2f}, {:.2f}]".format(minx, maxx, miny, maxy))

envoltura_convexa = marcha_jarvis(intersecciones)

# Graficar las ecuaciones, intersecciones y el envoltorio convexo de las intersecciones
graficar(ecuaciones, minx, maxx, miny, maxy, intersecciones=intersecciones, envoltura_convexa=envoltura_convexa)