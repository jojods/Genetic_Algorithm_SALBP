from random import randint
from genes import StationGene


def find_keys_by_value(d: dict, target_value: int | float):
    key = [key for key, value in d.items() if target_value in value]
    return key[0]

def find_value_in_values(d:dict, vl:int|float):
    return any(vl in lt for lt in d.values())

def gen_indv(cross_type, mut_type, num_stations, num_operations):

    code: list[int] = []

    fixed_stations: dict[[int]:[int]] = {1:[1,2],
                                         2:[6,8],   
                                         3:[9,10,11],
                                         4:[13,14,15],
                                         5:[19,21],
                                         6:[22,23,25],
                                         7:[26,27,28],
                                         11:[50,51,52,53,54,55,56,57,58,59]
                                        }
    for i in range(num_operations):
        if not find_value_in_values(fixed_stations, i):
            code.append(randint(0, num_stations - 1))
        else:
            code.append(find_keys_by_value(fixed_stations, i))

    return StationGene(num_operations, num_stations, code, cross_type=cross_type, mut_type=mut_type)


def create_population(pop_size, cross_type, mut_type, num_stations, num_operations):
    """
    Creates the initial population.

    Args:
        pop_size (int): the size of the population
        cross_type (string): crossing technique
        mut_type (string): mutation technique
        num_stations (int): number of stations
        num_operations (int): number of operations

    Returns:
        (list(Individual)): initial population
    """
    pop = [gen_indv(cross_type, mut_type, num_stations, num_operations) for i in range(pop_size)]

    return pop


def rank_population(k, graph, times, pop, gen):
    """
    Return the sorted population.

    Args:
        k (float): time of the slowest operation
        graph (dict): precedence graph of the problem
        times (list(float)): list containing the time of each operation
        pop (list(Individual)): Population
        gen (int): current generation

    Returns:
        (list(Individual)): Sorted population
    """

    return sorted(pop, key=lambda x:x.calc_fitness(gen, graph, times, k=k*10, scalling_factor=0) if x.fitness is 0 else x.fitness, reverse=False)