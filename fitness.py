from math import radians, sin, cos
import numpy as np
from forward_kinematics import calculate_joint_positions

base_angles = [45, 75, 105, 135, -135, -105, -75, -45]
a = 1.5
b = 1.0 
# ^ Ellipse axes for body

# Pre-calculate base position of the legs since it'll be the same each time
base_angles = [radians(angle) for angle in base_angles]
base_positions = []
for angle in base_angles:
    x_base = a * cos(angle)
    y_base = b * sin(angle)
    base_positions.append((x_base, y_base))        

def find_endpoints(all_angles: [float]) -> [(float)]:
    """Finds the endpoints of the legs of the spider
    i.e. where the leg connects to the body, its joints, and its end 
    
    Input is 1x24 list of leg angles
    Output is 8x4x3 list of endpoints of leg segments
    8 legs
    4 points (j)
    3 dimensions"""
    segment_lengths = [0.5, 1.0, 1.0] # coxa, femur, tibia lengths
    all_endpoints = []
    for i in range(8):
        leg_angles = all_angles[i*3:i*3+3]
        base_pos = np.array([base_positions[i][0], base_positions[i][1], 0])
        base_angle = base_angles[i]
        joint_positions = calculate_joint_positions(
            base_pos,
            base_angle,
            leg_angles,
            segment_lengths
        )
        all_endpoints.append(joint_positions)
    return all_endpoints

        

def evaluate_fitness(angles: [float], previous: [float]):
    """Evaluates a spider's fitness based on its joint angles and the previous state
    angles are a 1x24 list of radians each leg is 3 angles (coxa, femur, tibia) going in order of [left 1, left 2, left 3, left 4, right 4, right 3, right 2, right 1] 
    joints shouldn't be lower than the feet
    legs shouldn't be too far from previous state
    atleast 2 joints from either side should be on the ground
        LEFT 1 AND LEFT 3 should move at the same time as RIGHT 2 AND RIGHT 4
    fitness is higher for better spiders
    """
    
    fitness = 0
    leg_endpoints = find_endpoints(angles)
    # fail for joints being lower than feet
    for i in range(8):
        leg_angles = angles[i*3:i*3+3]
        foot_z = leg_endpoints[3][2]
        for j in range(3):
            joint_z = leg_endpoints[j][2]
            if joint_z.all() < foot_z.all():
                return -9999 # Arbitrary penalty factor

    # Penalty for legs moving too far from previous state
    for i in range(24):
        angle_diff = abs(angles[i] - previous[i])
        if angle_diff > radians(15): # Arbitrary threshold
            fitness -= 1 # Arbitrary penalty factor

    # Reward for having atleast 2 joints from either side on the ground
    left_grounded = 0
    right_grounded = 0
    for i in [0, 1, 2, 3]: # Left legs
        leg_angles = angles[i*3:i*3+3]
        endpoint = leg_endpoints[i]
        foot_z = endpoint[3][2]
        if foot_z.all() <= 0.01: # Arbitrary ground threshold
            left_grounded += 1
    for i in [4, 5, 6, 7]: # Right legs
        leg_angles = angles[i*3:i*3+3]
        endpoint = leg_endpoints[i]
        foot_z = endpoint[3][2]
        if foot_z.all() <= 0.01: # Arbitrary ground threshold
            right_grounded += 1
    if left_grounded >= 2:
        fitness += 20 # Arbitrary reward factor
    if right_grounded >= 2:
        fitness += 20 # Arbitrary reward factor

    return fitness


def evaluate_population_fitness(population, previous_fitest):
    fitnesses = []
    for individual in population:
        fitnesses.append(evaluate_fitness(individual, previous_fitest))
    return fitnesses
    #return evaluate_fitness(individual, previous_fitest) # Using first individual as previous state
    #return evaluate_fitness(population, previous_population)