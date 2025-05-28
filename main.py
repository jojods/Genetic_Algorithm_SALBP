from encoding import read_file, read_operations_file, read_file_tuple
from algorithm import engine 
from validation import printStationsDict, printResults
from config import *

ITERATIONS = 100

def main():

    pop, *_ = engine(DADOS_MARQUEZE,
           pop_size=10000, iterations=1000,
           perc_elitism=0.01, perc_mat=0.1, sel_type='roulette', cross_type='SP',
           mutation_rate=0.5, mut_type='heur')
    
    printResults(DADOS_MARQUEZE.times, 
                 pop, 
                 DADOS_MARQUEZE.automatic_operations, 
                 DADOS_MARQUEZE.number_of_operations)
    
    printStationsDict(DADOS_MARQUEZE.number_of_stations, 
                      pop)


if __name__ == '__main__':
    main()
