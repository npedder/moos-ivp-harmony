from SurveyArea import SurveyArea
from UxV import UxV
from AreaAssignment import startAssignArea
from ProportionCalculation import calculateProportions, calculateProportions2
from utils import plotAssignments

# This file is the main program file for the task allocation functions

# Pre-condition: Receives a dictionary that maps vehicle name to vehicle object, and receives a SurveyArea object defining
#                the entire survey area
# Post-condition: Returns a dictionary mapping vehicle name to lawnmower survey object
def allocateArea(vehicles: dict, surveyArea: SurveyArea) :

    # Calculate proportions of the area that should be assigned to each vehicle
    vehicleProportions = calculateProportions(vehicles, surveyArea)

    # Assign proportions of the area to each vehicle
    vehicleAssignments = startAssignArea(vehicleProportions, surveyArea)

    return vehicleAssignments

# Defining some vehicles and a survey area for a test (can be removed)
surveyArea = SurveyArea(30, 30, (10, 10))

vehicle1 = UxV("Alpha", (0, 0), 1, 7, 100)
vehicle2 = UxV("Beta", (10, 3), 5, 3, 100)
vehicle3 = UxV("Charlie", (10, 10), 3, 7, 100)
vehicle4 = UxV("Delta", (1, 5), 3, 8, 100)

vehicles = {vehicle1.name: vehicle1, vehicle2.name: vehicle2, vehicle3.name: vehicle3, vehicle4.name: vehicle4}

vehicleAssignments = allocateArea(vehicles, surveyArea)
plotAssignments(vehicleAssignments, surveyArea)
