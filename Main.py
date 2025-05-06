from algorithm import engine, read_file

if __name__ == '__main__':
    k, num_op, graph, times = read_file('dados_marqueze.txt')
    num_stations = 6

    engine(k, num_op, graph, times, num_stations=num_stations,
           pop_size=2000, iterations=100,
           perc_elitism=10 / 100, perc_mat=0.20, sel_type='roulette', cross_type='SP',
           mutation_rate=0.25, mut_type='heur')
