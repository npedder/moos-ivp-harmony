# Class to represent the Lawnmower waypoint function for MOOS IvP behavior scripting
class Lawnmower:
    def __init__(self, width, height, lane_width, position : tuple):
        self.width = width
        self.height = height
        self.lane_width = lane_width
        self.position = position  # (x, y) bottom left corner

    def __repr__(self):
        return f'"LAWNMOWER("points = format=lawnmower, x={self.position[0]}, y={self.position[1]}, height={self.height}, width={self.width}, lane_width={self.lane_width})""'

    def string(self):
        return f'points = format=lawnmower, x={self.position[0]}, y={self.position[1]}, height={self.height}, width={self.width}, lane_width={self.lane_width}'

    