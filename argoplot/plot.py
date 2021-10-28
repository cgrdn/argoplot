
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import gsw

from . import ticker
from . import labeller

class PltClass:
    '''
    argoplot plot class containing figure and axis objects
    '''

    def __init__(self, fig, axes):
        self.info = 'argoplot object'
        self.fig  = fig
        if axes is mpl.axes._subplots.Subplot or axes is mpl.axes._axes.Axes:
            self.ax = axes
            self.axes = [axes]
        else:
            self.axes = axes

def profile(x=None, y=None, data=None, hue=None, style=None, ax=None, legend=False, ax_prop={}, **kwargs):
    '''
    plot a profile using seaborn's lineplot function

    Args:
        x, y (vectors or keys in ``data``):
        Variables that specify positions on the x and y axes.
        hue (vector or key in ``data``):
            Grouping variable that will produce lines with different colors.
            Can be either categorical or numeric, although color mapping will
            behave differently in latter case.
        size (vector or key in ``data``):
            Grouping variable that will produce lines with different widths.
            Can be either categorical or numeric, although size mapping will
            behave differently in latter case.
        style (vector or key in ``data``):
            Grouping variable that will produce lines with different dashes
            and/or markers. Can have a numeric dtype but will always be treated
            as categorical.
        data (:class:`pandas.DataFrame`, :class:`numpy.ndarray`, mapping, or sequence):
            Input data structure. Either a long-form collection of vectors that can be
            assigned to named variables or a wide-form dataset that will be internally
            reshaped.
    Keyword Args:
        ax_prop (:class:`dict`):
            Keyword arguments to be passed to :meth:`matplotlib.axes.Axes.set`
        kwargs (key, value mappings):
            Other keyword arguments are passed down to
            :meth:seaborn.lineplot or :meth:`matplotlib.axes.Axes.plot`.
    '''

    sg = sns.lineplot(x=x, y=y, hue=hue, style=style, data=data, sort=False, legend=legend, ax=ax, **kwargs)

    # format figure
    ax.set_ylim(ticker.assign_ylim(ax, 'profile'))
    ax.set_xlabel(labeller.assign_label(x))
    ax.set_ylabel(labeller.assign_label(y))

    # rotate ylabels
    ax.grid()
    for yl in ax.get_yticklabels():
        yl.update(dict(rotation=90))
        yl.set_verticalalignment('center')

    # any user-set axis properties
    ax.set(**ax_prop)

    return sg

def ts_diagram(data, lat=45, lon=90, hue=None, style=None, legend=False, ax=None, **kwargs):
    '''
    plot a TS diagram using seaborn's scatterplot function

    Args:
        data (:class:`pandas.DataFrame`):
            Input data structure. Must contain Argo variables 'PSAL' and 'TEMP'.
        hue (vector or key in ``data``):
            Grouping variable that will produce lines with different colors.
            Can be either categorical or numeric, although color mapping will
            behave differently in latter case.
        size (vector or key in ``data``):
            Grouping variable that will produce lines with different widths.
            Can be either categorical or numeric, although size mapping will
            behave differently in latter case.
        style (vector or key in ``data``):
            Grouping variable that will produce lines with different dashes
            and/or markers. Can have a numeric dtype but will always be treated
            as categorical.
    Keyword Args:
        ax_prop (:class:`dict`):
            Keyword arguments to be passed to :meth:`matplotlib.axes.Axes.set`
        kwargs (key, value mappings):
            Other keyword arguments are passed down to
            :meth:seaborn.lineplot or :meth:`matplotlib.axes.Axes.plot`.
    '''
    # get density contours
    vs, vt = np.meshgrid(
        np.linspace(data['PSAL'].min()-0.5, data['PSAL'].max()+0.5, 100),
        np.linspace(data['TEMP'].min()-2, data['TEMP'].max()+2, 100)
    )

    pden = gsw.pot_rho_t_exact(gsw.SA_from_SP(vs, 0, lon, lat), vt, 0, 0) - 1000
    # contour levels
    levels = list(range(int(np.floor(np.min(pden))), int(np.ceil(np.max(pden)))+2, 2))

    # TS diagram w/ pot density contours 
    cs = ax.contour(vs, vt, pden, colors='black', levels=levels, zorder=1)
    labeller.contour_label_at_edge(levels, cs, ax, '%d', side='lowerleft', pad=0.1)
    sg = sns.scatterplot(x='PSAL', y='TEMP', hue=hue, style=style, data=data, legend=legend, ax=ax, zorder=2)
    sg.cs = cs

    for yl in ax.get_yticklabels():
        yl.update(dict(rotation=90))
        yl.set_verticalalignment('center')

    ax.set_xlabel(labeller.assign_label('PSAL'))
    ax.set_ylabel(labeller.assign_label('TEMP'))

    return sg