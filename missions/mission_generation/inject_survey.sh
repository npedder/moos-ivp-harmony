#!/bin/bash -e

# Nathan Pedder, UMD 



# These values can be overwritten if the user passes the 4 necessary arguments.
width=300
height=100
x_pos=50
y_pos=50


# Check if parameters are provided correctly
if [ $# -eq 4 ]; then
    width=$1
    height=$2
    x_pos=$3
    y_pos=$4
elif [ $# -eq 0 ]; then
    echo "Injecting default survey."
else
    echo "Error: You must provide 4 parameters. If no parameters provided, the default survey area defined within inject_survey.sh will be injected. "
    echo "Usage: $0 <width> <height> <x_pos> <y_pos>"
    exit 1
fi

# Inject survey area
uPokeDB shoreside.moos SURVEY_AREA="WIDTH=$width,HEIGHT=$height,X_POS=$x_pos,Y_POS=$y_pos"


