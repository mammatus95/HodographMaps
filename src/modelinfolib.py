#!/usr/bin/python3
"""
# ICON Nest
points = 904689
nlon = 1377
nlat = 657
nlev = 51
lonmin = -23.5
lonmax =  45.0
latmin =  29.5
latmax =  70.5
d_grad = 0.0625

# IFS
points = 405900
nlon = 900
nlat = 451
nlev = 
lonmin = 0
lonmax = 359
latmin = -90
latmax = 90
d_grad = 0.4

# GFS
points = 1038240
nlon = 1440
nlat = 721
nlev = 
lonmin = 0
lonmax = 359
latmin = -90
latmax = 90
d_grad = 0.25

"""


class MODELIFNO:

    def __init__(self, nlon, nlat, d_grad, nlev, levtyp):
        self.points = nlon*nlat
        self.nlon = nlon
        self.nlat = nlat
        self.nlev = nlev
        self.d_grad = d_grad
        self.levtyp = levtyp

    """
    def __init__(self, nlon, nlat, nlev, lonmin, lonmax, latmin, latmax, d_grad):
        self.points = nlon*nlat
        self.nlon = nlon
        self.nlat = nlat
        self.nlev = nlev
        self.d_grad = d_grad
        print(lonmin, lonmax, latmin, latmax)
    """

    def __str__(self):
        return (
                f"Model Information:\nPoints: {self.points}\n"
                f"Number of Longitudes: {self.nlon}\nNumber of Latitudes: {self.nlat}\n"
                f"Horizontal resolution: {self.d_grad}\n"
                f"Number of Levels: {self.nlev}\tLeveltyps: {self.levtyp}\n"
               )

    def getpoints(self):
        return self.points

    def getnlon(self):
        return self.nlon

    def getnlat(self):
        return self.nlat

    def getnlev(self):
        return self.nlev

    def getlevtyp(self):
        return self.d_grad

    def getd_grad(self):
        return self.d_grad


# Example usage:
icon_nest = MODELIFNO(1377, 657, 0.0625, 54, "model")  # lowest 74 and we download till 20
