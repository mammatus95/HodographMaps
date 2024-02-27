#!/usr/bin/python3
"""
##  COSMO-REA2
points = 564720 #(724x780)
nlon = 724
nlat = 780
nlev = 50
lonmin = -7.5
lonmax =  5.514
latmin = -6.0
latmax =  8.022
##gradients
d_grad = 0.018
#nortpole
#north_lon=
#noth_lat=


##  COSMO-RE6
points = 698752 #(848x824)
nlon = 848
nlat = 824
nlev = 40
lonmin = -28.403
lonmax =  18.182
latmin = -23.403
latmax =  21.862
##gradients
d_grad = 0.055
#nortpole
#north_lon=
#noth_lat=


## ICON Nest
points = 904689 #(1377x657)
nlon = 1377
nlat = 657
nlev = 51
lonmin = -23.5
lonmax =  45.0
latmin =  29.5
latmax =  70.5
##gradients
d_grad = 0.0625


## COSMO D2
points = 466116 #(651x716)
nlon = 651
nlat = 716
nlev = 65
lonmin = -7.5
lonmax =  5.5
latmin = -6.3
latmax =  8.0
##gradients
d_grad = 0.02
#nortpole
north_lon=-170
noth_lat=40

##ERAINTERIM
points=115680 #(480x241)
nlon=480
nlat=241
nlev=23
lonmin = -180.0
lonmax = 179.25
latmin = -90
latmax = 90
d_grad = 0.75
"""

class MODELIFNO:
    def __init__(self, nlon, nlat, nlev, d_grad):
        self.points = nlon*nlat
        self.nlon = nlon
        self.nlat = nlat
        self.nlev = nlev
        self.d_grad = d_grad

    def __init__(self, nlon, nlat, nlev, lonmin, lonmax, latmin, latmax, d_grad):
        self.points = nlon*nlat
        self.nlon = nlon
        self.nlat = nlat
        self.nlev = nlev
        self.d_grad = d_grad
        print(lonmin, lonmax, latmin, latmax)

    def __str__(self):
        return (
                f"Model Information:\nPoints: {self.points}\n"
                f"Number of Longitudes: {self.nlon}\nNumber of Latitudes: {self.nlat}\n"
                f"Number of Levels: {self.nlev}\nGradient: {self.d_grad}"
               )
    
    def getpoints(self):
        return self.points

    def getnlon(self):
        return self.nlon
    
    def getnlat(self):
        return self.nlat

    def getnlev(self):
        return self.nlev

    def getd_grad(self):
        return self.d_grad

# Example usage:
icon_nest = MODELIFNO(1377, 657, 51, -23.5, 45.0, 29.5, 70.5, 0.0625)
cosmo_d2 = MODELIFNO(651, 716, 65, 0.02)
ifs = MODELIFNO(450, 900, 10, 0.4)
