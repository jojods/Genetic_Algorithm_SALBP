from typing import Any

from algorithm import engine, read_file, read_fixed_op_file

if __name__ == '__main__':
    k, num_op, graph, times = read_file('dados_marqueze.txt')
    num_stations = 11
    fixed_operations = read_fixed_op_file('fixed_operations.txt')

    engine(k, num_op, graph, times, num_stations=num_stations,
           pop_size=5000, iterations=10000,
           perc_elitism=5 / 100, perc_mat=0.40, sel_type='roulette', cross_type='SP',
           mutation_rate=0.6, mut_type='heur',
           fixed_operations=fixed_operations)
