import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from intersecciones import calcular_todas_intersecciones, calcular_intersecciones_factibles
from marchaJarvis import marcha_jarvis
from graficacion import plot_lines, plot_intersections, plot_hull
import config


class EquationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Región Factible")
        self.root.geometry("1200x700")

        self.ecuaciones = []
        self.equation_rows = []
        self._setup_styles()
        self._create_widgets()
        self._add_default_equations()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('Remove.TButton', foreground='red')

    def _create_widgets(self):
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(main_paned, width=400)
        main_paned.add(control_frame, weight=0)

        canvas_frame = ttk.Frame(main_paned)
        main_paned.add(canvas_frame, weight=1)

        self._create_control_panel(control_frame)
        self._create_canvas(canvas_frame)

    def _create_control_panel(self, parent):
        header = ttk.Label(parent, text="Restricciones: ax + by ≤ c  o  ax + by ≥ c", font=('Arial', 12, 'bold'))
        header.pack(pady=10)

        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        canvas = tk.Canvas(list_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.equations_container = ttk.Frame(canvas)

        self.equations_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.equations_container, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(button_frame, text="Agregar Ecuacion", command=self._add_equation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar Grafico", command=self._update_plot).pack(side=tk.LEFT, padx=5)

        self.status_label = ttk.Label(parent, text="", font=('Arial', 9))
        self.status_label.pack(pady=5)

    def _create_canvas(self, parent):
        self.fig = Figure(figsize=(8, 7), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _add_default_equations(self):
        default_equations = [
            [1, 0, 0, '>='],
            [0, 1, 0, '>='],
            [1, 1, 2, '<='],
        ]
        for eq in default_equations:
            self._add_equation_row(eq)

    def _add_equation_row(self, values=None):
        row_idx = len(self.equation_rows)

        if values is None:
            values = [1, 1, 2, '<=']

        row_frame = ttk.Frame(self.equations_container)
        row_frame.pack(fill=tk.X, pady=2, padx=5)

        label = ttk.Label(row_frame, text=f"{row_idx + 1}:", width=3)
        label.pack(side=tk.LEFT, padx=1)

        entries = {}
        for key, val in zip(['a', 'b', 'c'], values[:3]):
            ttk.Label(row_frame, text=f"{key}:", width=2).pack(side=tk.LEFT)
            entries[key] = tk.StringVar(value=str(val))
            entry = ttk.Entry(row_frame, textvariable=entries[key], width=5)
            entry.pack(side=tk.LEFT, padx=1)

        inequality_var = tk.StringVar(value=values[3])
        inequality_combo = ttk.Combobox(
            row_frame, textvariable=inequality_var, 
            values=['<=', '>='], width=3, state='readonly'
        )
        inequality_combo.pack(side=tk.LEFT, padx=1)
        entries['inequality'] = inequality_var

        ttk.Button(
            row_frame, text="X", style='Remove.TButton', width=2,
            command=lambda: self._remove_equation(row_idx)
        ).pack(side=tk.LEFT, padx=2)

        self.equation_rows.append({
            'frame': row_frame,
            'entries': entries,
            'idx': row_idx
        })

    def _add_equation(self):
        self._add_equation_row()

    def _remove_equation(self, idx):
        for row in self.equation_rows:
            if row['idx'] == idx:
                row['frame'].destroy()
                self.equation_rows.remove(row)
                break
        self._reindex_rows()

    def _reindex_rows(self):
        for i, row in enumerate(self.equation_rows):
            row['idx'] = i

    def _get_equations(self):
        ecuaciones = []
        for row in self.equation_rows:
            try:
                a = float(row['entries']['a'].get())
                b = float(row['entries']['b'].get())
                c = float(row['entries']['c'].get())
                inequality = row['entries']['inequality'].get()
                ecuaciones.append([a, b, c, inequality])
            except ValueError:
                pass
        return np.array(ecuaciones) if ecuaciones else np.array([])

    def _calculate_limits(self, intersecciones):
        if not intersecciones:
            return -10, 10, -10, 10
        xs = [p[0] for p in intersecciones]
        ys = [p[1] for p in intersecciones]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
        padding = config.PADDING
        return minx - padding, maxx + padding, miny - padding, maxy + padding

    def _update_plot(self):
        ecuaciones = self._get_equations()

        if ecuaciones.size == 0:
            self.status_label.config(text="No hay ecuaciones validas")
            return

        intersecciones_factibles = calcular_intersecciones_factibles(ecuaciones)
        intersecciones_todas = calcular_todas_intersecciones(ecuaciones)
        envoltura = marcha_jarvis(intersecciones_factibles)
        
        minx, maxx, miny, maxy = self._calculate_limits(intersecciones_factibles if intersecciones_factibles else intersecciones_todas)

        self.ax.clear()

        plot_lines(self.ax, ecuaciones, minx, maxx, miny, maxy)
        plot_intersections(self.ax, intersecciones_factibles)
        plot_hull(self.ax, envoltura)

        self.ax.set_xlim(minx, maxx)
        self.ax.set_ylim(miny, maxy)
        self.ax.axhline(0, color=config.COLORS['axes'], lw=config.AXES_LINEWIDTH, ls=config.AXES_LINESTYLE)
        self.ax.axvline(0, color=config.COLORS['axes'], lw=config.AXES_LINEWIDTH, ls=config.AXES_LINESTYLE)
        self.ax.grid(True, color=config.COLORS['grid'], alpha=config.GRID_ALPHA)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title(config.TITLE)
        self.ax.legend(loc='upper right', fontsize=8)

        self.fig.tight_layout()
        self.canvas.draw()

        self.status_label.config(text=f"Intersecciones factibles: {len(intersecciones_factibles)}, Restricciones: {len(ecuaciones)}")


def main():
    root = tk.Tk()
    app = EquationGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
