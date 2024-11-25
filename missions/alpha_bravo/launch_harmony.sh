#!/bin/bash -e
#----------------------------------------------------------
#  Script: launch.sh
#  Author: Michael Benjamin
#  LastEd: May 20th 2019
#----------------------------------------------------------
#  Part 1: Set Exit actions and declare global var defaults
#----------------------------------------------------------
TIME_WARP=1
COMMUNITY="alpha"
HARMONY_PATH="../../py/HARMONY/main.py"
GUI="yes"

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

echo "Launching HARMONY app from $HARMONY_PATH" 
xterm -e "python3 $HARMONY_PATH" &

echo "Launching $COMMUNITY MOOS Community with WARP:" $TIME_WARP 
pAntler $COMMUNITY.moos --MOOSTimeWarp=$TIME_WARP >& /dev/null &
pAntler bravo.moos --MOOSTimeWarp=$TIME_WARP >& /dev/null &
pAntler shoreside.moos --MOOSTimeWarp=$TIME_WARP >& /dev/null &
uMAC -t shoreside.moos &
uMAC -t bravo.moos &
uMAC -t $COMMUNITY.moos 
kill -- -$$
