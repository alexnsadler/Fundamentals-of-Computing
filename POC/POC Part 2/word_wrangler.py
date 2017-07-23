"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists
def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    no_dup_list = []
    for idx in range(len(list1)):
        if list1[idx] not in no_dup_list:
            no_dup_list.append(list1[idx])
            
    return no_dup_list


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    
    int_list = []
    for idx in list1:
        if idx in list2:
            int_list.append(idx)
            
    return int_list


# Functions to perform merge sort
def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    
    add_list = list1 + list2
    merge_list = []
    while add_list != []:
        merge_list.append(min(add_list))
        add_list.remove(min(add_list))
        
    return merge_list


def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if list1 == []:
        return list1
    else:
        pivot = list1[0]
        lesser = [num for num in list1 if num < pivot]
        pivots = [num for num in list1 if num == pivot]
        greater = [num for num in list1 if num > pivot]
        return merge_sort(lesser) + pivots + merge_sort(greater)


# Function to generate all strings for the word wrangler game
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return ['']
    else:
        first = word[0]
        rest = word[1:]
        
        rest_strings = gen_all_strings(rest)
        
        new_list = []
        for string in list(rest_strings):
            for idx in range(len(string)+1):
                new_item = list(string)
                new_item.insert(idx, first)
                new_list.append(''.join(new_item))

        return rest_strings + new_list
    

# Function to load words from a file
def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []


def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()
