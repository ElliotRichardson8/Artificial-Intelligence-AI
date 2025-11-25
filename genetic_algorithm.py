import initial, fitness, selection, crossover, mutation
import plot_spider_pose

from matplotlib import pyplot as plt

import numpy as np

DEFAULT_GENERATIONS = 50
POPULATION_SIZE = 50
DEFAULT_MUTATION_RATE = 0.01
DEFAULT_TRACKING_PERCENTILES = np.array([100, 75, 50, 25])

def evaluate_fitnesses(population):
    fitnesses = np.zeros(len(population))
    for i in range(len(population)):
        fitnesses[i] = fitness.single_pose_fitness(population[i])

    return fitnesses

class Genetic_Algorithm:
    def __init__(
        self,
        population_size: int,
        mutation_rate=DEFAULT_MUTATION_RATE,
        tracking_percentiles=DEFAULT_TRACKING_PERCENTILES
    ):
        self.generation = 0
        self.population_size = population_size
        self.mutation_rate = mutation_rate

        self.population = initial.initial_population(population_size)
        self.fitnesses = evaluate_fitnesses(self.population)

        self.tracking_percentiles = tracking_percentiles
        self.recorded_fitnesses = np.zeros(shape=(len(tracking_percentiles),0))

    def set_mutation_rate(self, mutation_rate):
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

        generation_entries = np.zeros((len(self.tracking_percentiles),1))

        for i, percentile in enumerate(self.tracking_percentiles):
            sorted_fitnesses = sorted(self.fitnesses)
            generation_entries[i] = sorted_fitnesses[
                round(percentile/100 * (self.population_size-1)) # the -1 is there because idk how else to prevent index errors
            ]

        self.recorded_fitnesses = np.append(self.recorded_fitnesses, 
                                            generation_entries, 
                                            axis=1)
            
    def perform_generations(self, n=DEFAULT_GENERATIONS):
        for i in range(n):
            self.perform_generation()

    def fittest_individual(self):
        fittest_individual_index = 0
        fittest_fitness = self.fitnesses[0]

        for i in range(1, self.population_size):
            if self.fitnesses[i] > fittest_fitness:
                fittest_fitness = self.fitnesses[i]
                fittest_individual_index = i

        return fittest_individual_index

    def plot_fittest(self, ax):
        index = ga.fittest_individual()
        angles = self.population[index]
        fitness = self.fitnesses[index]
        plot_spider_pose.plot_spider_pose(angles, ax)

    def plot_generational_progression(self, ax):
        for i in range(len(self.tracking_percentiles)):
            ax.plot(range(self.generation), self.recorded_fitnesses[i], label=i)

        ax.set_xlabel("Generation")
        ax.set_ylabel("Fitness")
        ax.grid(True)
        ax.legend(self.tracking_percentiles, title="Percentile")
        
    def show_generational_progression(self):
        fig = plt.figure()
        ax = fig.add_subplot()
        self.plot_generational_progression(ax)
        plt.show()

    def show_fittest(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        self.plot_fittest(ax)
        plt.show()

    def show(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(2,1,1, projection="3d")
        ax2 = fig.add_subplot(2,1,2)
        self.plot_fittest(ax1)
        self.plot_generational_progression(ax2)
        plt.show()

ga = Genetic_Algorithm(POPULATION_SIZE)
ga.perform_generations(DEFAULT_GENERATIONS)