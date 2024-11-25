#!/bin/bash

#remove vehicle files and rebuild so if changes are made
#or a vehicle is removed singularly because config
#changes, then you have a safe bet nothing will
#be misalligned of broken in a file
#!/bin/bash

word="vehicle_"

# Check for file names containing the word
if ls *"$word"* 1> /dev/null 2>&1; then
rm *vehicle_*
fi

# Define the file
file="InitVehicleConfig.txt"

# Count the number of lines in the file
line_count=$(wc -l < "$file")

# Declare array to store line data
my_array=()

# Fill array with line data to input into each .moos variable
for i in $(seq 1 "$line_count"); do
  LINE_DATA=$(sed -n "${i}p" "$file")
  my_array[$((i - 1))]="$LINE_DATA"  # Store in zero-based index
done

# Counter to track the next vehicle's variables
next_vehicle=0

# Port number to increment
n=9000
m=0
# Run through every set of vehicles by dividing the line count
# by the number of variables required for each nsplug call
for i in $(seq 1 $((line_count / 10))); do
    nsplug vehicle.moos vehicle_"$m.moos" \
    PORT="$n" \
    VNAME=vehicle_"$m" \
    LATORG="${my_array[$((0 + next_vehicle))]}" \
    LONGORG="${my_array[$((1 + next_vehicle))]}" \
    START_X="${my_array[$((2 + next_vehicle))]}" \
    START_Y="${my_array[$((3 + next_vehicle))]}" \
    HEADING="${my_array[$((4 + next_vehicle))]}" \
    SPEED="${my_array[$((5 + next_vehicle))]}" \
    ENDURANCE="${my_array[$((6 + next_vehicle))]}" \
    SENSOR_RANGE="${my_array[$((7 + next_vehicle))]}"\
    VEHICLE_TYPE="${my_array[$((8 + next_vehicle))]}" \
    VEHICLE_COLOR="${my_array[$((9 + next_vehicle))]}" \
  # Increment next_vehicle by 4 to move to the next set of variables
  ((next_vehicle += 10)) #we divide by 8 because of the number of
  #nsplug variables minus the port, we need to divide to move
  #to the next line for the next vehicle set, so if you tinker nsplug
  #to add another tweakable variable to the vehicle default file PLEASE increment
  # to divide by your new amount of variables AND add
  # the variable here for easy execution!

#increment port number
((n++))
((m++))
#if [[ "$VNAME" || "$VEHCLE_TYPE" || "$VEHCLE_COLOR"  =~ ^-?[0-9]+$ ]]; then
    #echo "$One of your elements is of incorrect type, please check the #variable.txt script"
#elif  [["$LATORG" || "$LONGORG" || "$START_X" || "$START_Y" || "$HEADING" || "$SPEED" =~ ^[a-zA-Z]+$ ]]; then
    #echo "$One of your elements is of incorrect type, please check the #variable.txt script"
#fi
done
#check if size of array is less than value for testing purposes, return error and that code wont work
#also add line_count - 1 to live vehicle.txt vehicle instructions without reading the last line of code
