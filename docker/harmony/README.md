# Docker container setup for moos-ivp-harmony
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