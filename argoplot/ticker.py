
import numpy as np

def assign_ylim(ax, plot_type):
    '''
    assign appropriate y-limits give a certain plot type
    '''

    if plot_type == 'profile':
        top = 0
        current_bottom = np.max(ax.get_ylim())

        thresholds = [1000, 500, 200, 100]
        for t in thresholds:
            if current_bottom > t:
                bottom = np.ceil(10*current_bottom/t)*t/10
                break
        
        ylim = (bottom, top)
    
    return ylim

def arrange(ax, loc):
    '''
    move x or y ticks and labels to desired location
    '''

    if loc in ['right', 'upperright', 'lowerright']:
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position('right')
    if loc in ['top', 'upperleft', 'upperright']:
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')
        
def extent_factor(c, i):
    '''
    widen extent depending on coordinate sign and location in extent list
    '''

    if i % 2 == 0:
        if c > 0:
            f = 0.9
        else:
            f = 1.1
    else:
        if c > 0:
            f = 1.1
        else:
            f = 0.9

    return f

def geo_extent(data):
    '''
    create a cartopy extent that will create a square plot shape
    '''

    # extent of the data
    data_extent = [
        data.longitude.min(),
        data.longitude.max(),
        data.latitude.min(),
        data.latitude.max(),
    ]

    # extent to fit the data
    fit_extent = [extent_factor(c, i)*c for i, c in enumerate(data_extent)]

    # get the longer extent
    lon_range = fit_extent[1] - fit_extent[0]
    lat_range = fit_extent[3] - fit_extent[2]
    max_range = np.max([lon_range, lat_range])

    lon_mean = np.mean(fit_extent[:2])
    lat_mean = np.mean(fit_extent[2:])

    # set square extent
    extent = [
        lon_mean - max_range/2,
        lon_mean + max_range/2,
        lat_mean - max_range/2,
        lat_mean + max_range/2,
    ]

    return extent