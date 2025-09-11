#!/bin/bash
set -e

#!/bin/bash
set -e

# Ensure HOST_IP is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <HOST_IP> [MISSION_FILE] [TIME_WARP]"
    exit 1
fi

HOST_IP=$1
MISSION_FILE=${2:-alpha.txt}   # Default mission file
TIME_WARP=${3:-1}                        # Default time warp

# Update MOOS-HARMONY files with HOST_IP
sed -i "s/^MOOS_HOST = .*/MOOS_HOST = '$HOST_IP'/" /opt/moos-ivp-harmony/py/HARMONY/main.py
sed -i "s/try_shore_host = pshare_route=localhost:8999/try_shore_host = pshare_route=$HOST_IP:8999/" /opt/moos-ivp-harmony/missions/mission_generation/uav.moos
sed -i "s/try_shore_host = pshare_route=localhost:8999/try_shore_host = pshare_route=$HOST_IP:8999/" /opt/moos-ivp-harmony/missions/mission_generation/vehicle.moos

# Update launch_harmony.sh for container-friendly execution
sed -i 's|xterm -e "python3 \(.*\)" &|python3 \1 &|' /opt/moos-ivp-harmony/missions/mission_generation/launch_harmony.sh
sed -i '/pAntler shoreside\.moos/d' /opt/moos-ivp-harmony/missions/mission_generation/launch_harmony.sh
sed -i 's/uMAC -t shoreside\.moos/uMAC -t vehicle_1.moos/' /opt/moos-ivp-harmony/missions/mission_generation/launch_harmony.sh

echo "Starting with HOST_IP: $HOST_IP, mission file: $MISSION_FILE, TIME_WARP: $TIME_WARP"


# Generate the mission with the mission file and timewarp
cd /opt/moos-ivp-harmony/missions/mission_generation/
./GenerateMission.sh "$MISSION_FILE" "$TIME_WARP"

# Launch Mission
./launch_harmony.sh
