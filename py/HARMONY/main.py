import time
from MOOSHandler import MOOSHandler

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
            if moos_handler.available_uavs:
                moos_handler.notify("VIEW_GRID", moos_handler.survey_area_land.areaToGrid("Survey Area UAV"));
            # print(moos_handler.survey_area.areaToGrid())
            moos_handler.assign_waypoints_and_notify_uavs()
            while(len(moos_handler.completed_uavs) != len(moos_handler.available_uavs)):
                moos_handler.visualizeGrid(moos_handler.survey_area)
                messages = moos_handler.fetch_messages()
                moos_handler.parse_incoming_messages(messages)
                time.sleep(1)
            # Reset grid for UUVs
            # moos_handler.notify("VIEW_GRID_RESET", "true")
            # Poke with shallow areas
            moos_handler.assign_waypoints_and_notify_uuvs()
            while True:
                moos_handler.visualizeGrid(moos_handler.survey_area)

            moos_handler.survey_area = None  # Reset survey area for the next iteration
            moos_handler.survey_area_land = None

        # if moos_handler.survey_area_land is not None:
        #     moos_handler.notify("VIEW_GRID", moos_handler.survey_area_land.areaToGrid());
        #     # print(moos_handler.survey_area.areaToGrid())
        #     moos_handler.assign_and_notify()
        #     moos_handler.survey_area_land = None  # Reset survey area for the next iteration

if __name__ == "__main__":
    main()
