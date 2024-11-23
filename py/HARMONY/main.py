import time
from MOOSHandler import MOOSHandler

# Nathan Pedder
# Connect to a shore-side
# listen for NODE_REPORTs from vehicles
# and add to a dictionary of available vehicles.
# Generate waypoint information and send to 

PORT = 8999
MOOS_HOST = 'localhost'
CLIENT_NAME = "HARMONY"


def main():
    # Handles MOOSDB connection, stores survey area and vehicle information, and sends waypoints based on algorithm
    moos_handler = MOOSHandler(MOOS_HOST, PORT, CLIENT_NAME)

    moos_handler.connect()

    # Forever loop
    while True:
        time.sleep(1)
        messages = moos_handler.fetch_messages()

        # When respective messages are received, moos_handler.survey_area and mood_handler.available_vehicles updates.
        moos_handler.parse_incoming_messages(messages)


        if moos_handler.survey_area is not None:
            moos_handler.assign_and_notify()
            moos_handler.survey_area = None  # Reset survey area for the next iteration


if __name__ == "__main__":
    main()
