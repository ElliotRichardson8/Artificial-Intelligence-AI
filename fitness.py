import numpy as np
import kinematics

def single_pose_fitness(chromosome) -> float:
    """Evaluates the fitness of a single spider pose in isolation.
    Takes a chromosome of length 24, corresponding to 8*3 joint angles in radians."""

    # Convert 24x1 array into 8x3 array
    angles = np.reshape(chromosome, (8, 3))

    # Initialise joints
    all_joints = np.zeros(shape=(8, 4, 3))
    for i, leg_angles in enumerate(angles):
        all_joints[i] = kinematics.calculate_joint_positions(i, leg_angles)


    foot_height_reward = 0
    foot_distance_reward = 0
    leg_crossover_reward = 0

    foot_height_weight = 30
    foot_distance_weight = 1
    leg_crossover_weight = 20

    for leg_joints in all_joints:

        # Ensure legs don't intersect body
        # Ignore first joint because position of coxa on body is irrelevant
        if legs_intersect_body(leg_joints[1:]):
            return 0

        # Reward spider for feet being low down -------------------------------
        foot_height_reward -= leg_joints[-1, 2]
        # Subtracting the z position of the foot encourages
        # the foot to have a low z value

        # Reward spider for feet being far from body --------------------------
        foot_x, foot_y = leg_joints[-1, 0:2]
        foot_distance_reward += (kinematics.B * foot_x)**2 + (kinematics.A * foot_y)**2
        # Could use sqrt to find a more accurate representation of distance
        # But it would be a lot slower


    # Punish spider for legs crossing over ------------------------------------
    for i in range(3):
        if all_joints[i, -1, 0] < all_joints[i+1, -1, 0]:
            leg_crossover_reward -= 1

    for i in range(4,7):
        if all_joints[i, -1, 0] > all_joints[i+1, -1, 0]:
            leg_crossover_reward -= 1

    # Calculate and combine rewards
    return (
        foot_height_reward * foot_height_weight
        + foot_distance_reward * foot_distance_weight
        + leg_crossover_reward * leg_crossover_weight
    )
    



    
def legs_intersect_body(joints):
    """Checks if any of the legs intersect the body.
    Returns True if so, False if not"""

    # Iterate over all but the last joint
    for i in range(len(joints) - 1):
        # Consider two joints at a time
        j1, j2 = joints[i:i+2]

        # The body exists in the XY plane where Z=0
        # If both ends of the joint are on one side of this plane,
        # Then we know the leg does not intersect it.
        if j1[2] > 0 and j2[2] > 0 or j1[2] < 0 and j2[2] < 0:
            continue
        
        # Find where the line intersects the XY plane -------------------------

        # Determine the rate of change of x with respect to z
        ax = (j2[0] - j1[0]) / (j2[2] - j1[2])
        # Determine the rate of change of y with respect to z
        by = (j2[1] - j1[1]) / (j2[2] - j1[2])

        # Determine the value of x when z=0
        x = j1[0] - ax * j1[2]

        # Determine the value of y when z=0
        y = j1[1] - by * j1[2]

        if point_inside_ellipse(x, y, kinematics.A, kinematics.B):
            return True

        # else continue; consider next leg

    # No legs intersect body; return False
    return False


def point_inside_ellipse(x, y, a, b):
    """Returns a boolean corresponding to if point (x, y)
    lies inside an ellipse with major axis `a` and minor axis `b`
    (where a is aligned with the x axis and b is aligned with the y axis)
    
    Assumes the ellipse is centered on (0, 0)"""

    # Optimisations. If either ordinate lies outside the extrema
    # of the ellipse, the coordinate can be rejected
    if x > a:
        return False

    if y > b:
        return False

    # Pretty sure this works
    return (x**2)/(a**2) + (y**2)/(b**2) <= 1

def footprint_area(foot1, foot2, foot3):
    """Uses trigonometry to find footprint area"""