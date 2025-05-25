from typing import Dict
from config import DADOS_MARQUEZE

def read_dict(src: Dict):
    number_of_operations = src.get("number_of_operations", 0)
    zoning = src.get("zoning", {})
    number_of_stations = src.get("number_of_stations", 0)
    number_of_workers = src.get("number_of_workers", 0)

    return number_of_operations, zoning, number_of_stations, number_of_workers

def read_file(file_name):
    """
    Read file to get times and graph

    <Number of operations>
    <Time in operation 1>
    …
    <Time in operation n>
    <vertex op_i,op_j >
    …
    <vertex op_k,op_g >

    Args:
        file_name (string): file name

    Returns:
        (float): Time of slowest operation
        (int): Number of operations
        (dict): Precedence graph of the problem
        (list(float)): times of each operation
    """

    times = []
    graph = dict()

    with open(file_name) as fd:
        operations = int(fd.readline()[:-1])
        for slowest_op in range(operations):
            times.append(int(fd.readline()))
            graph[slowest_op] = []
        while (True):
            line = fd.readline()
            if not line:
                break
            ij = line.split(',')
            graph[int(ij[0]) - 1].append(int(ij[1][:-1]) - 1)
    for i, slowest_op in graph.items():
        print(f"{i}: {slowest_op}")
    return max(times), len(times), graph, times


def read_file_tuple(file_name):
    """
    Read file to get times and graph

    <Number of operations>
    <Time in operation 1>
    …
    <Time in operation n>
    <vertex op_i,op_j >
    …
    <vertex op_k,op_g >

    Args:
        file_name (string): file name

    Returns:
        (float): Time of slowest operation
        (int): Number of operations
        (dict): Precedence graph of the problem
        (list(float)): times of each operation
    """

    times = []
    graph = {}

    with open(file_name, 'r') as fd:
        # Lê o número de operações
        operations = int(fd.readline().strip())
        
        # Inicializa o grafo com tuplas vazias para cada operação
        for k in range(operations):
            graph[k] = ()
            
        # Lê os tempos de cada operação
        for _ in range(operations):
            times.append(float(fd.readline().strip()))
        
        # Lê as arestas do grafo e armazena temporariamente
        temp_edges = {}
        for k in range(operations):
            # Começamos com a própria chave como primeiro elemento
            temp_edges[k] = [k]
            
        for line in fd:
            if line.strip():  # Verifica se a linha não está vazia
                i, j = line.strip().split(',')
                temp_edges[int(i) - 1].append(int(j) - 1)
        
        # Converte as listas temporárias para tuplas no grafo final
        for k in range(operations):
            graph[k] = tuple(temp_edges[k])
    
    # Retorna os valores solicitados
    return max(times), len(times), graph, times


def read_operations_file(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                values = stripped_line.split(',')
                row = [int(v)-1 for v in values]
                matrix.append(row)
    return matrix

if __name__ == "__main__":
    print(read_dict(DADOS_MARQUEZE))