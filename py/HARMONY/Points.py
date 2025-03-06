# Class to represent a list of waypoints for MOOS-IvP behavior scripting
class Points:
    def __init__(self, waypoints: list[tuple]):
        # Initialize with a list of (x, y) waypoints.
        # :param waypoints: List of tuples [(x1, y1), (x2, y2), ...]

        self.waypoints = waypoints

    def __repr__(self):
        # String representation for debugging.
        return f'"POINTS(points = {self.string()})"'

    def string(self):
        # Returns the waypoints formatted as a MOOS-IvP string.
        return f'points = ' + ":".join(f"{x},{y}" for x, y in self.waypoints)

    def add_waypoint(self, x, y):
        #Add a new waypoint to the list.
        self.waypoints.append((x, y))
