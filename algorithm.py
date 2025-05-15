import copy
from random import random
from genes import Individual
from functools import reduce
from selection import SelectionFunction
import population as pop


def read_file(file_name):
    """
    Read file to get times and graph

    <Number of operations>
    <Time in operation 1>
    …
    <Time in operation n>
    <vertex op_i,op_j >
    …
    <vertex op_k,op_g >

    Args:
        file_name (string): file name

    Returns:
        (float): Time of slowest operation
        (int): Number of operations
        (dict): Precedence graph of the problem
        (list(float)): times of each operation
    """
    with open(file_name) as fd:
        lines = fd.readlines()
        
        # Get number of operations from first line
        operations = int(lines[0].strip())
        
        # Get operation times using list comprehension
        times = [int(lines[i].strip()) for i in range(1, operations + 1)]
        
        # Initialize graph
        graph = {i: [] for i in range(operations)}
        
        # Process precedence relationships
        for line in lines[operations + 1:]:
            if line.strip():
                i, j = map(lambda x: int(x) - 1, line.strip().split(','))
                graph[i].append(j)

    return max(times), operations, graph, times


def engine(k, num_operations, graph, times, num_stations=10,
           pop_size=100, iterations=100,
           perc_elitism=0.1, perc_mat=0.1, select=SelectionFunction, cross_type='SP',
           mutation_rate=0.05, mut_type='random'
           ):
    """
    Performs the genetic algorithm

    Args:
        k (float): Time of the slowest station
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
                                    - swap -> Swap mutation (select 2 elemtents and swaps them)
                                    - scramble -> scramble subset
                                    - inverse -> Inverse subset

    Returns:
        (Individual): Best individual
        (list(float)): Fitness of the bests solutions for every generation. Useful for plotting
        (list(float)): Mean fitness of the population for every generation. Useful for plotting
    """

    population = pop.rank_population(k, graph, times,
                                 pop.create_population(pop_size, cross_type, mut_type, num_stations, num_operations),
                                 0)

    best = []
    mean = []

    for i in range(iterations):

        best.append(population[0].fitness)
        mean.append(reduce(lambda x, y: x + y.fitness, population, 0)/pop_size)
        if population[0].gen < i - 50:
            break

        # Elitism
        new_generation = population[:int(perc_elitism*pop_size)]

        # Selection
        the_chosen_ones = select(population[:int(pop_size * perc_mat)], num=(pop_size - int(perc_elitism*pop_size))) #Verificar algoritmo para seleção

        mut = 2
        # Crossover
        for j in range(0, len(the_chosen_ones), 2):

            if j == len(the_chosen_ones) - 1:
                new_generation.append(the_chosen_ones[j])
                mut = 1
            else:
                new_generation.extend(the_chosen_ones[j].crossover(the_chosen_ones[j+1]))

            # Mutation
            for indv in new_generation[-mut:]:
                if random() < mutation_rate: #Verificar se a função random() é a melhor opção
                    if mut_type == 'heur':
                        indv.mutate(graph)
                    else:
                        indv.mutate()

        # Evaluation
        population = pop.rank_population(k, graph, times, new_generation, i)

    if (population[0].calc_number_violations(graph)) > 0:
        print("SOLUCION NO VALIDA: ", population[0].calc_number_violations(graph))
        population[0].print_violations(graph)

    print(f"Parameters of the best solution : {[i+1 for i in population[0].code]}")
    print(f"Best solution reached after {population[0].gen} generations.")
    print(f"Fitness of the best solution : {population[0].fitness}")

    return population[0], best, mean