import selection

class Genetic_Algorithm:
    """ A Genetic Algorithm object which only needs to be given an initial
 population, a fitness function, a crossover function, and a mutation function.""" 
    def __init__(self,
        initial_population,
        fitness_function,
        crossover_function,
        mutation_function
    ):
        self.population = initial_population
        self.fitness_function = fitness_function
        self.crossover_function = crossover_function
        self.mutation_function = mutation_function

    # One of the assumptions we're going to make is that the fitness function
    # considers each individual in isolation
    def evaluate_fitnesses(self):
        """Evaluates and returns all the fitnesses of the population"""
        fitnesses = []
        for individual in self.population:
            fitnesses.append(
                self.fitness_function(individual)
            )

        return fitnesses

    def perform_generation(self):
        """Performs 1 generation. 

        This includes fitness evaluation, selection, crossover, and mutation."""

        fitnesses = self.evaluate_fitnesses()

        # idk what selection function to use. Does it matter?
        # TODO test all the selection functions
        parents = selections.tournament_selection_population(
            self.population,
            fitnesses,
            len(population)
        )

        # we're gonna assume the crossover function works over an entire population
        offspring = self.crossover_function(parents)

        # Similarly for the mutation function
        mutated_offspring = self.mutation_function(offspring)

        self.population = mutated_offspring


    def perform_generations(self, n=50):
        """Performs n generations"""
        for i in range(n):
            self.perform_generation
