from typing import List, Dict
from classes import Individual
from config import DATA
from encoding import read_file

# def printAutomaticStationsTime(autoStat: List[List[int]], times: List[int]) -> None:
#     auto_act = [st[0]-1 for st in autoStat]
#     auto_stat_times = [times[act] for act in auto_act]
#     print(f"\nAUTOMATIC STATIONS TIME\n")
#     print(f"Total time of fixed stations: {sum(auto_stat_times)}")

def printAutomaticStationsTime(autoStat: Dict[int, List[int]], times: List[int], number_of_operations: int) -> None:
    auto_act = [act for act in range(number_of_operations) if act not in autoStat.keys()]
    auto_stat_times = [times[actv] for actv in auto_act]
    print(f"\nAUTOMATIC STATIONS TIME\n")
    print(f"Total time of fixed stations: {sum(auto_stat_times)}")


def printParameters(times: int, pop: Individual) -> None:
    print(f"\nPARAMETERS OF THE BEST SOLUTION\n")
    print(f"Cromossome : {[st for st in pop.code]}")
    print(f"Best solution reached after {pop.gen} generations.")
    print(f"Fitness of the best solution : {pop.fitness}")


def printCycleTime(times: int, pop: Individual) -> None:
    """
    Print the cycle time of the best solution.
    """
    print(f"\nCYCLE TIME ANALYSIS OF THE BEST SOLUTION\n")
    all_station_times = pop.get_station_time(times)
    all_operator_times = pop.get_operator_time(times)
    print(f"Cycle time of the best solution: {max(all_operator_times)/100}")
    print(f"Station times: {[i/100 for i in all_station_times]}")
    print(f"Total Station times: {sum(all_station_times)/100}")
    print(f"Operator times: {[i/100 for i in all_operator_times]}")
    print(f"Total Operator times: {sum(all_operator_times)/100}")


def printResults(times: int, pop: Individual, autoStat: Dict[int, List[int]] | None, num_op: int) -> None:
    """
    Print the results of the best solution.
    """
    printParameters(times, pop)
    printCycleTime(times, pop)
    if autoStat is None:
        return
    printAutomaticStationsTime(autoStat, times, num_op)


def printStationsDict(num_stations: int, pop: Individual) -> None:
    """
    Print the stations dictionary in a formatted way.
    """
    station_activity = {i:[] for i in range(num_stations)}

    for atv, st in enumerate(pop.code): 
        station_activity[st].append(atv)

    print("\nSTATIONS DICTIONARY\n")

    for key, value in station_activity.items():
        print(f"Estação {key}: {value}")

if __name__ == "__main__":
    slowest_op, num_op, graph, times = read_file('dados_marqueze.txt')
    printAutomaticStationsTime(DATA, times)
    pass