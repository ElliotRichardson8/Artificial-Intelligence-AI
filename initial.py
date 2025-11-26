import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize, suppress=True, precision=4)

"""
Joint limits are set in place to keep joint angles within plausible range

These values are sorta pulled from nowhere but they work pretty well. 
"""
JOINT_LIMITS = np.array([
    (-1, 1), # coxa
    (-2, 0.5), # femur
    (-2, 0.5) # tibia
])

def generate_chromosome(joint_limits=JOINT_LIMITS):
    chromosome = np.zeros(shape=(8, 3))
    for leg in range(8):
        for segment in range(3):
            angle = np.random.uniform(*joint_limits[segment])
            chromosome[leg, segment] = angle

    return chromosome

# TODO have these constants not be hardcoded
def initial_population(pop_size, joint_limits=JOINT_LIMITS):
    population = np.zeros(shape=(pop_size, 8, 3))
    for i, individual in enumerate(population):
        population[i] = generate_chromosome(joint_limits)

    return population

def test():
    population = initial_population(50)
    print(population[1])