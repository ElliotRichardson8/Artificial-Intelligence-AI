import matplotlib
import numpy as np

# Declare constants
segment_lengths = [] #TODO

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

    The first leg is L0 (front left), then legs go clockwise around the body
    until R0 (front right)
    """