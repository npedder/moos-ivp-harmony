#!/bin/bash -e

# Check if all three parameters are provided
if [ $# -ne 4 ]; then
    echo "Error: You must provide exactly 4 parameters."
    echo "Usage: $0 <width> <height> <x_pos> <y_pos>"
    exit 1
fi

# Parameters are available
width=$1
height=$2
x_pos=$3
y_pos=$4


uPokeDB shoreside.moos SURVEY_AREA="WIDTH=$width,HEIGHT=$height,X_POS=$x_pos,Y_POS=$y_pos"


