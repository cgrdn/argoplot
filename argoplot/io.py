
from pathlib import Path

import numpy as np
from netCDF4 import Dataset

from .  import config

def get_bathymetry(extent, local_path=config.gebco_path, file_name='GEBCO_2020.nc'):
    '''
    load GEBCO bathymetry data for a given box defined by extent

    Args:
        extent (list): bounding box
    Keyword Args:
        local_path (str or Path): location of the GEBCO bathymetry file
        file_name (str): name of the GEBCO bathymetry file, default is 'GEBCO_2020.nc'
    '''

    if type(local_path) is str:
        local_path = Path(local_path)
    nc = Dataset(local_path / file_name)

    lat  = nc['lat'][:]
    lon  = nc['lon'][:]
    elev = nc['elevation'][:]

    ix = np.logical_and(lon > extent[0], lon < extent[1])
    iy = np.logical_and(lat > extent[2], lat < extent[3])

    lon  = lon[ix]
    lat  = lat[iy]
    elev = elev[iy,:]
    elev = elev[:,ix]
    elev = -np.ma.masked_array(elev.data, elev > 0)

    return lon, lat, elev
