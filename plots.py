import matplotlib.pyplot as plt
from algorithm import engine
import math    

def to_str(i):
    if i % 1000 == 0:
        return r'${ret}\times10^3$'.format(ret=str(int(i / 1000)))
    elif i % 100 == 0:
        return r'${ret}\times10^2$'.format(ret=str(int(i / 100)))
    return str(i)


def compare_crossover(k, num_operations, graph, times, num_stations=10):
    """
    Compares crossover type and plots them
    """

    bests = []
    f = lambda x: x < 3000

    plt.figure(figsize=(6.8, 10))
    plt.title("Crossover")
    plt.xlabel('Generation', fontsize='large')
    plt.ylabel('Fitness', fontsize='large')

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=200,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='blue', linestyle=':')
    plt.plot(best, label='Single Point', color='blue')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=200,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='DP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='red', linestyle=':')
    plt.plot(best, label='Double Point', color='red')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=200,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='UX',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='green', linestyle=':')
    plt.plot(best, label='Uniform', color='green')
    bests.append(best[-1])

    plt.yscale('log')
    ticks = sorted(bests + [1000, 3000])

    i = 0
    while i < len(ticks):
        if ticks[i - 1] < ticks[i] <= ticks[i - 1] + 5.5 * 10 ** int(math.log10(ticks[i - 1]) - 1):
            if not ticks[i - 1] in bests:
                del ticks[i - 1]
            else:
                del ticks[i]
        elif ticks[i] <= ticks[i - 1] <= ticks[i] + 5.5 * 10 ** int(math.log10(ticks[i]) - 1):
            if not ticks[i] in bests:
                del ticks[i]
            else:
                del ticks[i - 1]
        else:
            i += 1

    plt.yticks(ticks)
    plt.yticks(ticks, [to_str(i) for i in ticks])

    plt.legend(frameon=False, fontsize='large')
    plt.show()


def compare_selection(k, num_operations, graph, times, num_stations=10):
    """
    Compares selection type and plots them
    """

    bests = []
    f = lambda x: x < 3000

    plt.figure(figsize=(6.8, 10))
    plt.title("Selection")
    plt.xlabel('Generation', fontsize='large')
    plt.ylabel('Fitness', fontsize='large')

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=200,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='blue', linestyle=':')
    plt.plot(best, label='Roulette', color='blue')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=200,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='rank', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='red', linestyle=':')
    plt.plot(best, label='Rank', color='red')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=200,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='tournament', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='green', linestyle=':')
    plt.plot(best, label='Tournament', color='green')
    bests.append(best[-1])
    plt.yscale('log')
    ticks = sorted(bests + [1000, 3000])

    i = 0
    while i < len(ticks):
        if ticks[i - 1] < ticks[i] <= ticks[i - 1] + 5.5 * 10 ** int(math.log10(ticks[i - 1]) - 1):
            if not ticks[i - 1] in bests:
                del ticks[i - 1]
            else:
                del ticks[i]
        elif ticks[i] <= ticks[i - 1] <= ticks[i] + 5.5 * 10 ** int(math.log10(ticks[i]) - 1):
            if not ticks[i] in bests:
                del ticks[i]
            else:
                del ticks[i - 1]
        else:
            i += 1

    plt.yticks(ticks)
    plt.yticks(ticks, [to_str(i) for i in ticks])

    plt.legend(frameon=False, fontsize='large')
    plt.show()


def compare_mutation(k, num_operations, graph, times, num_stations=10):
    """
    Compares mutation type and plots them
    """

    bests = []

    f = lambda x: x < 3000
    plt.figure(figsize=(6.8, 10))
    plt.title("Mutations types")
    plt.xlabel('Generation', fontsize='large')
    plt.ylabel('Fitness', fontsize='large')

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=200,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='blue', linestyle=':')
    plt.plot(best, label='Heur', color='blue')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=200,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='random')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='red', linestyle=':')
    plt.plot(best, label='Random', color='red')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=200,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='swap')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='green', linestyle=':')
    plt.plot(best, label='Swap', color='green')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=200,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='inversion')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='orange', linestyle=':')
    plt.plot(best, label='Inversion', color='orange')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=200,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='scramble')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='purple', linestyle=':')
    plt.plot(best, label='Scramble', color='purple')
    bests.append(best[-1])
    plt.yscale('log')
    ticks = sorted(bests + [1000, 3000])

    i = 0
    while i < len(ticks):
        if ticks[i - 1] < ticks[i] <= ticks[i - 1] + 5.5 * 10 ** int(math.log10(ticks[i - 1]) - 1):
            if not ticks[i - 1] in bests:
                del ticks[i - 1]
            else:
                del ticks[i]
        elif ticks[i] <= ticks[i - 1] <= ticks[i] + 5.5 * 10 ** int(math.log10(ticks[i]) - 1):
            if not ticks[i] in bests:
                del ticks[i]
            else:
                del ticks[i - 1]
        else:
            i += 1

    plt.yticks(ticks)
    plt.yticks(ticks, [to_str(i) for i in ticks])
    plt.legend(frameon=False, fontsize='large')
    plt.show()


def compare_perc_elitism(k, num_operations, graph, times, num_stations=10):
    """
    Compares mutation type and plots them
    """

    bests = []

    f = lambda x: x < 3000
    plt.figure(figsize=(6.8, 10))
    plt.title("Perc elitism")
    plt.xlabel('Generation', fontsize='large')
    plt.ylabel('Fitness', fontsize='large')

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=2 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='blue', linestyle=':')
    plt.plot(best, label='1%', color='blue')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='red', linestyle=':')
    plt.plot(best, label='5%', color='red')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=20 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='green', linestyle=':')
    plt.plot(best, label='10%', color='green')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=30 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='orange', linestyle=':')
    plt.plot(best, label='15%', color='orange')
    bests.append(best[-1])

    plt.yscale('log')
    ticks = sorted(bests + [1000, 3000])

    i = 0
    while i < len(ticks):
        if ticks[i - 1] < ticks[i] <= ticks[i - 1] + 5.5 * 10 ** int(math.log10(ticks[i - 1]) - 1):
            if not ticks[i - 1] in bests:
                del ticks[i - 1]
            else:
                del ticks[i]
        elif ticks[i] <= ticks[i - 1] <= ticks[i] + 5.5 * 10 ** int(math.log10(ticks[i]) - 1):
            if not ticks[i] in bests:
                del ticks[i]
            else:
                del ticks[i - 1]
        else:
            i += 1

    plt.yticks(ticks)
    plt.yticks(ticks, [to_str(i) for i in ticks])
    plt.legend(frameon=False, fontsize='large')
    plt.show()


def compare_perc_mat(k, num_operations, graph, times, num_stations=10):
    """
    Compares mutation type and plots them
    """

    bests = []

    f = lambda x: x < 3000
    plt.figure(figsize=(6.8, 10))
    plt.title("Perc mat")
    plt.xlabel('Generation', fontsize='large')
    plt.ylabel('Fitness', fontsize='large')

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=10 / 200, perc_mat=0.2, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='blue', linestyle=':')
    plt.plot(best, label='20%', color='blue')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=10 / 200, perc_mat=0.3, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='red', linestyle=':')
    plt.plot(best, label='30%', color='red')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=10 / 200, perc_mat=0.4, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='green', linestyle=':')
    plt.plot(best, label='40%', color='green')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='orange', linestyle=':')
    plt.plot(best, label='50%', color='orange')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=10 / 200, perc_mat=0.6, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='yellow', linestyle=':')
    plt.plot(best, label='60%', color='yellow')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=10 / 200, perc_mat=0.7, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.20, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='black', linestyle=':')
    plt.plot(best, label='70%', color='black')
    bests.append(best[-1])

    plt.yscale('log')
    ticks = sorted(bests + [1000, 3000])

    i = 0
    while i < len(ticks):
        if ticks[i - 1] < ticks[i] <= ticks[i - 1] + 5.5 * 10 ** int(math.log10(ticks[i - 1]) - 1):
            if not ticks[i - 1] in bests:
                del ticks[i - 1]
            else:
                del ticks[i]
        elif ticks[i] <= ticks[i - 1] <= ticks[i] + 5.5 * 10 ** int(math.log10(ticks[i]) - 1):
            if not ticks[i] in bests:
                del ticks[i]
            else:
                del ticks[i - 1]
        else:
            i += 1

    plt.yticks(ticks)
    plt.yticks(ticks, [to_str(i) for i in ticks])
    plt.legend(frameon=False, fontsize='large')
    plt.show()


def compare_mut_rate(k, num_operations, graph, times, num_stations=10):
    """
    Compares mutation type and plots them
    """

    bests = []

    f = lambda x: x < 3000
    plt.figure(figsize=(6.8, 10))
    plt.title("Mutation Rate")
    plt.xlabel('Generation', fontsize='large')
    plt.ylabel('Fitness', fontsize='large')

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.1, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='blue', linestyle=':')
    plt.plot(best, label='10%', color='blue')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.2, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='red', linestyle=':')
    plt.plot(best, label='20%', color='red')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.3, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='green', linestyle=':')
    plt.plot(best, label='30%', color='green')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.4, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='orange', linestyle=':')
    plt.plot(best, label='40%', color='orange')
    bests.append(best[-1])

    _, best, mean = engine(k, num_operations, graph, times, num_stations=num_stations,
                           pop_size=200, iterations=400,
                           perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                           mutation_rate=0.5, mut_type='heur')

    best = list(filter(f, best))
    mean = list(filter(f, mean))
    plt.plot(mean, color='purple', linestyle=':')
    plt.plot(best, label='50%', color='purple')
    bests.append(best[-1])

    plt.yscale('log')
    ticks = sorted(bests + [1000, 3000])

    i = 0
    while i < len(ticks):
        if ticks[i - 1] < ticks[i] <= ticks[i - 1] + 5.5 * 10 ** int(math.log10(ticks[i - 1]) - 1):
            if not ticks[i - 1] in bests:
                del ticks[i - 1]
            else:
                del ticks[i]
        elif ticks[i] <= ticks[i - 1] <= ticks[i] + 5.5 * 10 ** int(math.log10(ticks[i]) - 1):
            if not ticks[i] in bests:
                del ticks[i]
            else:
                del ticks[i - 1]
        else:
            i += 1

    plt.yticks(ticks)
    plt.yticks(ticks, [to_str(i) for i in ticks])
    plt.legend(frameon=False, fontsize='large')
    plt.show()


def get_best_num_stations_effort(k, num_operations, graph, times, i=1, j=10):
    """
    Tries to find the optimal number of stations (in a given range). It also plots the effort. We define effort as the product
    of time and fitness.

    Args:
        k (float) : time of the slowest operation
        num_operations (int): Number of operations
        graph (dict): Precedence graph of the problem
        times (list(float)): List containing the times of the stations
        i (int): lower bound of the search range
        j (int): upper bound of the search range

    Returns:
        (int): Number of stations in which the fitness is minimize
        (float): Time of the best solution
        ([int]): Codification of the best solution
    """

    my_best = math.inf
    best_indv = None
    num_stations = 0
    bests = []

    for z in range(i,j):

        print('Number of stations: %d' % z)
        rel_best, _, _ = engine(k, num_operations, graph, times, num_stations=z,
                          pop_size=200, iterations=500,
                          perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
                          mutation_rate=0.2, mut_type='heur')
        bests.append(rel_best.fitness)

        if rel_best.fitness < my_best:
            my_best = rel_best.fitness
            num_stations = z
            best_indv = rel_best
        print()

    plt.figure(figsize=(6.8, 10))
    plt.xlabel('Number of stations', fontsize='large')
    plt.ylabel('Quality', fontsize='large')

    esfuerzo = [0] * (j-i)

    for k in range(i, j):
        esfuerzo[k - i] = bests[k - i] * k

    plt.plot([sum(times)] * (j-i + 1), label='effort upper bound', color='black')
    plt.plot(*zip(*[(i+1, esfuerzo[i]) for i in range(len(esfuerzo))]), label='effort', marker='o', color='red')
    plt.plot(*zip(*[(i+1, bests[i]) for i in range(len(bests))]), label='time', marker='o', color='blue')

    plt.xticks([i for i in range(i,j)])

    plt.legend(frameon=False, fontsize='large')

    plt.show()

    print('\n********************************************************************************\n')
    print('\n********************************************************************************\n')
    print('Number of stations: %d, time = %d' % (num_stations, my_best))
    print('Individue: ', best_indv)
    return num_stations, best_indv, my_best
