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

def generate_chromosome(joint_limits=joint_limits):
    chromosome = np.zeros(shape=(8, 3))
    for leg in range(8):
        for segment in range(3):
            low, high = joint_limits[segment]
            angle = np.random.uniform(low, high)
            chromosome[leg, segment] = angle

    return chromosome

# TODO have these constants not be hardcoded
def initial_population(pop_size, joint_limits=joint_limits):
    population = np.zeros(shape=(pop_size, 8, 3))
    for i, individual in enumerate(population):
        population[i] = generate_chromosome(joint_limits)

    return population


def test():
    population = initial_population(50, joint_limits)
    print(population[1])