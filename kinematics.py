import numpy as np

# Declare constants -----------------------------------------------------------

N_LEGS = 8

# [coxa, femur, tibia]
SEGMENT_LENGTHS = np.array([1.2, 0.7, 1.0])
N_SEGMENTS = len(SEGMENT_LENGTHS)

# Ellipse dimensions for body
A = 1.5
B = 1.0

BASE_ANGLES = np.deg2rad([45, 75, 105, 135, -135, -105, -75, -45])
assert len(BASE_ANGLES) == N_LEGS

# Angle between coxa and XY plane
COXA_PITCH = np.deg2rad(30)
Z_AXIS = np.array([0, 0, 1])

# -----------------------------------------------------------------------------

def get_base_position(base_angle):
    """Returns the position of a leg-base given its angle round the body"""
    x_base = A * np.cos(base_angle)
    y_base = B * np.sin(base_angle)
    return np.array([x_base, y_base, 0])

def calculate_joint_positions(
    base_pos,
    base_angle,
    joint_angles,
    segment_lengths
    ):
    """Returns joint positions

    base_position
        [x, y, z] position of leg base on body
    base_angle
        angle around body ellipse where leg base is located (radians)
    joint_angles
        [coxa_yaw, femur_pitch, tibia_pitch] joint angles for the leg in radians
    segment_lengths
        [coxa, femur, tibia]
    """
    # TODO validate input maybe

    # Initialise array of joint positions.
    # Initially only includes where the coxa meets the body
    joints = [base_pos]

    # Initialise the "direction"
    # Initially the horizontal direction of leg in XY plane as a unit vector
    direction = np.array([
        np.cos(base_angle + joint_angles[0]),
        np.sin(base_angle + joint_angles[0]),
        0 # Zero corresponds to no Z direction
        ])

    # In the subsequent loop we treat each joint angle as the pitch
    # So we need to write the coxa pitch to the first joint_angle
    # To do that we need to make joint_angles writeable i.e. a list
    joint_angles = list(joint_angles)
    joint_angles[0] = COXA_PITCH

    # Main loop
    for i in range(3):
        rot_axis = np.cross(direction, Z_AXIS)
        direction = rotate_vector(direction, rot_axis, joint_angles[i])
        joints.append(joints[i] + direction * segment_lengths[i])

    return joints

def axis_angle_rotation_matrix(axis, angle):
    """Returns a rotation matrix corresponding to a rotation about the given axis by the given angle."""

    # Normalise the "axis" vector
    axis = axis / np.linalg.norm(axis)

    x, y, z = axis
    c = np.cos(angle)
    s = np.sin(angle)
    C = 1 - c
    
    # Rotation matrix
    # I've seperated out the construction to make it (hopefully) more readable
    r = np.array(
       [[x*x, x*y, x*z],
        [y*x, y*y, y*z],
        [z*x, z*y, z*z]],
        dtype=np.float64
    )
    r *= C
    r += np.array(
       [[c, -z*s, y*s],
        [z*s, c, -x*s],
        [-y*s, x*s, c]],
        dtype=np.float64
    )
    return r

def rotate_vector(vector, axis, angle):
    """Rotates a vector about the given axis by the given angle"""
    rotation_matrix = axis_angle_rotation_matrix(axis, angle)
    # Perform matrix multiplication (using the * operator results in broadcasting)
    return np.matmul(rotation_matrix, vector)