from random import randint
import numpy as np

def sp_crossover(parent1, parent2):
    """Performs single-point crossover to produce 2 offspring.

Requires that the parents have equal length chromosomes"""

    if len(parent1) != len(parent2):
        raise ValueError("Parents must have equal length chromosomes")

    crossover_point = randint(0, len(parent1))
    offspring1 = np.concatenate((parent1[0:crossover_point], parent2[crossover_point:]))
    offspring2 = np.concatenate((parent2[0:crossover_point], parent1[crossover_point:]))

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