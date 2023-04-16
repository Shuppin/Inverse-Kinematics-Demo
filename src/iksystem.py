from arm import Arm

# Explicity define wildcard import to avoid importing 'Arm'
__all__ = [
    'InverseKinematicSystem'
]

class InverseKinematicSystem:
    """
    System capable of simulating inverse kinematics with as many arms as you want.
    
    Example usage:
    ```
    from iksystem import InverseKinematicSystem
    ik_system = InverseKinematicSystem(0, 0)
    ik_system.add_arm(150)
    ik_system.add_arm(150)
    ik_system.add_arm(40)
    while 1:
        # ...
        ik_system.reach(mouse_x, mouse_y)
        # ...
    ```
    """
    def __init__(self, origin_x: int, origin_y: int):
        self.origin_x: int = origin_x
        self.origin_y: int = origin_y
        self.arms: list[Arm] = []
        self.current_arm: Arm | None = None
        
    def get_arms(self) -> list[Arm]:
        """
        Returns a list of the arms in the system
        """
        return self.arms
        
    def add_arm(self, length: float):
        """
        Adds an arm to the system
        """
        new_arm = Arm(0,0,length,0)
        # If there is an arm present in the system before this one,
        # set it's origin to the end position of the previous arm,
        # and set the new arm's parent to the previous arm
        if self.current_arm is not None:
            new_arm.x = self.current_arm.get_end_x()
            new_arm.y = self.current_arm.get_end_y()
            new_arm.parent = self.current_arm
        # Else assume the arm is the first one and place it at the origin of the system
        else:
            new_arm.x = self.origin_x
            new_arm.y = self.origin_y
        
        self.arms.append(new_arm)  # Add the arm to the system
        self.current_arm = new_arm  # Update the current arm
        
    def drag(self, x, y):
        """
        Updates the system in drag mode.
        Drag mode has no fixed points and arms are dragged around freely.
        """
        if self.current_arm is not None:
            self.current_arm.drag(x, y)
            
    def reach(self, x, y):
        """
        Updates the system in reach mode.
        Reach mode anchors the first arm to the origin of the system.
        """
        self.drag(x, y) # Firstly, perform a normal drag as usual
        
        # Then, move each arm back to it's origin/parent's end position,
        # while keeping it's new rotation.
        # This part of the operation is actually forward kinematics,
        # as shown in my previous repo: https://github.com/Shuppin/Forward-Kinematics-Demo
        for arm in self.arms:
            if arm.parent is not None:
                arm.x = arm.parent.get_end_x()
                arm.y = arm.parent.get_end_y()
            else:
                arm.x = self.origin_x
                arm.y = self.origin_y
        
                