from SurveyArea import SurveyArea
from Lawnmower import Lawnmower
from UxV import UxV

# vehicles is a dictionary that maps a vehicle name, to a tuple of a vehicle object and the proportion of the area
# that vehicle is responsible for
# vehicle[0] -> vehicle object
# vehicle[1] -> proportion of area

# vehicle areas is a dictionary that maps vehicle name to a lawnmower object

def startAssignArea(vehicles: dict, surveyArea: SurveyArea):
    
    vehicles_copy = vehicles.copy()
    vehicleAreas = {}
    lawnmowerSurveyArea = (Lawnmower(surveyArea.width, surveyArea.height, 0, surveyArea.position), surveyArea.width)

    # Commence recusrion
    newVehicleAreas = assignArea(vehicles_copy, lawnmowerSurveyArea, vehicleAreas)
    print("Area assignment complete")
    return newVehicleAreas

# Recursively assign survey area to each vehicle 
def assignArea(vehicles: dict, surveyArea: tuple, vehicleAreas: dict):
    
    # Base case
    if not vehicles:
        return vehicleAreas

    # Recursive case
    vehicle_name , (vehicle, proportion) = vehicles.popitem()
    print("Running recursive case")
    print("==============================================")
    print("===Currently on vehicle " + vehicle_name + "===")
    print("==============================================")

    # Define all points needed to be more readable
    start = surveyArea[0].position[0]
    midPoint = (start + surveyArea[0].width) / 2
    lastWidth = surveyArea[0].width
    currentEndPoint = (start + lastWidth)
    originalWidth = surveyArea[1]
    newWidth = originalWidth * proportion

    print("midPoint is " + str(midPoint))
    remainingArea = 0
    if vehicle.position[0] < midPoint:
        vehicleAreas[vehicle_name] = Lawnmower(newWidth, surveyArea[0].height, vehicle.sensorRange, (start, surveyArea[0].position[1]))
        
        print(str(vehicle.position[0]) + " < " + str(midPoint) + " thus " + str(vehicle_name) +
               " is assigned (" + str(start) +  ", " + str(newWidth) + ")")
        remainingArea = (Lawnmower(lastWidth - newWidth, surveyArea[0].height, 0, (start + newWidth, surveyArea[0].position[1])), originalWidth)
    else:
        vehicleAreas[vehicle_name] = (Lawnmower(newWidth, surveyArea[0].height, vehicle.sensorRange, (currentEndPoint - newWidth, surveyArea[0].position[1])))

        print(str(vehicle.position[0]) + " >= " + str(midPoint) + " thus " + str(vehicle_name) +
               " is assigned (" + str(currentEndPoint - (newWidth)) +  ", " + str(currentEndPoint) + ")")
        remainingArea = (Lawnmower(lastWidth - newWidth, surveyArea[0].height, 0, (start, surveyArea[0].position[1])), originalWidth)
    # Recurse
    print("New remaining area is: " + str(remainingArea[0]))
    return assignArea(vehicles, remainingArea, vehicleAreas)
        