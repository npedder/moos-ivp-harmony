# HARMONY
HARMONY is a system for allocating tasks among UAVs and UUVs with different capabilities to complete a survey mission. It is demonstrated by a python app that can connect to a MOOS shoreside database to receive incoming vehicle information and ouput waypoint information for each any number of vehicles.

# Directory Structure

The directory structure for the moos-ivp-extend is described below:

| Directory        | Description                                 |
|:---------------- |:------------------------------------------- |
| bin              | Directory for generated executable files    |
| build            | Directory for build object files            |
| build.sh         | Script for building moos-ivp-extend         |
| CMakeLists.txt   | CMake configuration file for the project    |
| data             | Directory for storing data                  |
| lib              | Directory for generated library files       |
| missions         | Directory for mission files                 |
| py               | Directory for Python application files      |
| README           | Contains helpful information - (this file). |
| scripts          | Directory for script files                  |
| src              | Directory for source code                   |


# Setup
The HARMONY system is demonstrated within a MOOS-IvP simulation. The MOOS-IvP Core modules are required to demonstrate the HARMONY system. The moos-ivp-umassd repository is needed to simulate UAVs. See "**Setup moos-ivp-umassd**" below. 


The HARMONY system uses the python-moos wrapper for MOOSApps for its shore-side application. 
To install python-moos:

## Python MOOS Build Instructions
Clone the repository:

```
git clone https://github.com/npedder/python-moos.git python-moos
```

Build and install python-moos:

```
cd python-moos
python setup.py build
python setup.py install
```

This will produce a "pymoos*.so" file that needs to be added to your python interpreter in order to import the pymoos library into your python code. 

## Python packages
- numpy
- matplotlib
  
# Usage
Once setup is complete, example HAMRONY missions can be generated in the missions/mission_generation folder. This folder contains bash scripts that can quickly set up new mission configurations based on the ".txt" files located in the 'MissionConfigs' folder.

To build the vehicles based on the config file, from inside the MissionGeneration folder, run
```
./GenerateMission.sh config.txt
```

To launch the mission with the HARMONY shoreside app, run
```
./launch_harmony.sh
```

Now, a survey area can be sent to the application using running "./inject_survey width height start_x start_y", for example, 
```
./inject_survey.sh 50 50 50 100
```

The survey area should appear in pMarineViewer followed by the vehicle assignments. The vehicles can be deployed onto their assigned waypoints with the "RUN" button.

# Setup moos-ivp-umassd
HARMONY uses the _uSimpleRobot_ application from moos-ivp-umassd. To set up, clone the following repo and follow the instructions found in its README. 
 
```
git clone https://github.com/scottsideleau/moos-ivp-umassd.git
```

## Possible fix to cmake build error
open moos-ivp-umassd in file directory
  
open CMakeLists.txt
  
in " # Set the output directories for the binary and library files " add below 

("pwd" in moos-ivp to find path)

```
set(MOOSIVP_SOURCE_TREE_BASE "/pasth/to/moos-ivp" CACHE STRING "MOOS-IvP Base Directory" FORCE) 
```

  ```
./build.sh
```
  
