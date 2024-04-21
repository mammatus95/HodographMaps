#!/usr/bin/python3

from datetime import datetime


import argparse

import numpy as np

# own moduls
import utilitylib as ut
import plotlib
import modelinfolib as model

# ---------------------------------------------------------------------------------------------------------------------------


def run(model_obj, fp):
    config = ut.load_yaml('config.yml')

    if model_obj.getname() == "IFS" or model_obj.getname() == "GFS":
        cape_fld, u_fld, v_fld, lats, lons = ut.open_gribfile_preslvl(model_obj, fp, path="./modeldata/")

        print(np.nanmean(u_fld, axis=(1, 2)))
        plotlib.basic_plot(model_obj, cape_fld, u_fld, v_fld, lats, lons, fp,
                           threshold=config["threshold"])
    else:
        # program_mode
        program_mode = config["program_mode"]

        # replace space with underscores
        fieldname = "CAPE_ML"  # args.field.replace(" ", "_")
        rundate = model_obj.getrundate()
        if program_mode == "Test":
            cape_fld, lats, lons = ut.open_gribfile_single(fieldname, rundate, model_obj.getrun(), fp, path="./modeldata/")
            assert cape_fld.shape == (model_obj.getnlat(), model_obj.getnlon()), "Shape inconsistency"
            plotlib.test_plot(cape_fld, lats, lons, fp, model_obj.getrun(), titel='CAPE')

        elif program_mode == "Basic":
            cape_fld, lats, lons = ut.open_gribfile_single(fieldname, rundate, model_obj.getrun(), fp, path="./modeldata/")

            nlvl = int(model_obj.getnlev())
            u_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
            u_fld.fill(np.nan)
            v_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
            v_fld.fill(np.nan)

            lvl_idx = 0
            pres_levels = model_obj.getlevels()
            for level in pres_levels:
                u_fld[lvl_idx, :, :] = ut.open_icon_gribfile_preslvl("U", level, rundate, model_obj.getrun(),
                                                                     fp, path="./modeldata/")
                v_fld[lvl_idx, :, :] = ut.open_icon_gribfile_preslvl("V", level, rundate, model_obj.getrun(),
                                                                     fp, path="./modeldata/")

                lvl_idx += 1
                if lvl_idx >= nlvl:
                    break

            print(np.nanmean(u_fld, axis=(1, 2)))
            plotlib.basic_plot(model_obj, cape_fld, u_fld, v_fld, lats, lons, fp,
                               threshold=config["threshold"])
            plotlib.basic_plot_custarea(model_obj, cape_fld, u_fld, v_fld, lats, lons, fp,
                                        threshold=config["threshold"])
        else:
            print("Wrong command line argument")
            exit(-1)

# ---------------------------------------------------------------------------------------------------------------------------


def main():
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

    if args.date is None:
        model_obj.setrundate(datetime.strptime(run_config["default_date"], "%Y-%m-%d"))
    else:
        model_obj.setrundate(datetime.strptime(args.date, "%Y-%m-%d"))

    if args.fp is None:
        fp = run_config["fp"]
    else:
        fp = args.fp

    if args.run is None:
        model_obj.setrun(run_config["run"])
    else:
        model_obj.setrun(args.run)

    print(f"\nArguments: {args}\n{model_obj}")

    run(model_obj, fp)

# ---------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
