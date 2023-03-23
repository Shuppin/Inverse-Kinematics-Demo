from pyray import *
import math

from arm import Arm
from iksystem import InverseKinematicSystem
from utils import hsv_to_rgb

PADDING = 10

init_window(1600, 800, "ik_demo_1")
set_target_fps(120)

screen_width, screen_height = get_screen_width(), get_screen_height()

ik_system_1 = InverseKinematicSystem(
    int(0.25*screen_width), int(screen_height)
)
ik_system_2 = InverseKinematicSystem(
    int(0.75*screen_width), int(screen_height)
)
ik_system_3 = InverseKinematicSystem(
    int(0.25*screen_width), 0
)
ik_system_4 = InverseKinematicSystem(
    int(0.75*screen_width), 0
)

x = 40

for _ in range(x):
    ik_system_1.addArm(30)

for _ in range(x):
    ik_system_2.addArm(30)
    
for _ in range(x):
    ik_system_3.addArm(30)
    
for _ in range(x):
    ik_system_4.addArm(30)
    

def render_ik_system(ik_system):
    arms = ik_system.get_arms()
    num_arms = len(arms)
    for i, arm in enumerate(arms):
        hue = int(i / num_arms * 360)
        rgb = hsv_to_rgb(hue/360, 1.0, 1.0)
        r, g, b = [int(val * 255) for val in rgb]
        limb_between_points(arm.x, arm.y, arm.get_end_x(), arm.get_end_y(), (r,g,b,255))

def limb_between_points(p1_x, p1_y, p2_x, p2_y, colour):
    """
    Draws an ellipse connecting two points
    """
    # Calculate the point between p1 and p2 to set as the center of our ellipse
    midpoint_x = int((p1_x+p2_x) / 2)
    midpoint_y = int((p1_y+p2_y) / 2)
    
    # Calculate the angle between the two points and convert from radians to degrees
    angle = math.atan2(p2_y - p1_y, p2_x - p1_x) * 180 / math.pi
    
    # Set radii of ellipse
    radius_1 = math.sqrt((p2_y-p1_y)**2 + (p2_x-p1_x)**2)//2
    radius_2 = 10  # This value is essetially the 'thickness' of the limb

    rl_push_matrix()                                # Enter a new local space
    rl_translatef(midpoint_x, midpoint_y, 0)        # Move local space origin to midpoint
    rl_rotatef(angle, 0, 0, 1)                      # Rotate local space origin to the angle between p1 and p2
    draw_ellipse(0, 0, radius_1, radius_2, colour)  # Draw the ellipse
    rl_pop_matrix()                                 # Return to world space


while not window_should_close():
    
    # Update -----------------------------------------------------------------------
    mouse_position = get_mouse_position()
    if is_key_down(32):
        ik_system_1.drag(mouse_position.x, mouse_position.y)
        ik_system_2.drag(screen_width-mouse_position.x, mouse_position.y)
        ik_system_3.drag(mouse_position.x, screen_height-mouse_position.y)
        ik_system_4.drag(screen_width-mouse_position.x, screen_height-mouse_position.y)
    else:
        ik_system_1.reach(mouse_position.x, mouse_position.y)
        ik_system_2.reach(screen_width-mouse_position.x, mouse_position.y)
        ik_system_3.reach(mouse_position.x, screen_height-mouse_position.y)
        ik_system_4.reach(screen_width-mouse_position.x, screen_height-mouse_position.y)
    # ------------------------------------------------------------------------------
    
    # Draw -------------------------------------------------------------------------
    begin_drawing()
    
    clear_background(BLACK)
    
    render_ik_system(ik_system_1)
    render_ik_system(ik_system_2)
    render_ik_system(ik_system_3)
    render_ik_system(ik_system_4)
    
    draw_text("ik_demo_1", 0+PADDING, 0+PADDING, 20, VIOLET)

    end_drawing()
    # ------------------------------------------------------------------------------

close_window()