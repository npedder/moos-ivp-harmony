
class UxV:
    def __init__(self, name, type, position : tuple, speed, sensorRange, endurance, heading=0.0, color="red"):
        """
        Initialize a UxV instance.

        :param name: str, name of the vehicle
        :param position: tuple, (x, y) coordinates of the vehicle's starting position
        :param speed: float, speed of the vehicle (in units per time)
        :param endurance: float, how far the vehicle can travel (could represent fuel capacity)
        """
        self.name = name
        self.type = type
        self.position = position  # (x, y)
        self.speed = speed        # Speed (in units per time, e.g., km/h or miles/h)
        self.sensorRange = sensorRange
        self.endurance = endurance # Maximum distance the vehicle can travel (e.g., miles or km)
        self.heading = heading
        self.color = color # Vehicle color
        if(speed < 0 or endurance < 0 or sensorRange < 0):
            raise Exception("Speed endurance and sensor range cannot be negative, please reinput values.")
        if not (0 <= heading <= 360):
            raise Exception("Heading must be between 0 and 360, please reinput values.")

    def __repr__(self):
        return f"UxV(name={self.name}, type={self.type}, position={self.position}, speed={self.speed}, sensorRange={self.sensorRange}, endurance={self.endurance}, heading={self.heading}, color={self.color})"
