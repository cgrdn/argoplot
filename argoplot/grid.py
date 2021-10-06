
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from .plot import PltClass
from . import geo

def gridder(grid_name, **kwargs):

    if grid_name == 'summary':

        projection = kwargs.pop('projection')

        fig  = plt.figure()
        gs   = GridSpec(2, 3)
        axes = [
            fig.add_subplot(gs[:,0]),
            fig.add_subplot(gs[:,1]),
            fig.add_subplot(gs[0,2]),
            geo.add_subplot(fig, gs[1,2], projection=projection)
        ]

        g = PltClass(fig, axes)
    
    return g