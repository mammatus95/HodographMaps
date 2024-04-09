#!/usr/bin/python3
"""
# ICON Nest
points = 904689
nlon = 1377
nlat = 657
lev = [1000, 950, 925, 900, 875, 850, 825, 800, 775, 700, 600, 500, 400, 300, 250, 200]
lonmin = -23.5
lonmax =  45.0
latmin =  29.5
latmax =  70.5
d_grad = 0.0625

# IFS
points = 405900
nlon = 900
nlat = 451
lev = [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200]
lonmin = 0
lonmax = 359
latmin = -90
latmax = 90
d_grad = 0.4

# GFS
points = 1038240
nlon = 1440
nlat = 721
nlev = [1000, 975, 950, 925, 900, 850, 800, 750, 700, 650, 600, 500, 400, 300, 250, 200]
lonmin = 0
lonmax = 359
latmin = -90
latmax = 90
d_grad = 0.25

"""


class MODELIFNO:

    def __init__(self, modelname, nlon, nlat, d_grad, levtyp):
        self.modelname = modelname
        self.points = nlon*nlat
        self.nlon = nlon
        self.nlat = nlat
        if "ICON" in modelname:
            self.levels = [1000, 950, 925, 900, 875, 850, 825, 800, 775, 700, 600, 500, 400, 300, 250, 200]
        elif modelname == "IFS":
            self.levels = [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200]
        elif modelname == "GFS":
            self.levels = [1000, 975, 950, 925, 900, 850, 800, 750, 700, 650, 600, 500, 400, 300, 250, 200]
        else:
            self.levels = [1000, 850, 700, 600, 500, 400, 300, 250, 200]
        self.d_grad = d_grad
        self.levtyp = levtyp


    def __str__(self):
        return (
                f"Model Information: {self.modelname}\nPoints: {self.points}\n"
                f"Number of Longitudes: {self.nlon}\nNumber of Latitudes: {self.nlat}\n"
                f"Horizontal resolution: {self.d_grad}\n"
                f"Number of Levels: {len(self.levels)}\tLeveltyps: {self.levtyp}\n"
               )

    def getname(self):
        return self.modelname

    def getpoints(self):
        return self.points

    def getnlon(self):
        return self.nlon

    def getnlat(self):
        return self.nlat

    def getlevels(self):
        return self.levels

    def getpreslevel_by_idx(self, idx):
        if idx >= 0 and idx < len(self.levels):
            return self.levels[idx]
        else:
            return -99

    def getnlev(self):
        return len(self.levels)

    def getlevtyp(self):
        return self.d_grad

    def getd_grad(self):
        return self.d_grad


# Example usage:
icon_nest = MODELIFNO("ICON EU", 1377, 657, 0.0625, "pres")
ifs = MODELIFNO("IFS", 451, 900, 0.4, "pres")
gfs = MODELIFNO("GFS", 721, 1440, 0.25, "pres")