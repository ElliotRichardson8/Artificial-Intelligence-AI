import matplotlib
import numpy as np

# Declare constants -----------------------------------------------------------

# [coxa, femur, tibia]
SEGMENT_LENGTHS = np.array([1.2, 0.7, 1.0])

# Ellipse dimensions for body
A = 1.5
B = 1.0

# Base angles
BASE_ANGLES = np.deg2rad([45, 75, 105, 135, -135, -105, -75, -45])

# Leg labels
LEG_LABELS = ("L1", "L2", "L3", "L4", "R4", "R3", "R2", "R1")

# Main function ---------------------------------------------------------------
def plot_spider_pose(angles):
    """Plot a static 3D spider pose based on joint angles

    Input:
        angles: 1x24 vector of joint angles in radians

    There are 8 legs with 3 angles each. 
    The segments of the leg are coxa, femur, tibia 
    The 3 angles of each leg correspond roughly to these three segments
    Angle 1 is the yaw (rotation about vertical axis) of the coxa
    Angle 2 is the pitch of the femur
    Angle 3 is the pitch of the tibia

    The first leg is L0 (front left), then legs go anticlockwise around the body
    until R0 (front right)
    """
    # Important to remember that "left" is the spider's left, not the observer's left