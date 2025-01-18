#!/usr/bin/python3
# ---------------------------------------------------------------------------------------------------------------------
#
# Meteorology Library
#
# ---------------------------------------------------------------------------------------------------------------------

import numpy as np

# ---------------------------------------------------------------------------------------------------------------------
# constants

ROCP = 0.28571426       # R over Cp
ZEROCNK = 273.15        # Zero Celsius in Kelvins
GRAV = 9.80665          # Gravity
TOL = 1e-10             # Floating Point Tolerance


# ---------------------------------------------------------------------------------------------------------------------
# thermodynamics


def q_to_mixrat(q):
    """
    Parameters
    ----------
    q : specific humidity in kg/kg
    """
    return q/(1.0-q)


def temp_at_mixrat(w, p):
    """
    Returns the temperature in K of air at the given mixing ratio in g/kg and pressure in hPa

    Parameters
    ----------
    w : Mixing Ratio in g/kg as numpy.array
    p : Pressure in hPa as numpy.array

    Returns
    -------
    Temperature in K of air at given mixing ratio and pressure

    """

    # Constants Used
    c1 = 0.0498646455
    c2 = 2.4082965
    c3 = 7.07475
    c4 = 38.9114
    c5 = 0.0915
    c6 = 1.2035

    x = np.log10(w * p / (622. + w))
    x = (np.power(10., ((c1 * x) + c2)) - c3 + (c4 * np.power((np.power(10, (c5 * x)) - c6), 2)))
    return x


# ---------------------------------------------------------------------------------------------------------------------
# kinematics

def uv2spddir(u, v):
    """
    Compute wind direction and speed from u and v components.

    Parameters
    ----------
    u, v : array_like
        zonal and meridional wind components

    Returns
    -------
    direction, speed : tuple of array_like
        direction in degrees and wind speed in m/s
    """
    direction = np.rad2deg(np.arctan2(-u, -v))
    if isinstance(direction, np.ndarray):
        direction = np.remainder(direction + 360, 360)
    else:
        direction = (direction + 360) % 360

    wind_speed = np.sqrt(np.square(u) + np.square(v))
    if type(wind_speed) is not np.ndarray:
        if wind_speed == 0:
            direction = np.nan
    else:
        direction[np.where(wind_speed == 0)] = np.nan

    return (direction, wind_speed)


def uv2spddir_rad(u, v):
    """
    Compute wind direction and speed from u and v components.

    Parameters
    ----------
    u, v : array_like
        zonal and meridional wind components

    Returns
    -------
    direction, speed : tuple of array_like
        direction in radians and wind speed in m/s
    """
    direction = np.arctan2(u, -v)

    wind_speed = np.sqrt(np.square(u) + np.square(v))
    if type(wind_speed) is not np.ndarray:
        if wind_speed == 0:
            direction = np.nan
    else:
        direction[np.where(wind_speed == 0)] = np.nan

    return (direction, wind_speed)


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
    d = 7.5

    # sfc-500m Mean Wind
    mnu500m, mnv500m = mean_wind(u[:i_500m], v[:i_500m], ps[:i_500m])

    # 5.5km-6.0km Mean Wind
    mnu5500m_6000m, mnv5500m_6000m = mean_wind(u[i_5km:i_6km], v[i_5km:i_6km], ps[i_5km:i_6km])

    # shear vector of the two mean winds
    shru = mnu5500m_6000m - mnu500m
    shrv = mnv5500m_6000m - mnv500m

    # SFC-6km Mean Wind
    mnu6, mnv6 = mean_wind(u[:i_6km], v[:i_6km], ps[:i_6km])

    # Bunkers Right Motion
    tmp = d / np.sqrt(shru*shru + shrv*shrv)
    rstu = mnu6 + (tmp * shrv)
    rstv = mnv6 - (tmp * shru)
    lstu = mnu6 - (tmp * shrv)
    lstv = mnv6 + (tmp * shru)

    return rstu, rstv, lstu, lstv, mnu6, mnv6
