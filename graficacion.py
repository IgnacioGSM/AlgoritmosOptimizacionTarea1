import numpy as np
import matplotlib.pyplot as plt
import config


def _get_style():
    return {
        'line_color': config.COLORS['line'],
        'point_color': config.COLORS['intersection_point'],
        'hull_color': config.COLORS['convex_hull'],
        'axes_color': config.COLORS['axes'],
        'grid_color': config.COLORS['grid'],
        'line_width': config.LINE_WIDTH,
        'marker_size': config.MARKER_SIZE,
    }


def plot_lines(ax, ecuaciones, minx, maxx, miny, maxy, style=None):
    if style is None:
        style = _get_style()
    x = np.linspace(minx, maxx, 100)
    i = 0
    for i, ecuacion in enumerate(ecuaciones):
        color = style['line_color'][i % len(style['line_color'])]
        a, b, c = float(ecuacion[0]), float(ecuacion[1]), float(ecuacion[2])
        inequality = str(ecuacion[3]) if len(ecuacion) > 3 else '<='
        symbol = '≤' if inequality == '<=' else '≥'
        
        if b == 0:
            x_vert = np.full_like(x, c / a)
            y = np.linspace(miny, maxy, 100)
            ax.plot(x_vert, y, color=color, linewidth=style['line_width'], label=f'{a}x + {b}y {symbol} {c}')
        else:
            y = (c - a * x) / b
            ax.plot(x, y, color=color, linewidth=style['line_width'], label=f'{a}x + {b}y {symbol} {c}')


def plot_intersections(ax, intersecciones, style=None):
    if style is None:
        style = _get_style()
    for inter in intersecciones:
        ax.plot(inter[0], inter[1], 'o', color=style['point_color'], markersize=style['marker_size'])


def plot_hull(ax, envoltura_convexa, style=None):
    if style is None:
        style = _get_style()
    if envoltura_convexa:
        envoltura_x = [p[0] for p in envoltura_convexa]
        envoltura_y = [p[1] for p in envoltura_convexa]
        ax.fill(envoltura_x, envoltura_y, color=style['hull_color'], alpha=config.HULL_ALPHA)
        ax.plot(envoltura_x, envoltura_y, '-', color=style['hull_color'], linewidth=style['line_width'])


def plot_optimal_point(ax, punto, cx, cy, style=None):
    if style is None:
        style = _get_style()
    ax.plot(punto[0], punto[1], '*', color=config.COLORS['optimal_point'], markersize=config.MARKER_SIZE * 2, label=f'Punto Optimo: {punto} \n Valor: ${punto[0] * cx + punto[1] * cy:.2f}')
