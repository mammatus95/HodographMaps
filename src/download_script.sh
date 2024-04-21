#!/bin/bash

source /etc/profile

conda activate HodographMaps

store_path=$(pwd)/modeldata

# create nwp directory and if not there a output images directory
mkdir -p ${store_path}
mkdir -p ./images

# select run
R=0
# Path of the icon nest on the opendata-sever
model_pfad=https://opendata.dwd.de/weather/nwp/icon-eu/grib/$(printf "%02d" "$R")
# date
D=$(date +"%Y%m%d")

echo "ICON EU NEST Run: " ${R}
echo "Date: " $(date)
echo "--------------------------------"


#######################################################################
# name of the model files
regular_single=icon-eu_europe_regular-lat-lon_single-level_${D}$(printf "%02d" "$R")_
regular_pressure=icon-eu_europe_regular-lat-lon_pressure-level_${D}$(printf "%02d" "$R")_
regular_model=icon-eu_europe_regular-lat-lon_model-level_${D}$(printf "%02d" "$R")_
invariant=icon-eu_europe_regular-lat-lon_time-invariant_${D}$(printf "%02d" "$R")_

for X in  15 #9 12 15 18 21 24 27 30 33 36 39 42 45 48 51 54 57 60
do
  T=$(printf "%03d" "$X")
  # single level
  for N in CAPE_ML CAPE_CON PS
  do
    typeset -l nvar
    nvar=${N}
    wget -q ${model_pfad}/${nvar}/${regular_single}${T}_${N}.grib2.bz2 -P ${store_path}
    bzip2 -dfq ${store_path}/${regular_single}${T}_${N}.grib2.bz2
  done

  for H in {20..74}
  do
    for N in U V T QV P
    do
      typeset -l nvar
      nvar=${N}
      wget -q ${model_pfad}/${nvar}/${regular_model}${T}_${H}_${N}.grib2.bz2 -P ${store_path}
      bzip2 -dfq ${store_path}/${regular_model}${T}_${H}_${N}.grib2.bz2
    done
  done

  # write run.yml
  echo run: ${R} > run.yml
  echo fp: ${X} >> run.yml
  echo default_date: \"$(date +%Y-%m-%d)\" >> run.yml

  # runt python script
  python3 main.py Basic
  # python3 main.py Basic --fp ${X} --run ${R} --date $(date +%Y-%m-%d)

  echo "done with leadtime ${T}h on $(date)"
done

# remove nwp files
# rm -rf ${store_path}
