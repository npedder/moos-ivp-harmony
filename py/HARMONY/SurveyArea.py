
class SurveyArea:
    def __init__(self, width, height, position : tuple):
        self.width = width
        self.height = height
        self.position = position  # (x, y)

    def __repr__(self):
        return f"SurveyArea(WIDTH={self.width}, HEIGHT={self.height}, POSITION={self.position})"