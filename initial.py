import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize, suppress=True, precision=4)

"""
Joint limits are set in place to prevent impossible joint angles
"""
joint_limits = [
    (-0.78, 0.78), # coxa
    (-1.047, 1.047), # femur
    (-1.57, 1.57) # tibia
]

def generate_chromosome(joint_limits):
    chromosome = []
    for i in range(8):
        for j in range(3):
            low, high = joint_limits[j]
            angle = np.random.uniform(low, high)
            chromosome.append(angle)
    return np.array(chromosome)

def initial_population(pop_size, join_limits):
    return np.array([generate_chromosome(joint_limits) for x in range (pop_size)])

#test initial population
population = initial_population(50, joint_limits=joint_limits)
print(population[1])