import random
from numpy import shape
from initial import JOINT_LIMITS

def random_resetting_mutation(chromo, mutation_rate=0.01):
    """
    Peforms random resetting mutation on a floating-point chromosome
    """
    assert shape(chromo) == (8,3)

    for i in range(8):
        for j in range(3):
            if random.random() < mutation_rate:
                #replace gene with random number from boundaries
                chromo[i,j] = random.uniform(*JOINT_LIMITS[j])

    return chromo

def mutate_population(population, mutation_rate=0.01):
    for i in range(len(population)):
        population[i] = random_resetting_mutation(population[i], mutation_rate)

    return population

#test mutation
def test():
    for x in range(0,100):        
        print(random_resetting_mutation([1,2,3], 0.1))