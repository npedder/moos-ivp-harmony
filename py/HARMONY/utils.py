import re
from UxV import UxV
from SurveyArea import SurveyArea



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

        vehicle = UxV(name, (lat,lon), 10, 100, 100 );
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
        width = match.group(1)
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
