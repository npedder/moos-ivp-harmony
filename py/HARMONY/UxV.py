
class UxV:
    def __init__(self, name, position : tuple, speed, sensorRange, endurance):
        """
        Initialize a UxV instance.

        :param name: str, name of the vehicle
        :param position: tuple, (x, y) coordinates of the vehicle's starting position
        :param speed: float, speed of the vehicle (in units per time)
        :param endurance: float, how far the vehicle can travel (could represent fuel capacity)
        """
        self.name = name
        self.position = position  # (x, y)
        self.speed = speed        # Speed (in units per time, e.g., km/h or miles/h)
        self.sensorRange = sensorRange
        self.endurance = endurance # Maximum distance the vehicle can travel (e.g., miles or km)

    def __repr__(self):
        return f"UxV(name={self.name}, position={self.position}, speed={self.speed}, sensorRange={self.sensorRange}, endurance={self.endurance})"
