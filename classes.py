import copy
from math import exp
from random import randint, random
from numpy.random import permutation, choice
from config import *
from utils import assign_coupled_operations

data = DADOS_MARQUEZE

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
    operations = 0
    stations = 0
    gen = 0

    def __init__(self, operations, stations, code, cross_type='SP', mut_type='random'):
        self.operations = operations
        self.stations = stations
        self.code = list(code)
        self.crossover = getattr(self, f'crossover_{cross_type}')
        self.mutate = getattr(self, f'mutate_{mut_type}')

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
    
    def _generate_random_station(self, op):
        allowed_stations = data.zonning[op]
        return allowed_stations[randint(0, len(allowed_stations) - 1)]
    
    def _generate_assign_couples(self, op):
        """
        Generates a random station for the operation and assigns it to all coupled operations.
        """
        new_station = self._generate_random_station(op)
        self.code[op] = new_station  # Assign the new station to the operation
        assign_coupled_operations(self.code, op, new_station, data.couples)

    def mutate_random(self):
        op = data.free_operations[randint(0, len(data.free_operations)-1)]
        self._generate_assign_couples(op) #randint(0, self.stations - 1)
        self.fitness = 0

    def mutate_heur(self, graph):

        has_changed = False
        for op in data.free_operations:
            for neighbor in graph[op]:
                if self.code[neighbor] < self.code[op]:
                    self._generate_assign_couples(op) #randint(0, self.stations - 1)
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

    def _make_child(self, code):
        return Individual(
            self.operations, self.stations, code=copy.deepcopy(code),
            cross_type=self.crossover.__name__[-2:],
            mut_type=self.mutate.__name__.split('_')[-1]
        )

    def crossover_SP(self, indv, graph=None):
        p = randint(0, self.operations)
        return (
            self._make_child(self.code[:p] + indv.code[p:]),
            self._make_child(indv.code[:p] + self.code[p:])
        )

    def crossover_DP(self, indv):

        i = randint(0, self.operations)
        j = randint(0, self.operations)
        if i > j:
            j, i = i, j

        return(
            self._make_child(self.code[:i] + indv.code[i:j] + self.code[j:]),
            self._make_child(indv.code[:i] + self.code[i:j] + indv.code[j:])
        )

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

        return (
            self._make_child(code_c1),
            self._make_child(code_c2)
        )

    def get_station_time_for_operator(self, times):
        station_times = [0] * self.stations
        for op in range(self.operations):
            station = int(self.code[op]) % self.stations
            if op not in data.automatic_operations:  # Assuming these are fixed operations
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
        return [sum((station_times[i]) for i in GROUP) for GROUP in data.operators_group]
