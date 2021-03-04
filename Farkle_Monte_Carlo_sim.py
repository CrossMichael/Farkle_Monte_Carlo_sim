# Farkle_Monte_Carlo_sim.py
# Presentation #2
#
# Purpose: Simulate x hands of Farkle and determine an average amount of points 
# earned for each hand played. Used to evaluate the Effectiveness of 
# Magnusson's algorithm. 
# 
# Author: Michael Cross     March 5, 2021

from scipy import random
import numpy as np
import matplotlib.pyplot as plt


def rollDice(n):
    # Rolls n amount of dice and stores the results in a dictionary of each 
    # possible outcome tagged with their number of occurrences. 

    hand = []
    for i in range(n):
        hand.append(random.randint(1,6))

    occurrences = dict((x, hand.count(x)) for x in set(hand))
    keys_seen = [1,2,3,4,5,6]
    
    for key in occurrences.keys():  #loop through each dictionary's keys
        if key not in keys_seen:  #if we haven't seen this key before, then...
            keys_seen.append(key)  #add it to the list of keys seen

    for key in keys_seen:  #loop through the list of keys that we've seen
        if key not in occurrences:  #if the dictionary is missing that key, then...
            occurrences[key] = 0  #add it and set it to 0

    return occurrences


def calculateHand(occurrences):
    # Calculates the score of a given hand, the number of potential dice left to
    # roll, and 0 or 1 indicating if the player has farkeled or not. 
    # The answer array looks like => [score, n_dice_left, is_Hand_Farkle].

    score = 0
    n_dice_scored = 0
    is_Hand_Farkle = 0
    answer = []
    # Set of hands where every dice scores
    # 6 of a kind
    if (isSixOfAKind(occurrences) != 0):
        score = 8*isSixOfAKind(occurrences)
        answer.append(score)
        answer.append(6)
        answer.append(0)
        return answer

     # Straight (1-2-3-4-5-6)
    if (all(value == 1 for value in occurrences.values())):
        score = 1500
        answer.append(score)
        answer.append(6)
        answer.append(0)
        return answer

    # 2 threes of a kind     
    if (isThreeOfaKind(occurrences)[0] == 2): 
        score = 1750
        answer.append(score)
        answer.append(6)
        answer.append(0)
        return answer

    # Three Pairs
    if (isThreePairs(occurrences)):
        score = 1000
        answer.append(score)
        answer.append(6)
        answer.append(0)
        return answer

    # Booleans to stop adding 100s or 50s if the score is already counting a 
    # rolled 1 or 5 in the hand
    three_Or_More_Ones = False
    three_Or_more_Fives = False

    # 1 three of a kind
    if (isThreeOfaKind(occurrences)[0] == 1):
        if (isThreeOfaKind(occurrences)[1] == 10):
            three_Or_More_Ones = True
        elif (isThreeOfaKind(occurrences)[1] == 5):
            three_Or_more_Fives = True

        n_dice_scored += 3
        score += (100*isThreeOfaKind(occurrences)[1])

    # 4 of a kind 
    if (isFourOfAkind(occurrences) != 0):
        if (isFourOfAkind(occurrences) == 10):
            three_Or_More_Ones = True
        elif (isFourOfAkind(occurrences) == 5):
            three_Or_more_Fives = True

        n_dice_scored += 4
        score += (200*isFourOfAkind(occurrences))

    # 5 of a kind 
    if (isFiveOfAKind(occurrences) != 0):
        if (isFiveOfAKind(occurrences) == 10):
            three_Or_More_Ones = True
        elif (isFiveOfAKind(occurrences) == 5):
            three_Or_more_Fives = True
        
        n_dice_scored += 5
        score += (400*isFiveOfAKind(occurrences))

    # Add score for 1s 
    if (three_Or_More_Ones == False and occurrences[1] !=0):
        n_dice_scored += occurrences[1]
        score += (100*occurrences[1])

    # Add score for 5s
    if (three_Or_more_Fives == False and occurrences[5] !=0):
        n_dice_scored += occurrences[5]
        score += (50*occurrences[5])

    if (score == 0):
        is_Hand_Farkle = 1

    # Get the number of dice that did not add up to your score. 
    n_dice_in_roll = 0
    for i in range(len(occurrences)):
        if (occurrences[i+1] != 0):
                n_dice_in_roll += occurrences[i+1]
    
    answer.append(score)

    # Account for "hot hand"
    if (n_dice_scored == 6):
        answer.append(n_dice_scored)
    else:
        answer.append(n_dice_in_roll - n_dice_scored)

    answer.append(is_Hand_Farkle)
    return answer


# -----------------------------------------------------------------------------
# SCORING RULES METHODS BEGIN
# -----------------------------------------------------------------------------

def isThreeOfaKind(occurrences):
    # Determines if there are one or two 3 of a kinds in the hand.

    number_of_threes = 0
    n_threes = 0
    for i in range(6):
        if(occurrences[i+1] == 3):
            number_of_threes += 1
            n_threes = i+1
    
    answer = []
    answer.append(number_of_threes)
    if (n_threes == 1):
        answer.append(10)
    else:
        answer.append(n_threes)
    return answer


def isFourOfAkind(occurrences):
    # Determines if there is a 4 of a kind in the hand.

    for i in range(6):
        if(occurrences[i+1] == 4):
            if (i+1 == 1):
                return 10
            return i+1

    return 0


def isFiveOfAKind(occurrences):
    # Determines if there is a 5 of a kind in the hand.

    for i in range(6):
        if(occurrences[i+1] == 5):
            if (i+1 == 1):
                return 10
            return i+1

    return 0


def isSixOfAKind(occurrences):
    # Determines if there is a 6 of a kind in the hand.

    for i in range(6):
        if(occurrences[i+1] == 5):
            return i+1

    return 0


def isThreePairs(occurrences):
    # Determines if there are three pairs in the hand.

    num_pairs = 0
    for i in range(6):
        if(occurrences[i+1] == 2):
            num_pairs += 1
    
    if (num_pairs == 3):
        return True
    
    return False
        

# -----------------------------------------------------------------------------
# SCORING RULES METHODS END
# -----------------------------------------------------------------------------

def preformStrategy(answer, fixed_stopping_point):
    # Applying the basic farkle rules to create a strategy for winning obtaining
    # an optimal score. Method essentially decides whether or not to roll again
    # after 1 hand has been calculated. 
    # fixed_stopping_point represents the users tolerance for risk.

    score_for_turn = (answer)[0]
    n_more_dice = (answer)[1]
    did_farkle = bool((answer)[2])

    keep_rolling = True
    while (keep_rolling == True):
        # If there are n or less dice, stop. 
        if (fixed_stopping_point >= n_more_dice and did_farkle == False):
            return score_for_turn

        # If you didn't farkle, and your running score is less than 1000, roll
        #if (did_farkle == False and score_for_turn <= 1000 
        if (did_farkle == False and  n_more_dice > fixed_stopping_point):
            new_occurrences = rollDice(n_more_dice)
            score_for_turn += calculateHand(new_occurrences)[0]
            n_more_dice = calculateHand(new_occurrences)[1]
            did_farkle = bool(calculateHand(new_occurrences)[2])

            if (did_farkle):
                return 0
        else:
            keep_rolling = False

        if (did_farkle):
            return 0

    return score_for_turn


def performMonteCarloAndGenerateGraphs():
    N = 100000
    areas = []
    returns = []

    for i in range(N): 
        integral = 0 

        occurrences = (rollDice(6))
        answer = calculateHand(occurrences)
        ultimate_score = preformStrategy(answer, 4)
        areas.append(ultimate_score)
    
    average_score = sum(areas)/ 100000
    std_dev = np.std(areas)

    plt.title('Scores per hand played')
    plt.hist(areas, bins = 30, ec = 'black')
    plt.xlabel('Scores')
    plt.xlim(0,8000)
    plt.ylim(0,35000)
    plt.show()
    returns.append(average_score)
    returns.append(std_dev)
    return returns

# test set that yeilds a score
#occurrences = {1: 1, 3: 4, 5: 1, 2: 0, 4: 0, 6: 0}

hand = rollDice(6)
print(hand)

score_for_hand = calculateHand(hand)
print(score_for_hand)

#x = preformStrategy(score_for_hand, 3)
#print(x)

#print('The average farkle hand scored')
print(performMonteCarloAndGenerateGraphs())