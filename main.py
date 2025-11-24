import crossover, fitness, general, initial, mutation, selection
import forward_kinematics, plot_spider_pose
import numpy as np

def plot_spider_from_chromosome(chromosome):
    leg_bases = general.get_leg_bases()
    segment_lengths = general.get_segment_lengths()
    all_joints = []
    for leg in range(6):
        base_pos = leg_bases[leg]
        base_angle = general.get_leg_base_angle(leg)
        joint_angles = chromosome[leg*3:(leg+1)*3]
        joints = forward_kinematics.calculate_joint_positions(
            base_pos,
            base_angle,
            joint_angles,
            segment_lengths
        )
        all_joints.append(joints)
    plot_spider_pose.plot_spider(all_joints)

def main():
    populations = []; # 300 24x1 lists at the end
    fitness_scores = []; # 24x1 lists at the end
    
    for generation in range(300):
        population = initial.generate_chromosome(initial.joint_limits)
        fitness_score = fitness.evaluate_population_fitness(population)
        selected_parents = selection.select_parents(population, fitness_score)
        offspring = crossover.perform_crossover(selected_parents, 12)
        mutated_offspring = []
        for child in offspring:
            mutated_child = mutation.random_resetting_mutation(child, 0.1, -np.pi/2, np.pi/2)
            mutated_offspring.append(mutated_child)
        population = selected_parents + mutated_offspring
        populations.append(population)
        fitness_scores.append(fitness.evaluate_population_fitness(population))
        plot_spider_from_chromosome(population[generation])


main()