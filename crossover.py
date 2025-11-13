from random import randint

def sp_crossover(parent1, parent2):
    """Performs single-point crossover to produce 2 offspring.

Requires that the parents have equal length chromosomes"""

    if len(parent1) != len(parent2):
        raise ValueError("Parents must have equal length chromosomes")

    crossover_point = randint(0, len(parent1))
    offspring1 = parent1[0:i] + parent2[i:]
    offspring2 = parent2[0:i] + parent1[i:]

    return [offspring1, offspring2]
    

def sp_crossover_pop(parents):
    """Performs single-point crossover on a population of parents to produce 
a population of offspring of equal size.

If an odd number of parents are given, then the last parent is directly 
carried over."""
    offspring = []
    for i in range(0, len(parents) - 1, 2):
        offspring += sp_crossover(parents[i], parents[i+1])

    if len(parents) % 2 == 1:
        offspring.append(parents[-1])

    return offspring