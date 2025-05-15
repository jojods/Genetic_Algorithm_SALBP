from random import randint
from functools import reduce
import numpy as np
from genes import Individual
from typing import Callable, List

# Selection function type
SelectionFunction = Callable[[List[Individual], float], List[Individual]]


def unit_random_tournament(population: list[Individual]) -> Individual:

    i = randint(0, len(population) - 1)
    j = randint(0, len(population) - 1)

    return population[i] if (population[i].fitness > population[j].fitness)else population[j]


def random_tournament(population: list[Individual], num: float=2) -> list[Individual]:

    return [unit_random_tournament(population) for i in range(num)]


def rank(population: list[Individual], num:float=2):

    total = len(population)*(1 + len(population))/2
    rank = [i/total for i in range(1, len(population) + 1)]
    return np.random.choice(a=population, size=num, p=rank)


def roulette(population: list[Individual], num:float=2):
    total = reduce(lambda x, y: x + y.fitness, population, 0) #Calcular o fitness total da população
    roulette = [indiv.fitness / total for indiv in population] # Normaliza o fitness de cada indivíduo com base no fitness total

    return np.random.choice(a=population, size=num, p=roulette) # Escolhe aleatoriamente os indivíduos com base no fitness normalizado