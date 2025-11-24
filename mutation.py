import random

def random_resetting_mutation(chromo, mutationRate, lower, upper):
    """
    Peforms randon resetting mutation on a floating-point chromosome
    """
    for x in range(len(chromo)):
        if random.random() < mutationRate:
            #replace gene with random number from boundaries
            chromo[x] = random.uniform(lower,upper)
    return chromo

#test mutation
def test():
    for x in range(0,100):        
        print(random_resetting_mutation([1.2,3.4,5.6], 0.1, -5, 5))