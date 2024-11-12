from SurveyArea import SurveyArea
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
    SimplifiedSurveyArea = (surveyArea.position[0], surveyArea.width, surveyArea.width)
    newVehicleAreas = assignArea(vehicles_copy, SimplifiedSurveyArea, vehicleAreas)
    print("Area assignment complete")
    return newVehicleAreas

# Recursively assign survey area to each vehicle 
def assignArea(vehicles: dict, surveyArea: tuple, vehicleAreas: dict):
    
    # Base case
    if not vehicles:
        print("base case for assignment hit")
        print("Vehicle areas are" + str(vehicleAreas))
        return vehicleAreas
    
    
    # Recursive case
    print("Running recursive case")
    vehicle_name , (vehicle, proportion) = vehicles.popitem()
    print("==============================================")
    print("===Currently on vehicle " + vehicle_name + "===")
    print("==============================================")
    start = surveyArea[0] # x value of the start of the survey area
    midPoint = (start + surveyArea[1]) / 2
    print("midPoint is " + str(midPoint))
    remainingArea = 0
    if vehicle.position[0] < midPoint:
        vehicleAreas[vehicle_name] = (start, start + (surveyArea[2] * proportion))
        print(str(vehicle.position[0]) + " < " + str(midPoint) + " thus " + str(vehicle_name) +
               " is assigned (" + str(start) +  ", " + str(surveyArea[2] * proportion) + ")")
        remainingArea = (surveyArea[2] * proportion, surveyArea[1], surveyArea[2])
    else:
        vehicleAreas[vehicle_name] = (surveyArea[1] - (surveyArea[2] * proportion), surveyArea[1])
        print(str(vehicle.position[0]) + " >= " + str(midPoint) + " thus " + str(vehicle_name) +
               " is assigned (" + str(surveyArea[1] - (surveyArea[2] * proportion)) +  ", " + str(surveyArea[1]) + ")")
        remainingArea = (start, surveyArea[1] - (surveyArea[2] * proportion), surveyArea[2])

    # Recurse
    print("New remaining area is (" + str(remainingArea[0]) + ", " + str(remainingArea[1]) + ")")
    return assignArea(vehicles, remainingArea, vehicleAreas)
        