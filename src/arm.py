import math

# Explicity define wildcard import to avoid importing 'math'
__all__ = [
    'Arm'
]

class Arm:
    """
    Represents an arm object and contains various
    functions to update and get information about the arm,
    used by `InverseKinematicSystem`
    """
    def __init__(self, x: int, y: int, length: float, angle: float):
        self.x: int = x
        self.y: int = y
        self.length: float = length
        self.angle: float = angle
        self.parent: Arm | None = None
        
    def get_end_x(self):
        """
        Calculates the x-coordinate of the end point of the arm
        based on its starting x-coordinate, length, and angle
        of rotation from the horizontal axis.
        """
        return self.x + math.cos(self.angle) * self.length
    
    def get_end_y(self):
        """
        Calculates the y-coordinate of the end point of the arm
        based on its starting y-coordinate, length, and angle
        of rotation from the horizontal axis.
        """
        return self.y + math.sin(self.angle) * self.length
    
    def point_at(self, x: int, y: int):
        """
        Sets the angle of the arm to point at the given coordinates.
        """
        dx = x - self.x
        dy = y - self.y
        self.angle = math.atan2(dy, dx)
        
    def drag(self, x, y):
        """
        This function drags the arm to a new position defined by
        the input x and y coordinates.
        """
        # Firstly, point the arm at the given coordinates.
        self.point_at(x, y)
        
        # Use trigonometry to find starting point of arm
        # Subtract the horizontal component and vertical component of the arm's length, 
        # as determined by cosine and sine of the arm's angle respectively, from the given coordinates.
        self.x = x - math.cos(self.angle) * self.length 
        self.y = y - math.sin(self.angle) * self.length

        
        # If the arm has a parent object, the drag function of the
        # parent object is called recursively with the new x and y coordinates
        # of the arm as input, so that the entire structure can be updated.
        if self.parent is not None:
            self.parent.drag(self.x, self.y)