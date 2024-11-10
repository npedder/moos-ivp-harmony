import pymoos
import time
import utils

# Nathan Pedder
# Connect to a shoreside
# listen for NODE_REPORTs from vehicles
# and add to a dictionary of available vehicles


comms = pymoos.comms()



def on_connect():
  #  c.wait_until_connected(2000)
    comms.register("NODE_REPORT")
    comms.register("SURVEY_AREA")

    # for msg in comms.fetch():
    #     if msg.key() == "NODE_REPORT":
    #         initial_pos[msg.key()] = msg.string();

    return comms.register('APPLES_ITER_HZ', 0)



# def parseNodeReportAndCreateVehilce(nodeReport):
#     # Regular expression to extract NAME, LAT, and LON
#     pattern = r"NAME=([^,]+),.*LAT=([-\d.]+),.*LON=([-\d.]+)"
#
#     # Search for the match
#     match = re.search(pattern, nodeReport)
#
#     if match:
#         name = match.group(1)
#         lat = float(match.group(2))
#         lon = float(match.group(3))
#
#         # print(f"Name: {name}")
#         # print(f"Latitude: {lat}")
#         # print(f"Longitude: {lon}")
#
#         vehicle = UxV(name, (lat,lon), 10, 10, 100);
#         if name in available_vehicles:
#             #print("UxV already added to available vehicles")
#             return None
#         else:
#             return vehicle
#     else:
#         print("Pattern not found in the string.")
#         return None

def main():
    available_vehicles = {}
    survey_area = None

    # my code here
    comms.set_on_connect_callback(on_connect)
    comms.run('localhost', 9200, 'pymoos')

    while True:
        time.sleep(1)
        comms.notify('simple_var', 'hello world', pymoos.time())
        #ap(lambda msg: msg.trace(), comms.fetch())

        for msg in comms.fetch():
            if msg.key() == "NODE_REPORT":
                #print(msg.string())
                vehicle = utils.parseNodeReportAndCreateVehilce(msg.string())
                if vehicle.name not in available_vehicles and vehicle != None:
                    available_vehicles[vehicle.name] = vehicle
                    print(available_vehicles)
            if msg.key() == 'SURVEY_AREA':
                if survey_area == None:
                    survey_area = utils.parseSurveyAreaAndCreateObject(msg.string())
                    print(survey_area)


# if __name__ == "__main__":
main()
