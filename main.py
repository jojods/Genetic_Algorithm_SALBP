from encoding import read_file, read_operations_file, read_file_tuple
from algorithm import engine 
from validation import printStationsDict, printResults
from config import DATA


def main():
    slowest_op, num_op, graph, times = read_file('dados_marqueze.txt')
    num_stations = 11
    fixed_operations = read_operations_file('fixed_operations.txt')

    pop, *_ = engine(slowest_op, num_op, graph, times, num_stations=num_stations,
           pop_size=5000, iterations=10000,
           perc_elitism=0.05, perc_mat=0.40, sel_type='roulette', cross_type='SP',
           mutation_rate=0.2, mut_type='heur',
           restricted_stations=fixed_operations)
    
    printResults(times, pop, DATA, num_op)
    
    printStationsDict(num_stations, pop)

if __name__ == '__main__':
    main()
