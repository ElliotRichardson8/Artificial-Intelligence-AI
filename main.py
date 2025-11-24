import crossover, fitness, initial, mutation, selection
import forward_kinematics, plot_spider_pose
import numpy as np
import pygad

# input 1x24 list of angles in radians
def plot_spider_from_angles(angles):
    plot_spider_pose.plot_spider_pose(np.array(angles))


def main():
    populations = []; # 300 1x24 lists at the end
    all_fitness_scores = []; # lists at the end
    parent_amount = 10 # number of parents to select from each generation
    
    plot_spider_from_angles([0.1, 0.2, -0.1, 0.3, -0.2, 0.1, -0.1, 0.4, -0.3, 0.2, 0.1, -0.2, -0.3, 0.2, 0.1, 0.4, -0.1, -0.2, 0.3, -0.4, 0.2, 0.1, -0.3, 0.2])

    '''generate 300 populations for 300 generations
    each population has 24 chromosomes
    after each generation evaluate fitness of populations
    select 10 parents using roulette wheel selection
    perform crossover to produce 10 offspring
    mutate offspring using random resetting mutation with mutation rate of 0.1
    create new population with parents and mutated offspring
    '''

    # create initial population
    population = initial.initial_population(20, initial.joint_limits)
    for generation in range(200):
        populations.append(population)
        gen_fitness_scores = []
        for pop in range(len(population)):
            fitness_score = fitness.evaluate_population_fitness(population[pop], population[pop-1])
            gen_fitness_scores.append(fitness_score)
        print(f"Generation {generation} Population {len(population)} \nFitness: {gen_fitness_scores}")

        all_fitness_scores.append(gen_fitness_scores)
        fitest_indivuals = selection.tournament_selection_population(population, gen_fitness_scores, 2)
        plot_spider_from_angles(fitest_indivuals[0])
        
        selected_parents = selection.tournament_selection_population(population, gen_fitness_scores, parent_amount) # get 10 fitest parents
        population = [] # reset population
        for i in range(int(parent_amount/2)):
            offspring = crossover.sp_crossover(selected_parents[i], selected_parents[i*2])
        mutated_offspring = []
        for child in offspring:
            mutated_child = mutation.random_resetting_mutation(child, 0.1, -np.pi/2, np.pi/2)
            population.append(mutated_child)
        #population = selected_parents + mutated_offspring


main()

plot_spider_from_angles([0.1, 0.2, -0.1, 0.3, -0.2, 0.1, -0.1, 0.4, -0.3, 0.2, 0.1, -0.2, -0.3, 0.2, 0.1, 0.4, -0.1, -0.2, 0.3, -0.4, 0.2, 0.1, -0.3, 0.2])    