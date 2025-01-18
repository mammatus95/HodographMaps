#!/usr/bin/python3
import numpy as np

# matplotlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap  # BoundaryNorm,

# cartopy
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
states_provinces = cfeature.NaturalEarthFeature(category='cultural', name='admin_0_boundary_lines_land',
                                                scale='10m', facecolor='none')

# own moduls
import src.utilitylib as ut
import src.meteolib as met

# ---------------------------------------------------------------------------------------------------------------------
# create plot class
# =====================================================================================================================
# https://scitools.org.uk/cartopy/docs/v0.16/crs/projections.html#cartopy-projections


config = ut.load_yaml('config.yml')
fontsize = config["fontsize"]
titlesize = config["titlesize"]

# ---------------------------------------------------------------------------------------------------------------------

def ce_states(hour, start, datetime_obj, projection=crs.EuroPP(), lon1=1.56, lon2=18.5, lat1=45.2, lat2=56.4):
    fig, ax = plt.subplots(figsize=(11, 9), subplot_kw=dict(projection=projection))
    plt.subplots_adjust(left=0.05, right=0.99, bottom=0.05, top=0.95)
    ax.set_extent([lon1, lon2, lat1, lat2])
    ax.coastlines('10m', linewidth=1.2)
    ax.add_feature(states_provinces, edgecolor='black')
    string1, string2 = ut.datum(hour, start, datetime_obj)
    plt.annotate(string1, xy=(0.82, 1.01), xycoords='axes fraction', fontsize=fontsize)
    plt.annotate(string2, xy=(0, 1.01), xycoords='axes fraction', fontsize=fontsize)
    return fig, ax


def customize_area(hour, start, datetime_obj, projection=crs.EuroPP(), lon1=10.7, lon2=18, lat1=49.8, lat2=54.8):
    fig, ax = plt.subplots(figsize=(11, 9), subplot_kw=dict(projection=projection))
    plt.subplots_adjust(left=0.05, right=0.99, bottom=0.1, top=0.95)
    ax.set_extent([lon1, lon2, lat1, lat2])
    ax.coastlines('10m', linewidth=1.2)
    ax.add_feature(states_provinces, edgecolor='black')
    string1, string2 = ut.datum(hour, start, datetime_obj)
    plt.annotate(string1, xy=(0.82, 1.01), xycoords='axes fraction', fontsize=fontsize)
    plt.annotate(string2, xy=(0, 1.01), xycoords='axes fraction', fontsize=fontsize)
    return fig, ax


# ---------------------------------------------------------------------------------------------------------------------
# create colormap for CAPE field
clevs = np.array([50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
                  1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000])
# cmap = LinearSegmentedColormap.from_list("", ["green", "yellow", "orange", "red", "darkred", "darkmagenta"])
cmap = LinearSegmentedColormap.from_list("", ["yellowgreen", "gold", "orange", "red"])
cmap = ListedColormap(cmap(np.linspace(0, 1, 256))[4:240])
# ---------------------------------------------------------------------------------------------------------------------

def test_plot(hour, run, model_obj, titel='TEST'):
    """
    Parameters:
    ------------
    hour       :
    run        :

    Returns:
    --------
    None
    """

    _, _ = ce_states(hour, run, model_obj.getrundate(), projection=crs.PlateCarree())
    plt.title(titel, fontsize=titlesize)

    name = f"test_ce_{hour}.png"
    plt.savefig(name)
    plt.close()

# ---------------------------------------------------------------------------------------------------------------------


def cape_plot(cape_fld, lats, lons, hour, run, rundate, titel='CAPE'):
    """
    Parameters:
    ------------
    cape_fld   : CAPE field
    lat        :
    lon        :
    hour       :
    run        :

    Returns:
    --------
    None
    """

    fig, ax = ce_states(hour, run, rundate, projection=crs.PlateCarree())
    plt.title(titel, fontsize=titlesize)

    wx = ax.contourf(lons, lats, cape_fld[:, :], levels=clevs, transform=crs.PlateCarree(),
                     cmap=cmap, extend='max', alpha=0.4, antialiased=True)

    cax = fig.add_axes([0.27, 0.05, 0.35, 0.05])
    fig.colorbar(wx, cax=cax, orientation='horizontal')

    name = f"testcape_ce_{hour}.png"
    plt.savefig(name)
    plt.close()

# ---------------------------------------------------------------------------------------------------------------------


def hodopoint(point, u, v, pres_levels, ax, width=0.1, clim=50, proj='polar', smooth=False):
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

    wdir, spd = met.uv2spddir_rad(u, v)
    wdir -= np.pi

    # smoothing
    if smooth is True:
        wdir[1:] = (wdir[1:] + wdir[:-1])/2
        spd[1:] = (spd[1:] + spd[:-1])/2

    # draw part of second cricle
    if np.max(spd[4:]) > 28:
        u_mean = np.mean(u[np.where(spd > 27)])
        v_mean = np.mean(v[np.where(spd > 27)])
        wdir_mean = met.uv2spddir_rad(u_mean, v_mean)[0] - np.pi
        ax2.plot(np.linspace(wdir_mean-np.pi/8,
                             wdir_mean+np.pi/8, 100),
                 np.zeros(100)+30, '-k', alpha=.3, lw=0.8)
    # plot data
    idx_low = pres_levels.index(850)
    idx_mid = pres_levels.index(600)
    ax2.plot(wdir[:idx_low+1:1], spd[:idx_low+1:1], '-', color='darkmagenta', lw=1.5)
    ax2.plot(wdir[idx_low:idx_mid+1:1], spd[idx_low:idx_mid+1:1], '-', color='navy', lw=1.5)
    ax2.plot(wdir[idx_mid:], spd[idx_mid:], '-', color='darkgreen', lw=1.5)
    ax2.scatter(0, 0, c="k", s=10, marker='x', alpha=0.75)

# ---------------------------------------------------------------------------------------------------------------------


def basic_plot(model_obj, cape_fld, u, v, lats, lons, hour, threshold=10., imfmt="png", parcel="ML"):
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
    threshold = -1
    pres_levels = model_obj.getlevels()
    model_name = model_obj.getname()
    start = model_obj.getrun()

    fig, ax = ce_states(hour, start, model_obj.getrundate(), projection=crs.PlateCarree())
    plt.title(model_obj.create_plottitle(), fontsize=titlesize)

    wx = ax.contourf(lons, lats, cape_fld[:, :], levels=clevs, transform=crs.PlateCarree(), cmap=cmap,
                     extend='max', alpha=0.4, antialiased=True)

    for i in model_obj.hodo_interval_lat:
        for j in model_obj.hodo_interval_lon:
            if np.mean(cape_fld[i-1:i+1, j-1:j+1]) > threshold:
                hodopoint((lons[i, j], lats[i, j]),
                          np.mean(u[:, i-1:i+1, j-1:j+1], axis=(1, 2)),
                          np.mean(v[:, i-1:i+1, j-1:j+1], axis=(1, 2)), pres_levels, ax, width=0.1)  # proj=crs.PlateCarree()

    cax = fig.add_axes([0.44, 0.03, 0.35, 0.05])
    fig.colorbar(wx, cax=cax, orientation='horizontal')

    ax.annotate(f"CAPE {parcel}(contour plot)", xy=(0.8, -0.07), xycoords='axes fraction', fontsize=14)
    ax.annotate(r'in $J/kg$', xy=(0.8, -0.1), xycoords='axes fraction', fontsize=14)

    ax.annotate('1000-850 hPa in magenta', xy=(0.02, -0.03), xycoords='axes fraction', fontsize=13)
    ax.annotate(' 850-600 hPa in blue', xy=(0.02, -0.06), xycoords='axes fraction', fontsize=13)
    ax.annotate(' 600-300 hPa in green', xy=(0.02, -0.09), xycoords='axes fraction', fontsize=13)
    ax.annotate("grey circles are 10 and 30m/s", xy=(0.02, -0.12), xycoords='axes fraction', fontsize=13)

    name = f"./images/hodographmap_{model_name.replace(' ', '_')}_{hour}.{imfmt}"
    plt.savefig(name)
    plt.close()


def basic_plot_custarea(model_obj, cape_fld, lpi_fld, u, v, lats, lons, hour, threshold=10., imfmt="png"):
    pres_levels = model_obj.getlevels()
    model_name = model_obj.getname()
    start = model_obj.getrun()
    lon1 = config["customize"]["lon1"]
    lon2 = config["customize"]["lon2"]
    lat1 = config["customize"]["lat1"]
    lat2 = config["customize"]["lat2"]
    fig, ax = customize_area(hour, start, model_obj.getrundate(), model_name,
                             projection=crs.PlateCarree(), lon1=lon1, lon2=lon2, lat1=lat1, lat2=lat2)
    plt.title(model_obj.create_plottitle(), fontsize=titlesize)

    wx = ax.contourf(lons, lats, cape_fld[:, :], levels=clevs, transform=crs.PlateCarree(),
                     cmap=cmap, extend='max', alpha=0.4, antialiased=True)

    # LPI contours
    lpi_levs = np.array([50, 500])
    cs = plt.contour(lons, lats, lpi_fld[:,:], levels=lpi_levs, transform=crs.PlateCarree(), colors='darkred', linewidths=1.4)
    fmt = '%.f'
    plt.clabel(cs, fontsize=9, inline=1, fmt=fmt)

    for i in range(340, 400, 5):
        for j in range(555, 665, 5):
            if np.mean(cape_fld[i-1:i+1, j-1:j+1]) > threshold:
                hodopoint((lons[i, j], lats[i, j]),
                          np.mean(u[:, i-1:i+1, j-1:j+1], axis=(1, 2)),
                          np.mean(v[:, i-1:i+1, j-1:j+1], axis=(1, 2)), pres_levels, ax, width=0.1)  # proj=crs.PlateCarree()

    cax = fig.add_axes([0.44, 0.03, 0.35, 0.05])
    fig.colorbar(wx, cax=cax, orientation='horizontal')

    ax.annotate("CAPE ML(contour plot)", xy=(0.8, -0.03), xycoords='axes fraction', fontsize=14)
    ax.annotate(r'in $J/kg$', xy=(0.8, -0.06), xycoords='axes fraction', fontsize=14)
    ax.annotate("LPI (darkred contours)", xy=(0.8, -0.1), xycoords='axes fraction', fontsize=14)

    ax.annotate('1000-850 hPa in magenta', xy=(0.02, -0.025), xycoords='axes fraction', fontsize=13)
    ax.annotate(' 850-600 hPa in blue', xy=(0.02, -0.05), xycoords='axes fraction', fontsize=13)
    ax.annotate(' 600-300 hPa in green', xy=(0.02, -0.075), xycoords='axes fraction', fontsize=13)
    ax.annotate("grey circles are 10 and 30m/s", xy=(0.02, -0.11), xycoords='axes fraction', fontsize=13)

    name = f"./images/hodographmap_area_{model_name.replace(' ', '_')}_{hour}.{imfmt}"
    if imfmt == "png":
        plt.savefig(name, dpi=800)
    else:
        plt.savefig(name)
    plt.close()
