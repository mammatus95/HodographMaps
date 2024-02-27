#!/usr/bin/python3
################################
#
# kinematiclib 
#
################################

import numpy as np


def uv2spddir(u,v):
    val = 180./np.pi
    rad = np.pi/180
    direction = np.rad2deg(np.arctan2(-u,v))

    if type(direction) == np.ndarray:
        direction[np.where(direction < 0)] += 360
    else:
        if direction < 0:
            direction += 360

    return (np.deg2rad(direction), np.sqrt(u*u + v*v))


def mean_wind(u, v, ps, stu=0, stv=0):
    """
    Parameter:
    ----------

    Returns:
    ---------
    """
    return np.average(u, weights=ps)-stu, np.average(v, weights=ps)-stv


def non_parcel_bunkers_motion_experimental(u, v, ps, i_500m, i_5km, i_6km):
    """
    Calculate the storm motion vector according to Bunker.

    Parameter:
    ----------

    Returns:
    ---------
    rstu, rstv : right-mover components
    lstu, lstv : left-mover components
    mnu6, mnv6 : mean wind components


    """
    d=7.5

    # sfc-500m Mean Wind
    mnu500m, mnv500m = mean_wind(u[:i_500m], v[:i_500m], ps[:i_500m])

    ## 5.5km-6.0km Mean Wind
    mnu5500m_6000m, mnv5500m_6000m = mean_wind(u[i_5km:i_6km], v[i_5km:i_6km], ps[i_5km:i_6km])

    # shear vector of the two mean winds
    shru = mnu5500m_6000m - mnu500m
    shrv = mnv5500m_6000m - mnv500m

    # SFC-6km Mean Wind
    mnu6, mnv6 =  mean_wind(u[:i_6km], v[:i_6km], ps[:i_6km])

    # Bunkers Right Motion
    tmp = d / np.sqrt(shru*shru + shrv*shrv)
    rstu = mnu6 + (tmp * shrv)
    rstv = mnv6 - (tmp * shru)
    lstu = mnu6 - (tmp * shrv)
    lstv = mnv6 + (tmp * shru)

    return rstu, rstv, lstu, lstv, mnu6, mnv6