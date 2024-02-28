#!/usr/bin/python3

import datetime
import requests
import yaml
import pygrib
from netCDF4 import Dataset
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------


def datum (h, start):
    if not isinstance(h, int):
        h = int(h)

    if not isinstance(start, int):
        start = int(start)

    today = datetime.date.today()
    today = today.timetuple()
    x = datetime.datetime(today.tm_year, today.tm_mon, today.tm_mday, start)
    # string = "Forecasttime " + x.strftime("%d.%m. %H:%M") + " UTC "
    string1 = "Run: " + x.strftime("%d.%m. %H UTC")
    x = datetime.datetime(today.tm_year, today.tm_mon, today.tm_mday, start) + datetime.timedelta(hours=h)
    string2 = x.strftime("%A, %d.%m. %H UTC")
    
    return string1, string2

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

    opendataserver="https://opendata.dwd.de/weather/nwp/icon-eu/grib"
    nwp_name=f"icon-eu_europe_regular-lat-lon_single-level_{datum}{run}_{fp:03d}_{fieldname.upper()}.grib2.bz2"
    url_link=f"{opendataserver}/{run}/{fieldname.lower()}/{nwp_name}"

    response = requests.get(url_link)
    with open(f"{store_path}/test.grib2.bz2", 'wb') as f:
        f.write(response.content)
    
    print("Download complete.")

# ---------------------------------------------------------------------------------------------------------------------


def open_gribfile_single(fieldname, datetime_obj, run, fp, path="./iconnest/"):
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

def open_gribfile_multi(fieldname, lvl, datetime_obj, run, fp, path="./iconnest/"):
    date_string = datetime_obj.strftime("%Y%m%d")
    nwp_modellevel = "icon-eu_europe_regular-lat-lon_model-level"

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

# ---------------------------------------------------------------------------------------------------------------------


def open_netcdf(fieldname, path="./iconnest/"):
    data = Dataset(f"{path}{fieldname}", 'r')

    lat = data.variables['lat'][:]
    lon = data.variables['lon'][:]

    lons, lats = np.meshgrid(lon, lat)

    data = data.variables[fieldname.lower()][0, :, :, :].filled(np.nan)

    data.close()

    print("Data shape:", data.shape)
    print("Maximum:", np.nanmax(data))
    return data, lats, lons
