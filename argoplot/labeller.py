
import numpy as np
from matplotlib.transforms import Bbox

global var_dict
global unit_dict
var_dict = dict(
    TEMP='Temperature',
    PSAL='Practical Salinity',
    PRES='Pressure',
    DOXY='Dissolved Oxygen',
    CHLA='Chlorophyll',
    BBP700='Backscatter [700nm]',
    CDOM='CDOM',
    PAR='PAR',
)
unit_dict = dict(
    TEMP='{}C'.format(chr(176)),
    PSAL='',
    PRES='dbar',
    DOXY='$\mathregular{\mu}$mol kg$^{{-1}}$',
    CHLA='mg m$^{{-3}}$',
    BBP700='m$^{{-1}}',
    CDOM='mg m$^{{-3}}$',
    PAR='',
)

def assign_label(name):
    '''
    give a nicely formatted axis label for a given Argo variable name
    '''

    if type(name) is not str:
        label = ''
    elif name in var_dict.keys():
        varname = var_dict[name]
        varunit = unit_dict[name]

        if varunit == '':
            label = varname
        else:
            label = '{} ({})'.format(varname, varunit)
    else:
        label = name

    return label


def contour_label_at_edge(levels, cs, ax, fmt, side='both', pad=0.005, **kwargs):
    '''
    Label contour lines at the edge of plot

    Args:
        levels (1d array): contour levels.
        cs (QuadContourSet obj): the return value of contour() function.
        ax (Axes obj): matplotlib axis.
        fmt (str): formating string to format the label texts. E.g. '%.2f' for
            floating point values with 2 demical places.
    Keyword Args:
        side (str): on which side of the plot intersections of contour lines
            and plot boundary are checked. Could be: 'left', 'right', 'top',
            'bottom', 'upperleft', 'upperright', 'bottomleft', 'bottomright'
            or 'all'. E.g. 'left' means only intersections of contour
            lines and left plot boundary will be labeled. 'all' means all 4
            edges.
        pad (float): padding to add between plot edge and label text.
        **kwargs: additional keyword arguments to control texts. E.g. fontsize,
            color.
    '''
    collections = cs.collections
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    bbox = Bbox.from_bounds(xlim[0], ylim[0], xlim[1]-xlim[0], ylim[1]-ylim[0])
    eps = 1e-5  # error for checking boundary intersection
    # -----------Loop through contour levels-----------
    for col, l in zip(collections, levels):
        paths = col.get_paths()  # the Paths for these contours
        if len(paths) == 0:
            continue
        for p in paths:
            # check first whether the contour intersects the axis boundary
            if not p.intersects_bbox(bbox, False):  # False significant here
                continue
            x = p.vertices[:, 0]
            y = p.vertices[:, 1]
            # intersection with the left edge
            if side in ['left', 'all', 'lowerleft', 'upperleft']:
                inter_idx = np.where(abs(x-xlim[0]) <= eps)[0]
                for k in inter_idx:
                    inter_x = x[k]
                    inter_y = y[k]
                    ax.text(inter_x-pad, inter_y, fmt % l,
                            ha='right',
                            va='center',
                            **kwargs)
            # intersection with the right edge
            if side in ['right', 'all', 'lowerright', 'upperright']:
                inter_idx = np.where(abs(x-xlim[1]) <= eps)[0]
                for k in inter_idx:
                    inter_x = x[k]
                    inter_y = y[k]
                    ax.text(inter_x+pad, inter_y, fmt % l,
                            ha='left',
                            va='center',
                            **kwargs)
            # intersection with the bottom edge
            if side in ['bottom', 'all', 'lowerleft', 'lowerright']:
                inter_idx = np.where(abs(y-ylim[0]) <= eps)[0]
                for k in inter_idx:
                    inter_x = y[k]
                    inter_y = y[k]
                    ax.text(inter_x, inter_y-5*pad, fmt % l,
                            ha='center',
                            va='top',
                            **kwargs)
            # intersection with the top edge
            if side in ['top', 'all', 'upperleft', 'upperright']:
                inter_idx = np.where(abs(y-ylim[-1]) <= eps)[0]
                for k in inter_idx:
                    inter_x = y[k]
                    inter_y = y[k]
                    ax.text(inter_x, inter_y+pad, fmt % l,
                            ha='center',
                            va='bottom',
                            **kwargs)
    return