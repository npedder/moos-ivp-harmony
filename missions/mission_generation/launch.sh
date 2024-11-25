#!/bin/bash -e
#----------------------------------------------------------
#  Script: launch.sh
#  Author: Michael Benjamin
#  LastEd: May 20th 2019
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

if [ $m -eq 0 ]; then
    echo "No vehicle_*.moos files found. Exiting."
    exit 1
fi

<<<<<<< HEAD:missions/s1_alpha/launch.sh
echo "Launching $COMMUNITY MOOS Community with WARP:" $TIME_WARP

# Launch the main community process
pAntler $COMMUNITY.moos --MOOSTimeWarp=$TIME_WARP >& /dev/null &

=======
>>>>>>> mission-gen-rework:missions/mission_generation/launch.sh
# Launch all vehicle_*.moos files
for vehicle in "${vehicle_files[@]}"; do
    pAntler $vehicle --MOOSTimeWarp=$TIME_WARP >& /dev/null &
done

# Launch the shoreside process
pAntler shoreside.moos --MOOSTimeWarp=$TIME_WARP >& /dev/null &

# Launch uMAC for shoreside and all vehicles
<<<<<<< HEAD:missions/s1_alpha/launch.sh
uMAC -t shoreside.moos &
for vehicle in "${vehicle_files[@]}"; do
    uMAC -t $vehicle &
done

# Launch uMAC for the main community
uMAC -t $COMMUNITY.moos

# Kill all processes after completion
kill -- -$$
=======
uMAC -t shoreside.moos 

# Kill all processes after completion
kill -- -$$
>>>>>>> mission-gen-rework:missions/mission_generation/launch.sh
