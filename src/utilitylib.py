#!/usr/bin/python3

from datetime import datetime, timedelta
import requests
import yaml
import pygrib
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------


def datum(leadtime, start, datetime_obj):
    if not isinstance(leadtime, int):
        leadtime = int(leadtime)

    if not isinstance(start, int):
        start = int(start)

    today = datetime_obj.timetuple()
    x = datetime(today.tm_year, today.tm_mon, today.tm_mday, start)
    modelrun_string = "Run: " + x.strftime("%d.%m. %H UTC")
    x = datetime(today.tm_year, today.tm_mon, today.tm_mday, start) + timedelta(hours=leadtime)
    valid_string = x.strftime("%A, %d.%m. %H UTC")

    return modelrun_string, valid_string

# ---------------------------------------------------------------------------------------------------------------------


def load_yaml(yaml_file, yaml_path='./'):
    """
    Parameters:
    -----------
    yaml_file : name of yaml file
    """
    with open(f"{yaml_path}/{yaml_file}", 'r') as yhand:
        config_data = yaml.safe_load(yhand)
    return config_data

# ---------------------------------------------------------------------------------------------------------------------
# https://opendata.dwd.de/weather/nwp/icon-eu/grib/00/cape_ml/icon-eu_europe_regular-lat-lon_single-level_2024022700_006_CAPE_ML.grib2.bz2
# https://opendata.dwd.de/weather/nwp/icon-eu/grib/00/u/icon-eu_europe_regular-lat-lon_model-level_2024022700_000_10_U.grib2.bz2


def download_nwp(fieldname, datum="20240227", run="00", fp=0, store_path="./"):
    opendataserver = "https://opendata.dwd.de/weather/nwp/icon-eu/grib"
    nwp_name = f"icon-eu_europe_regular-lat-lon_single-level_{datum}{run}_{fp:03d}_{fieldname.upper()}.grib2.bz2"
    url_link = f"{opendataserver}/{run}/{fieldname.lower()}/{nwp_name}"

    response = requests.get(url_link)
    with open(f"{store_path}/test.grib2.bz2", 'wb') as f:
        f.write(response.content)

    print("Download complete.")

# ---------------------------------------------------------------------------------------------------------------------


def open_gribfile_single(fieldname, datetime_obj, run, fp, path="./modeldata/"):
    date_string = datetime_obj.strftime("%Y%m%d")
    nwp_singlelevel = "icon-eu_europe_regular-lat-lon_single-level"

    # Open the GRIB file
    grbs = pygrib.open(f"{path}{nwp_singlelevel}_{date_string}{run:02d}_{fp:03d}_{fieldname.upper()}.grib2")

    # Read specific data from the file
    first_message = grbs[1]

    data = first_message.values
    # Convert missing values to NaNs
    data[data == first_message.missingValue] = np.nan

    lats, lons = first_message.latlons()
    grbs.close()

    # print("Data shape:", data.shape)
    print("Maximum:", np.nanmax(data))
    return data, lats, lons


def open_icon_gribfile_preslvl(fieldname, lvl, datetime_obj, run, fp, path="./modeldata/"):
    date_string = datetime_obj.strftime("%Y%m%d")
    nwp_modellevel = "icon-eu_europe_regular-lat-lon_pressure-level"

    # Open the GRIB file
    grbs = pygrib.open(f"{path}{nwp_modellevel}_{date_string}{run:02d}_{fp:03d}_{lvl}_{fieldname.upper()}.grib2")

    # Read specific data from the file
    first_message = grbs[1]

    data = first_message.values
    # Convert missing values to NaNs
    data[data == first_message.missingValue] = np.nan

    grbs.close()

    # print("Data shape:", data.shape)
    print("Maximum:", np.nanmax(data))
    return data


def open_gribfile_preslvl(model_obj, fp, path="./modeldata/"):
    date_string = model_obj.getrundate_as_str("%Y%m%d")

    # create numpy.array fields
    shape = (model_obj.getnlev(), model_obj.getnlat(), model_obj.getnlon())
    u_fld = np.full(shape, np.nan)
    v_fld = np.full(shape, np.nan)

    shape = (model_obj.getnlat(), model_obj.getnlon())
    cape_fld = np.full(shape, np.nan)
    lats = np.full(shape, np.nan)
    lons = np.full(shape, np.nan)
    pres_levels = model_obj.getlevels()
    run = model_obj.getrun()

    # Open the GRIB file
    # modelname_RRz_YYYYMMDD_f015.grib2
    gribidx = pygrib.index(f"{path}{model_obj.getname().lower()}_{run:02d}z_{date_string}_f{fp:03d}.grib2",
                           'shortName', 'typeOfLevel', 'level')
    # grbs.seek(0)

    for par in model_obj.getParamter():
        try:
            grb_message = gribidx.select(shortName=par[0], typeOfLevel=par[1], level=par[2])[0]
            if par[0] == "cape":
                cape_fld = grb_message.values
                lats, lons = grb_message.latlons()
            else:
                idx = pres_levels.index(par[2])
                if par[0] == 'u':
                    u_fld[idx, :, :] = grb_message.values
                elif par[0] == 'v':
                    v_fld[idx, :, :] = grb_message.values
                else:
                    raise ValueError(f"Unknown Parameter: {par[0]}")
        except ValueError as e:
            print(f"Error: {e}\t shortName: {par[0]} typeOfLevel: {par[1]} level: {par[2]}")
            pass

    return cape_fld, u_fld, v_fld, lats, lons

# ---------------------------------------------------------------------------------------------------------------------


def open_netcdf(fieldname, path="./iconnest/"):
    from netCDF4 import Dataset
    data = Dataset(f"{path}{fieldname}", 'r')

    lat = data.variables['lat'][:]
    lon = data.variables['lon'][:]

    lons, lats = np.meshgrid(lon, lat)

    data = data.variables[fieldname.lower()][0, :, :, :].filled(np.nan)

    data.close()

    print("Data shape:", data.shape)
    print("Maximum:", np.nanmax(data))
    return data, lats, lons
