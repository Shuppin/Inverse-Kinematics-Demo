from pyray import *

import math
import sys

from iksystem import InverseKinematicSystem
from utils import hsv_to_rgb

# UI consts
UI_PADDING = 10
UI_SPACING = 5
FONT_SIZE = 30

# Snake demo consts
ARM_SEGMENTS = 30
ARM_LENGTH = 20

def render_ik_system(ik_system: InverseKinematicSystem, rainbow=True):
    """
    Draws an `InverseKinematicSystem` object to the screen.
    Must be called inside `begin_drawing()`
    """
    arms = ik_system.get_arms()
    
    if rainbow:
        num_arms = len(arms)
        for i, arm in enumerate(arms):
            
            # Calculate rainbow colour based on current index
            hue = int(i / num_arms * 360)
            r, g, b = hsv_to_rgb(float(hue/360), 1, 1)
            colour = (r,g,b,255)
            
            # Actually draw each arm/limb
            limb_between_points(arm.x, arm.y, arm.get_end_x(), arm.get_end_y(), colour)
            
    # Else we can skip all the colour computation since it isn't used
    else:
        red = (255,0,0,255)
        for arm in arms:
            limb_between_points(arm.x, arm.y, arm.get_end_x(), arm.get_end_y(), red)

def limb_between_points(p1_x, p1_y, p2_x, p2_y, colour):
    """
    Draws an ellipse connecting two points,
    assumes given points are valid coordinates within the bounds of the screen.
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
    rl_translatef(midpoint_x, midpoint_y, 0)        # Move local space origin to midpoint of p1 and p2
    rl_rotatef(angle, 0, 0, 1)                      # Rotate local space origin to the angle between p1 and p2
    draw_ellipse(0, 0, radius_1, radius_2, colour)  # Draw the ellipse
    rl_pop_matrix()                                 # Return to world space

def main():
    # Since the algorithm uses recursion,
    # just check to ensure the number of arms doesn't exceed the recursion limit
    if ARM_SEGMENTS > sys.getrecursionlimit():
        sys.setrecursionlimit(ARM_SEGMENTS+100)  # This assumes the current call stack isn't >100 in depth already
    
    init_window(1600, 800, "ik_demo_1")
    set_target_fps(120)
    
    screen_width, screen_height = get_screen_width(), get_screen_height()

    # Initialise arm IK system
    arm_ik_system = InverseKinematicSystem(
        int(0.5*screen_width), int(0.5*screen_height)
    )
    
    # Add arms
    arm_ik_system.add_arm(150)
    arm_ik_system.add_arm(150)
    arm_ik_system.add_arm(40)
    
    # Initialise snake IK system
    snake_ik_system = InverseKinematicSystem(
        int(0.5*screen_width), int(0.5*screen_height)
    )

    # Add arms (limbs? segements?)
    for _ in range(ARM_SEGMENTS):
        snake_ik_system.add_arm(ARM_LENGTH)
        
    systems = [arm_ik_system, snake_ik_system]
    current_system_index = 0
    
    mode = 0
    mode_text = "REACH MODE"
    title_text = "ik_demo_1"
    
    frame_times = []
    avg_fps = -1
    min_fps = -1
    max_fps = -1

    # Main program loop
    while not window_should_close():
        
        # Update -----------------------------------------------------------------------
        frame_time = get_frame_time()
        mouse_position = get_mouse_position()
    
        # The first frame always has a frame time of 0, so we skip computation for it.
        if frame_time != 0:  
            frame_times.append(1/frame_time)
            
        # We only want the average of the last 200 frames,
        # so if the list is longer, remove the oldest ones.
        if len(frame_times) > 200:
            frame_times.pop(0)
        # Make sure there are actual frames to calculate values from,
        # then calculate the min, max and average fps
        if len(frame_times) != 0:
            avg_fps = sum(frame_times)/len(frame_times)
            min_fps = min(frame_times)
            max_fps = max(frame_times)
        
        # The first line of text that gets displayed in the top left of the screen
        title_text = f"ik_demo_1 | {avg_fps:.2f} ({min_fps:.2f}/{max_fps:.2f}) FPS"
        
        # If space is pressed, switch to the next system
        if is_key_pressed(32):  # SPACE
            current_system_index = int(not current_system_index)
        
        # If x is pressed, change the mode
        if is_key_pressed(120) or is_key_pressed(88):  # 'x' and 'X'
            mode = int(not mode)
            mode_text = "DRAG (slither.io) MODE" if mode == 1 else "REACH MODE"
        if mode == 1:
            systems[current_system_index].drag(mouse_position.x, mouse_position.y)
        else:
            systems[current_system_index].reach(mouse_position.x, mouse_position.y)
        # ------------------------------------------------------------------------------
        
        # Draw -------------------------------------------------------------------------
        begin_drawing()
        
        clear_background(BLACK)  # Clear the screen so we don't see things from previous frames
        
        # Firstly, draw the current ik system
        render_ik_system(systems[current_system_index])

        vertical_increment = FONT_SIZE+UI_SPACING

        # Then draw the text after, so it always appears on top
        draw_text(title_text, 0+UI_PADDING, 0+UI_PADDING, FONT_SIZE, VIOLET)
        draw_text(mode_text, 0+UI_PADDING, vertical_increment+UI_PADDING, FONT_SIZE, VIOLET)
        draw_text("press SPACE to change systems", 0+UI_PADDING, vertical_increment*2+UI_PADDING, FONT_SIZE, VIOLET)
        draw_text("press X to change modes", 0+UI_PADDING, vertical_increment*3+UI_PADDING, FONT_SIZE, VIOLET)

        end_drawing()
        # ------------------------------------------------------------------------------

    close_window()
    
if __name__ == '__main__':
    main()