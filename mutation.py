import random

def random_resetting_mutation(chromo, mutation_rate=0.01, lower=0, upper=1):
    """
    Peforms random resetting mutation on a floating-point chromosome
    """
    for i in range(len(chromo)):
        if random.random() < mutation_rate:
            #replace gene with random number from boundaries
            chromo[i] = random.uniform(lower, upper)

    return chromo

def mutate_population(population, mutation_rate=0.01, lower=0.1, upper=1):
    for i in range(len(population)):
        population[i] = random_resetting_mutation(population[i])

#test mutation
def test():
    for x in range(0,100):        
        print(random_resetting_mutation([1.2,3.4,5.6], 0.1, -5, 5))