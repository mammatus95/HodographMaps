#!/usr/bin/python3
from datetime import datetime, date
import pygrib
import numpy as np
import utilitylib as ut

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
points = 1038240
nlon = 1440
nlat = 721
lev = [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200]
lonmin = 0
lonmax = 359
latmin = -90
latmax = 90
d_grad = 0.25

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
# ---------------------------------------------------------------------------------------------------------------------
#             name    typeOfLevel    level
par_list_gfs = [
               ('u', 'isobaricInhPa', 1000),
               ('u', 'isobaricInhPa',  975),
               ('u', 'isobaricInhPa',  950),
               ('u', 'isobaricInhPa',  925),
               ('u', 'isobaricInhPa',  900),
               ('u', 'isobaricInhPa',  850),
               ('u', 'isobaricInhPa',  800),
               ('u', 'isobaricInhPa',  750),
               ('u', 'isobaricInhPa',  700),
               ('u', 'isobaricInhPa',  650),
               ('u', 'isobaricInhPa',  600),
               ('u', 'isobaricInhPa',  500),
               ('u', 'isobaricInhPa',  400),
               ('u', 'isobaricInhPa',  300),
               ('v', 'isobaricInhPa', 1000),
               ('v', 'isobaricInhPa',  975),
               ('v', 'isobaricInhPa',  950),
               ('v', 'isobaricInhPa',  925),
               ('v', 'isobaricInhPa',  900),
               ('v', 'isobaricInhPa',  850),
               ('v', 'isobaricInhPa',  800),
               ('v', 'isobaricInhPa',  750),
               ('v', 'isobaricInhPa',  700),
               ('v', 'isobaricInhPa',  650),
               ('v', 'isobaricInhPa',  600),
               ('v', 'isobaricInhPa',  500),
               ('v', 'isobaricInhPa',  400),
               ('v', 'isobaricInhPa',  300),
               ('cape', 'pressureFromGroundLayer', 9000),  # 9000 18000 25500
               # ('cape', 'surface', 0),
               # ('cape', 'pressureFromGroundLayer', 9000),  # 9000 18000 25500
               # ('10u',  'heightAboveGround', 10),
               # ('10v', 'heightAboveGround',  10),
               # ('100u', 'heightAboveGround', 100),
               # ('100v', 'heightAboveGround', 100),
]
par_list_ifs = [
               ('u', 'isobaricInhPa', 1000),
               ('u', 'isobaricInhPa',  925),
               ('u', 'isobaricInhPa',  850),
               ('u', 'isobaricInhPa',  700),
               ('u', 'isobaricInhPa',  600),
               ('u', 'isobaricInhPa',  500),
               ('u', 'isobaricInhPa',  400),
               ('u', 'isobaricInhPa',  300),
               ('v', 'isobaricInhPa', 1000),
               ('v', 'isobaricInhPa',  925),
               ('v', 'isobaricInhPa',  850),
               ('v', 'isobaricInhPa',  700),
               ('v', 'isobaricInhPa',  600),
               ('v', 'isobaricInhPa',  500),
               ('v', 'isobaricInhPa',  400),
               ('v', 'isobaricInhPa',  300),
               ('cape', 'entireAtmosphere', 0),
               # ('10u',  'heightAboveGround', 10),
               # ('10v', 'heightAboveGround',  10),
               # ('100u', 'heightAboveGround', 100),
               # ('100v', 'heightAboveGround', 100),
]

# ---------------------------------------------------------------------------------------------------------------------


class MODELINFO:

    def __init__(self, modelname, nlon, nlat, d_grad, levtyp):
        config = ut.load_yaml('config.yml')
        self.debug_flag = config['debugflag']
        self.modelname = modelname
        self.points = nlon*nlat
        self.nlon = nlon
        self.nlat = nlat
        if "ICON" in modelname:
            self.levels = [1000, 950, 925, 900, 875, 850, 825, 800, 775, 700, 600, 500, 400, 300]
            self.parlist = None
            self.hodo_interval_lat = range(272, 415, 12)
            self.hodo_interval_lon = range(420, 670, 15)
        elif modelname == "IFS":
            self.levels = [1000, 925, 850, 700, 600, 500, 400, 300]
            self.parlist = par_list_ifs
            self.hodo_interval_lat = range(143, 174, 3)
            self.hodo_interval_lon = range(731, 794, 3)
        elif modelname == "GFS":
            self.levels = [1000, 975, 950, 925, 900, 850, 800, 750, 700, 650, 600, 500, 400, 300]
            self.parlist = par_list_gfs
            self.hodo_interval_lat = range(143, 174, 3)
            self.hodo_interval_lon = range(11, 74, 3)
        else:
            self.levels = [1000, 850, 700, 600, 500, 400, 300]
        self.d_grad = d_grad
        self.levtyp = levtyp
        self.run = -99
        self.rundate = date.today()

    def __str__(self):
        return (
                f"Model Information: {self.modelname}  Run: {self.run} Date: {self.rundate}\n"
                f"Points: {self.points}\n"
                f"Number of Longitudes: {self.nlon}\tNumber of Latitudes: {self.nlat}\n"
                f"Horizontal resolution: {self.d_grad}\n"
                f"Number of Levels: {len(self.levels)}\tLeveltyps: {self.levtyp}\n"
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

    def getdebug(self):
        return self.debug_flag

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
        return self.levtyp

    def getd_grad(self):
        return self.d_grad

    def create_plottitle(self):
        return f"Hodographmap of {self.modelname}"
    # ------------------------------------------------------------------------------------------------------------------------

    def open_gribfile_preslvl(self, fp, path="./modeldata/"):
        date_string = self.getrundate_as_str("%Y%m%d")

        # create numpy.array fields
        shape = (self.getnlev(), self.getnlat(), self.getnlon())
        u_fld = np.full(shape, np.nan)
        v_fld = np.full(shape, np.nan)

        shape = (self.getnlat(), self.getnlon())
        cape_fld = np.full(shape, np.nan)
        lats = np.full(shape, np.nan)
        lons = np.full(shape, np.nan)
        pres_levels = self.getlevels()
        run = self.getrun()

        # Open the GRIB file
        # modelname_RRz_YYYYMMDD_f015.grib2
        gribidx = pygrib.index(f"{path}{self.getname().lower()}_{run:02d}z_{date_string}_f{fp:03d}.grib2",
                            'shortName', 'typeOfLevel', 'level')
        # grbs.seek(0)

        for par in self.getParamter():
            try:
                grb_message = gribidx.select(shortName=par[0], typeOfLevel=par[1], level=par[2])[0]
                if par[0] == "cape":
                    cape_fld = grb_message.values
                    lats, lons = grb_message.latlons()
                else:
                    idx = pres_levels.index(par[2])
                    if par[0] == 'u':
                        u_fld[idx, :, :] = grb_message.values
                        if self.debug_flag is True:
                            print(f"Lvl: {par[2]:>4d} u_max: {np.nanmax(u_fld):.1f}")
                    elif par[0] == 'v':
                        v_fld[idx, :, :] = grb_message.values
                    else:
                        raise ValueError(f"Unknown Parameter: {par[0]}")
            except ValueError as e:
                print(f"Error: {e}\t shortName: {par[0]} typeOfLevel: {par[1]} level: {par[2]}")
                pass
        if self.debug_flag is True:
            print(f"Shape: {np.shape(cape_fld)}")
        return cape_fld, u_fld, v_fld, lats, lons

    def open_icon_gribfile_preslvl(self, fieldname, lvl, fp, path="./modeldata/"):
        date_string = self.getrundate_as_str("%Y%m%d")
        nwp_modellevel = "icon-eu_europe_regular-lat-lon_pressure-level"
        shape = (self.getnlat(), self.getnlon())
        data_fld = np.full(shape, np.nan)
        # Open the GRIB file
        grbs = pygrib.open(f"{path}{nwp_modellevel}_{date_string}{self.getrun():02d}"
                           f"_{fp:03d}_{lvl}_{fieldname.upper()}.grib2")

        # Read specific data from the file
        first_message = grbs[1]

        data_fld = first_message.values
        # Convert missing values to NaNs
        data_fld[data_fld == first_message.missingValue] = np.nan

        grbs.close()

        if self.debug_flag is True:
            # print("Data shape:", data.shape)
            print(f"Lvl: {lvl:>4d} {fieldname}_max: {np.nanmax(data_fld):.1f}")
        return data_fld

    def open_icon_gribfile_single(self, fieldname, fp, path="./modeldata/"):
        date_string = self.getrundate_as_str("%Y%m%d")
        nwp_singlelevel = "icon-eu_europe_regular-lat-lon_single-level"
        shape = (self.getnlat(), self.getnlon())
        cape_fld = np.full(shape, np.nan)

        # Open the GRIB file
        grbs = pygrib.open(f"{path}{nwp_singlelevel}_{date_string}{self.getrun():02d}_{fp:03d}_{fieldname.upper()}.grib2")

        # Read specific data from the file
        first_message = grbs[1]

        cape_fld = first_message.values
        # Convert missing values to NaNs
        cape_fld[cape_fld == first_message.missingValue] = np.nan

        lats, lons = first_message.latlons()
        grbs.close()

        if self.debug_flag is True:
            # print("Data shape:", data.shape)
            print(f"{fieldname}_max: {np.nanmax(cape_fld):.1f}")
        return cape_fld, lats, lons


# Example usage:
icon_nest = MODELINFO("ICON Nest", 1377, 657, 0.0625, "pres")
ifs = MODELINFO("IFS", 1440, 721, 0.25, "pres")
gfs = MODELINFO("GFS", 1440, 721, 0.25, "pres")
