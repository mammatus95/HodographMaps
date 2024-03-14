#!/bin/bash

#source /etc/profile

#python3=/home/mammatus95/Dokumente/miniconda3/bin/python3
#conda activate HodographMaps



store_path=$(pwd)/iconnest
inv_path=$(pwd)/invariant

rm -rf ${store_path}
mkdir -p ${store_path}

#select run
R=0
#Path of the icon nest on the opendata-sever
model_pfad=https://opendata.dwd.de/weather/nwp/icon-eu/grib/$(printf "%02d" "$R")
#date
D=$(date +"%Y%m%d")

echo "ICON EU NEST Run: " ${R}
echo "Date: " $(date)
echo "------------------------"
cd ${path_icon}

#######################################################################
#name of the model files
regular_single=icon-eu_europe_regular-lat-lon_single-level_${D}$(printf "%02d" "$R")_
regular_pressure=icon-eu_europe_regular-lat-lon_pressure-level_${D}$(printf "%02d" "$R")_
regular_model=icon-eu_europe_regular-lat-lon_model-level_${D}$(printf "%02d" "$R")_
invariant=icon-eu_europe_regular-lat-lon_time-invariant_${D}$(printf "%02d" "$R")_

[ -f "gitter_icon" ] || python3 creategridinfo.py

# get files with wget
if [ ! -f "./invariant/lon.nc" ]; then
  wget -q ${model_pfad}/rlat/${invariant}RLAT.grib2.bz2 -P ${inv_path}
  wget -q ${model_pfad}/rlon/${invariant}RLON.grib2.bz2 -P ${inv_path}
  bzip2 -dfq ${inv_path}/${invariant}RLAT.grib2.bz2
  bzip2 -dfq ${inv_path}/${invariant}RLON.grib2.bz2
  cdo -s -f nc4 -copy ${invariant}RLON.grib2 lon.nc
  cdo -s -f nc4 -copy ${invariant}RLAT.grib2 lat.nc
  cdo -s -f nc4 -remapbil,gitter_icon2 lon.nc intlon.nc
  cdo -s -f nc4 -remapbil,gitter_icon2 lat.nc intlat.nc
  rm -f ${invariant}RLON.grib2 ${invariant}RLAT.grib2
fi
#if [ ! -f "hhl3D.nc" ]; then
  #wget -q ${model_pfad}/hhl/${invariant}HHL.grib2.bz2 -P ${path_icon} #some chances take place
  #wget -q ${model_pfad}/hsurf/${invariant}HSURF.grib2.bz2 -P ${path_icon}
  #bzip2 -dfq ${invariant}HHL.grib2.bz2
  #bzip2 -dfq ${invariant}HSURF.grib2.bz2
  #cdo -s -f nc4 -sub ${invariant}HHL.grib2 ${invariant}HSURF.grib2 hhlhsurf3D.nc
  #cdo -s -f nc4 -copy ${invariant}HHL.grib2 hhl3D.nc
  #rm -f ${invariant}HHL.grib2 ${invariant}HSURF.grib2
#fi



for X in 9 #12 15 18 21 24 27 30 33 36 39 42 45 48 51 54 57 60
do
  cd ${path_icon}
  T=$(printf "%03d" "$X")
  #single level
  for N in CAPE_ML #CAPE_CON
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

  #rm -f 
  python3 main.py $(pwd)/Basic --fp ${X} --run ${R} --date $(date)

  echo "done with ${T}"
done

