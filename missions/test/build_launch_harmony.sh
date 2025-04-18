#!/bin/bash


if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <input_file> <timewarp>"
  exit 1
fi

INPUT_FILE="$1"
NUMBER="$2"

./GenerateMission.sh "$INPUT_FILE" "$NUMBER"
./launch_harmony.sh "$NUMBER"

