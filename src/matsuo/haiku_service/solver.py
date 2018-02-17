
import random

from deap import base
from deap import creator
from deap import tools
from nltk.corpus import brown
from textstat import textstat

words = set(brown.words())
keywords = None


def _mutate(individual):
    fxs = []
    can_add
    fx_idx = random.randint(0, len(fxs) - 1)




def _crossover(individual1, individual2):
    new_ind1 = [[], [], []]
    new_ind2 = [[], [], []]
    for idx in len(individual1):
        if random.randint(0, 1) == 0:
            individual1[idx], individual2[idx] = individual1[idx], individual2[idx]
        else:
            individual1[idx], individual2[idx] = individual2[idx], individual1[idx]
    return new_ind1, new_ind2


def _coherence_score(individual):
    if len(individual) != 3:
        return -1
    constraints = [5, 7, 5]
    line_lengths = [0, 0, 0]
    for idx in len(line_lengths):
        for word in individual[idx]:
            line_lengths[idx] += textstat.textstat.syllable_count(word)

    syllable_fitness = 0
    for idx in line_lengths:
        syllable_fitness += 1 - (1 / len(line_lengths)) * abs(line_lengths[idx] - constraints[idx])
    words = list()
    for line in individual:
        words.extend(line)

    words = set(words)
    occurance = 0
    for keyword in keywords:
        if keyword in words:
            occurance += 1
    keyword_fitness = 1 - 1/occurance

    return keyword_fitness * syllable_fitness


def _create_individual():
    return [[random.choice(keywords)], [random.choice(keywords)], [random.choice(keywords)]]


def create_haiku_with_ga(kws, mutation_prob=0.05, crossover_prob=0.1):
    global keywords
    keywords = kws
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, _create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", _coherence_score)
    toolbox.register("mate", _crossover)
    toolbox.register("mutate", _mutate, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=300)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]
    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while max(fits) < 100 and g < 1000:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < crossover_prob:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutation_prob:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        pop[:] = offspring
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
    return pop[max(fits)]


def create_haiku(keywords, fx=create_haiku_with_ga, **kwargs):
    return fx(keywords, kwargs)
