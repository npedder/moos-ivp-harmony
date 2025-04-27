# HARMONY
HARMONY is a system for allocating tasks among UAVs and UUVs with different capabilities to complete a survey mission. It is demonstrated by a python app that can connect to a MOOS shoreside database to receive incoming vehicle information and output waypoint information for each any number of vehicles.

# Directory Structure

The directory structure for the moos-ivp-extend is described below:

| Directory        | Description                                 |
|:---------------- |:------------------------------------------- |
| bin              | Directory for generated executable files    |
| build            | Directory for build object files            |
| build.sh         | Script for building moos-ivp-extend         |
| CMakeLists.txt   | CMake configuration file for the project    |
| missions         | Directory for mission files                 |
| py               | Directory for Python application files      |
| README           | Contains helpful information - (this file). |
| src              | Directory for source code                   |


# Setup
The HARMONY system is demonstrated within a MOOS-IvP simulation. The MOOS-IvP Core modules are required to demonstrate the HARMONY system. The moos-ivp-umassd repository is needed to simulate UAVs. See "**Setup moos-ivp-umassd**" below. 

## pReturnSignal Build Instructions
pReturn Signal is a simple application made for HARMONY that signals the shoreside that a vehicle has returned.

### Build pReturn Signal 
Run the ```build.sh``` script in the root moos-ivp-harmony. This will build the pReturnSignal executable file in the the bin folder. 

## Add to PATH environment variable.
pReturnSignal needs to be added to the PATH environment variable in order to be launched with pAntler. To do so, try one of the following: 
- Add the line export PATH=“$PATH:your/installpath/moos-ivp-harmony/bin” to the .bashrc in your home/user directory	 

- Add the line export PATH=“$PATH:your/installpath/moos-ivp-harmony/bin” to the .profile in your home/user directory 

- Add the line :/your/installpath/moos-ivp-harmony/bin to the environment file in your etc directory (etc/environment).
  - E.g.
    - PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/home/user/moos-ivp/bin:/home/nate/moos-ivp-umassd/bin:/home/nate/moos-ivp-harmony/bin" 



## Python MOOS Build Instructions

The HARMONY system uses the python-moos wrapper for MOOSApps for its shore-side application. 
To install python-moos:

### Clone the repository:

```
git clone https://github.com/npedder/python-moos.git python-moos
```

### Build and install python-moos:

```
cd python-moos
python setup.py build
python setup.py install
```

This will produce a "pymoos*.so" file that needs to be added to your python interpreter in order to import the pymoos library into your python code. 

## Important Python packages
- numpy
- matplotlib
- networkx
- scipy
  
# Usage
Once setup is complete, example HAMRONY missions can be generated in the missions/mission_generation folder. This folder contains bash scripts that can quickly set up new mission configurations based on the ".txt" files located in the 'MissionConfigs' folder.

To build and launch the vehicles based on the config file, from inside the MissionGeneration folder, run
```
./build_launch_harmony <config_file.txt> <time_warp>
```

Now, a survey area can be sent to the application using running 

```
./inject_survey <width> <height> <start_x> <start_y>
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

# Notes: 
- Due to the limitations of pMarineViewer, large numbers of vehicles or survey areas with a large number of cell may freeze the viewer.

