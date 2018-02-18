
import random

from deap import base
from deap import creator
from deap import tools
from nltk.corpus import brown
from textstat import textstat

from matsuo.utils.haiku import Haiku

from matsuo.haiku_judge.judge import HaikuJudge, HaikuModel


def get_words():
    w = list(set(brown.words()))
    good_words = list()
    for word in w:
        if word not in ('!', '?', "'"):
            good_words.append(word)
    return good_words


words = get_words()
haiku_judge = None
keywords = None


class Fitness:
    def __init__(self):
        self.values = list()
        self.valid = False

    def __lt__(self, other):
        return self.values < other.values

    def __le__(self, other):
        return self.values <= other.values

    def __eq__(self, other):
        return self.values == other.values

    def __ne__(self, other):
        return self.values != other.values

    def __gt__(self, other):
        return self.values > other.values

    def __ge__(self, other):
        return self.values >= other.values


class Individual:

    def __init__(self, lines):
        self.lines = lines
        self.fitness = Fitness()

    def __copy__(self):
        return Individual([list(line) for line in self.lines])


def _mutate(individual):
    fxs = [add_word, delete_word, jumble_words]
    random.choice(fxs)(individual)


def add_word(individual):
    random.choice(individual.lines).insert(random.randint(0, len(individual.lines)-1), random.choice(words))


def delete_word(individual):
    try:
        random.choice(individual.lines).remove(random.randint(0, len(individual.lines) - 1))
    except Exception:
        pass


def jumble_words(individual):
    random.shuffle(random.choice(individual.lines))


def _crossover(individual1, individual2):
    new_ind1 = [[], [], []]
    new_ind2 = [[], [], []]
    for idx in range(len(individual1.lines)):
        if random.randint(0, 1) == 0:
            individual1.lines[idx], individual2.lines[idx] = individual1.lines[idx], individual2.lines[idx]
        else:
            individual1.lines[idx], individual2.lines[idx] = individual2.lines[idx], individual1.lines[idx]
    return new_ind1, new_ind2


def _coherence_score(individual):
    if len(individual.lines) != 3:
        return [-1]
    constraints = [5, 7, 5]
    line_lengths = [0, 0, 0]
    for idx in range(len(line_lengths)):
        for word in individual.lines[idx]:
            try:
                if len(word) > 0:
                    line_lengths[idx] += textstat.textstat.syllable_count(word)
                else:
                    return [-1]
            except Exception:
                return [-1]

    syllable_constraint = 0
    for idx in range(len(line_lengths)):
        syllable_constraint += 1/len(line_lengths) - (1/len(line_lengths)) * abs(line_lengths[idx] - constraints[idx])

    haiku_words = list()
    for line in individual.lines:
        haiku_words.extend(line)
    haiku_words = set(haiku_words)
    occurance = sum(map(lambda word: 1 if word in keywords else 0, haiku_words))
    keyword_fitness = 1 - 1/occurance
    return [syllable_constraint * keyword_fitness * haiku_judge.judge_haiku(individual.lines)]


def _create_individual():
    return Individual([[random.choice(keywords), random.choice(words), random.choice(words)],
                       [random.choice(words), random.choice(keywords), random.choice(words)],
                       [random.choice(words), random.choice(words), random.choice(keywords)]])


def create_haiku_with_ga(kws, mutation_prob=0.5, crossover_prob=0.1, max_gen=200, pop_size=30):
    global keywords
    keywords = kws
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", Individual, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    # Structure initializers
    toolbox.register("individual", _create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", _coherence_score)
    toolbox.register("mate", _crossover)
    toolbox.register("mutate", _mutate)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=pop_size)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]
    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while max(fits) < 100 and g < max_gen:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(lambda ind: ind.__copy__(), offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < crossover_prob:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutation_prob:
                toolbox.mutate(mutant)
                try:
                    del mutant.fitness.values
                except AttributeError:
                    pass
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

    sorted_idxs = sorted(range(len(fits)), key=lambda idx: fits[idx])
    sorted_pop = [pop[idx] for idx in sorted_idxs]

    while len(sorted_pop) > 0:
        try:
            return Haiku(sorted_pop.pop(-1).lines)
        except ValueError:
            pass
    return None


def create_haiku(kes, fx=create_haiku_with_ga):
    global haiku_judge
    if haiku_judge is None:
        haiku_judge = HaikuJudge(HaikuModel(load=True))
    return fx(kes)


if __name__ == "__main__":
    keys = set(random.choice(words) for i in range(20))
    print(create_haiku(['student', 'school', 'phone', 'pen', 'power']))
