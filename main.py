import crossover, fitness, initial, mutation, selection
import forward_kinematics, plot_spider_pose
import numpy as np

"fresh start"

chromosomes = [] # 300 1x24 array 
all_fitness_scores = [] # 300 fitness scores
mutation_rate = 0.1
pop_size = 50
generations = 50


def generate_population(parent1, parent2, pop_size):
    offspring = []
    while len(offspring) < pop_size - 2:
        children = crossover.sp_crossover(parent1, parent2)
        for child in children:
            mutated_child = mutation.random_resetting_mutation(child, mutation_rate, -np.pi/2, np.pi/2)
            offspring.append(mutated_child)
            if len(offspring) >= pop_size - 2:
                break
    return offspring


def main():
    population = []
    # start with 1 individual and mutate for gen 2 then do crossover+mutatuion for gen 3-300
    individual = initial.initial_population(1, initial.joint_limits)
    chromosomes.append(individual[0])
    population.append(individual[0])

    # mutate individual. then breed untill we have 300 population
    mutated_individual = mutation.random_resetting_mutation(individual[0], 1, -np.pi/2, np.pi/2)
    population.append(mutated_individual)
    # crossover individual and mutated individual to create offspring untill we have 300 population
    while len(population) < pop_size:
        offspring = crossover.sp_crossover(population[0], population[1])
        for child in offspring:
            mutated_child = mutation.random_resetting_mutation(child, mutation_rate, -np.pi/2, np.pi/2)
            population.append(mutated_child)
    print(f"Initial Population Size: {len(population)}")

    '''loop for 298 generations
    evaluate fitness
    select fittest individual and add to chromosomes
    perform crossover to produce offspring
    mutate offspring
    add mutated offspring to chromosomes
    '''
    for generation in range(1, generations):
        gen_fitness_scores = []
        for pop in range(len(population)):
            fitness_score = fitness.evaluate_population_fitness(population[pop], population[pop-1])
            gen_fitness_scores.append(fitness_score)
        all_fitness_scores.append(gen_fitness_scores)
        fittest_individual = selection.tournament_selection_population(population, gen_fitness_scores, 1)[0]
        chromosomes.append(fittest_individual)

        # create new population
        population = []

        # create offspring from fittest individual and previous individual
        while len(population) < pop_size:
            offspring = crossover.sp_crossover(fittest_individual, chromosomes[generation-1])
            for child in offspring:
                mutated_child = mutation.random_resetting_mutation(child, mutation_rate, -np.pi/2, np.pi/2)
                population.append(mutated_child)
        if len(population) >= pop_size:
            population = population[:pop_size] # ensure population size is maintained
        print(f"End of Generation {generation} Population Size: {len(population)}")

    # visualize fittest individual from each generation
    #for angles in chromosomes:
    #    print(f"Fittest Individual Angles: {angles}")
    #    plot_spider_pose.plot_spider_pose(np.array(angles))
    plot_spider_pose.plot_spider_animation(chromosomes)

main()
    

