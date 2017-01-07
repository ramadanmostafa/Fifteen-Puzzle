"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def gen_all_sequences_ind(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in range(len(outcomes)):
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def find_repeat(tpl):
    """
    return true if an input tuple has a repeated value
    otherwise return false
    """
    for idx in range(len(tpl)):
        for idy in range(idx+1,len(tpl)):
            if tpl[idx] == tpl[idy]:
                return True
    return False

def index_to_values(hand,indexes):
    """
    take a set of tuples (indexes) containing the indexes and return a set to the 
    same length but with the values stored in the hand tuple
    """
    result = set([])
    tmp=[]
    for tpitem in indexes:
        for element in tpitem:
            tmp.append(hand[element])
        result.add(tuple(tmp))
        tmp=[]
    return result

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand 
    according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    scores = [0] * (max(hand) +1)
    for item in hand:
        scores[item] += item
    #print scores
    return max_val(scores)

def max_val(sequence):
    """
    return a max value in a dictionary
    """
    maximum = -1*float("inf")
    for item in sequence:
        if item >= maximum:
            maximum = item
    return maximum

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    dice_values = []
    for idx in range(num_die_sides):
        dice_values.append(idx+1)
    all_possible_hands = gen_all_sequences(dice_values,num_free_dice)
    accumulation = 0.0
    for sub_hand in all_possible_hands:
        accumulation += score(held_dice + sub_hand)
    return accumulation / len(all_possible_hands)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    result = set([])
    for idx in range(len(hand)+1):
        tmp = list(gen_all_sequences_ind(hand,idx))
        print tmp
        for item in tmp:
            if len(item) > 1:
                item = tuple(sorted(item))
            if not find_repeat(item):
                result.add(item)
    return index_to_values(hand,result)


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    max_expected_value = 0.0
    max_expected_value_tpl = ()
    for hold in all_holds:
        tmp_expected = expected_value(hold, num_die_sides, len(hand)-len(hold))
        if tmp_expected > max_expected_value:
            max_expected_value = tmp_expected
            max_expected_value_tpl = hold
    return (max_expected_value, max_expected_value_tpl)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


import poc_holds_testsuite
poc_holds_testsuite.run_suite(gen_all_holds)
