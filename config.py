COLORS = {
    'line': ['#1f77b4',
             '#ff7f0e', 
             '#2ca02c', 
             '#d62728', 
             '#9467bd', 
             '#8c564b', 
             '#e377c2', 
             '#7f7f7f', 
             '#bcbd22', 
             '#17becf'],
    'intersection_point': 'black',
    'convex_hull': 'red',
    'optimal_point': 'gold',
    'axes': 'black',
    'grid': '#cccccc',
}

LINE_WIDTH = 1
MARKER_SIZE = 8
PADDING = 1
GRID_ALPHA = 0.3
HULL_ALPHA = 0.3
AXES_LINEWIDTH = 1.5
AXES_LINESTYLE = '--'
TITLE = 'Region Factible'

DEFAULT_EQUATIONS = [
    [1, 0, 0, '>='],
    [0, 1, 0, '>='],
    [1, 1, 2, '<='],
]