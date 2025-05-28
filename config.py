from dataclasses import dataclass
from typing import List, Dict

def get_slowest_operation(times: List[int]) -> int:
    if not times:
        return 0
    return max(times)


@dataclass
class Zonning_Data:
    number_of_operations: int
    number_of_stations: int
    number_of_workers: int
    operators_group: List[List[int]] = None
    graph: Dict[int, List[int]] = None 
    times: List[int] = None
    free_operations: List[int] = None
    zonning: Dict[int, List[int]] = None
    automatic_operations: List[int] = None
    slowest_operation: int = None
    couples: Dict[int,List[int]] = None

    
ZONNING_1 = {
    0: [0],
    1: [0],
    2: [0],
    3: [0,1],
    4: [0,1],
    5: [1],
    6: [1],
    7: [1],
    8: [2],
    9: [2],
    10: [2],
    11: [2],
    12: [3],
    13: [3],
    14: [3],
    15: [3],
    16: [2,3],
    17: [3,4],
    18: [4],
    19: [4],
    20: [4],
    21: [5],
    22: [5],
    23: [5],
    24: [5],
    25: [6],
    26: [6],
    27: [6],
    28: [6],
    29: [7,8,9],
    30: [7,8,9],
    31: [7,8,9],
    32: [7,8,9],
    33: [7,8,9],
    34: [7,8,9],
    35: [7,8,9],
    36: [7,8,9],
    37: [7,8,9],
    38: [7,8,9],
    39: [7,8,9],
    40: [5,6,7,8,9],
    41: [5,6,7,8,9],
    42: [7,8,9],
    43: [7,8,9],
    44: [7,8,9],
    45: [7,8,9],
    46: [7,8,9],
    47: [7,8,9],
    48: [7,8,9],
    49: [10],
    50: [10],
    51: [10],
    52: [10],
    53: [10],
    54: [10],
    55: [10],
    56: [10],
    57: [10],
    58: [10]
}

AUTOMATIC_OPERATIONS_1 = [2, 6, 11, 15, 19, 23, 28]

FREE_OPERATIONS = [3, 4, 16, 17, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]

OPERATORS_GROUP_1 = [
    [0,1,2,3],
    [4,5,6],
    [7],
    [8],
    [9],
    [10]
]

TEMPOS_MIX_80_20 = [
    3720, 972, 23121, 1251, 4935, 2541, 4065, 1938, 789, 2697,
    879, 16329, 933, 2001, 1044, 3957, 2100, 1701, 1608, 9819,
    2205, 1443, 834, 9045, 2424, 2037, 2058, 927, 18243, 2376,
    1410, 1164, 1008, 14871, 10482, 1959, 1917, 1758, 8040, 16347,
    4878, 2511, 1416, 2313, 1899, 3990, 9411, 5433, 2175, 1440,
    2625, 696, 1932, 630, 2340, 618, 2130, 2223, 5964
]

GRAPH_1 = {
    0: [1],
    1: [2],
    2: [3],
    3: [4],
    4: [5],
    5: [6],
    6: [7],
    7: [8, 9],
    8: [10],
    9: [10],
    10: [11],
    11: [16],
    12: [14],
    13: [14],
    14: [15],
    15: [17],
    16: [18],
    17: [18],
    18: [19],
    19: [20],
    20: [21],
    21: [22],
    22: [23],
    23: [24],
    24: [25],
    25: [26],
    26: [27],
    27: [28],
    28: [29, 42],
    29: [30],
    30: [31, 33, 34, 37, 38, 39, 45, 46],
    31: [32],
    32: [47],
    33: [47],
    34: [48],
    35: [],
    36: [],
    37: [47],
    38: [48],
    39: [48],
    40: [41],
    41: [42],
    42: [43],
    43: [44],
    44: [48, 48],
    45: [48],
    46: [47],
    47: [48],
    48: [49],
    49: [50, 52, 54, 56],
    50: [51],
    51: [57],
    52: [53],
    53: [57],
    54: [55],
    55: [57],
    56: [55],
    57: [58],
    58: []
}

COUPLED_ACTIVITIES = [
    [40,41],
    [43,44],
    [31,32],
    [29,30]
]

COUPLED_ACTIVITIES_DICT = {
    40: [41],
    41: [40],
    43: [44],
    44: [43],
    31: [32],
    32: [31]
}

DADOS_MARQUEZE = Zonning_Data(
    number_of_operations=59,
    number_of_stations=11,
    number_of_workers=6,
    operators_group=OPERATORS_GROUP_1,
    graph=GRAPH_1,
    times=TEMPOS_MIX_80_20,
    free_operations=FREE_OPERATIONS,
    zonning=ZONNING_1,
    automatic_operations=AUTOMATIC_OPERATIONS_1,
    slowest_operation=get_slowest_operation(TEMPOS_MIX_80_20),
    couples=COUPLED_ACTIVITIES_DICT
)
