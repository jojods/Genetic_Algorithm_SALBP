from algorithm import *
import selection as sel

def run_main() -> None:
    k, num_op, graph, times = read_file('dados_marqueze.txt')
    num_stations = 11

    engine(k, num_op, graph, times, num_stations=num_stations,
        pop_size=200, iterations=200,
        perc_elitism=10 / 200, perc_mat=0.5, select=sel.roulette, cross_type='SP',
        mutation_rate=0.20, mut_type='heur')


if __name__ == '__main__':
    run_main()