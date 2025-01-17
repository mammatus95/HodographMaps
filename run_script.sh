#!/bin/bash

# run
# conda activate HodographMaps
# first!

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
    echo "Error: No arguments provided."
    echo "Usage: $0 <FP>"
    echo "Usage: FP has to be in hours."
    exit 1
fi


FP=${1}
R=00 # select run 0 or 12z
D=$(date +"%Y%m%d") # date in format YYYYMMDD
#######################################################################

echo 
echo 
echo "Hodograph Maps Run Script"
echo "Version: 0.1"
echo 
echo "Configurations:"
echo "Model run: ${R}z"
echo "Leadtime: ${FP}z"
echo "Today Date: " $(date +"%d.%m.%Y")
echo 
echo 

#######################################################################
# load bash profile and add Pythonpath
#source /etc/profile
export PYTHONPATH=$(pwd):$PYTHONPATH

#######################################################################
cd src
store_path=$(pwd)/modeldata

# rm log
rm ./log.txt > /dev/null 2>&1
echo "Configurations:" > log.txt
echo "Model run: ${R}z" >> log.txt
echo "Leadtime: ${FP}z" >> log.txt
echo "Today Date: " $(date +"%d.%m.%Y") >> log.txt

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


T=$(printf "%03d" "$FP")
echo "Start downloading leadtime ${T}h"

# ICON
# single level
for N in CAPE_ML CAPE_CON PS LPI_CON_MAX
do
  typeset -l nvar
  nvar=${N}
  wget -q ${icon_model_pfad}/${nvar}/${icon_single}${T}_${N}.grib2.bz2 -P ${store_path} 2>&1 log.txt
  bzip2 -dfq ${store_path}/${icon_single}${T}_${N}.grib2.bz2 >> log.txt 2>&1
done

for H in 1000 950 925 900 875 850 825 800 775 700 600 500 400 300
do
  for N in U V
  do
    typeset -l nvar
    nvar=${N}
    wget -q ${icon_model_pfad}/${nvar}/${icon_pressure}${T}_${H}_${N}.grib2.bz2 -P ${store_path} >> log.txt 2>&1
    bzip2 -dfq ${store_path}/${icon_pressure}${T}_${H}_${N}.grib2.bz2 >> log.txt 2>&1
  done
done

# ifs
ifs_file=${ifs_model_pfad}/${D}/$(printf "%02d" "$R")z/ifs/0p25/oper/${D}$(printf "%02d" "$R")0000-${FP}h-oper-fc.grib2
ifs_index=${ifs_model_pfad}/${D}/$(printf "%02d" "$R")z/ifs/0p25/oper/${D}$(printf "%02d" "$R")0000-${FP}h-oper-fc.index
wget -q ${ifs_file} -P ${store_path}/ >> log.txt 2>&1
wget -q ${ifs_index} -P ${store_path}/ >> log.txt 2>&1
mv ${store_path}/${D}$(printf "%02d" "$R")0000-${FP}h-oper-fc.grib2 ${store_path}/ifs_$(printf "%02d" "$R")z_${D}_f${T}.grib2
mv ${store_path}/${D}$(printf "%02d" "$R")0000-${FP}h-oper-fc.index ${store_path}/ifs_$(printf "%02d" "$R")z_${D}_f${T}.index

# gfs
gfs_file=${gfs_model_pfad}/gfs.${D}/$(printf "%02d" "$R")/atmos/gfs.t$(printf "%02d" "$R")z.pgrb2.0p25.f${T}
wget -q ${gfs_file} -P ${store_path}/ >> log.txt 2>&1
mv ${store_path}/gfs.t$(printf "%02d" "$R")z.pgrb2.0p25.f${T} ${store_path}/gfs_$(printf "%02d" "$R")z_${D}_f${T}.grib2

# Plot Hodograph
# write run.yml configuration
echo run: ${R} > run.yml
echo fp: ${FP} >> run.yml
echo default_date: \"$(date +%Y-%m-%d)\" >> run.yml

echo "Plot Hodograph Maps"
# run python script
#which python3
python3 main.py ICON #>> log.txt 2>&1
python3 main.py IFS #>> log.txt 2>&1
python3 main.py GFS #>> log.txt 2>&1

#rm run.yml
# remove nwp files
#rm -r ${store_path}

echo "done with leadtime ${T}h on $(date)"
cd ..
mkdir -p ./results_img
mv ./src/images/*${FP}.png ./results_img
ls -lh ./results_img/*${FP}.png
