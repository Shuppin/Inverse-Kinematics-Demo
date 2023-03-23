from arm import Arm

class InverseKinematicSystem:
    def __init__(self, origin_x, origin_y):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.arms: list[Arm] = []
        self.last_arm: Arm | None = None
        
    def get_arms(self):
        return self.arms
        
    def addArm(self, length):
        arm = Arm(0,0,length,0)
        if self.last_arm is not None:
            arm.x = self.last_arm.get_end_x()
            arm.y = self.last_arm.get_end_y()
            arm.parent = self.last_arm
        else:
            arm.x = self.origin_x
            arm.y = self.origin_y
            
        self.last_arm = arm
        self.arms.append(arm)
        
    def drag(self, x, y):
        if self.last_arm is not None:
            self.last_arm.drag(x, y)
            
    def reach(self, x, y):
        self.drag(x, y)
        self.update()
        
    def update(self):
        for arm in self.arms:
            if arm.parent is not None:
                arm.x = arm.parent.get_end_x()
                arm.y = arm.parent.get_end_y()
            else:
                arm.x = self.origin_x
                arm.y = self.origin_y
                