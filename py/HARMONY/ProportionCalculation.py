from SurveyArea import SurveyArea
from UxV import UxV
from AreaAssignment import startAssignArea
import math as math


# Pre-condition:
#   Takes a dictionary that maps vehicle name to vehicle object, and a survey area
# Post-condition
#   Returns a dictionary that maps vehicle name to tuple of object and proportion of area
def calculateProportions(vehicles: dict, surveyArea: SurveyArea):

    totalSurveyArea = surveyArea.height * surveyArea.width
    vehicleProportions = {}
    totalCoverageRate = 0
    totalWeightedCapacity = 0

    # Iterate through vehicles, get totalCoverageRate sum
    for vehicle in vehicles.items():
        # Coverage rate for the specific vehicle ((m^2)/sec)
        totalCoverageRate += (vehicle[1].speed * vehicle[1].sensorRange)

    # Iterate through vehicles, get time effiency ratio for each vehicle, add it to new dictionary
    for vehicle in vehicles.items():
        
        # Calc timeEffRatio for each vehicle
        timeEffRatio = (vehicle[1].speed * vehicle[1].sensorRange) / totalCoverageRate
        vehicleProportions[vehicle[1].name] = (vehicle[1], timeEffRatio)

        # Calc total weighted capacity to use for ratios in te next step
        totalWeightedCapacity += (min(totalSurveyArea * vehicleProportions[vehicle[1].name][1], 
                            vehicle[1].endurance * vehicle[1].sensorRange))


    # Calculate the final proportions
    for vehicle in vehicles.items():
        weightedCapRatio = (min(totalSurveyArea * vehicleProportions[vehicle[1].name][1], 
                            vehicle[1].endurance * vehicle[1].sensorRange))/totalWeightedCapacity
        vehicleProportions[vehicle[1].name] = (vehicle[1], weightedCapRatio)
        # print(vehicle[1].name + "'s propotion of the area is " + str(weightedCapRatio))
    return vehicleProportions
        
# Below is a re-implementation of the startAreaAssign function which utilizes new
# equations which consider 
def calculateProportions2(vehicles: dict, surveyArea: SurveyArea):

    # Initial variables
    surveyCenter = (surveyArea.position[0] + surveyArea.width / 2, surveyArea.position[1] + surveyArea.height / 2)
    totalSurveyArea = surveyArea.height * surveyArea.width
    totalCoverageRate = 0
    totalWeightCapSum = 0
    vehicleProportions = {}
    T_max = 0 # estimated time taken to cover survey area

    # First sum coverage rates
    for vehicle_name, vehicle in vehicles.items():
        totalCoverageRate += (vehicle.speed * vehicle.sensorRange)

    # Then calculate all the fun stuff
    for vehicle_name, vehicle in vehicles.items():

        coverageRate = vehicle.speed * vehicle.sensorRange
        timeEffRatio = coverageRate / totalCoverageRate
        assignedArea = totalSurveyArea * timeEffRatio

        startTravelDistance = math.dist(vehicle.position, surveyCenter)
        startTravelTime = startTravelDistance / vehicle.speed
        # Subject to change once we have an endpoint attribute for the vehicle
        endTravelDistance = math.dist(vehicle.position, surveyCenter)  
        totalTravelDistance = startTravelDistance + endTravelDistance

        T_max += (assignedArea / coverageRate) + startTravelTime

    # Now calc the weight 
    for vehicle_name, vehicle in vehicles.items():
        
        coverageRate = vehicle.speed * vehicle.sensorRange
        timeEffRatio = coverageRate / totalCoverageRate
        assignedArea = totalSurveyArea * timeEffRatio
        totalAreaCapability = vehicle.endurance * vehicle.sensorRange

        startTravelDistance = math.dist(vehicle.position, surveyCenter)
        startTravelTime = startTravelDistance / vehicle.speed
        # Subject to change once we have an endpoint attribute for the vehicle
        endTravelDistance = math.dist(vehicle.position, surveyCenter)  
        totalTravelDistance = startTravelDistance + endTravelDistance
        if(startTravelTime >= 1):
            startTimeScalar = 1 - (startTravelTime - 1)/(T_max - 1)
        else:
            startTimeScalar = 1
        totalWeightCapSum += min(totalSurveyArea * (timeEffRatio * startTimeScalar), totalAreaCapability - (totalTravelDistance * vehicle.sensorRange))
        
    for vehicle_name, vehicle in vehicles.items():
        coverageRate = vehicle.speed * vehicle.sensorRange
        timeEffRatio = coverageRate / totalCoverageRate
        assignedArea = totalSurveyArea * timeEffRatio
        totalAreaCapability = vehicle.endurance * vehicle.sensorRange

        startTravelDistance = math.dist(vehicle.position, surveyCenter)
        startTravelTime = startTravelDistance / vehicle.speed
        # Subject to change once we have an endpoint attribute for the vehicle
        endTravelDistance = math.dist(vehicle.position, surveyCenter)  
        totalTravelDistance = startTravelDistance + endTravelDistance
        if(startTravelTime >= 1):
            startTimeScalar = 1 - (startTravelTime - 1)/(T_max - 1)
        else:
            startTimeScalar = 1
        vehicleProportions[vehicle_name] = (vehicle, min(totalSurveyArea * (timeEffRatio * startTimeScalar), totalAreaCapability - (totalTravelDistance * vehicle.sensorRange))/totalWeightCapSum)
    return vehicleProportions

