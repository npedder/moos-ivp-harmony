from SurveyArea import SurveyArea
from Lawnmower import Lawnmower
from UxV import UxV

# vehicles is a dictionary that maps a vehicle name, to a tuple of a vehicle object and the proportion of the area
# that vehicle is responsible for
# vehicle[0] -> vehicle object
# vehicle[1] -> proportion of area

# vehicle areas is a dictionary that maps vehicle name to a tuple of vehicle object and a tuple containing the 
# two x values representing the width of the area

def startAssignArea(vehicles: dict, surveyArea: SurveyArea):
    # Commence recusrion
    vehicles_copy = vehicles.copy()
    vehicleAreas = {}
    # SimplifiedSurveyArea = (surveyArea.position[0], surveyArea.width, surveyArea.width)

    lawnmowerSurveyArea = (Lawnmower(surveyArea.width, surveyArea.height, 0, surveyArea.position), surveyArea.width)

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

    # Define points
    # start = surveyArea[0] # x value of the start of the survey area
    # midPoint = (start + surveyArea[1]) / 2
    # currentEndPoint = surveyArea[1]
    # originalWidth = surveyArea[2]

    # If we used lawnmower object
    start = surveyArea[0].position[0]
    midPoint = (start + surveyArea[0].width) / 2
    lastWidth = surveyArea[0].width
    currentEndPoint = (start + lastWidth)
    originalWidth = surveyArea[1]
    newWidth = originalWidth * proportion

    print("midPoint is " + str(midPoint))
    remainingArea = 0
    if vehicle.position[0] < midPoint:
        # vehicleAreas[vehicle_name] = (start, start + (newWidth))

        # If we use lawnmower
        vehicleAreas[vehicle_name] = Lawnmower(newWidth, surveyArea[0].height, vehicle.sensorRange, (start, surveyArea[0].position[1]))
        
        print(str(vehicle.position[0]) + " < " + str(midPoint) + " thus " + str(vehicle_name) +
               " is assigned (" + str(start) +  ", " + str(newWidth) + ")")
        
        # remainingArea = (newWidth, currentEndPoint, originalWidth)
        # if we use lawnmower
        remainingArea = (Lawnmower(lastWidth - newWidth, surveyArea[0].height, 0, (start + newWidth, surveyArea[0].position[1])), originalWidth)
        
    else:
        # vehicleAreas[vehicle_name] = (currentEndPoint - (newWidth), currentEndPoint)

        # if we use lawnmower
        vehicleAreas[vehicle_name] = (Lawnmower(newWidth, surveyArea[0].height, vehicle.sensorRange, (currentEndPoint - newWidth, surveyArea[0].position[1])))

        print(str(vehicle.position[0]) + " >= " + str(midPoint) + " thus " + str(vehicle_name) +
               " is assigned (" + str(currentEndPoint - (newWidth)) +  ", " + str(currentEndPoint) + ")")
        
        # remainingArea = (start, currentEndPoint - (newWidth), originalWidth)
        # if we use lawnmower

        remainingArea = (Lawnmower(lastWidth - newWidth, surveyArea[0].height, 0, (start, surveyArea[0].position[1])), originalWidth)

    # Recurse
    print("New remaining area is: " + str(remainingArea[0]))
    return assignArea(vehicles, remainingArea, vehicleAreas)
        