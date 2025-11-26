import numpy as np
import kinematics

def get_all_joints(angles):
    assert np.shape(angles) == (8,3)
    
    joints = np.zeros(shape=(8, 4, 3))
    for i, leg_angles in enumerate(angles):
        joints[i] = kinematics.calculate_joint_positions(i, leg_angles)

    return joints

def static_fitness_angles(angles) -> float:
    assert np.shape(angles) == (8,3)
    joints = get_all_joints(angles)
    return static_fitness_joints(joints)

def static_fitness_joints(joints) -> float:
    """Evaluates the fitness of a single spider pose in isolation.
    Takes a chromosome of length 24, corresponding to 8*3 joint angles in radians."""

    assert np.shape(joints) == (8,4,3)

    foot_height_reward = 0
    foot_distance_reward = 0
    leg_crossover_reward = 0

    foot_height_weight = 30
    foot_distance_weight = 1
    leg_crossover_weight = 20

    for leg_joints in joints:

        # Ensure legs don't intersect body ------------------------------------
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
        if joints[i, -1, 0] < joints[i+1, -1, 0]:
            leg_crossover_reward -= 1

    for i in range(4,7):
        if joints[i, -1, 0] > joints[i+1, -1, 0]:
            leg_crossover_reward -= 1

    # Calculate and combine rewards
    return (
        foot_height_reward * foot_height_weight
        + foot_distance_reward * foot_distance_weight
        + leg_crossover_reward * leg_crossover_weight
    )

class CompoundFitnessEvaluator:
    def __init__(
        self, 
        previous_angles,
        static_fitness_weight = 1,
        dynamic_fitness_weight = 1
    ):
        assert np.shape(previous_angles) == (8,3)

        self.previous_angles = previous_angles
        self.previous_joints = get_all_joints(previous_angles)

        self.static_fitness_weight = static_fitness_weight
        self.dynamic_fitness_weight = dynamic_fitness_weight

        self.get_relative_feet_height()

    def get_relative_feet_height(self):
        """Calculates the range of z positions of feet in previous pose.
        
        Then, assigns each leg a new `foot_height` which is the distance of
        the foot to the midpoint of the range"""
        j = self.previous_joints

        lowest_foot_index = 0
        lowest_foot_height = j[lowest_foot_index, 3, 2]

        highest_foot_index = 0
        highest_foot_height = j[highest_foot_index,3,2]

        for leg in range(8):
            foot_height = j[leg,3,2]
            if foot_height < lowest_foot_height:
                lowest_foot_index = leg
                lowest_foot_height = foot_height
            elif foot_height > highest_foot_height:
                highest_foot_index = leg
                highest_foot_height = foot_height


        mid_height = (lowest_foot_height + highest_foot_height) / 2

        foot_height = np.zeros(8)
        for leg in range(8):
            foot_height[leg] = j[leg, 3, 2] - mid_height

        self.foot_height = foot_height
        
    def evaluate_fitness(self, new_angles):
        assert np.shape(new_angles) == (8,3)

        new_joints = get_all_joints(new_angles)

        static_fitness = static_fitness_joints(new_joints)
        dynamic_fitness = self.two_pose_fitness(new_angles, new_joints)

        return (
            static_fitness * self.static_fitness_weight
            + dynamic_fitness * self.dynamic_fitness_weight
        )

    def two_pose_fitness(self, new_angles, new_joints):
        foot_horizontal_reward = 0
        foot_vertical_reward = 0
        angle_stability_reward = 0

        foot_horizontal_weight = 1
        foot_vertical_weight = 1
        angle_stability_weight = 1

        for leg in range(8):

            # Low feet move back; high feet move forward ----------------------
            old_x = self.previous_joints[leg, 3, 0]
            new_x = new_joints[leg,3,0]

            distance_forward = new_x - old_x

            # High feet have positive height; reward them moving forward
            # Low feet have negative height; reward them moving backward
            foot_horizontal_reward += distance_forward * self.foot_height[leg]
            
            # Angles don't change too much ------------------------------------
            for angle in range(3):
                # Punish spider proportional to angle change
                angle_stability_reward -= abs(
                    new_angles[leg, angle] - self.previous_angles[leg, angle]
                )
            
        # Forward feet move up; backward feet move down -----------------------

        # Need to handle right and left sides seperately
        # Because angle behaviour is different for each side

        # Left legs; positive angle means leg is back
        for leg in range(4):
            coxa_angle = self.previous_angles[leg, 0]

            old_z = self.previous_joints[leg, 3, 2]
            new_z = new_joints[leg,3,2]

            distance_up = new_z - old_z

            # Reward spider for foot moving up while leg is back (and punish inverse)
            foot_vertical_reward += coxa_angle * distance_up

        for leg in range(4,8):
            coxa_angle = self.previous_angles[leg,0]
            old_z = self.previous_joints[leg,3,2]
            new_z = new_joints[leg,3,2]

            distance_up = new_z - old_z

            # Punish spider for foot moving up while leg is forward (and reward inverse)
            foot_vertical_reward -= coxa_angle * distance_up

        # Return final value --------------------------------------------------
        return (
            foot_horizontal_reward * foot_horizontal_weight
            + foot_vertical_reward * foot_vertical_weight
            + angle_stability_reward * angle_stability_weight
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
