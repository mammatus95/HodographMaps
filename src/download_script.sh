#!/bin/bash

# run
# conda activate HodographMaps
# first!

# change configuration here
R=0 # select run 0 or 12z
D=$(date +"%Y%m%d") # date in format YYYYMMDD
D=20240502 # date in format YYYYMMDD

echo "Hodograph Maps"
echo "Script configurations:"
echo "Model run: " ${R}
echo "Date: " ${D}
echo "Today Date: " $(date)
echo "--------------------------------"

#######################################################################
# load bash profile
source /etc/profile

store_path=$(pwd)/modeldata

# create nwp directory and if not there a output images directory
mkdir -p ${store_path}
mkdir -p ./images


# Path of the icon nest on the opendata-sever
icon_model_pfad=https://opendata.dwd.de/weather/nwp/icon-eu/grib/$(printf "%02d" "$R")
# Path the ifs on the opendata-sever
ifs_model_pfad=https://data.ecmwf.int/forecasts #/20240406/00z/ifs/0p4-beta/oper/
# Path the gfs on the opendata-sever
gfs_model_pfad=https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod


#######################################################################
# name of the model files
icon_single=icon-eu_europe_regular-lat-lon_single-level_${D}$(printf "%02d" "$R")_
icon_pressure=icon-eu_europe_regular-lat-lon_pressure-level_${D}$(printf "%02d" "$R")_



for fp in  3 #9 12 15 18 21 24 27 30 33 36 39 42 45 48 51 54 57 60
do
  echo "Start downloading fp" ${fp}
  T=$(printf "%03d" "$fp")
  # single level
  for N in CAPE_ML CAPE_CON PS
  do
    typeset -l nvar
    nvar=${N}
    wget -q ${icon_model_pfad}/${nvar}/${icon_single}${T}_${N}.grib2.bz2 -P ${store_path}
    bzip2 -dfq ${store_path}/${icon_single}${T}_${N}.grib2.bz2
  done

  for H in 1000 950 925 900 875 850 825 800 775 700 600 500 400 300 250 200
  do
    for N in U V
    do
      typeset -l nvar
      nvar=${N}
      wget -q ${icon_model_pfad}/${nvar}/${icon_pressure}${T}_${H}_${N}.grib2.bz2 -P ${store_path}
      bzip2 -dfq ${store_path}/${icon_pressure}${T}_${H}_${N}.grib2.bz2
    done
  done

  # ifs
  ifs_file=${ifs_model_pfad}/${D}/$(printf "%02d" "$R")z/ifs/0p25/oper/${D}$(printf "%02d" "$R")0000-${fp}h-oper-fc.grib2
  ifs_index=${ifs_model_pfad}/${D}/$(printf "%02d" "$R")z/ifs/0p25/oper/${D}$(printf "%02d" "$R")0000-${fp}h-oper-fc.index
  wget ${ifs_file} -P ${store_path}/
  wget ${ifs_index} -P ${store_path}/
  mv ${store_path}/${D}$(printf "%02d" "$R")0000-${fp}h-oper-fc.grib2 ${store_path}/ifs_$(printf "%02d" "$R")z_${D}_f${T}.grib2
  mv ${store_path}/${D}$(printf "%02d" "$R")0000-${fp}h-oper-fc.index ${store_path}/ifs_$(printf "%02d" "$R")z_${D}_f${T}.index
    
  # gfs
  gfs_file=${gfs_model_pfad}/gfs.${D}/$(printf "%02d" "$R")/atmos/gfs.t$(printf "%02d" "$R")z.pgrb2.0p25.f${T}
  wget ${gfs_file} -P ${store_path}/
  mv ${store_path}/gfs.t$(printf "%02d" "$R")z.pgrb2.0p25.f${T} ${store_path}/gfs_$(printf "%02d" "$R")z_${D}_f${T}.grib2
  # Plot Hodograph
  # write run.yml configuration
  echo run: ${R} > run.yml
  echo fp: ${fp} >> run.yml
  echo default_date: \"$(date +%Y-%m-%d)\" >> run.yml

  echo "Plot Hodograph Maps"
  # run python script

  python3 main.py IFS
  python3 main.py GFS
  python3 main.py ICON

  echo "done with leadtime ${T}h on $(date)"
done

# remove nwp files
rm -rf ${store_path}
