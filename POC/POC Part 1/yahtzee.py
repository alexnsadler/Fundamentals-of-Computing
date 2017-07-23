"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor, math
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


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    count_list = ([])
    for idx in range(1,7):
        count_list.append(hand.count(idx)*idx)
    
    return max(count_list)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    # Turns the set from gen_all_sequences into a list to make it
    # iterable. Uses from 1 to num_die_sides as the range for outcomes,
    # and num_free_dice as the length.
    dice_seqs = list(gen_all_sequences(range(1, num_die_sides + 1), num_free_dice))

    sum_free_dice = 0.0
    for idx in dice_seqs:
        sum_free_dice += score(held_dice+idx)
    hand_exp_val = (sum_free_dice / len(dice_seqs))
    
    return hand_exp_val


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    answer_set = set([()])
    for dummy_idx in range(len(hand)):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in hand:
                new_sequence = list(partial_sequence)
                temp_set.add(tuple(new_sequence))
                new_sequence.append(item)
                new_sequence.sort()
                if hand.count(item) >= new_sequence.count(item):
                    temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    # Creates a list of expected values based off of a given hand using gen_all_holds
    score_list = []
    for idx in list(gen_all_holds(hand)):
        score_list.append(expected_value(idx, num_die_sides, len(hand) - len(idx)))
        
    index_pos = score_list.index(max(score_list))
    dice_to_hold = list(gen_all_holds(hand))[index_pos]
    return (max(score_list), dice_to_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
