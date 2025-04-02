class Status:
    def __init__(self, name, status):
        """
        Initialize a Status instance.

        :param name: str, name of the vehicle
        :param status: float, vehicle status, denoted by the number of resets of scripts
        """
        self.name = name
        self.status = status

        def __repr__(self):
            return f"Status(name={self.name}, status={self.status})"