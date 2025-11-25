import random
import numpy as np

def uniform_crossover(parent1, parent2):
    """Performs uniform crossover, returns a single child
    Each parent is an array of dimensions 8*3"""
    child = parent1
    for i in range(len(parent1)):
        for j in range(len(parent1[i])):
            # 50% chance to write parent2's gene. Otherwise, parent1's gene is inherited
            if random.random() > 0.5:
                child[i, j] = parent2[i, j]

    return child

def uniform_crossover_population(parents):
    """Performs uniform crossover on a population of parents to produce a
    population of offspring, of equal size."""
    offspring = np.zeros(shape=(len(parents), 8, 3))

    # This gives us an offspring population 1 less than the parent population
    # Every parent produces 2 offspring except the first and last
    for i in range(len(parents) - 1):
        offspring[i] = uniform_crossover(parents[i], parents[i+1])

    # For the final offspring, crossover the first and last parent
    # to give them 2 offspring each
    offspring[-1] = uniform_crossover(parents[0], parents[-1])
    return offspring