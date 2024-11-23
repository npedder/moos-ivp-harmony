import re
import numpy as np
from UxV import UxV
from SurveyArea import SurveyArea



def parseNodeReportAndCreateVehicle(nodeReport):
    # Regular expression to extract NAME, LAT, and LON
    pattern = r"NAME=([^,]+),.*X=([-\d.]+),.*Y=([-\d.]+)"

    # Search for the match
    match = re.search(pattern, nodeReport)

    if match:
        name = match.group(1)
        x = float(match.group(2))
        y = float(match.group(3))

        # print(f"Name: {name}")
        # print(f"Latitude: {lat}")
        # print(f"Longitude: {lon}")

        vehicle = UxV(name, (x,y), None, None, None);
        return vehicle
    else:
        print("Pattern not found in the string.")
        return None

def parseHarmonyReportAndCreateVehicle(nodeReport):
    # Regular expression to extract NAME, LAT, and LON
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

        vehicle = UxV(name, (x, y), speed,sensor_range,endurance);
        return vehicle
    else:
        print("Pattern not found in the string.")
        return None

def parseSurveyAreaAndCreateObject(survey_msg):
    # Regular expression to extract NAME, LAT, and LON
    pattern = r"WIDTH=([^,]+),.*HEIGHT=([-\d.]+),.*X_POS=([-\d.]+),.*Y_POS=([-\d.]+)"


    # Search for the match
    match = re.search(pattern, survey_msg)

    if match:
        width = float(match.group(1))
        height = float(match.group(2))
        x_pos = float(match.group(3))
        y_pos = float(match.group(4))

        # print(f"Height: {height}")
        # print(f"Width: {width}")
        # print(f"X_pos: {x_pos}")
        # print(f"Y_pos: {y_pos}")

        surveyArea = SurveyArea(width, height, (x_pos, y_pos));
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
