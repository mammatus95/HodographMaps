#!/usr/bin/python3

from datetime import datetime


import argparse

import numpy as np

# own moduls
import utilitylib as ut
import plotlib
import modelinfolib as model

# ---------------------------------------------------------------------------------------------------------------------


def run(model_obj, program_mode, fieldname, rundate, model_run, fp):
    config = ut.load_yaml('config.yml')
    print(model_obj)
    if program_mode == "Test":
        cape_fld, lats, lons = ut.open_gribfile_single(fieldname, rundate, model_run, fp, path="./modeldata/")
        assert cape_fld.shape == (model_obj.getnlat(), model_obj.getnlon()), "Shape inconsistency"
        plotlib.test_plot(cape_fld, lats, lons, fp, model_run, titel='CAPE')

    elif program_mode == "Basic":
        cape_fld, lats, lons = ut.open_gribfile_single(fieldname, rundate, model_run, fp, path="./modeldata/")

        nlvl = int(model_obj.getnlev())
        u_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
        u_fld.fill(np.nan)
        v_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
        v_fld.fill(np.nan)

        lvl_idx = 0
        pres_levels = model_obj.getlevels()
        for level in pres_levels:
            u_fld[lvl_idx, :, :] = ut.open_icon_gribfile_preslvl("U", level, rundate, model_run, fp, path="./modeldata/")
            v_fld[lvl_idx, :, :] = ut.open_icon_gribfile_preslvl("V", level, rundate, model_run, fp, path="./modeldata/")

            lvl_idx += 1
            if lvl_idx >= nlvl:
                break

        print(np.nanmean(u_fld, axis=(1, 2)))
        plotlib.basic_plot(cape_fld, u_fld, v_fld, pres_levels, lats, lons, fp, model_run,
                           titel='CAPE', threshold=config["threshold"])
        plotlib.basic_plot_custarea(cape_fld, u_fld, v_fld, pres_levels, lats, lons, fp, model_run,
                                    titel='CAPE', threshold=config["threshold"])
    else:
        print("Wrong command line argument")
        exit(-1)

# ---------------------------------------------------------------------------------------------------------------------


def main():
    config = ut.load_yaml('config.yml')
    run_config = ut.load_yaml('run.yml')

    # command line arguments
    parser = argparse.ArgumentParser(description="Hodograph Maps")
    # Add positional argument
    parser.add_argument('Model', type=str,
                        help='Model: ICON, IFS, or GFS')

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

    if args.field is None:
        args.field = "CAPE ML"

    if (args.field != "CAPE ML") and (args.field != "CAPE CON") and (args.field != "LPI") and (args.field != "WMAXSHEAR"):
        print("Unknown field")
        exit(-1)

    if args.date is None:
        rundate = datetime.strptime(run_config["default_date"], "%Y-%m-%d")
    else:
        rundate = datetime.strptime(args.date, "%Y-%m-%d")

    if args.fp is None:
        fp = run_config["fp"]
    else:
        fp = args.fp

    if args.run is None:
        model_run = run_config["run"]
    else:
        model_run = args.run

    if args.Model is None:
        model_obj = model.MODELIFNO("ICON EU", 1377, 657, 0.0625, "pres")
    elif "ICON" in args.Model:
        model_obj = model.icon_nest
    elif args.Model == "IFS":
        model_obj = model.ifs
    elif args.Model == "GFS":
        model_obj = model.gfs
    else:
        print("Unkown model! Exit.")
        exit(0)

    # program_mode
    program_mode = config["program_mode"]

    # replace space with underscores
    fieldname = args.field.replace(" ", "_")

    print(f"\nDate: {rundate}\n Arguments: {args} \nConfig-File: {config}\n\n")

    run(model_obj, program_mode, fieldname, rundate, model_run, fp)

# ---------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
