
class SurveyArea:
    def __init__(self, width, height, position : tuple, gcd):
        self.width = width
        self.height = height
        self.position = position  # (x, y)
        self.gcd = gcd
    def areaToGrid(self, label):
        # neded for VIEW_GRID
        x, y = self.position

        bottom_right = (x + self.width, y)
        top_right = (x + self.width, y + self.height)
        top_left = (x, y + self.height)

        # Return the corners in order

        grid = f"pts={{{self.position[0]},{self.position[1]}:{top_left[0]},{top_left[1]}:{top_right[0]},{top_right[1]}:{bottom_right[0]},{bottom_right[1]}}},label='{label}',msg='{label},cell_size=5"
        return grid


    def __repr__(self):
        return f"SurveyArea(WIDTH={self.width}, HEIGHT={self.height}, POSITION={self.position})"