import re
import numpy as np
from UxV import UxV
from SurveyArea import SurveyArea
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as patches
import random
import math
from Status import Status


def parseNodeReportAndCreateVehicle(nodeReport):
    # Regular expression to extract NAME, LAT, and LON
    pattern = r"NAME=([^,]+),.*X=([-\d.]+),.*Y=([-\d.]+),.*HDG=([-\d.]+),.*COLOR=([^,]+)"
    # Search for the match
    match = re.search(pattern, nodeReport)

    if match:
        name = match.group(1)
        x = float(match.group(2))
        y = float(match.group(3))
        heading = match.group(4)
        color = match.group(5)

        # print(f"Name: {name}")
        # print(f"Latitude: {lat}")
        # print(f"Longitude: {lon}")
        # print(f"Color: {color}")
        vehicle = UxV(name, '',(x,y), None, None, None, heading, color)
        return vehicle
    else:
        print("Pattern not found in the string.")
        return None

def parseHarmonyReportAndCreateVehicle(nodeReport):
    # Regular expression to extract NAME, LAT, and LONRun = uTimerScript @ NewConsole = false
    pattern = r"NAME=([^,]+),.*TYPE=([^,]+),.*X=([-\d.]+),.*Y=([-\d.]+),.*SPD=([-\d.]+),.*ENDURANCE=([-\d.]+),.*SENSOR_RANGE=([-\d.]+)"

    # Search for the match
    match = re.search(pattern, nodeReport)

    if match:
        name = match.group(1)
        type = match.group(2) # TODO incorporate type (UUV or UAV)
        x = float(match.group(3))
        y = float(match.group(4))
        speed = float(match.group(5))
        endurance = float(match.group(6))
        sensor_range = float(match.group(7))

        # print(f"Name: {name}")
        # print(f"Latitude: {lat}")
        # print(f"Longitude: {lon}")

        vehicle = UxV(name, type, (x, y), speed,sensor_range,endurance, None, None)
        return vehicle
    else:
        print("Pattern not found in the string.")
        return None

def parseSurveyAreaAndCreateObject(survey_msg, gcd):
    # Regular expression to extract NAME, LAT, and LON
    pattern = r"WIDTH=([^,]+),.*HEIGHT=([-\d.]+),.*X_POS=([-\d.]+),.*Y_POS=([-\d.]+)"

    # Search for the match
    match = re.search(pattern, survey_msg)

    if match:
        width = float(match.group(1))
        height = float(match.group(2))
        x_pos = float(match.group(3))
        y_pos = float(match.group(4))

        # rounding width and height to match sensor range
        width = math.ceil(width / gcd) * gcd
        height = math.ceil(height / gcd) * gcd

        surveyArea = SurveyArea(width, height, (x_pos, y_pos), gcd)
        return surveyArea
    else:
        print("Pattern not found in the string.")
        return None

def convertSurveyAreaIntoMatrix(survey_area):
    start_x = survey_area.position[0]
    start_y = survey_area.position[1]
    max_x = start_x + survey_area.width
    max_y= start_y + survey_area.height

    # define the lower and upper limits for x and y
    minX, maxX, minY, maxY = start_x, max_x, start_y, max_y

    # create one-dimensional arrays for x and y
    x = np.arange(minX, maxX, (maxX - minX) / 10. + 1)
    y = np.arange(minY, maxY, (maxY - minY) / 10. + 1)
    # create the mesh based on these arrays
    x, y = np.meshgrid(x, y)

    print(x)
    print(y)

    coords = zip(x, y)

    print(tuple(coords))

def plotAssignments(vehicleAssignments: dict, vehicles: dict, totalSurvey: SurveyArea):
    # Create a figure and axis
    fig, ax = plt.subplots()

    count = 0
    legend_labels = []  # To store legend labels
    legend_colors = []  # To store legend color patches

    for name, survey in vehicleAssignments.items():
        # Create a rectangle
        colors = ["purple", "blue", "green", "yellow", "orange", "red"]
        color = colors[count % 5]
        rect = patches.Rectangle(
            (survey.position[0], survey.position[1]), survey.width, survey.height, 
            linewidth=1, edgecolor='g', facecolor=color
        )

        count = count + 1
        
        # Add the rectangle to the plot
        ax.add_patch(rect)
        ax.scatter(vehicles[name].position[0], vehicles[name].position[1], color=color)
        ax.text(vehicles[name].position[0], vehicles[name].position[1], f"{name}", fontsize=8, color='black')

        # Create legend entry for this rectangle
        if color not in legend_colors:  # Avoid duplicate legend entries for the same color
            legend_labels.append(name)  # Vehicle name
            legend_colors.append(patches.Patch(color=color))  # Color patch for legend

    ax.autoscale()
    plt.gca().set_aspect('equal', adjustable='box')

    # Add the legend
    ax.legend(legend_colors, legend_labels, title="Vehicles", bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    # plt.tight_layout()
    ax.set_title("Vehicle Assignments")

    plt.show()

def gcd_of_list(numList):
    gcd = math.gcd(numList[0], numList[1])
    for i in range(2, len(numList)):
        gcd = math.gcd(gcd, numList[i])
    return gcd


def parseStatusAndCreateObject(status_msg):
    pattern = r"NAME=([^,]+),.*STATUS=([^,]+)"

    match = re.search(pattern, status_msg)
    if match:
        name = match.group(1)
        status = match.group(2)

        vehicleStatus = Status(name, status)
        return vehicleStatus
    else:
        print("Pattern not found in the string.")
        return None

