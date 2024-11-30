#!/bin/bash -e
#----------------------------------------------------------
#  Script: launch.sh
#  Author: HARMONY TEAM
#  LastEd: November 29 2024
#----------------------------------------------------------
#  Part 1: Set Exit actions and declare global var defaults
#----------------------------------------------------------

TIME_WARP=1
GUI="yes"
m=0
n=0
#----------------------------------------------------------
#  Part 2: Check for and handle command-line arguments
#----------------------------------------------------------
for ARGI; do
    if [ "${ARGI}" = "--help" -o "${ARGI}" = "-h" ] ; then
        echo "launch.sh [SWITCHES] [time_warp]   "
        echo "  --help, -h           Show this help message            " 
        exit 0;
    elif [ "${ARGI}" = "--nogui" ] ; then
        GUI="no"
    elif [ "${ARGI//[^0-9]/}" = "$ARGI" -a "$TIME_WARP" = 1 ]; then 
        TIME_WARP=$ARGI
    else 
        echo "launch.sh Bad arg:" $ARGI " Exiting with code: 1"
        exit 1
    fi
done


#----------------------------------------------------------
#  Part 3: Launch the processes
#----------------------------------------------------------

# Find all vehicle_* files in the current directory
vehicle_files=(vehicle_*.moos)

# Get the total number of vehicle files found
m=${#vehicle_files[@]}

# Find all uav_* files in the current directory 
uav_files=(uav_*.moos)

# Get the total number of uav files found
u=${#uav_files[@]}

if [ $m -eq 0] && [$u -eq 0]; then
    echo "No vehicle_*.moos or urav_*.moos files found. Exiting."
    exit 1
fi

# Launch all vehicle_*.moos files
for vehicle in "${vehicle_files[@]}"; do
    pAntler $vehicle --MOOSTimeWarp=$TIME_WARP >& /dev/null &
done

# Launch all uav_*.moos files
for uav in "${uav_files[@]}"; do
    pAntler $uav --MOOSTimeWarp=$TIME_WARP >& /dev/null &
done

# Launch the shoreside process
pAntler shoreside.moos --MOOSTimeWarp=$TIME_WARP >& /dev/null &

# Launch uMAC for shoreside and all vehicles
uMAC -t shoreside.moos 

# Kill all processes after completion
kill -- -$$
