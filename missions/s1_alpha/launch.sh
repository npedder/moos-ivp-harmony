#!/bin/bash -e
#----------------------------------------------------------
#  Script: launch.sh
#  Author: Michael Benjamin
#  LastEd: May 20th 2019
#----------------------------------------------------------
#  Part 1: Set Exit actions and declare global var defaults
#----------------------------------------------------------
#source file to run your congfig and vehicle amounts before launch!
m=(grep'^m='MakeVehicle.sh|cut -d'='-f2|tr-d"")
TIME_WARP=1
COMMUNITY="vehicle_0"
GUI="yes"
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
echo "Launching $COMMUNITY MOOS Community with WARP:" $TIME_WARP
pAntler $COMMUNITY.moos --MOOSTimeWarp=$TIME_WARP >& /dev/null &
for i in {seq 0 to "$m"}; do
pAntler vehicle_"$n".moos --MOOSTimeWarp=$TIME_WARP >& /dev/null &
((n++))
done
pAntler shoreside.moos --MOOSTimeWarp=$TIME_WARP >& /dev/null &
uMAC -t shoreside.moos &
for i in {seq 0 to "$m"}; do
uMAC -t vehicle_"$n".moos &
((n++))
done
uMAC -t $COMMUNITY.moos
kill -- -$$
