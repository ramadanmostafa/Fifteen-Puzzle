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
    if len(list1) < 1 :
        return []
    result = list()
    result.append(list1[0])
    for item in list1:
        if item != result[-1]:
            result.append(item)
    return result

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    index1 = 0
    index2 = 0
    result = list()
    while(index1 < len(list1) and index2 < len(list2)):
        if list1[index1] == list2[index2]:
            result.append(list1[index1])
            index1 += 1
            index2 += 1
        elif list1[index1] > list2[index2]:
            index2 += 1
        elif list2[index2] > list1[index1]:
            index1 += 1   
    return result

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    index1 = 0
    index2 = 0
    result = list()
    while(index1 < len(list1) or index2 < len(list2)):
        if index1 >= len(list1):
            result += list2[index2:]
            break
        if index2 >= len(list2):
            result += list1[index1:]
            break
        if list1[index1] == list2[index2]:
            result.append(list1[index1])
            result.append(list1[index1])
            index1 += 1
            index2 += 1
        elif list1[index1] > list2[index2]:
            result.append(list2[index2])
            index2 += 1
        elif list2[index2] > list1[index1]:
            result.append(list1[index1])
            index1 += 1  
    return result
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    length = len(list1)
    if list1 == [] or length == 1:
        return list1
    return merge( merge_sort(list1[:length/2]), merge_sort(list1[length/2:]))

# Function to generate all strings for the word wrangler game
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == "":
        return [""]
    if len(word) == 1:
        return ["",word]
    first = word[0]
    rest = word[1:]
    all_strings = gen_all_strings(rest)
    result = list()
    result.append(first)
    result += all_strings
    for item in all_strings:
        if item == "":
            continue        
        result.append(first+item)
        result.append(item+first)
        if len(item) == 1:
            continue
        for ch_idx in range(1,len(item)):
            result.append(item[:ch_idx]+first+item[ch_idx:])
    return result

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    file1 = urllib2.urlopen(codeskulptor.file2url(filename))
    result = list()
    for line in file1.readlines():
        result.append(line[:-1])
    return result

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
run()

    
    
