# HARMONY
HARMONY is a system for allocating tasks among UAVs and UUVs with different capabilities to complete a survey mission. It is demonstrated by a python app that can connect to a MOOS shoreside database to receive incoming vehicle information and output waypoint information for each any number of vehicles.

First, a preliminary survey with UAVs is conducted. Then, a secondary survey is conducted with UUVs that has deadspace, or areas not needed to be covered but can be passed through. 

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
Run the ```build.sh``` script in the root directory of moos-ivp-harmony. This will build the pReturnSignal executable file in the bin folder. 

## Add to PATH environment variable.
pReturnSignal needs to be added to the PATH environment variable in order to be launched with pAntler. To do so, try one of the following: 
- Add the line export PATH="$PATH:your/installpath/moos-ivp-harmony/bin" to the .bashrc in your home/user directory	 

- Add the line export PATH="$PATH:your/installpath/moos-ivp-harmony/bin" to the .profile in your home/user directory 

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

If the xterm python window crashes, make sure these packages are installed in your python environment, or run ```pip install -r requirements.txt``` in the py/HARMONY folder.
  
# Usage
Once setup is complete, example HARMONY missions can be generated in the missions/mission_generation folder. This folder contains bash scripts that can quickly set up new mission configurations based on the ".txt" files located in the 'MissionConfigs' folder.

To build and launch the vehicles based on the config file, from inside the MissionGeneration folder, run
```
./build_launch_harmony <config_file.txt> <time_warp>
```

Now, a survey area can be sent to the application by running in a separate terminal:

```
./inject_survey <width> <height> <start_x> <start_y>
```

Width and height are in meters. The survey area should appear in pMarineViewer followed by the vehicle assignments. The vehicles can be deployed onto their assigned waypoints with the "RUN" button.

# Setup moos-ivp-umassd
HARMONY uses the _uSimpleRobot_ application from moos-ivp-umassd. To set up, clone the following repo and follow the instructions found in its README. 
 
```
git clone https://github.com/scottsideleau/moos-ivp-umassd.git
```

# Alternative Docker container setup for moos-ivp-harmony
Containerizing moos-ivp-harmony simplifies the setup process by automating the installation of moos-ivp-umassd and python-moos and helps with consistency across platforms. This container will be responsible for the vehicle MOOSDB and applications, as well as the shoreside python application for generating and assigning vehicle tasks. A seperate host machine will need to have core MOOS-IVP modules installed and will host the shoreside MOOSDB and apps including the pMarineViewer GUI. 

### Build the container
To build the container, navigate to the folder containing the Dockerfile and run:
``docker build -t container_tag .``

### Run the container
To run the container:
``docker run --rm -p 8999-9300:8999-9100/udp container-tag <host-ip> <missionfile.txt> <timewarp>``

The <host-ip> argument is mandatory. <missionfile.txt> will default to alpha.txt and <timewarp> will default to 1. The opened ports should support the host and a mission conifguration for 100 vehicles. The host port is 8999 and the vehicle ports are 8999 + n. 

### Run the host
On a machine with moos-ivp installed and moos-ivp-harmony downloaded, navigate to:
``/path/to/moos-ivp-harmony/missions/mission_generation/``
and run
``./launch.sh <timewarp>``

with the same timewarp used to run the container. Then open another terminal window to inject the survey.

# Possible fix to cmake build error
open moos-ivp-umassd in file directory
  
open CMakeLists.txt
  
in " # Set the output directories for the binary and library files " add below 

("pwd" in moos-ivp to find path)

```
set(MOOSIVP_SOURCE_TREE_BASE "/path/to/moos-ivp" CACHE STRING "MOOS-IvP Base Directory" FORCE) 
```

```
./build.sh
```

# Notes: 
- Due to the limitations of pMarineViewer, large numbers of vehicles or survey areas with a large number of cell may freeze the viewer.
- The layout of the deadspace in the UUV mission is contained in py/HARMONY/missionLayouts.py, and is used in py/HARMONY/MOOSHandler.py.

