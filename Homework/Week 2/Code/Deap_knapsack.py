from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import random
import numpy
import time
import testcasePrepocessing as TCP
import knapsack as ks

# Genetic Algorithm constants:
P_CROSSOVER = 0.9  # probability for crossover
P_MUTATION = 0.1   # probability for mutating an individual
MAX_GENERATIONS = 100
HALL_OF_FAME_SIZE = 1

# set the random seed:
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
TIME_LIMIT = 120

def readTestFromFile(filePath):
    values = []
    weights = [[]]
    capacities = []
    items = []

    with open(filePath, 'r') as reader:
        lines = reader.readlines()

        # Line 2 always contain capacity
        c = int(lines[2].rstrip())
        capacities.append(c)

        # Our weights and values start from line 4
        for line in lines[4:]:
            l = line.rstrip().split(" ")

            values.append(int(l[0]))
            weights[0].append(int(l[1]))
            items.append([int(l[1]), int(l[0])])

    return values, weights, capacities, items

def deapSolver(items, maxCapacity, testCasePath):

    knapsack = ks.Knapsack01Problem(items, maxCapacity)

    def knapsackValue(individual):
        return knapsack.getValue(individual),  # return a tuple

    toolbox = base.Toolbox()

    # create an operator that randomly returns 0 or 1:
    toolbox.register("zeroOrOne", random.randint, 0, 1)

    # define a single objective, maximizing fitness strategy:
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))

    # create the Individual class based on list:
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # create the individual operator to fill up an Individual instance:
    toolbox.register("individualCreator", tools.initRepeat,
                     creator.Individual, toolbox.zeroOrOne, len(knapsack))

    # create the population operator to generate a list of individuals:
    toolbox.register("populationCreator", tools.initRepeat,
                     list, toolbox.individualCreator)

    # fitness calculation
    toolbox.register("evaluate", knapsackValue)

    # genetic operators:mutFlipBit

    # Tournament selection with tournament size of 3:
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Single-point crossover:
    toolbox.register("mate", tools.cxTwoPoint)

    # Flip-bit mutation:
    # indpb: Independent probability for each attribute to be flipped
    toolbox.register("mutate", tools.mutFlipBit,
                     indpb=1.0/len(knapsack))

    # create initial population (generation 0):
    population = toolbox.populationCreator(n=len(knapsack))

    # prepare the statistics object:
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", numpy.max)
    stats.register("avg", numpy.mean)

    # define the hall-of-fame object:
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    # perform the Genetic Algorithm flow with hof feature added:
    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=False)

    # print best solution found:
    best = hof.items[0]
    total_weight, computed_value = knapsack.result(best)
    
    return [computed_value, total_weight]

def solve_deap():

    TestCases= TCP.Get_All_TestCases()
    file_test_path='.\\Dataset\\kplib-master\\'
    data=[]
    
    for name in TestCases:
        file_name=file_test_path+name
        print('Deap: ',file_name)
        start=time.time()
        _, _, capacities, items = readTestFromFile(file_name)
        optimal_answer= deapSolver( items, capacities[0], file_name)
        end=time.time()
        print('Done.')
        tmp=[]
        for e in name:
            if(e=='\\'):
                tmp.append('_')
            else:
                tmp.append(e)
        data.append(["".join(tmp),optimal_answer[0],optimal_answer[1],'TRUE' if(end-start < TIME_LIMIT) else 'FALSE'])
    return data
