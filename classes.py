import copy
from math import exp
from random import randint, random
from numpy.random import permutation, choice
from config import *

class Individual:
    """
    Each individual is coded as a list of integers. The nth-element of the list corresponds to station asigned
    to the operation n.

    The fitness of a route is given by the sum of the time of the slowest station and the number of precedence
    violations multiplied by a constant k (equal to the slowest operation).

    SP -> Single point crossover
    DP -> Double point crossover
    UX -> Uniform crossover

    random -> Random mutation (gives a random value to a random element)
    heur -> Heuristic mutation
    swap -> Swap mutation (select 2 elemtents and swaps them)
    scramble -> scramble subset
    inverse -> Inverse subset

    """
    _fitness = 0
    code = list()
    operations = 0
    stations = 0
    gen = 0

    def __init__(self, operations, stations, code, cross_type='SP', mut_type='random'):
        self.operations = operations
        self.stations = stations
        self.code = code
        self.crossover = eval('self.crossover_' + cross_type)
        self.mutate = eval('self.mutate_' + mut_type)

    def __repr__(self):
        return str(self.code)

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, fitness):
        self._fitness = fitness

    def calc_violations(self, graph, is_last):
        """
        Calculates the number of precedence violations

        Args:
            is_last: if True, prints what is the violation
            graph (dict): precedence graph of the problem

        Returns:
            (int)
        """
        violations = 0
        for op in range(self.operations):
            for neighbor in graph[op]:
                if self.code[neighbor] < self.code[op]:
                    if is_last:
                        print(f"{op+1} (station {self.code[op]}) should come before {neighbor+1} (station {self.code[neighbor]})")
                    violations += 1
        return violations

    def calc_fitness(self, gen, graph, times, slowest_op=10, scalling_factor=0):
        """
        Calculates fitness of the code.

        Args:
            gen (int): current generation
            graph (dict): precedence graph of the problem
            k (float): time of slowest operations (it can be scaled)
            times (list(float)): list containing the times of each operation

        Returns:
            (float)
        """

        time_op = self.get_station_time(times) # time of station **including** automatic-operation time
        time_operator = self.get_operator_time(times) # time of operator **excluding** automatic-operation time

        # Scalling factor...
        # self.fitness = -exp(scalling_factor * (max(time_op) + k * calc_violations(indv)))
        # No scalling factor
        # self.fitness = max(time_op) + (k * self.calc_violations(graph)) if (scalling_factor is 0) else
        # exp(-scalling_factor * (max(time_op) + k * self.calc_violations(graph)))

        # self.fitness = (10000 * self.calc_violations(graph, False)) #(k * self.calc_violations(graph, False) + zmax(time_operator)
        self.fitness = max(time_operator) + (100000 * self.calc_violations(graph, False)) #(k * self.calc_violations(graph, False)
        if max(time_op) > max(time_operator):
            self.fitness = self.fitness + 1000000
        if self.fitness == 0:
            self.fitness = max(time_operator)

        self.gen = gen

        return self.fitness

    def mutate_random(self):
        op = FREE_OPERATIONS[randint(0, len(FREE_OPERATIONS)-1)]
        allowed_stations = DATA[op]
        self.code[op] = allowed_stations[randint(0,len(allowed_stations)-1)] #randint(0, self.stations - 1)
        self.fitness = 0

    def mutate_heur(self, graph):

        has_changed = False
        for op in FREE_OPERATIONS:
            for neighbor in graph[op]:
                if self.code[neighbor] < self.code[op]:
                    allowed_stations = DATA[op]
                    self.code[op] = allowed_stations[randint(0,len(allowed_stations)-1)] #randint(0, self.stations - 1)
                    has_changed = True

        if not has_changed:
            self.mutate_random()
        else:
            self.fitness = 0

    def mutate_swap(self):

        i = randint(0, self.operations - 1)
        j = randint(0, self.operations - 1)

        self.code[i], self.code[j] = self.code[j], self.code[i]
        self.fitness = 0

    def mutate_scramble(self):

        i = randint(0, self.operations)
        j = randint(0, self.operations)

        if i > j:
            i, j = j, i

        self.code[i:j] = copy.deepcopy(permutation(self.code[i:j]))
        self.fitness = 0

    def mutate_inversion(self):

        i = randint(0, self.operations)
        j = randint(0, self.operations)

        if i > j:
            i, j = j, i

        self.code[i:j].reverse()
        self.fitness = 0

    def crossover_SP(self, indv, graph = None):

        p = randint(0, self.operations)

        code_c1 = self.code[:p] + indv.code[p:]
        code_c2 = indv.code[:p] + self.code[p:]

        ch1 = Individual(self.operations, self.stations, code=copy.deepcopy(code_c1),
                         cross_type=self.crossover.__name__[-2:],
                         mut_type=self.mutate.__name__.split('_')[-1])

        ch2 = Individual(self.operations, self.stations, code=copy.deepcopy(code_c2),
                         cross_type=self.crossover.__name__[-2:],
                         mut_type=self.mutate.__name__.split('_')[-1])
        
        # if ch1.calc_violations(graph, False) > 0 or ch2.calc_violations(graph, False) > 0:
        #     return self, indv

        return ch1, ch2

    def crossover_DP(self, indv):

        i = randint(0, self.operations)
        j = randint(0, self.operations)
        if i > j:
            j, i = i, j

        code_c1 = copy.deepcopy(self.code[:i] + indv.code[i:j] + self.code[j:])
        code_c2 = copy.deepcopy(indv.code[:i] + self.code[i:j] + indv.code[j:])

        ch1 = Individual(self.operations, self.stations, code=code_c1,
                         cross_type=self.crossover.__name__[-2:],
                         mut_type=self.mutate.__name__.split('_')[-1])

        ch2 = Individual(self.operations, self.stations, code=code_c2,
                         cross_type=self.crossover.__name__[-2:],
                         mut_type=self.mutate.__name__.split('_')[-1])
        return ch1, ch2

    def crossover_UX(self, indv):

        code_c1 = [0] * self.operations
        code_c2 = [0] * self.operations

        for i in range(self.operations):
            if random() < 0.5:
                code_c1[i] = self.code[i]
                code_c2[i] = indv.code[i]
            else:
                code_c2[i] = self.code[i]
                code_c1[i] = indv.code[i]

        ch1 = Individual(self.operations, self.stations, code=copy.deepcopy(code_c1),
                         cross_type=self.crossover.__name__[-2:],
                         mut_type=self.mutate.__name__.split('_')[-1])

        ch2 = Individual(self.operations, self.stations, code=copy.deepcopy(code_c2),
                         cross_type=self.crossover.__name__[-2:],
                         mut_type=self.mutate.__name__.split('_')[-1])

        return ch1, ch2

    def get_station_time_for_operator(self, times):
        station_times = [0] * self.stations
        for op in range(self.operations):
            station = int(self.code[op]) % self.stations
            if op in FREE_OPERATIONS:
                station_times[station] += times[op]
        return station_times

    def get_station_time(self, times):
        station_times = [0] * self.stations
        for op in range(self.operations):
            station = int(self.code[op]) % self.stations
            station_times[station] += times[op]
        return station_times

    def get_operator_time(self, times):
        station_times = self.get_station_time_for_operator(times)
        operator_times = [0] * 6
        operator_times[0] = station_times[0]+station_times[1]+station_times[2]+station_times[3]
        operator_times[1] = station_times[4]+station_times[5]+station_times[6]
        operator_times[2] = station_times[7]
        operator_times[3] = station_times[8]
        operator_times[4] = station_times[9]
        operator_times[5] = station_times[10]

        return operator_times

# class StationCromossome:
#     """
#     Class to represent a cromossome of stations
#     """
#     def __init__(self, operations, stations, zoning):
#         self.operations = operations
#         self.stations = stations
#         self.code = self._generate_code(operations, stations, zoning)
#         self.fitness = 0

#     def _generate_code(operations, zoning):
#         """
#         Generate a random code for the cromossome
#         """
#         code = [0] * operations
#         for i in range(operations):
#             code[i] = choice(zoning[i], 1)[0]
#         return code

#     def calc_violations():
#         ...

#     def calc_fitness(self, times, gen):
#         time_op = self.get_station_time(times) # time of station **including** automatic-operation time
#         time_operator = self.get_operator_time(times) # time of operator **excluding** automatic-operation time

#         # Scalling factor...
#         # self.fitness = -exp(scalling_factor * (max(time_op) + k * calc_violations(indv)))
#         # No scalling factor
#         # self.fitness = max(time_op) + (k * self.calc_violations(graph)) if (scalling_factor is 0) else
#         # exp(-scalling_factor * (max(time_op) + k * self.calc_violations(graph)))

#         # self.fitness = (10000 * self.calc_violations(graph, False)) #(k * self.calc_violations(graph, False) + zmax(time_operator)
#         self.fitness = max(time_operator) + (1000 * self.calc_violations(zoning, False)) #(k * self.calc_violations(graph, False)
#         if self.fitness == 0:
#             self.fitness = max(time_operator)

#         self.gen = gen

#         return self.fitness
    
#     def mutate():
#         ...
    
#     def crossover():
#         ...

#     def get_station_time_for_operator(self, times):
#         station_times = [0] * self.stations
#         for op in range(self.operations):
#             station = int(self.code[op]) % self.stations
#             if op not in self.fixed_operations:
#                 station_times[station] += times[op]

#         return station_times

#     def get_station_time(self, times):
#         station_times = [0] * self.stations
#         for op in range(self.operations):
#             station = int(self.code[op]) % self.stations
#             station_times[station] += times[op]

#         return station_times

#     def get_operator_time(self, times):
#         station_times = self.get_station_time_for_operator(times)
#         operator_times = [0] * 6
#         operator_times[0] = station_times[0]+station_times[1]+station_times[2]+station_times[3]
#         operator_times[1] = station_times[4]+station_times[5]+station_times[6]
#         operator_times[2] = station_times[7]
#         operator_times[3] = station_times[8]
#         operator_times[4] = station_times[9]
#         operator_times[5] = station_times[10]
        
#         return operator_times    
