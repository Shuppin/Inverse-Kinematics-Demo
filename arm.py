import math

class Arm:
    def __init__(self, x, y, length, angle):
        self.x = x
        self.y = y
        self.length = length
        self.angle = angle
        self.parent: Arm | None = None
        
    def get_end_x(self):
        return self.x + math.cos(self.angle) * self.length
    
    def get_end_y(self):
        return self.y + math.sin(self.angle) * self.length
    
    def pointAt(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.angle = math.atan2(dy, dx)
        
    def drag(self, x, y):
        self.pointAt(x, y)
        
        self.x = x - math.cos(self.angle) * self.length
        self.y = y - math.sin(self.angle) * self.length
        
        if self.parent is not None:
            self.parent.drag(self.x, self.y)