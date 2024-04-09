#!/usr/bin/python3
import os

import numpy as np

path_icon = './'

if (os.getcwd() != path_icon):
    os.chdir(path_icon)


def creategridinfo(d_grad=0.0625, filename="gitter_icon"):
    lonmin = -23.5
    lonmax = 45.0
    latmin = 29.5
    latmax = 70.5
    xsize = np.size(np.arange(lonmin, lonmax+d_grad, d_grad))
    ysize = np.size(np.arange(latmin, latmax+d_grad, d_grad))
    test_string = (f"#\n# gridID 1\n#\ngridtype  = lonlat\ngridsize  = {xsize*ysize}\nxname     = lon\nxlongname = longitude"
                   f"\nxunits    = degrees_east\nyname     = lat\nylongname = latitude\nyunits    = degrees_north"
                   f"\nxsize     = {xsize}\nysize     = {ysize}\nxfirst    = -23.5\nxinc      = {d_grad}\n"
                   f"yfirst    = 29.5\nyinc      = {d_grad}"
                   )
    fd = open(filename, "x")
    fd.write(test_string)
    fd.close()


creategridinfo()
creategridinfo(d_grad=0.12, filename="gitter_icon1.2")
creategridinfo(d_grad=0.2, filename="gitter_icon2")
