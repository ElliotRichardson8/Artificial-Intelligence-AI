class Genetic_Algorithm:
    """ A Genetic Algorithm object which only needs to be given an initial
 population, a fitness function, a crossover function, and a mutation function.
 
 Assumes that the fitness function considers each individual in isolation.
 Assumes that the selection, crossover and mutation functions operate over an 
 entire population.
 Assumes that the crossover function produces a population of equal size.""" 
    def __init__(self,
        initial_population,
        fitness_function,
        selection_function,
        crossover_function,
        mutation_function
    ):
        self.population = initial_population
        self.evaluate_fitness = fitness_function
        self.select_parents = selection_function
        self.crossover_population = crossover_function
        self.mutate_population = mutation_function

    # One of the assumptions we're going to make is that the fitness function
    # considers each individual in isolation
    def evaluate_fitnesses(self):
        """Evaluates and returns all the fitnesses of the population"""
        fitnesses = []
        for individual in self.population:
            fitnesses.append(
                self.evaluate_fitness(individual)
            )

        return fitnesses

    def perform_generation(self):
        """Performs 1 generation. 

        This includes fitness evaluation, selection, crossover, and mutation.
        Overwrites the current population with the post-gen population."""

        fitnesses = self.evaluate_fitnesses()
        parents = self.select_parents(self.population, fitnesses, len(population))
        offspring = self.crossover_population(parents)
        mutated_offspring = self.mutate_population(offspring)
        self.population = mutated_offspring

    def perform_generations(self, n=50):
        """Performs n generations"""
        for i in range(n):
            self.perform_generation
