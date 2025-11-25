import general, initial, fitness, selection, crossover, mutation
import plot_spider_pose

import numpy as np

DEFAULT_GENERATIONS = 50
POPULATION_SIZE = 50
DEFAULT_MUTATION_RATE = 0.001

def evaluate_fitnesses(population):
    fitnesses = np.zeros(len(population))
    for i in range(len(population)):
        fitnesses[i] = fitness.single_pose_fitness(population[i])

    return fitnesses

class Genetic_Algorithm:
    def __init__(
        self,
        population_size: int,
        mutation_rate=DEFAULT_MUTATION_RATE
    ):
        self.generation = 0
        self.population_size = population_size
        self.mutation_rate = mutation_rate

        self.population = initial.initial_population(population_size)
        self.fitnesses = evaluate_fitnesses(self.population)

    def set_mutation_rate(mutation_rate):
        self.mutation_rate = mutation_rate

    def perform_generation(self):
        parents = selection.tournament_selection_population(
            self.population, 
            self.fitnesses)
        offspring = crossover.uniform_crossover_population(parents)
        self.population = mutation.mutate_population(
            offspring, 
            self.mutation_rate)

        self.generation += 1
        self.fitnesses = evaluate_fitnesses(self.population)

    def perform_generations(self, n=DEFAULT_GENERATIONS):
        for i in range(n):
            self.perform_generation()

    def advance_generations(self, n):
        self.perform_generations(n)
        self.visualise_fittest()

    def visualise_fittest(self):
        print("Visualising the fittest individual")
        index = ga.fittest_individual()
        angles = self.population[index]
        fitness = self.fitnesses[index]
        print(f"Fitness: {fitness}")
        print(angles)
        plot_spider_pose.plot_spider_pose(angles)

    def fittest_individual(self):
        fittest_individual_index = 0
        fittest_fitness = self.fitnesses[0]

        for i in range(1, self.population_size):
            if self.fitnesses[i] > fittest_fitness:
                fittest_fitness = self.fitnesses[i]
                fittest_individual_index = i

        return fittest_individual_index
        
ga = Genetic_Algorithm(POPULATION_SIZE)
ga.perform_generations(DEFAULT_GENERATIONS)
ga.visualise_fittest()