#!/usr/bin/python3

from datetime import datetime


import argparse

import numpy as np

# own moduls
import utilitylib as ut
import plotlib
import modelinfolib as model

# ---------------------------------------------------------------------------------------------------------------------


def run(model_obj, program_mode, fieldname, fp):
    config = ut.load_yaml('config.yml')

    if program_mode == "Test":
        cape_fld, lats, lons = ut.open_gribfile_single(model_obj, fieldname, fp, path="./modeldata/")
        assert cape_fld.shape == (model_obj.getnlat(), model_obj.getnlon()), "Shape inconsistency"
        plotlib.test_plot(model_obj, cape_fld, lats, lons, fp)

    elif program_mode == "Sounding":
        cape_fld, lats, lons = ut.open_gribfile_single(model_obj, fieldname, fp, path="./modeldata/")

        steps = config["steps"]
        nlvl = int(model_obj.getnlev()/steps)
        t_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
        t_fld.fill(np.nan)
        q_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
        q_fld.fill(np.nan)
        p_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
        p_fld.fill(np.nan)

        if config["levels"][0] > config["levels"][1]:
            steps *= -1
        elif config["levels"][0] == config["levels"][1]:
            print("Wrong levels in config.yml!")
            exit(0)

        lvl_idx = 0
        for level in range(config["levels"][0], config["levels"][1], steps):
            t_fld[lvl_idx, :, :] = ut.open_gribfile_multi(model_obj, "T", level, fp, path="./modeldata/")
            q_fld[lvl_idx, :, :] = ut.open_gribfile_multi(model_obj, "QV", level, fp, path="./modeldata/")
            p_fld[lvl_idx, :, :] = ut.open_gribfile_multi(model_obj, "P", level, fp, path="./modeldata/")

            lvl_idx += 1
            if lvl_idx >= nlvl:
                break

        print(np.nanmean(t_fld, axis=(1, 2))-273.15)
        plotlib.sounding_plot(model_obj, cape_fld, t_fld, q_fld, p_fld, lats, lons, fp)
    elif program_mode == "Basic":
        cape_fld, lats, lons = ut.open_gribfile_single(model_obj, fieldname, fp, path="./modeldata/")

        steps = config["steps"]
        nlvl = int(model_obj.getnlev()/steps)
        u_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
        u_fld.fill(np.nan)
        v_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
        v_fld.fill(np.nan)

        if config["levels"][0] > config["levels"][1]:
            steps *= -1
        elif config["levels"][0] == config["levels"][1]:
            print("Wrong levels in config.yml!")
            exit(0)

        lvl_idx = 0
        for level in range(config["levels"][0], config["levels"][1], steps):
            u_fld[lvl_idx, :, :] = ut.open_gribfile_multi(model_obj, "U", level, fp, path="./modeldata/")
            v_fld[lvl_idx, :, :] = ut.open_gribfile_multi(model_obj, "V", level, fp, path="./modeldata/")

            lvl_idx += 1
            if lvl_idx >= nlvl:
                break

        print(np.nanmean(u_fld, axis=(1, 2)))
        plotlib.basic_plot(model_obj, cape_fld, u_fld, v_fld, lats, lons, fp,
                           threshold=config["threshold"])
        plotlib.basic_plot_custarea(model_obj, cape_fld, u_fld, v_fld, lats, lons, fp,
                                    threshold=config["threshold"])
    elif program_mode == "Nixon":
        cape_fld, lats, lons = ut.open_gribfile_single(model_obj, fieldname, fp, path="./modeldata/")

        steps = config["steps"]
        nlvl = int(model_obj.getnlev()/steps)
        u_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
        u_fld.fill(np.nan)
        v_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
        v_fld.fill(np.nan)
        h_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
        h_fld.fill(np.nan)
        p_fld = np.empty(nlvl*model_obj.getpoints()).reshape((nlvl, model_obj.getnlat(), model_obj.getnlon()))
        p_fld.fill(np.nan)

        if config["levels"][0] > config["levels"][1]:
            steps *= -1
        elif config["levels"][0] == config["levels"][1]:
            print("Wrong levels in config.yml!")
            exit(0)

        lvl_idx = 0
        for level in range(config["levels"][0], config["levels"][1], steps):
            u_fld[lvl_idx, :, :] = ut.open_gribfile_multi(model_obj, "U", level, fp, path="./modeldata/")
            v_fld[lvl_idx, :, :] = ut.open_gribfile_multi(model_obj, "V", level, fp, path="./modeldata/")
            h_fld[lvl_idx, :, :] = ut.open_gribfile_multi(model_obj, "H", level, fp, path="./modeldata/")
            p_fld[lvl_idx, :, :] = ut.open_gribfile_multi(model_obj, "P", level, fp, path="./modeldata/")

            lvl_idx += 1
            if lvl_idx >= nlvl:
                break

        print(np.nanmean(p_fld, axis=(1, 2)))

        du = np.subtract(u_fld[30, :, :], u_fld[0, :, :])
        dv = np.subtract(v_fld[30, :, :], v_fld[0, :, :])
        dls_fld = np.sqrt(np.add(np.square(du), np.square(dv)))
        plotlib.nixon_proj(model_obj, cape_fld, dls_fld, u_fld, v_fld, p_fld, h_fld, lats, lons, fp, imfmt="png")
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
    parser.add_argument('mode', type=str,
                        help='Mode: Test, Basic, Sounding, or Nixon')

    # Add optional argument
    parser.add_argument('-f', '--field', type=str,
                        help='Which background field: CAPE ML, CAPE CON or LPI ')

    parser.add_argument('-d', '--date', type=str,
                        help='Date Format YYYY-MM-DD')

    parser.add_argument('-fp', '--fp', type=str,
                        help='Leadtime or forecast periode')

    parser.add_argument('-r', '--run', type=str,
                        help='Run (0,6,12,18,.. .etc)')

    parser.add_argument('-m', '--model', type=str,
                        help='--model: ICON, IFS, or GFS')

    # Parse the command line arguments
    args = parser.parse_args()

    if args.field is None:
        args.field = "CAPE ML"

    if (args.field != "CAPE ML") and (args.field != "CAPE CON") and (args.field != "LPI") and (args.field != "WMAXSHEAR"):
        print("Unknown field")
        exit(-1)

    if args.model is None:
        model_obj = model.MODELIFNO("ICON EU", 1377, 657, 0.0625, 54, "pres")
    elif "ICON" in args.model:
        model_obj = model.icon_nest
    # elif args.model == "IFS":
    #     model_obj = model.ifs
    # elif args.model == "GFS":
    #    model_obj = model.gfs
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

    if args.mode != "Test" and args.mode != "Sounding" and args.mode != "Basic" and args.mode != "Nixon":
        print("Unknown Mode. Exit program.")
        exit(0)
    else:
        program_mode = args.mode

    # replace space with underscores
    fieldname = args.field.replace(" ", "_")

    print(f"\nArguments: {args}\n{model_obj}")
    run(model_obj, program_mode, fieldname, fp)

# ---------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
