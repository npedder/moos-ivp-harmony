import pymoos
import time
import utils
import AllocationControl

# Nathan Pedder
# Connect to a shoreside
# listen for NODE_REPORTs from vehicles
# and add to a dictionary of available vehicles

# determines how long the to wait for vehicle messages. Not needed if receiving SURVEY_AREA determines start time.
#FETCH_TIMER = 5

PORT = 9200

comms = pymoos.comms()



def on_connect():
  #  c.wait_until_connected(2000)
    comms.register("NODE_REPORT")
    comms.register("SURVEY_AREA")
    return True


def main():
    available_vehicles = {}
    survey_area = None

    comms.set_on_connect_callback(on_connect)
    comms.run('localhost', PORT, 'pymoos')

    # Checks every second for new message and parses information based on message key until FETCH_TIMER runs out
    timer = 1 #TODO not used now, can be deleted. Make sure to change while loop logic.
    while timer != 0:
        time.sleep(1)
        #timer -= 1
        for msg in comms.fetch():
            if msg.key() == "NODE_REPORT":
                # print(msg.string())
                vehicle = utils.parseNodeReportAndCreateVehicle(msg.string())
                if vehicle.name not in available_vehicles and vehicle != None:
                    available_vehicles[vehicle.name] = vehicle
                    print(available_vehicles)
            if msg.key() == 'SURVEY_AREA':
                if survey_area == None:
                    survey_area = utils.parseSurveyAreaAndCreateObject(msg.string())
                    #print(utils.convertSurveyAreaIntoMatrix(survey_area))
                    timer = 0 #ends while loop
        print(".", end="")

    print(len(available_vehicles), "vehicles found.", "Survey area will be: ", survey_area, ".")

    # comms.notify('simple_var', 'hello world', pymoos.time())
    # ap(lambda msg: msg.trace(), comms.fetch())

    vehicle_assignments = AllocationControl.allocateArea(available_vehicles, survey_area)
    print(vehicle_assignments)
    AllocationControl.plotAssignments(vehicle_assignments)

    for name in vehicle_assignments:
        wpt_var = name + "_WPT_UPDATE"
        print("SENDING", vehicle_assignments[name].string() ," ", wpt_var)

        comms.notify(wpt_var, vehicle_assignments[name].string(), pymoos.time())


if __name__ == "__main__":
    main()
