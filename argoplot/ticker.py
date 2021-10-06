
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
        
def geo_extent_squate(data):
    '''
    create a cartopy extent that will create a square plot shape
    '''

    return