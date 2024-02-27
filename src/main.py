#!/usr/bin/python3

from datetime import datetime


import argparse

import numpy as np

# own moduls
import utilitylib as ut
import plotlib
import modelinfolib as model
model = model.icon_nest
# ---------------------------------------------------------------------------------------------------------------------

def main():
    config = ut.load_yaml('config.yml')

    # command line arguments
    parser = argparse.ArgumentParser(description="Hodograph Maps")
    # Add positional argument
    parser.add_argument('mode', type=str, 
                        help='Mode: Test, Basic, or Nixon')

    # Add optional argument
    parser.add_argument('-f', '--field', type=str, 
                        help='Which background field: CAPE ML, CAPE CON or LPI ')
    
    parser.add_argument('-d', '--date', type=str, 
                        help='Date Format YYYY-MM-DD')
    
    parser.add_argument('-fp', '--fp', type=str, 
                        help='Leadtime or forecast periode')
    
    parser.add_argument('-r', '--run', type=str, 
                        help='Run (0,6,12,18,.. .etc)')

    # Parse the command line arguments
    args = parser.parse_args()

    if args.field == None:
        args.field = "CAPE ML"

    if (args.field != "CAPE ML") and (args.field != "CAPE CON") and (args.field != "LPI"):
        print("Unknown field")
        exit(-1)

    if args.date == None:
        rundate = datetime.strptime(config["default_date"], "%Y-%m-%d")
    else:
        rundate = datetime.strptime(args.date, "%Y-%m-%d")

    if args.fp == None:
        fp = config["fp"]
    else:
        fp = args.fp

    if args.run == None:
        run = config["run"]
    else:
        run = args.run

    # replace space with underscores
    fieldname = args.field.replace(" ", "_")


    
    print(f"\nDate: {rundate}\n Arguments: {args} \nConfig-File: {config}\n\n")

    #ut.download_nwp(fieldname, datum="20240227", run="00", fp=0, store_path="./")


    
    if args.mode == "Test":
        cape_fld, lats, lons = ut.open_gribfile_single(fieldname, rundate, run, fp, path="./iconnest/")
        assert cape_fld.shape == (model.getnlat, model.getnlon), "Shape inconsistency"
        plotlib.test_plot (cape_fld, lats, lons, fp, run, titel='CAPE')
    else:
        cape_fld, lats, lons = ut.open_gribfile_single(fieldname, rundate, run, fp, path="./iconnest/")

        steps=config["steps"]
        nlvl = int(model.getnlev()/steps)
        u_fld = np.empty(nlvl*model.getpoints()).reshape((nlvl, model.getnlat(), model.getnlon()))
        u_fld.fill(np.nan)
        v_fld = np.empty(nlvl*model.getpoints()).reshape((nlvl, model.getnlat(), model.getnlon()))
        v_fld.fill(np.nan)
        
        if config["levels"][0] > config["levels"][1]:
            steps *= -1
        elif config["levels"][0] == config["levels"][1]:
            print("Wrong levels in config.yml!")
            exit(0)

        lvl_idx = 0
        for level in range(config["levels"][0], config["levels"][1], steps):
            u_fld[lvl_idx,:,:] = ut.open_gribfile_multi("U", level, rundate, run, fp, path="./iconnest/")
            v_fld[lvl_idx,:,:] = ut.open_gribfile_multi("V", level, rundate, run, fp, path="./iconnest/")

            lvl_idx += 1
            if lvl_idx >= nlvl:
                break
    
        print(np.nanmean(u_fld, axis=(1,2)))

        plotlib.basic_plot (cape_fld, u_fld, v_fld, lats, lons, 9, 0, titel='CAPE', threshold=config["threshold"])



if __name__ == "__main__":
    main()

