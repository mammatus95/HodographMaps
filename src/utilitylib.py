#!/usr/bin/python3

from datetime import datetime, timedelta
import requests
import yaml
import bz2

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

def decompress_file(input_file, output_file):
    """
    Decompresses a bz2 compressed file.

    Parameters:
    -----------
    input_file : str
        Path to the bz2 compressed input file.
    output_file : str
        Path where the decompressed file will be saved.
    """

    with bz2.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            f_out.write(f_in.read())

# ---------------------------------------------------------------------------------------------------------------------
# https://opendata.dwd.de/weather/nwp/icon-eu/grib/00/cape_ml/icon-eu_europe_regular-lat-lon_single-level_2024022700_006_CAPE_ML.grib2.bz2
# https://opendata.dwd.de/weather/nwp/icon-eu/grib/00/u/icon-eu_europe_regular-lat-lon_model-level_2024022700_000_10_U.grib2.bz2


def download_nwp(fieldname, datum="20240227", run="00", fp=0, store_path="./"):
    """
    Downloads ICON EU NWP data from DWD's opendata server. The filename is constructed
    from the given parameters. The downloaded file is stored in the given path with
    the name "test.grib2.bz2".

    Parameters:
    -----------
    fieldname : str
        name of the field to download (e.g. "cape_ml", "cin_ml", "t_2m")
    datum : str
        date of the model run in the format "YYYYMMDD"
    run : str
        model run identifier (e.g. "00", "12")
    fp : int
        forecast time (0-48)
    store_path : str
        path where the downloaded file will be stored

    Returns:
    -------
    None

    Notes:
    -----
    This function does not perform any error checking. If the file does not exist
    on the server, this function will raise an exception.
    """
    opendataserver = "https://opendata.dwd.de/weather/nwp/icon-eu/grib"
    nwp_name = f"icon-eu_europe_regular-lat-lon_single-level_{datum}{run}_{fp:03d}_{fieldname.upper()}.grib2.bz2"
    grb_name = f"icon-eu_europe_regular-lat-lon_single-level_{datum}{run}_{fp:03d}_{fieldname.upper()}.grib2"
    url_link = f"{opendataserver}/{run}/{fieldname.lower()}/{nwp_name}"

    response = requests.get(url_link)
    with open(f"{store_path}/{fieldname}.grib2.bz2", 'wb') as f:
        f.write(response.content)

    decompress_file(f"{store_path}/{fieldname}.grib2.bz2", f"{store_path}/{grb_name}")

    print(f"Download complete. File name is {store_path}{fieldname}.grib2.")
