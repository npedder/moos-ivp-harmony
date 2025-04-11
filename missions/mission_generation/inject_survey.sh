#!/bin/bash -e

# Nathan Pedder, UMD 



# These values can be overwritten if the user passes the 4 necessary arguments.
<<<<<<< Updated upstream
width=300
=======
width=200
>>>>>>> Stashed changes
height=100
x_pos=50
y_pos=50
x_end=250
y_end=150

# Check if parameters are provided correctly
if [ $# -eq 4 ]; then
    width=$1
    height=$2
    x_pos=$3
    y_pos=$4

    # Values used for pSearchGrid 
    x_end=$(($x_pos + $width))
    y_end=$(($y_pos + $height))

elif [ $# -eq 0 ]; then
    echo "Injecting default survey."
else
    echo "Error: You must provide 4 parameters. If no parameters provided, the default survey area defined within inject_survey.sh will be injected. "
    echo "Usage: $0 <width> <height> <x_pos> <y_pos>"
    exit 1
fi


# Inject survey area
uPokeDB shoreside.moos SURVEY_AREA="WIDTH=$width,HEIGHT=$height,X_POS=$x_pos,Y_POS=$y_pos"

# Inject pSearchGrid with Survey Area Parameters
# uPokeDB shoreside.moos VIEW_GRID="pts={$x_pos,$y_pos: $x_end,$y_pos: $x_end,$y_end: $x_pos,$y_end},cell_size=5,cell_vars=x:0:y:0,cell_min=x:0,cell_max=x:10,label=psg"

# Reset grid on execution
# uPokeDB shoreside.moos "PSG_GRID_RESET='