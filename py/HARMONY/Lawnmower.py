
class Lawnmower:
    def __init__(self, width, height, lande_width, position : tuple):
        self.width = width
        self.height = height
        self.lane_width = lande_width
        self.position = position  # (x, y)

    def __repr__(self):
        return f'"LAWNMOWER="points = format=lawnmower, x={self.position[0]}, y={self.position[1]}, height={self.height}, width={self.width}, lane_width={self.lane_width}""'
    