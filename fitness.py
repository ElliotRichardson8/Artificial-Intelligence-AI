import numpy as np
import kinematics

def single_pose_fitness(chromosome) -> float:
    """Evaluates the fitness of a single spider pose in isolation.
    Takes a chromosome of length 24, corresponding to 8*3 joint angles in radians."""

    # Convert 24x1 array into 8x3 array
    angles = np.reshape(chromosome, (8, 3))

    # Initialise joints
    all_joints = []
    for i, leg_angles in enumerate(angles):
        all_joints.append(kinematics.calculate_joint_positions(i, leg_angles))
    
    # Initialise fitness; we will modify this value henceforth
    fitness = 0


    # Legs don't intersect body
    if legs_intersect_body(joints):
        # Legs intersecting body is impossible; return a very bad fitness
        return -10000

    # Reward spider for having feet below the body
    for joints in all_joints:
        foot = joints[-1]

        # Subtract the z position of the foot
        # This encourages spider to have negative z position on feet
        # i.e. have its feet be below the body
        fitness -= foot[2]

    # Reward for having feet be the lowest joint
    # (technically just punishes for having feet not be the lowest joint)
    for joints in all_joints:
        lowest = 0
        for joint in joints:
            lowest = min(lowest, joint[2])

        foot = joints[-1]
        # If lowest joint is not foot, "lowest" will be lesser than foot[2]
        # Punish proportional to the distance between foot and lowest joint
        fitness -= foot[2] - lowest

    # Operations on footprint

    # Footprint 

    
    return fitness
    
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

single_pose_fitness(np.ones(24))

def footprint_area(foot1, foot2, foot3):
    """Uses trigonometry to find footprint area"""