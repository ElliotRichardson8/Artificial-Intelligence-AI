import random

def affirm_suitability(population, fitnesses):
    """Raises an error if these inputs are unsuitable for selection"""

    if len(fitnesses) != len(population):
        raise ValueError("Length of elements and fitnesses must be equal")

    if len(population) < 2:
        raise ValueError(
            f"Size of population must be greater than 1.\nRecieved {len(population)}")

    # doesn't check for type consistency because that would take forever
    # Just use type hints you guys

#TODO
# There's a bunch of selection methods here because I implemented them as homework
# I don't think I tested these ... per se. 
# We only need one selection algorithm, of course. We can use one or none of these
# Should delete the ones we don't use.

# TODO test this
def tournament_selection_individual(population, fitnesses, x=2):
    """Selects a single individual from an x-way tournament"""

    if x < 2:
        raise ValueError(f"Value for x must be greater than 1\n Received {x}")

    # Select indexes corresponding to x different individuals
    candidates = random.sample(range(0,len(population)),len(population))
    fitest_candidate = 0
    greatest_fitness = fitnesses[0]

    for candidate in candidates:
        if fitnesses[candidate] > greatest_fitness:
            greatest_fitness = fitnesses[candidate]
            fitest_candidate = candidate

    return population[fitest_candidate]

# TODO test this
def tournament_selection_population(population, fitnesses: [int], n: int, x=2):
    """Performs x-way tournament selection until n individuals are selected"""

    affirm_suitability(population, fitnesses)

    parents = []
    for i in range(n):
        parents.append(
            tournament_selection_individual(population, fitnesses, x)
        )

    return parents

# TODO test this
def calculate_cumulative_fitnesses(fitnesses):
    """Returns normalised cumulative fitnesses"""
    sum_fitness = sum(fitnesses)
    cumulative_fitnesses = [0] * len(fitnesses)
    cumulative_fitnesses[0] = fitnesses[0] / sum_fitness

    for i in range(1, len(fitnesses)):
        cumulative_fitnesses[i] = (fitnesses[i] / sum_fitness) + cumulative_fitnesses[i - 1]

    # ^Should add up to 1 but maybe it won't because of floating point imprecision
    return cumulative_fitnesses

# TODO test this
def roulette_wheel_selection_individual(population, cumulative_fitnesses):
    """Selects a single individual using roulette wheen selection"""
    selection_point = random.uniform(0, 1)
    
    i = 0
    while selection_point > cumulative_fitnesses[i]:
        i += 1

    # if this produces an error it's probly cause of floating point imprecision
    return cumulative_fitnesses[i]

# TODO test this
def roulette_wheel_selection_population(population, fitnesses: [int], n: int):
    """Performs roulette wheel selection until n individuals are selected"""

    affirm_suitability(population, fitnesses)

    # Calculate cumulative fitnesses
    cumulative_fitnesses = calculate_cumulative_fitnesses(fitnesses)

    # Do the selection innit
    parents = []
    for i in range(n):
        parents.append(
            roulette_wheel_selection_individual(population, cumulative_fitnesses)
        )

    return parents


# TODO test this
def SUS_selection_population(population, fitnesses: [int], n: int):
    """Selects n elements using Stochastic Universal Sampling"""

    affirm_suitability(population, fitnesses)
    cumulative_fitnesses = calculate_cumulative_fitnesses(fitnesses)

    parents = []
    selection_points = [random.uniform(0, 1) for i in range(n)]
    for i, fitness in enumerate(cumulative_fitnesses):
        for sp in selection_points:
            if sp < fitness:
                parents.append(population[i])
                selection_points.remove(sp)
    # This has 3 levels of indentation which I know some consider bad form

    return parents

