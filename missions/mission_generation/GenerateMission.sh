#!/bin/bash

word="vehicle_"

# Check for file names containing the word "vehicle"
if ls *"$word"* 1> /dev/null 2>&1; then
  rm *vehicle_*
fi

word="uav_"

# Check for file names containing the word "uav"
if ls *"$word"* 1> /dev/null 2>&1; then
  rm *uav_*
fi

START_PORT=9000
CURRENT_OBJECT_TYPE="vehicle"  # Start with vehicle as default

# Check if a file argument is passed
# if [ "$#" -ne 1 ]; then
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <file.txt> <-time-warp value>"
  exit 1
fi

input_file="MissionConfigs/${1}"
TIME_WARP=${2:-1}  # Default time warp is 1 if not provided

# Check if the file exists
if [ ! -f "$input_file" ]; then
  echo "File $input_file does not exist."
  exit 1
fi

# Read the file line by line
line_number=0
uuvcount=0
uavcount=0
while IFS= read -r line; do
  # Stop processing if line contains the stop character (~)
  if [[ "$line" == *~* ]]; then
    echo "Found stop character '~'. Switching to UAV creation."
    CURRENT_OBJECT_TYPE="uav"
    continue  # Skip the line with ~ and continue with the rest
  fi

  # Skip comments and empty lines
  if [[ "$line" =~ ^#.* ]] || [[ -z "$line" ]]; then
    continue
  fi

  # Increment the line number
  ((line_number++))
  PORT=$(($START_PORT + $line_number - 1))
  # Define an array of colors sorted by ROYGBIV order

  warm_colors=(
    'crimson' 'hotpink' 'red'
    'yellow' 'gold' 'lemonchiffon'
    'lightgoldenrod' 'palegoldenrod'
    )

  cool_colors=(
    'dodgerblue' 'deepskyblue' 'royalblue'
    'lightskyblue' 'powderblue' 'orchid'
    'violet' 'darkviolet' 'plum' 'indigo' 'lavender'
  )

  if [ "$CURRENT_OBJECT_TYPE" == "vehicle" ]; then
    # For vehicles, use the vehicle templates
    # nsplug vehicle.moos "vehicle_${line_number}.moos" VNAME="vehicle_${line_number}" PORT="$PORT" BHV="vehicle_${line_number}.bhv" VEHICLE_COLOR=${warm_colors[uuvcount]} $line
    nsplug vehicle.moos "vehicle_${line_number}.moos" VNAME="vehicle_${line_number}" PORT="$PORT" BHV="vehicle_${line_number}.bhv" VEHICLE_COLOR=${warm_colors[uuvcount]} TIME_WARP="$TIME_WARP" $line
    nsplug default.bhv "vehicle_${line_number}.bhv" $line
    ((uuvcount++))
  elif [ "$CURRENT_OBJECT_TYPE" == "uav" ]; then
    # For UAVs, use the uav templates
    # nsplug uav.moos "uav_${line_number}.moos" VNAME="uav_${line_number}" PORT="$PORT" BHV="uav_${line_number}.bhv" VEHICLE_COLOR=${cool_colors[uavcount]} $line
    nsplug uav.moos "uav_${line_number}.moos" VNAME="uav_${line_number}" PORT="$PORT" BHV="uav_${line_number}.bhv" VEHICLE_COLOR=${cool_colors[uavcount]} TIME_WARP="$TIME_WARP" $line
    nsplug uav.bhv "uav_${line_number}.bhv" $line
    ((uavcount++))
  fi
done < "$input_file"

echo "Processing completed!"
