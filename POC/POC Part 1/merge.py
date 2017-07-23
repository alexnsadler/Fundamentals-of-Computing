"""Merge function for 2048 game."""


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    
    # this code shifts all non-zero values to the beginning,
    # then combines pairs and repeats step one
    
    result_list = [0]*len(line)
    result_list_1 = [0]*len(line)
    
    for idx in line:
        if idx != 0:
            result_list[result_list.index(0)] = idx
    
    for idx in range(len(line) - 1):
        if result_list[idx] == result_list[idx+1]:
            result_list[idx] = result_list[idx] * 2
            result_list[idx+1] = 0
    
    for idx in result_list:
        if idx != 0:
            result_list_1[result_list_1.index(0)] = idx
        
    return result_list_1
