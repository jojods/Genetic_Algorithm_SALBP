from random import random, randint, choice
from classes import Individual
from functools import reduce
from typing import List, Dict
import numpy as np
from config import Zonning_Data
from utils import assign_coupled_operations


def gen_indv_possible(cross_type: str, 
                      mut_type: str, 
                      num_stations: int, 
                      num_operations: int, 
                      possible_stations: Dict[int, List[int]],
                      couples: Dict[int, List[int]] = None):
    # print(f"Lenth of fixed: {len(fixed_operations)}")
    code = [0]*num_operations

    for act, sts in possible_stations.items():
        new_station = sts[randint(0, len(sts) - 1)]
        code[act] = new_station
    
    assign_coupled_operations(code, act, new_station, couples)

    #print(f"Code: {code}")
    return Individual(num_operations, num_stations, code, cross_type, mut_type)


def create_population(pop_size: int, 
                      cross_type: str, 
                      mut_type: str, 
                      num_stations: str, 
                      num_operations: int, 
                      possible_stations: Dict[int, List[int]],
                      couples: Dict[int, List[int]] = None):
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
    pop = [gen_indv_possible(cross_type, mut_type, num_stations, num_operations, possible_stations, couples) for i in range(pop_size)]

    return pop


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
