#!/usr/bin/python3

import argparse

# own moduls
import utilitylib as ut
import plotlib

# ---------------------------------------------------------------------------------------------------------------------

def main():
    # config = ul.load_yaml('config.yml')

    # command line arguments
    parser = argparse.ArgumentParser(description="Hodograph Maps")
    # Add positional argument
    parser.add_argument('mode', type=str, 
                        help='Mode: Test, Basic, or Nixon')

    # Add optional argument
    parser.add_argument('-f', '--field', type=str, 
                        help='Which background field: CAPE ML, CAPE CON or LPI ')

    # Parse the command line arguments
    args = parser.parse_args()

    if args.field == None:
        args.field = "CAPE ML"

    if (args.field != "CAPE ML") and (args.field != "CAPE CON") and (args.field != "LPI"):
        print("Unknown field")
        exit(-1)

    # replace space with underscores
    fieldname = args.field.replace(" ", "_")


    
    print(args)

    #ut.download_nwp(fieldname, datum="20240227", run="00", fp=0, store_path="./")


    cape_fld, lats, lons = ut.open_gribfile(fieldname, path="./iconnest/")
    print(lats.shape)
    if args.mode == "Test":
        plotlib.test_plot (cape_fld, lats, lons, 9, 0, titel='CAPE')

if __name__ == "__main__":
    main()

