import matplotlib.pyplot as plt
import numpy as np

def graficar_lineas(ecuaciones, minx, maxx, miny, maxy):
    x = np.linspace(minx, maxx, 100)
    for ecuacion in ecuaciones:
        a, b, c = ecuacion      # b no deberia ser 0, pero si lo es, se puede manejar como caso especial
        if b == 0:            # Ecuacion vertical ax = c
            x = np.full_like(x, c / a)
            y = np.linspace(miny, maxy, 100)
            plt.plot(x, y, label=f'{a}x + {b}y = {c}')
        else:
            y = (c - a * x) / b
            plt.plot(x, y, label=f'{a}x + {b}y = {c}')

def graficar_intersecciones(intersecciones):
    for inter in intersecciones:
        plt.plot(inter[0], inter[1], 'ro')

def graficar_envoltura(envoltura_convexa):
    if envoltura_convexa:
        envoltura_x = [p[0] for p in envoltura_convexa]
        envoltura_y = [p[1] for p in envoltura_convexa]
        plt.plot(envoltura_x, envoltura_y, 'b-', linewidth=2)

def graficar(ecuaciones, minx, maxx, miny, maxy, intersecciones=None, envoltura_convexa=None):
    graficar_lineas(ecuaciones, minx, maxx, miny, maxy)

    if intersecciones is not None:
        graficar_intersecciones(intersecciones)

    if envoltura_convexa is not None:
        graficar_envoltura(envoltura_convexa)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(minx, maxx)
    plt.ylim(miny, maxy)
    plt.axhline(0, color='black', lw=1, ls='--')
    plt.axvline(0, color='black', lw=1, ls='--')
    plt.title('Intersecciones de ecuaciones lineales')
    plt.legend()
    plt.show()