
import matplotlib.pyplot as plt

from .plot import PltClass
from . import plot
from . import ticker
from . import grid
from . import geo

def summary(df, traj, axes=None, projection=geo.default_projection, temp_prop={}, psal_prop={}, ts_prop={}, map_prop={}):
    '''
    Produce a figure with 4 axes - the first, temperature profiles, second,
    salinity profiles, third a TS diagram, and fourth a map. Axes can be
    provided as a list for customization.

    Args:
        df (pandas.DataFrame): dataframe contianing Argo data and using Argo
        naming conventions.
    Keyword Args:
        axes (list or 1D array): list of axes to plot on, defaults to gridspec
        format if not provided.
    Returns:
        argoplot.PltClass: argoplot object with fig and axes attributes
    '''

    if axes is None:
        g = grid.gridder('summary', projection=projection)
    else:
        g = PltClass(plt.gcf(), axes)
    
    # first plot, temperature
    plot.profile(x='TEMP', y='PRES', hue='file', data=df, legend=True, ax=g.axes[0], **temp_prop)
    # second plot, salinity
    plot.profile(x='PSAL', y='PRES', hue='file', data=df, ax=g.axes[1], ax_prop=dict(yticklabels=[], ylabel=''),  **psal_prop)
    # third plot, TS diagram
    plot.ts_diagram(df, hue='file', xticks='top', yticks='right', contour_labels='lowerleft', ax=g.axes[2], **ts_prop)
    ticker.arrange(g.axes[2], 'upperright')
    # fourth plot, float map
    geo.trajectory(traj, ax=g.axes[3], **map_prop)

    return g