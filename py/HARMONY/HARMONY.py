# Nathan Pedder
# Connect to a shoreside
# listen for NODE_REPORTs from vehicles
# and add to a dictionary of available vehicles


comms = pymoos.comms()
available_vehicles = {}

class UxV:
    def __init__(self, name, position, speed, endurance):
        """
        Initialize a UxV instance.

        :param name: str, name of the vehicle
        :param position: tuple, (x, y) coordinates of the vehicle's starting position
        :param speed: float, speed of the vehicle (in units per time)
        :param endurance: float, how far the vehicle can travel (could represent fuel capacity)
        """
        self.name = name
        self.position = position  # (x, y)
        self.speed = speed        # Speed (in units per time, e.g., km/h or miles/h)
        self.endurance = endurance # Maximum distance the vehicle can travel (e.g., miles or km)
    def __repr__(self):
        return f"UxV(name={self.name}, position={self.position}, speed={self.speed}, endurance={self.endurance})"


def on_connect():
  #  c.wait_until_connected(2000)
    comms.register("NODE_REPORT")

    # for msg in comms.fetch():
    #     if msg.key() == "NODE_REPORT":
    #         initial_pos[msg.key()] = msg.string();

    return comms.register('APPLES_ITER_HZ', 0)



def parseNodeReportAndCreateVehilce(nodeReport):
    # Regular expression to extract NAME, LAT, and LON
    pattern = r"NAME=([^,]+),.*LAT=([-\d.]+),.*LON=([-\d.]+)"

    # Search for the match
    match = re.search(pattern, nodeReport)

    if match:
        name = match.group(1)
        lat = float(match.group(2))
        lon = float(match.group(3))

        # print(f"Name: {name}")
        # print(f"Latitude: {lat}")
        # print(f"Longitude: {lon}")

        vehicle = UxV(name, (lat,lon), 10, 100 );
        if name in available_vehicles:
            #print("UxV already added to available vehicles")
            return None
        else:
            return vehicle
    else:
        print("Pattern not found in the string.")
        return None

def main():
    # my code here
    comms.set_on_connect_callback(on_connect)
    comms.run('localhost', 9200, 'pymoos')

    while True:
        time.sleep(1)
        comms.notify('simple_var', 'hello world', pymoos.time())
        #ap(lambda msg: msg.trace(), comms.fetch())

        for msg in comms.fetch():
            if msg.key() == 'APPLES_ITER_HZ':
                print(msg.double())
            if msg.key() == "NODE_REPORT":
                #print(msg.string())
                vehicle = parseNodeReportAndCreateVehilce(msg.string())
                if vehicle != None:
                    available_vehicles[vehicle.name] = vehicle
                    print(available_vehicles)


# if __name__ == "__main__":
main()
