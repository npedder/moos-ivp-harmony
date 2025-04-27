
# Mission Generation
Mission folder that can quickly test different sets of vehicle configurations with the HARMONY algorithm and shoreside app. First, create and edit a configuration file. Then, build and launch using the configuration. Inject a survey into the simulation. First UAVs will receive assignments. Once UAVs return, UUVs will receive their assignments. 

## Creating a new configuration
- Create a new .txt file in the MissionConfigs folder.
- Each line will represent a vehicle and its attributes in the simulation.
    - START_X=200  START_Y=400   HEADING=100 SPEED=2.1   ENDURANCE=10000 SENSOR_RANGE=80 VEHICLE_TYPE=UAV    VEHICLE_COLOR=crimson
- To add UAVs, place a '~' before the lines intended to be built as UAVs. 
- Comments can be added with #.
- *Endurance currently has no implementation.

## Running a vehicle configuration
- Vehicle configurations can be quickly built and launched with the ./build_launch_harmony.sh that will build the necessary vehicle files with nsplug, then launch the vehicle moos files and shoreside moos file. Last, the python application will launch and connect to the shoreside MOOSDB. 

## Scripts
- build_launch_harmony.sh 
    - Builds the vehicle files, launches the simulation, and launches the python app. 
- inject_survey.sh
    - Sends a SURVEY_AREA message set by the user to the shoreside app. The python app subscribes to SURVEY_AREA, sends the view grid information, then sends the vehicles assignments when the algorithm is done running. 
    - Run after simulation and python app are running. 
- GenerateMission.sh
    - Builds the vehicles files, does not launch. 
- launch.sh
    - Launches the vehicle and shoreside files without the python app.
- launch_harmony.sh
    - Launch the vehicles, the shoreside, and the python app.
- clean.sh
    - Clears the mission log folders.

## Notes: 
- Our algorithm divides the survey area into cells based on the GCD of the vehicles. 
- Due to the limitations of pMarineViewer, large numbers of vehicles or survey areas with a large number of cell may freeze the viewer. 
- In order to track the coverage of cells, our python app sends many messages to the shoreside, resulting in a warning. 
- Time warp between uSimMarine and uSimpleRobot scale differently. For example, a Time warp of 25 for uSimMarine is equivalent to a time warp of uSimpleRobot 5 for uSimpleRobot. The relationship may be:
    - (uSimpleRobot time warp)^2 = (uSimMarine time warp)