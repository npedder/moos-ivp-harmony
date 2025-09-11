# A HOST_IP environment variable should be provided when running the container

FROM ubuntu:22.04


# Setup the base Debian 8 container
RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip \
  g++ \
  subversion \
  xterm \
  cmake \
  libfltk1.3-dev \
  freeglut3-dev \
  libpng-dev \
  libjpeg-dev \
  libxft-dev \
  libxinerama-dev \
  libtiff5-dev \
  espeak \
  build-essential \
  git


# Setup the MOOS-IvP_15.5 environment
RUN \
  cd /opt && \
  git clone https://github.com/moos-ivp/moos-ivp.git && \
  cd moos-ivp && \
  sed -i s/BUILD_GUI_CODE=\"ON\"/BUILD_GUI_CODE=\"OFF\"/ build-ivp.sh && \
  sed -i s/j12/j1/ build-ivp.sh && \
  sed -i s/O3/Os/ build-ivp.sh && \
  sed -i s/j12/j1/ build-moos.sh && \
  ./build.sh \
  ls -la /opt/moos-ivp && \
  test -d /opt/moos-ivp/bin

# Setup the moos-ivp-umassd environment
RUN \
  cd /opt && \
  git clone https://github.com/scottsideleau/moos-ivp-umassd.git && \
  cd moos-ivp-umassd && \
  ./build.sh

# Setup the moos-ivp-harmony environment
RUN \
  cd /opt && \
  git clone https://github.com/npedder/moos-ivp-harmony.git && \
  cd moos-ivp-harmony && \
  ./build.sh

# Add MOOS-IvP to the PATH
ENV PATH=/opt/moos-ivp/bin:/opt/moos-ivp-umassd/bin:/opt/moos-ivp-harmony/bin:$PATH

# Add behaviors 
ENV IVP_BEHAVIOR_DIRS=/opt/moos-ivp-umassd/lib


# Setup python-moos
RUN \
  cd /opt && \
  git clone https://github.com/npedder/python-moos.git python-moos &&\
  cd python-moos &&\
  python3 setup.py build && \
  python3 setup.py install && \
  mv build/lib.linux-*/pymoos.*.so /opt/moos-ivp-harmony/py/HARMONY/ && \
  cd /opt/moos-ivp-harmony/py/HARMONY && \
  pip install -r requirements.txt

# Make neccesary changes to existing files to run in vehicles in container
# RUN \
#   cd /opt/moos-ivp-harmony/py/HARMONY && \ 
#   sed -i "s/^MOOS_HOST = .*/MOOS_HOST = '$HOST_IP'/" main.py && \
#   cd /opt/moos-ivp-harmony/missions/mission_generation && \
#   sed -i "s/try_shore_host = pshare_route=localhost:8999/try_shore_host = pshare_route=$HOST_IP:8999/" uav.moos && \
#   sed -i "s/try_shore_host = pshare_route=localhost:8999/try_shore_host = pshare_route=$HOST_IP:8999/" vehicle.moos && \
#   sed -i 's|xterm -e "python3 \(.*\)" &|python3 \1 &|' launch_harmony.sh && \
#   sed -i '/pAntler shoreside\.moos/d' launch_harmony.sh && \ 
#   sed -i 's/uMAC -t shoreside\.moos/uMAC -t vehicle_1.moos/' launch_harmony.sh


# Copy the entrypoint script into the image
COPY docker_entrypoint.sh /usr/local/bin/docker_entrypoint.sh

# Make it executable
RUN chmod +x /usr/local/bin/docker_entrypoint.sh

# Use it as the container entrypoint
ENTRYPOINT ["/usr/local/bin/docker_entrypoint.sh"]

