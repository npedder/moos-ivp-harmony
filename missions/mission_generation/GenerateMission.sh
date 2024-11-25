#!/bin/bash


word="vehicle_"

# Check for file names containing the word
if ls *"$word"* 1> /dev/null 2>&1; then
rm *vehicle_*
fi


START_PORT=9000

# Check if a file argument is passed
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <file.txt>"
  exit 1
fi

input_file=$1

# Check if the file exists
if [ ! -f "$input_file" ]; then
  echo "File $input_file does not exist."
  exit 1
fi

# Read the file line by line
line_number=0
while IFS= read -r line; do
  # Skip comments and empty lines
  if [[ "$line" =~ ^#.* ]] || [[ -z "$line" ]]; then
    continue
  fi

  # Increment the line number
  ((line_number++))
  PORT=$(($START_PORT+$line_number-1))
  # Run the nsplug command with arguments from the line
  nsplug vehicle.moos "vehicle_${line_number}.moos" VNAME="vehicle_${line_number}" PORT="$PORT" BHV="vehicle_${line_number}.bhv" $line
  nsplug default.bhv "vehicle_${line_number}.bhv" $line
done < "$input_file"

echo "Processing completed!"

