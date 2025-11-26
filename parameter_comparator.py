import genetic_algorithm
import matplotlib.pyplot as plt

class Parameter_Comparator:
    """Compares 4 genetic algorithms"""
    def __init__(
        self,
        population_sizes: [int],
        mutation_rates: [float],
        tracking_percentiles=[100,90,75,50,25,10]
    ):
        self.population_sizes = population_sizes
        self.mutation_rates = mutation_rates
        self.tracking_percentiles = tracking_percentiles

        assert len(population_sizes) == len(mutation_rates) == 4
        
        self.simulations = []
        for i in range(4):
            self.simulations.append(
                genetic_algorithm.Genetic_Algorithm(
                    population_sizes[i],
                    mutation_rates[i],
                    tracking_percentiles
                )
            )

    @property
    def generation(self):
        return self.simulations[0].generation
    
    def perform_generations(self, n):
        assert n>0

        for simulation in self.simulations:
            simulation.perform_generations(n)

    def show(self):
        fig = plt.figure()
        axes = []
        for i in range(4):
            axes.append(fig.add_subplot(2,2,i+1))
            axes[i].set_title(f"Population {self.population_sizes[i]}, "
                              f"Mutation Rate {self.mutation_rates[i]}")
            self.simulations[i].plot_generational_progression(axes[i])

        plt.show()

population_sizes = [50,100,150,200]
mutation_rates = [0.05,0.05,0.05,0.05]
pc = Parameter_Comparator(population_sizes, mutation_rates)