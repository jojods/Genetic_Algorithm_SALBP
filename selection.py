from random import random, randint, choice
from classes import Individual
from functools import reduce
import numpy as np
from config import *

def gen_indv(cross_type, mut_type, num_stations, num_operations, possible_stations):
    # print(f"Lenth of fixed: {len(fixed_operations)}")
    code = [randint(0, num_stations - 1) for i in range(num_operations)]
    for i in range(len(possible_stations)):
        code[possible_stations[i][0]] = possible_stations[i][1]

    #print(f"Code: {code}")
    return Individual(num_operations, num_stations, code,cross_type, mut_type)


def gen_indv_possible(cross_type, mut_type, num_stations, num_operations, possible_stations):
    # print(f"Lenth of fixed: {len(fixed_operations)}")
    code = [0]*num_operations

    for act, sts in POSSIBLE_STATIONS_ACT.items():
        code[act] = sts[randint(0, len(sts) - 1)]

    #print(f"Code: {code}")
    return Individual(num_operations, num_stations, code,cross_type, mut_type)

# def gen_indv_zoning(num_stations, num_operations, zoning):
#     # print(f"Lenth of fixed: {len(fixed_operations)}")

#     #print(f"Code: {code}")
#     return Individual(num_operations, num_stations, zoning)


def create_population(pop_size, cross_type, mut_type, num_stations, num_operations, restricted_stations):
    """
    Creates the initial population.

    Args:
        fixed_operations: list of fixed operations
        pop_size (int): the size of the population
        cross_type (string): crossing technique
        mut_type (string): mutation technique
        num_stations (int): number of stations
        num_operations (int): number of operations

    Returns:
        (list(Individual)): initial population
    """
    pop = [gen_indv_possible(cross_type, mut_type, num_stations, num_operations, restricted_stations) for i in range(pop_size)]

    return pop

# def create_population_zoning(pop_size, num_stations, num_operations, zoning):
#     """
#     Creates the initial population.
#     """
#     pop = [gen_indv_zoning(num_stations, num_operations, zoning) for i in range(pop_size)]

#     return pop


def rank_population(slowest_op, graph, times, pop, gen):
    """
    Return the sorted population.

    Args:
        slowest_op (float): time of the slowest operation
        graph (dict): precedence graph of the problem
        times (list(float)): list containing the time of each operation
        pop (list(Individual)): Population
        gen (int): current generation

    Returns:
        (list(Individual)): Sorted population
    """

    return sorted(pop, key=lambda x:x.calc_fitness(gen, graph, 
                                                   times, slowest_op=slowest_op*10,
                                                   scalling_factor=0)
                                                   if x.fitness == 0 else x.fitness,
                                                   reverse=False)


# def rank_population_zoning(slowest_op, graph, times, pop, gen):
#     """
#     Return the sorted population.
#     """

#     return sorted(pop, key=lambda x:x.calc_fitness(gen, graph, 
#                                                    times, slowest_op=slowest_op*10,
#                                                    scalling_factor=0)
#                                                    if x.fitness == 0 else x.fitness,
#                                                    reverse=False)


def select_by_tournament_(population):

    i = randint(0, len(population) - 1)
    j = randint(0, len(population) - 1)

    return population[i] if (population[i].fitness > population[j].fitness)else population[j]


def select_by_tournament(population, num=2):

    return [select_by_tournament_(population) for i in range(num)]


def select_by_rank(population, num=2):

    total = len(population)*(1 + len(population))/2
    rank = [i/total for i in range(1, len(population) + 1)]
    return np.random.choice(a=population, size=num, p=rank)


def select_by_roulette(population, num=2):
    total = reduce(lambda x, y: x + y.fitness, population, 0)
    roulette = [indiv.fitness / total for indiv in population]

    return np.random.choice(a=population, size=num, p=roulette)
