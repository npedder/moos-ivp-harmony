import time
from MOOSHandler import MOOSHandler
from AlgorithmDevelopment.missionLayouts import *


# Nathan Pedder
# Connect to a shore-side
# listen for NODE_REPORTs from vehicles
# and add to a dictionary of available vehicles.
# Generate waypoint information and send to 
import sys

PORT = 8999
MOOS_HOST = 'localhost'
CLIENT_NAME = "HARMONY"

if len(sys.argv) > 1:
    TIME_WARP = int(sys.argv[1])
else:
    TIME_WARP = 1

def main():

    # shallow_spots = " "
    check = 0
    # Handles MOOSDB connection, stores survey area and vehicle information, and sends waypoints based on algorithm
    moos_handler = MOOSHandler(MOOS_HOST, PORT, CLIENT_NAME, TIME_WARP)

    moos_handler.connect()

    # Forever loop
    while True:
        time.sleep(1)

        messages = moos_handler.fetch_messages()

        # moos_handler.notify("APPCAST", "node=HARMONY")
        # When respective messages are received, moos_handler.survey_area and mood_handler.available_vehicles updates.
        moos_handler.parse_incoming_messages(messages)


        if moos_handler.survey_area is not None:
            moos_handler.notify("VIEW_GRID", moos_handler.survey_area.areaToGrid("Survey Area UUV"));
            # print(moos_handler.survey_area.areaToGrid())
            moos_handler.assign_waypoints_and_notify_uavs()
            while(len(moos_handler.completed_uavs) != len(moos_handler.available_uavs)):
                moos_handler.visualizeGrid(moos_handler.survey_area, moos_handler.available_uavs)
                messages = moos_handler.fetch_messages()
                moos_handler.parse_incoming_messages(messages)
                time.sleep(0.01)

            # Reset grid for UUVs and allow separate deploying
            moos_handler.comms.notify("VIEW_GRID", moos_handler.gridMSG)
            moos_handler.notify("DEPLOY_ALL", "false")

            # Poke with shallow areas
            moos_handler.assign_waypoints_and_notify_uuvs()

            # VISUALIZING THE SHALLOW WATER
            # check to make sure method only runs once
            while check == 0:
                moos_handler.visualize_shallow_space()
                check = 1

            # Clear UAV waypoint information
            for name in moos_handler.available_uavs:
                moos_handler.notify("VIEW_SEGLIST",
                            f'pts={{0,0}},label={name}_wpt_survey, active=false')  # removes any prior waypoint visuals
                # Remove waypoint data from UAVs to allow separate deploying of UUVs
                moos_handler.unassign_and_notify(moos_handler.available_uavs)

            while (len(moos_handler.completed_uuvs) != len(moos_handler.available_vehicles)):
                messages = moos_handler.fetch_messages()
                moos_handler.parse_incoming_messages(messages)
                moos_handler.visualizeGrid(moos_handler.survey_area, moos_handler.available_vehicles)

            # Clear UUV waypoint information
            for name in moos_handler.available_vehicles:
                moos_handler.notify("VIEW_SEGLIST",
                                    f'pts={{0,0}},label={name}_wpt_survey, active=false')  # removes any prior waypoint visuals

            moos_handler.survey_area = None  # Reset survey area for the next iteration
            moos_handler.survey_area_land = None

        # if moos_handler.survey_area_land is not None:
        #     moos_handler.notify("VIEW_GRID", moos_handler.survey_area_land.areaToGrid());
        #     # print(moos_handler.survey_area.areaToGrid())
        #     moos_handler.assign_and_notify()
        #     moos_handler.survey_area_land = None  # Reset survey area for the next iteration


if __name__ == "__main__":
    main()
