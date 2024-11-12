from SurveyArea import SurveyArea
from UxV import UxV
from AreaAssignment import startAssignArea
import matplotlib.pyplot as plt

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
        print(vehicle[1].name + "'s propotion of the area is " + str(weightedCapRatio))
    return vehicleProportions
        
def plotAssignments(vehicleAssignments: dict):
    plt.figure(figsize=(10, 5))

    for vehicle_name, (x_start, x_end) in vehicleAssignments.items():
        # Plot the range as a horizontal line
        plt.plot([x_start, x_end], [vehicle_name, vehicle_name], label=vehicle_name, marker='o')
    
    # Set labels and title
    plt.xlabel("Survey Area Range")
    plt.ylabel("Vehicle Name")
    plt.title("Vehicle Assignment Ranges in Survey Area")
    plt.legend()
    plt.grid(True)
    plt.show()




    


