#!/usr/bin/python3
from copy import deepcopy

import numpy as np

# matplotlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap  # ListedColormap, BoundaryNorm,
from matplotlib.projections import register_projection

# cartopy
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural', name='admin_0_boundary_lines_land', scale='10m', facecolor='none')

# own moduls
import utilitylib as ut
import meteolib as met
from skewT import SkewXAxes

# ---------------------------------------------------------------------------------------------------------------------
# create plot class
# =====================================================================================================================
# https://scitools.org.uk/cartopy/docs/v0.16/crs/projections.html#cartopy-projections


config = ut.load_yaml('config.yml')
fontsize = config["fontsize"]
titlesize = config["titlesize"]


def eu_merc(hour, start, projection=crs.Mercator(), factor=3):
    fig, ax = plt.subplots(figsize=(3*factor, 3.5091*factor), subplot_kw=dict(projection=projection))
    ax.set_extent([-10.5, 28.0, 30.5, 67.5])
    # ax.stock_img()
    ax.coastlines('50m', linewidth=1.2)
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    string1, string2 = ut.datum(hour, start)
    plt.annotate(string1, xy=(0.8, 1), xycoords='axes fraction', fontsize=fontsize)
    plt.annotate(string2, xy=(0, 1), xycoords='axes fraction', fontsize=fontsize)
    return fig, ax


def eu_states(hour, start, projection=crs.EuroPP()):
    fig, ax = plt.subplots(figsize=(9, 7), subplot_kw=dict(projection=projection))
    plt.subplots_adjust(left=0.05, right=0.97, bottom=0.05, top=0.95)
    ax.set_extent([-9.5, 33.0, 38.5, 58.5])
    ax.coastlines('50m', linewidth=1.2)
    ax.add_feature(states_provinces, edgecolor='black')
    string1, string2 = ut.datum(hour, start)
    plt.annotate("ICON Nest (DWD)", xy=(0.7, -0.04), xycoords='axes fraction', fontsize=10)
    plt.annotate(string1, xy=(0.8, 1), xycoords='axes fraction', fontsize=fontsize)
    plt.annotate(string2, xy=(0, 1), xycoords='axes fraction', fontsize=fontsize)
    return fig, ax


def ce_states(hour, start, projection=crs.EuroPP(), lon1=1.56, lon2=18.5, lat1=45.1, lat2=56.6):
    fig, ax = plt.subplots(figsize=(11, 9), subplot_kw=dict(projection=projection))
    plt.subplots_adjust(left=0.05, right=0.99, bottom=0.05, top=0.95)
    ax.set_extent([lon1, lon2, lat1, lat2])
    ax.coastlines('10m', linewidth=1.2)
    ax.add_feature(states_provinces, edgecolor='black')
    string1, string2 = ut.datum(hour, start)
    plt.annotate("ICON Nest (DWD)", xy=(0.02, -0.04), xycoords='axes fraction', fontsize=10)
    plt.annotate(string1, xy=(0.835, 1.02), xycoords='axes fraction', fontsize=fontsize)
    plt.annotate(string2, xy=(0, 1.02), xycoords='axes fraction', fontsize=fontsize)
    return fig, ax


def customize_area(hour, start, projection=crs.EuroPP(), lon1=10.7, lon2=18, lat1=49.8, lat2=54.8):
    fig, ax = plt.subplots(figsize=(11, 9), subplot_kw=dict(projection=projection))
    plt.subplots_adjust(left=0.05, right=0.99, bottom=0.1, top=0.95)
    ax.set_extent([lon1, lon2, lat1, lat2])
    ax.coastlines('10m', linewidth=1.2)
    ax.add_feature(states_provinces, edgecolor='black')
    string1, string2 = ut.datum(hour, start)
    plt.annotate("ICON Nest (DWD)", xy=(0.02, -0.04), xycoords='axes fraction', fontsize=10)
    plt.annotate(string1, xy=(0.82, 1.01), xycoords='axes fraction', fontsize=fontsize)
    plt.annotate(string2, xy=(0, 1.01), xycoords='axes fraction', fontsize=fontsize)
    return fig, ax


def alps(hour, start, projection=crs.EuroPP(), lon1=5.8, lon2=17.8, lat1=45.23, lat2=49.5):
    fig, ax = plt.subplots(figsize=(11, 9), subplot_kw=dict(projection=projection))
    ax.set_extent([lon1, lon2, lat1, lat2])
    ax.coastlines('10m', linewidth=1.2)
    ax.add_feature(states_provinces, edgecolor='black')
    string1, string2 = ut.datum(hour, start)
    plt.annotate("ICON Nest (DWD)", xy=(0.7, -0.04), xycoords='axes fraction', fontsize=10)
    plt.annotate(string1, xy=(0.8, 1), xycoords='axes fraction', fontsize=fontsize)
    plt.annotate(string2, xy=(0, 1), xycoords='axes fraction', fontsize=fontsize)
    return fig, ax


def two_plots(projection=crs.EuroPP(), lon1=3.56, lon2=16.5, lat1=46.2, lat2=55.6, fac=3):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5*fac, 3*fac), subplot_kw=dict(projection=projection))
    fig.subplots_adjust(left=0.02, right=0.92, top=0.95, bottom=0.05, wspace=0.14)
    ax1.set_extent([lon1, lon2, lat1, lat2])
    ax1.coastlines('10m', linewidth=1.2)
    ax1.add_feature(states_provinces, edgecolor='black')
    ax2.set_extent([lon1, lon2, lat1, lat2])
    ax2.coastlines('10m', linewidth=1.2)
    ax2.add_feature(states_provinces, edgecolor='black')
    plt.annotate("ICON Nest (DWD)", xy=(0.6, -0.03), xycoords='axes fraction', fontsize=fontsize)
    return fig, ax1, ax2


# ---------------------------------------------------------------------------------------------------------------------
# create colormap for CAPE field
clevs = np.array([50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
                  1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000])
cmap = LinearSegmentedColormap.from_list("", ["green", "yellow", "orange", "red", "darkred", "darkmagenta"])
cmap2 = LinearSegmentedColormap.from_list("", ["gold", "orange", "darkorange", "red", "darkred", "darkmagenta"])

# ---------------------------------------------------------------------------------------------------------------------


def test_plot(cape_fld, lats, lons, hour, run, titel='CAPE'):
    """
    Parameters:
    ------------
    cape_fld   : CAPE field
    lat        :
    lon        :
    hour       :
    run      :

    Returns:
    --------
    None
    """

    fig, ax = ce_states(hour, run, projection=crs.PlateCarree())
    plt.title(titel, fontsize=titlesize)

    wx = ax.contourf(lons, lats, cape_fld[:, :], levels=clevs, transform=crs.PlateCarree(),
                     cmap=cmap, extend='max', alpha=0.4, antialiased=True)

    cax = fig.add_axes([0.27, 0.05, 0.35, 0.05])
    fig.colorbar(wx, cax=cax, orientation='horizontal')

    name = f"test_ce_{hour}.png"
    plt.savefig(name)
    plt.close()

# ---------------------------------------------------------------------------------------------------------------------


def soundingpoint(point, temp, q, pres, ax, width=0.1, proj='skewT', smooth=False):
    """
    Parameters:
    ------------
    point : tuple of data coordinates (10, 55)
    temp  : temperature
    width : width of added axes for the soundings as fig coordinates (examples: 0.5 are half of the image)
    proj  : 'polar'

    Returns:
    --------
    None
    """
    register_projection(SkewXAxes)

    # this takes us from the data coordinates to the display coordinates.
    test = ax.transData.transform(point)

    # this should take us from the display coordinates to the axes coordinates.
    trans = ax.transAxes.inverted().transform(test)

    # create new axes
    ax2 = plt.axes([trans[0]-width/2, trans[1]-width/2, width, width])  # , projection='skewx')

    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    ax2.set_frame_on(False)

    # ax2.set_xlim(-, )
    # ax2.set_ylim(0, )

    # 10 ms circle
    # ax2.plot(np.linspace(0, 2*np.pi, 100), np.zeros(100)+10, '-k', alpha=.3, lw=0.8)
    # ax2.plot(np.linspace(0, 2*np.pi, 100), np.zeros(100)+30, '-k', alpha=.3, lw=0.8)

    # calculate dewpoint
    pres /= 100
    dewpoint = met.temp_at_mixrat(met.q_to_mixrat(q)*1000.0, pres)

    # smoothing
    if smooth is True:
        temp[1:] = (temp[1:] + temp[:-1])/2
        dewpoint[1:] = (dewpoint[1:] + dewpoint[:-1])/2

    ax2.semilogy(temp[:40:1]-met.ZEROCNK, pres[:40:1], 'b-', lw=1.5)
    ax2.semilogy(dewpoint[:40:1]-met.ZEROCNK, pres[:40:1], 'g-', lw=1.5)
    ax2.vlines(x=0, ymin=300, ymax=1000, colors='purple', ls='--', lw=0.6)  # freezing level
    ax2.set_ylim(1050, 300)
    # ax2.invert_xaxis()

# ---------------------------------------------------------------------------------------------------------------------


def sounding_plot(cape_fld, temp, q_fld, p_fld, lats, lons, hour, start, titel='CAPE', imfmt="png"):
    """
    Parameters:
    ------------
    cape_fld   : CAPE field
    temp       : temperature
    lats       :
    lons       :
    hour       :
    start      :

    Returns:
    --------
    None
    """

    fig, ax = ce_states(hour, start, projection=crs.PlateCarree())
    plt.title(titel, fontsize=titlesize)

    wx = ax.contourf(lons, lats, cape_fld[:, :], levels=clevs, transform=crs.PlateCarree(), cmap=cmap2,
                     extend='max', alpha=0.4, antialiased=True)

    for i in range(275, 415, 10):
        for j in range(420, 670, 15):
            soundingpoint((lons[i, j], lats[i, j]),
                          np.mean(temp[:, i-1:i+1, j-1:j+1], axis=(1, 2)),
                          np.mean(q_fld[:, i-1:i+1, j-1:j+1], axis=(1, 2)),
                          np.mean(p_fld[:, i-1:i+1, j-1:j+1], axis=(1, 2)),
                          ax, width=0.05)  # , proj=crs.PlateCarree()

    cax = fig.add_axes([0.27, 0.05, 0.35, 0.05])
    fig.colorbar(wx, cax=cax, orientation='horizontal')
    ax.annotate(r'$J/kg$', xy=(0.65, -0.04), xycoords='axes fraction', fontsize=14)
    ax.annotate('red dot line: freezing level', xy=(0.75, -0.1), xycoords='axes fraction', fontsize=14)
    ax.annotate('blue lines: temperature', xy=(0.75, -0.04), xycoords='axes fraction', fontsize=14)
    ax.annotate('green lines: dewpoints', xy=(0.75, -0.07), xycoords='axes fraction', fontsize=14)
    name = f"./images/soundingmap_ce_{hour}.{imfmt}"
    plt.savefig(name)
    plt.close()

# ---------------------------------------------------------------------------------------------------------------------


def hodopoint(point, u, v, ax, width=0.1, clim=40, proj='polar', smooth=False):
    """
    Parameters:
    ------------
    point : tuple of data coordinates (10, 55)
    u, v  : wind components
    width : width of added axes for the hodograph as fig coordinates (examples: 0.5 are half of the image)
    clim  : max. wind speed magnitude of the hodograph
    proj  : 'polar'

    Returns:
    --------
    None
    """
    # this takes us from the data coordinates to the display coordinates.
    test = ax.transData.transform(point)

    # this should take us from the display coordinates to the axes coordinates.
    trans = ax.transAxes.inverted().transform(test)

    # create new axes
    ax2 = plt.axes([trans[0]-width/2, trans[1]-width/2, width, width], projection=proj)

    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    ax2.set_frame_on(False)

    # ax2.set_xlim(-clim, clim)
    ax2.set_ylim(0, clim)
    ax2.set_theta_offset(np.pi/2)
    # ax2.set_theta_direction(-1)

    # 10 ms circle
    ax2.plot(np.linspace(0, 2*np.pi, 100), np.zeros(100)+10, '-k', alpha=.3, lw=0.8)
    # ax2.plot(np.linspace(0, 2*np.pi, 100), np.zeros(100)+30, '-k', alpha=.3, lw=0.8)

    # plot data
    wdir, spd = met.uv2spddir(u, v)

    # smoothing
    if smooth is True:
        wdir[1:] = (wdir[1:] + wdir[:-1])/2
        spd[1:] = (spd[1:] + spd[:-1])/2

    # draw part of second cricle
    if np.max(spd[:-20]) > 28:
        ax2.plot(np.linspace(np.mean(wdir[np.where(spd[:-20] > 25)])-np.pi/8, 
                             np.mean(wdir[np.where(spd[:-20] > 25)])+np.pi/8, 100),
                 np.zeros(100)+30, '-k', alpha=.3, lw=0.8)

    ax2.plot(wdir[:10:1], spd[:10:1], 'r-', lw=1.5)
    ax2.plot(wdir[9:21:2], spd[9:21:2], 'g-', lw=1.5)
    ax2.plot(wdir[19:-20:2], spd[19:-20:2], 'b-', lw=1.5)
    ax2.scatter(0, 0, c="k", s=10, marker='x', alpha=0.75)

# ---------------------------------------------------------------------------------------------------------------------


def basic_plot(cape_fld, u, v, lats, lons, hour, start, titel='CAPE', threshold=10., imfmt="png"):
    """
    Parameters:
    ------------
    cape_fld   : CAPE field
    u, v       : wind components
    lats       :
    lons       :
    hour       :
    start      :

    Returns:
    --------
    None
    """

    fig, ax = ce_states(hour, start, projection=crs.PlateCarree())
    plt.title(titel, fontsize=titlesize)

    wx = ax.contourf(lons, lats, cape_fld[:, :], levels=clevs, transform=crs.PlateCarree(), cmap=cmap,
                     extend='max', alpha=0.4, antialiased=True)

    for i in range(275, 415, 10):
        for j in range(420, 670, 15):
            if np.mean(cape_fld[i-1:i+1, j-1:j+1]) > threshold:
                hodopoint((lons[i, j], lats[i, j]),
                          np.mean(u[:, i-1:i+1, j-1:j+1], axis=(1, 2)),
                          np.mean(v[:, i-1:i+1, j-1:j+1], axis=(1, 2)), ax, width=0.1)  # , proj=crs.PlateCarree()

    cax = fig.add_axes([0.27, 0.05, 0.35, 0.05])
    fig.colorbar(wx, cax=cax, orientation='horizontal')

    if "CAPE" in titel:
        ax.annotate(r'$J/kg$', xy=(0.65, -0.04), xycoords='axes fraction', fontsize=14)
    else:
        ax.annotate(r'$m^2/s^2$', xy=(0.65, -0.04), xycoords='axes fraction', fontsize=14)
    ax.annotate('red: 1-10 model level', xy=(0.75, -0.04), xycoords='axes fraction', fontsize=14)
    ax.annotate('green: 10-20 model level', xy=(0.75, -0.07), xycoords='axes fraction', fontsize=14)
    ax.annotate('blue: 20-50 model level', xy=(0.75, -0.1), xycoords='axes fraction', fontsize=14)
    ax.annotate("grey circles are 10 and 30m/s", xy=(0.02, -0.07), xycoords='axes fraction', fontsize=10)

    name = f"./images/hodographmap_ce_{hour}.{imfmt}"
    plt.savefig(name)
    plt.close()


def basic_plot_custarea(cape_fld, u, v, lats, lons, hour, start, titel='CAPE', threshold=10., imfmt="png"):
    lon1 = config["customize"]["lon1"]
    lon2 = config["customize"]["lon2"]
    lat1 = config["customize"]["lat1"]
    lat2 = config["customize"]["lat2"]
    fig, ax = customize_area(hour, start, projection=crs.PlateCarree(), lon1=lon1, lon2=lon2, lat1=lat1, lat2=lat2)
    plt.title(titel, fontsize=titlesize)

    wx = ax.contourf(lons, lats, cape_fld[:, :], levels=clevs, transform=crs.PlateCarree(),
                     cmap=cmap, extend='max', alpha=0.4, antialiased=True)

    for i in range(340, 400, 5):
        for j in range(555, 665, 5):
            if np.mean(cape_fld[i-1:i+1, j-1:j+1]) > threshold:
                hodopoint((lons[i, j], lats[i, j]),
                          np.mean(u[:, i-1:i+1, j-1:j+1], axis=(1, 2)),
                          np.mean(v[:, i-1:i+1, j-1:j+1], axis=(1, 2)), ax, width=0.1)  # , proj=crs.PlateCarree()

    cax = fig.add_axes([0.27, 0.05, 0.35, 0.05])
    fig.colorbar(wx, cax=cax, orientation='horizontal')

    if "CAPE" in titel:
        ax.annotate(r'$J/kg$', xy=(0.65, -0.04), xycoords='axes fraction', fontsize=14)
    else:
        ax.annotate(r'$m^2/s^2$', xy=(0.65, -0.04), xycoords='axes fraction', fontsize=14)
    ax.annotate('red: 1-10 model level', xy=(0.75, -0.04), xycoords='axes fraction', fontsize=14)
    ax.annotate('green: 10-20 model level', xy=(0.75, -0.07), xycoords='axes fraction', fontsize=14)
    ax.annotate('blue: 20-50 model level', xy=(0.75, -0.1), xycoords='axes fraction', fontsize=14)
    ax.annotate("grey circles are 10 and 30m/s", xy=(0.02, -0.07), xycoords='axes fraction', fontsize=10)

    name = f"./images/hodographmap_area_{hour}.{imfmt}"
    plt.savefig(name)
    plt.close()

# ---------------------------------------------------------------------------------------------------------------------


def nixon_hodograph(point, u, v, p, height, ax, width=0.1, clim=40, proj='polar', smooth=False):
    """
    u, v : horizontal wind components
    rstu, rstv : storm motion vector for right mover
    """

    i = 0
    while height[i] < 500:
        i += 1
    i_500m = deepcopy(i)

    while height[i] < 5500:
        i += 1
    i_5km = deepcopy(i)
    while height[i] < 6000:
        i += 1
    i_6km = deepcopy(i)

    rstu, rstv, lstu, lstv, mwu6, mwv6 = met.non_parcel_bunkers_motion_experimental(u, v, p, i_500m, i_5km, i_6km)

    u -= rstu
    v -= rstv

    # plot
    test = ax.transData.transform(point)
    # this should take us from the display coordinates to the axes coordinates.
    trans = ax.transAxes.inverted().transform(test)
    ax2 = plt.axes([trans[0]-width/2, trans[1]-width/2, width, width], projection=proj)

    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    # ax2.patch.set_visible(False)
    ax2.set_frame_on(False)
    # ax2.set_xlim(-clim, clim)
    ax2.set_ylim(0, clim)
    ax2.set_theta_offset(np.pi/2)
    # ax2.set_theta_direction(-1)

    # 10 ms circle
    ax2.plot(np.linspace(0, 2*np.pi, 100), np.zeros(100)+10, '-k', alpha=.3, lw=0.8)

    # plot data
    wdir, spd = met.uv2spddir(u, v)

    # smoothing
    if smooth is True:
        wdir[1:] = (wdir[1:] + wdir[:-1])/2
        spd[1:] = (spd[1:] + spd[:-1])/2

    ax2.plot(wdir[:10:1], spd[:10:1], 'r-', lw=1.5)
    ax2.plot(wdir[9:21:2], spd[9:21:2], 'g-', lw=1.5)
    ax2.plot(wdir[19:-20:2], spd[19:-20:2], 'b-', lw=1.5)
    ax2.scatter(0, 0, c="k", s=2, marker='x', alpha=0.75)

    theta, mag = met.uv2spddir(rstu, rstv)
    ax2.arrow(theta, 0, 0, mag, head_width=0.1, head_length=0.1)


def nixon_proj(cape_fld, dls_fld, u, v, p, high, lats, lons, hour, start, imfmt="png"):
    """
    Nixon projection
    cape_fld : 2D cape field
    dls_fld  : 2D deep layer shear field or brn shear ...
    u, v : wind components
    high : model level high
    or
    rstu, rstv : storm motion vector
    background filed is cape ...
    only hodographs with more the 10 m/s dls
    """

    titel = 'CAPE with Hodographs'

    fig, ax = ce_states(hour, start, projection=crs.PlateCarree())
    plt.title(titel, fontsize=titlesize)

    clevs = np.array([20, 250, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500])
    # clevs = np.array([20, 50, 100, 250, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500])
    cmap = LinearSegmentedColormap.from_list("", ["green", "yellow", "orange", "red", "darkred", "darkmagenta"])

    wx = ax.contourf(lons, lats, cape_fld[:, :], levels=clevs, transform=crs.PlateCarree(),
                     cmap=cmap, extend='max', alpha=0.4)
    # cb = plt.colorbar(wx, ticks=clevs, shrink=.8)
    # cb.set_label(r'$m^2/s^2$')

    # cleves = np.array([500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000])
    # cs = plt.contour(lons, lats, wx_fld[:, :], levels=cleves, transform=crs.PlateCarree(), colors='k', linewidths=0.8)
    # plt.clabel(cs, np.array([500, 1000, 2000, 3000]), fontsize=7, inline=1, fmt='%.f') # contour labels

    for i in range(280, 410, 10):
        for j in range(420, 670, 15):
            if np.mean(dls_fld[i-1:i+1, j-1:j+1]) > 10.0 and np.mean(cape_fld[i-1:i+1, j-1:j+1]) > 10.0:  # m/s
                nixon_hodograph((lons[i, j], lats[i, j]),
                                np.mean(u[::-1, i-1:i+1, j-1:j+1], axis=(1, 2)),
                                np.mean(v[::-1, i-1:i+1, j-1:j+1], axis=(1, 2)),
                                np.mean(p[::-1, i-1:i+1, j-1:j+1], axis=(1, 2)),
                                np.mean(high[::-1, i-1:i+1, j-1:j+1], axis=(1, 2)), ax, width=0.1, proj=crs.PlateCarree())

    cax = fig.add_axes([0.27, 0.05, 0.35, 0.05])
    fig.colorbar(wx, cax=cax, orientation='horizontal')
    ax.annotate(r'$J/kg$', xy=(0.65, -0.04), xycoords='axes fraction', fontsize=14)

    ax.annotate('red: 1-10 model level', xy=(0.75, -0.04), xycoords='axes fraction', fontsize=14)
    ax.annotate('green: 10-20 model level', xy=(0.75, -0.07), xycoords='axes fraction', fontsize=14)
    ax.annotate('blue: 20-40 model level', xy=(0.75, -0.1), xycoords='axes fraction', fontsize=14)
    ax.annotate("grey circles are 10 and 30m/s", xy=(0.02, -0.07), xycoords='axes fraction', fontsize=10)

    name = f"./images/nixon_ce_{hour}.{imfmt}"
    plt.savefig(name)
    plt.close()
