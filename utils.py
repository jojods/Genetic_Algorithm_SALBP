from random import randint
from typing import List, Dict

def assign_coupled_operations(code, op, new_station, couples: Dict[int, List[int]]):
    if op not in couples.keys():
        return
    
    for couple in couples[op]:
        code[couple] = new_station  # Assign the same station to the coupled operations
