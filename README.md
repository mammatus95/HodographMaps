# HodographMaps

## Installation

**Conda**

```bash
conda env create -f environment.yml

conda activate HodographMaps
```

You need to addg Conda initialization to your etc/profile, as well.

## Example Image

![Example](images/example.png)

![Map of Hodographs IFS](images/hodographmap_IFS.png)

![Map of Hodographs GFS](images/hodographmap_GFS.png)


## How to run

```bash
cd src
bash download_script.sh
conda activate HodographMaps

# Plot Hodograph
python3 main.py IFS
python3 main.py GFS
python3 main.py ICON
cd images
```

## Datasource
- [ICON Nest](https://opendata.dwd.de/weather/nwp/icon-eu/)
- [IFS](https://www.ecmwf.int/en/forecasts/datasets/open-data)
- [GFS (NOAA)](https://www.nco.ncep.noaa.gov/pmb/products/gfs/)

## Cartopy?

- https://github.com/mammatus95/cartopy
- https://scitools.org.uk/cartopy/docs/latest/#

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.
