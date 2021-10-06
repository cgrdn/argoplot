
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import cmocean.cm as cmo

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

from .plot import PltClass
from . import ticker
from . import io

default_projection = ccrs.PlateCarree()

def add_subplot(fig, loc, projection=default_projection):
    '''
    add subplot to a figure with a given projection
    '''
    
    fig.add_subplot(loc, projection=projection)

def trajectory(data, hue=None, style=None, ax=None, markers=True, projection=default_projection, **kwargs):
    '''
    map Argo float position data over bathymetry
    '''

    extent = ticker.geo_extent(data)

    if ax is None:
        fig = plt.figure()
        g   = PltClass(fig, fig.add_subplot(projection=projection))
        ax  = g.ax
    
    # get bathymetry data
    lon, lat, elev = io.get_bathymetry(extent)

    # map of float deployment locations
    im = ax.contourf(
        lon, lat, elev,
        transform=ccrs.PlateCarree(),
        cmap=cmo.deep,
        vmim=0, extend='max'
    )
    sg = sns.lineplot(x='longitude', y='latitude', hue=hue, style=style, data=data, markers=markers, legend=False, ax=ax, transform=ccrs.PlateCarree(), **kwargs)
    sg.im = im

    ax.set_xticks(np.arange(np.ceil(extent[0]), np.floor(extent[1]), 4), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(np.ceil(extent[2]), np.floor(extent[3]), 4), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.yaxis.tick_right()
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_extent(extent)
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.LAND.with_scale('10m'))
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.RIVERS.with_scale('10m'))
    ax.add_feature(cfeature.LAKES.with_scale('10m'))

    return sg