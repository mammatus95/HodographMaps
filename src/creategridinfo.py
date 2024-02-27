#!/usr/bin/python3
import os

import numpy as np

path_icon='./'

if (os.getcwd() != path_icon):
    os.chdir(path_icon)

def creategridinfo(d_grad=0.0625, filename="gitter_icon"):
    lonmin = -23.5
    lonmax =  45.0
    latmin =  29.5
    latmax =  70.5
    xsize=np.size(np.arange(lonmin, lonmax+d_grad, d_grad))
    ysize=np.size(np.arange(latmin, latmax+d_grad, d_grad))
    test_string='#\n# gridID 1\n#\ngridtype  = lonlat\ngridsize  = %d\nxname     = lon\nxlongname = longitude\nxunits    = degrees_east\nyname     = lat\nylongname = latitude\nyunits    = degrees_north\nxsize     = %d\nysize     = %d\nxfirst    = -23.5\nxinc      = %.1f\nyfirst    = 29.5\nyinc      = %.1f' %(xsize*ysize, xsize, ysize, d_grad, d_grad)
    fd = open(filename, "x") 
    fd.write(test_string)
    fd.close()

creategridinfo()
creategridinfo(d_grad=0.12, filename="gitter_icon1.2")
creategridinfo(d_grad=0.2, filename="gitter_icon2")
