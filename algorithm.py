import copy
from random import random
from classes import Individual
from functools import reduce
from random import randint
from selection import *


def engine(slowest_time, num_operations, graph, times, num_stations=10,
           pop_size=100, iterations=100,
           perc_elitism=0.1, perc_mat=0.1, sel_type='roulette', cross_type='SP',
           mutation_rate=0.05, mut_type='random',
           restricted_stations=None,
           ):
    """
    Performs the genetic algorithm

    Args:
        fixed_operations: matrix of fixed operations
        slowest_op (float): Time of the slowest station
        num_operations (int): Number of operations
        graph (dict): Precedence graph of the problem
        times (list(float)): List containing the times of the stations
        num_stations (int): Number of stations
        pop_size (int): Number of individuals in each population
        iterations (int): Number of generations
        perc_elitism (float): Percentage of the best individuals of the current generation that will carry over the next
                              Default to 0.1
        perc_mat (float): Percentage of the best individuals of the current generation that will have a chance to be
                          selected as a parent. Default to 0.1
        sel_type (String): Selection method that will be used.
                           OPTIONS: - roulette (default)
                                    - tournament
                                    - rank
        cross_type (String): Crossover operator that will be used
                             OPTIONS : - SP -> Single point crossover (default)
                                       - DP -> Double point crossover
                                       - UX -> Uniform crossover
        mutation_rate (float): Mutation rate. Default to 0.05
        mut_type (String): Mutation operator
                           OPTIONS: - random -> Random mutation (gives a random value to a random element) (default)
                                    - heur -> Heuristic mutation
                                    - swap -> Swap mutation (select 2 elements and swaps them)
                                    - scramble -> scramble subset
                                    - inverse -> Inverse subset

    Returns:
        (Individual): Best individual-ç
        (list(float)): Fitness of the bests solutions for every generation. Useful for plotting
        (list(float)): Mean fitness of the population for every generation. Useful for plotting
    """

    if restricted_stations is None:
        fixed_operations = []
    population = rank_population(slowest_time, graph, times,
                                 create_population(pop_size, cross_type, mut_type, num_stations, num_operations, restricted_stations),
                                 0)

    best = []
    mean = []
    invalid_sol = True

    select = eval('select_by_' + sel_type)

    i = 0

    while (i < iterations):

        best.append(population[0].fitness)
        mean.append(reduce(lambda x, y: x + y.fitness, population, 0)/pop_size)
        # Break after:
        if population[0].gen < i - 25:
            break

        # Elitism
        new_generation = population[:int(perc_elitism*pop_size)]

        # Selection
        the_chosen_ones = select(population[:int(pop_size * perc_mat)], num=(pop_size - int(perc_elitism*pop_size)))

        mut = 2
        # Crossover
        for j in range(0, len(the_chosen_ones), 2):

            if j == len(the_chosen_ones) - 1:
                new_generation.append(Individual(num_operations, num_stations, copy.deepcopy(the_chosen_ones[j].code),
                                                cross_type=cross_type, mut_type=mut_type))
                mut = 1
            else:
                new_generation.extend(the_chosen_ones[j].crossover(the_chosen_ones[j+1], graph))

            # Mutation
            for indv in new_generation[-mut:]:
                if random() < mutation_rate:
                    if mut_type == 'heur':
                        indv.mutate(graph)
                    else:
                        indv.mutate()

        # Evaluation
        population = rank_population(slowest_time, graph, times, new_generation, i)
        all_station_times = population[0].get_station_time(times)
        all_operator_times = population[0].get_operator_time(times)
        print(f"Gen {i}; Best Fitness: {population[0].fitness/100}; Cycle time: {max(all_operator_times)/100}; Max station time: {max(all_station_times)/100}")
        #print(f"Cromossome: {population[0].code}")

        if population[0].calc_violations(graph, False) > 0:
            print(f"Cromossome: {population[0].code}")
        # else:
        #     invalid_sol = False
            
        i = i + 1

    # if (population[0].calc_violations(graph, True)) > 0:
    print("SOLUCION NO VALIDA: ", population[0].calc_violations(graph, True))
    # else:
    #     # invalid_sol = False
    #     print("No violations")

    return population[0], best, mean

def engine_zoning(slowest_time, num_operations, times, num_stations=10,
           pop_size=100, iterations=100,
           perc_elitism=0.1, perc_mat=0.1, sel_type='roulette', cross_type='SP',
           mutation_rate=0.05, mut_type='random'
           ):
    """
    Performs the genetic algorithm
    """

    population = rank_population(slowest_time, times,
                                 create_population(pop_size, cross_type, mut_type, num_stations, num_operations),
                                 0)

    best = []
    mean = []
    invalid_sol = True

    select = eval('select_by_' + sel_type)

    i = 0

    while (i < iterations): #and invalid_sol:

        best.append(population[0].fitness)
        mean.append(reduce(lambda x, y: x + y.fitness, population, 0)/pop_size)
        # Break after:
        if population[0].gen < i - 50:
            break

        # Elitism
        new_generation = population[:int(perc_elitism*pop_size)]

        # Selection
        the_chosen_ones = select(population[:int(pop_size * perc_mat)], num=(pop_size - int(perc_elitism*pop_size)))

        mut = 2
        # Crossover
        for j in range(0, len(the_chosen_ones), 2):

            if j == len(the_chosen_ones) - 1:
                new_generation.append(Individual(num_operations, num_stations, copy.deepcopy(the_chosen_ones[j].code),
                                                cross_type=cross_type, mut_type=mut_type))
                mut = 1
            else:
                new_generation.extend(the_chosen_ones[j].crossover(the_chosen_ones[j+1], graph))

            # Mutation
            for indv in new_generation[-mut:]:
                if random() < mutation_rate:
                    if mut_type == 'heur':
                        indv.mutate(graph)
                    else:
                        indv.mutate()

        # Evaluation
        population = rank_population(slowest_time, graph, times, new_generation, i)
        all_station_times = population[0].get_station_time(times)
        all_operator_times = population[0].get_operator_time(times)
        print(f"Gen {i}; Best Fitness: {population[0].fitness}; Cycle time: {max(all_operator_times)}; Max station time: {max(all_station_times)}")
        
        if population[0].calc_violations(graph, False) > 0:
            pass
        else:
            ...
            #invalid_sol = False
            
        i = i + 1

    # if (population[0].calc_violations(graph, True)) > 0:
    print("SOLUCION NO VALIDA: ", population[0].calc_violations(graph, True))
    # else:
    #     # invalid_sol = False
    #     print("No violations")

    return population[0], best, mean


def to_str(i):
    if i % 1000 == 0:
        return r'${ret}\times10^3$'.format(ret=str(int(i / 1000)))
    elif i % 100 == 0:
        return r'${ret}\times10^2$'.format(ret=str(int(i / 100)))
    return str(i)