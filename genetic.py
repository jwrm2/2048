import controller
from multiprocessing import Pool
import random


def breed(parent1, parent2, sigma, num):
    """
    Breeds two controllers to create a child.
    The dimensions of the nets of the two parents must match.
    The parameter of the child is drawn from a normal distribution, with mean given by the average of the
    parental values and variance as specified.

    @param parent1: first parent
    @param parent2: second parent
    @param sigma: standard deviation of the normal distribution
    @param num: the number of games to average the fitness over
    @return child: a blending of the two parents
    """
    if parent1.net.params.shape != parent2.net.params.shape:
        raise ValueError("Can't breed nets: they are not the same shape")
    child = controller.Controller(1, [1], num)
    child.net = parent1.net.copy()
    for i in range(child.net.params.size):
        mu = (parent1.net.params[i] + parent2.net.params[i]) / 2
        child.net.params[i] = random.gauss(mu, sigma)
    child.net.sortModules()
    return child


def run_breeding(pop, sel, grid_size, hidden_list, drift, sigma, gen, num, proc):
    """
    Runs a complete simulation, breeding the nets.

    @param pop: number of nets in each generation
    @param sel: number of nets that survive to breed
    @param grid_size: dimension of the 2048 grid
    @param hidden_list: shape of the hidden layers in the net
    @param drift: determines how much asexual variation in each child
    @param sigma: determines how much sexual variation in each child
    @param gen: number of generation to run
    @param num: number of runs to average over when calculating fitness
    @param proc: the number of different threads to use when evaluating fitnesses
    """
    # Generate the initial population
    population = []
    for i in range(pop):
        population.append(controller.Controller(grid_size, hidden_list, num))

    best_fitness = 0
    best_params = []

    # Loop over the number of generations
    for i in range(gen):
        print "BEGINNING GENERATION " + str(i)

        pop_best_fitness = 0
        pop_best_params = []

        # Get fitness for each controller
        fitnesses = {}
        for j in range(pop/proc + 1):
            if proc*(j + 1) <= pop:
                p = proc
            else:
                p = pop - j*proc
            pool = Pool(p)
            fits = pool.map(controller.Controller.get_fitness, population[j*proc:j*proc + p])
            for k in range(len(fits)):
                fitnesses[population[]]

            fitnesses[population[j].get_fitness(num)] = population[j]

        # Select the best controllers
        breeding_population = []
        for key in sorted(fitnesses, reverse=True):
            if len(breeding_population) >= sel:
                break
            breeding_population.append(fitnesses[key])
            print "Adding controller with fitness " + str(key) + " to breeding population"
            if key > pop_best_fitness:
                pop_best_fitness = key
                pop_best_params = fitnesses[key].net.params
                print "New best fitness: " + str(best_fitness)
            if key > best_fitness:
                best_fitness = key
                best_params = fitnesses[key].net.params
                print "New best fitness: " + str(best_fitness)

        # Create the children by randomly selecting breeding pairs
        population = []
        while len(population) < pop:
            p1 = random.randint(0, len(breeding_population) - 1)
            p2 = p1
            while p2 == p1:
                p2 = random.randint(0, len(breeding_population) - 1)
            print "Breeding child from parent " + str(p1) + " and " + str(p2)
            child = breed(breeding_population[p1], breeding_population[p2], sigma)
            child.mutate(drift)
            population.append(child)

        print "Best population fitness: " + str(pop_best_fitness)
        print "Best population parameters: " + str(pop_best_params)
        print "Best fitness: " + str(best_fitness)
        print "Best parameters: " + str(best_params)
        print "END GENERATION " + str(i)
