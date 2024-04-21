#!/usr/bin/python3
from datetime import datetime, date


class MODELIFNO:

    def __init__(self, modelname, nlon, nlat, d_grad, nlev, levtyp):
        self.modelname = modelname
        self.points = nlon*nlat
        self.nlon = nlon
        self.nlat = nlat
        self.nlev = nlev
        self.d_grad = d_grad
        self.levtyp = levtyp
        self.run = -99
        self.rundate = date.today()
        self.hodo_interval_lat = range(272, 415, 12)
        self.hodo_interval_lon = range(420, 670, 15)
        
    def __str__(self):
        return (
                f"Model Information:\nPoints: {self.points}\n"
                f"Number of Longitudes: {self.nlon}\nNumber of Latitudes: {self.nlat}\n"
                f"Horizontal resolution: {self.d_grad}\n"
                f"Number of Levels: {self.nlev}\tLeveltyps: {self.levtyp}\n"
               )

    def setrun(self, run):
        if isinstance(run, int):
            self.run = run
        else:
            self.run = int(run)

    def setrundate(self, rundate):
        if isinstance(rundate, datetime):
            self.rundate = rundate
        else:
            self.rundate = datetime.strptime(rundate, "%Y-%m-%d")

    def getrun(self):
        return self.run

    def getrundate(self):
        return self.rundate

    def getrundate_as_str(self, fmt="%Y%m%d"):
        return self.rundate.strftime(fmt)

    def getname(self):
        return self.modelname

    def getParamter(self):
        return self.parlist

    def getpoints(self):
        return self.points

    def getnlon(self):
        return self.nlon

    def getnlat(self):
        return self.nlat

    def getnlev(self):
        return int(self.nlev)

    def getlevtyp(self):
        return self.d_grad

    def getd_grad(self):
        return self.d_grad

    def create_plottitle(self):
        return f"Hodographmap of {self.modelname}"


# Example usage:
icon_nest = MODELIFNO("ICON Nest", 1377, 657, 0.0625, 54, "model")  # lowest 74 and we download till 20
