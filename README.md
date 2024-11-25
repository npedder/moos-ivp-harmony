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
The HARMONY system is demonstrated within a MOOS-IvP simulation. The MOOS-IvP Core modules are required to demonstrate the HARMONY system. 


The HARMONY system uses the python-moos wrapper for MOOSApps for its shore-side application. 
To install python-moos:

## `python-moos`
```shell
git clone https://github.com/msis/python-moos
cd python-moos
mkdir build
cd build
cmake ../
make
sudo make install
cd ../..
```

This will produce a "pymoos*.so" file that needs to be added to your python interpreter in order to import the pymoos library into your python code. 

# Usage
Once setup is complete, example HAMRONY missions can be generated in the missions/s1_alpha folder. This folder contains bash scripts that can quickly set up new mission configurations based on the InitVehicleConig.txt file. 


