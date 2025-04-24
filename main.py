from algorithm import *

if __name__ == '__main__':
    k, num_op, graph, times = read_file('SALBP_GIT_Refactored/databases/dados_marqueze.txt')
    num_stations = 11

    engine(k, num_op, graph, times, num_stations=num_stations,
        pop_size=200, iterations=200,
        perc_elitism=10 / 200, perc_mat=0.5, sel_type='roulette', cross_type='SP',
        mutation_rate=0.20, mut_type='heur')