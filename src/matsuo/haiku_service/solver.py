
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
cache = dict()


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
    constraints = [5, 7, 5]
    line_lengths = [0, 0, 0]
    for idx in range(len(line_lengths)):
        for word in individual.lines[idx]:
            try:
                if len(word) > 0:
                    line_lengths[idx] += textstat.textstat.syllable_count(word)
                else:
                    return
            except Exception:
                return

    for idx in range(len(line_lengths)):
        if line_lengths[idx] < constraints[idx]:
            add_word(idx, individual)
        elif line_lengths[idx] > constraints[idx]:
            delete_word(idx, individual)
        else:
            random.choice((jumble_words, replace_word))(idx, individual)


def add_word(idx, individual):
    individual.lines[idx].insert(random.randint(0, len(individual.lines) - 1), random.choice(words))


def delete_word(idx, individual):
    try:
        individual.lines[idx].remove(random.randint(0, len(individual.lines) - 1))
    except Exception:
        pass


def jumble_words(idx, individual):
    random.shuffle(individual.lines[idx])


def replace_word(idx, individual):
    individual.lines[idx][random.randint(0, len(individual.lines[idx]) - 1)] = random.choice(words)


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

    for idx in range(len(line_lengths)):
        if line_lengths[idx] != constraints[idx]:
            return [-1]

    haiku_words = list()
    for line in individual.lines:
        haiku_words.extend(line)
    haiku_words = set(haiku_words)

    occurance = sum(map(lambda word: 1 if word in keywords else 0, haiku_words))

    annotations = list()
    for line in individual.lines:
        annotated = list()
        for word in line:
            if word in cache:
                annotated.append(cache[word])
            else:
                for annotation in haiku_judge.tag_line(' '.join(line)):
                    cache[annotation[0]] = annotation[1]
                    annotated.append(annotation[1])
        annotations.append(annotated)
    return [occurance * haiku_judge.judge_haiku(annotations, annotated=True)]


def _create_individual():
    return Individual([[random.choice(keywords) if random.randint(0, 2) == 0 else random.choice(words)],
                       [random.choice(keywords)],
                       [random.choice(keywords) if random.randint(0, 2) == 0 else random.choice(words)]])


def create_haiku_with_ga(kws, mutation_prob=0.75, crossover_prob=0.5, max_gen=100, pop_size=500):
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
        haiku_judge = HaikuJudge(HaikuModel(load=True), optimized=True)
    return fx(kes)


if __name__ == "__main__":
    keys = set(random.choice(words) for i in range(20))
    print(create_haiku(['student', 'school', 'phone', 'pen', 'power']))
