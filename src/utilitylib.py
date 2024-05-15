#!/usr/bin/python3

from datetime import datetime, timedelta
import requests
import yaml

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


def load_yaml(yaml_file, yaml_path='.'):
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
