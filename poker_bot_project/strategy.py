from range import Range
from equity_calculator import *
import numpy as np
from ranges import *
from opponent import Opponent
import random

# def parse_data(log)
#   get the necessary parameters for get_strategy

'''
def get_preflop_strategy(hand, stack, bbsize, position, players_acted, players_to_act):
    hand: bot's hand [Card, Card]
    stack: bot's stack size
    bbsize: how much the big blind currently is   
    position: bot's position 
    players_acted: list of all players (Opponent objects, see Opponent.py) who called/raised
    players_to_act: list of all players (Opponent objects) who have NOT acted but not folded either.

  returns the size of the bet to be used 
  
def get_postflop_strategy(hand, stack, bbsize, players_acted, players_to_act, pot, board):
    pot: size of pot (will have to calculate)
    board: list of Cards of size 3 <= n <= 5
  
'''

np.set_printoptions(linewidth=100)

def get_preflop_strategy(hand, stack, bbsize, position, players_acted, players_in_hand):
    stack_in_bbs = stack/bbsize
    bet = -1
    current_bet = 0
    if stack_in_bbs < 10:
        effective = '10BB'
    elif stack_in_bbs < 17:
        effective = '17BB'
    else:
        effective = '50BB'
    if players_acted == []: # if we are first to act
        for action in bot_open_ranges[effective][position]:
            if hand in bot_open_ranges[effective][position][action]:
                if action == 'raise':
                    bet = bbsize * 2.1
                    break
                elif action == 'all in':
                    bet = stack
                    break
                elif action == 'limp':
                    bet = bbsize
                    break
    else: # if others have acted
        current_bet = max(players_acted, key=lambda x: x.bet).bet
        percent_stack = current_bet/stack
        for action in bot_facing_bets_ranges[effective][position]: 
            action_as_percentage = int(action[:-1])/100 
            if hand in bot_facing_bets_ranges[effective][position][action] and percent_stack <= action_as_percentage:
                if action_as_percentage == 1:
                    bet = stack
                    break
                elif 3*current_bet <= action_as_percentage * stack:
                    bet = 3*current_bet
                    break
                else:
                    bet = current_bet
                    break
        if bet == -1 and current_bet == bbsize and position == 'BB': # check
            bet = 0
    if bet >= stack:
        return stack
    else:
        for player in players_in_hand:
            player.update_preflop_range(bet, bbsize)
        return bet

def get_postflop_strategy(hand, stack, players_in_hand, pot, board):
    bet = -1
    num_regs = 0
    num_recs = 0
    current_bet = max(players_in_hand, key = lambda x: x.bet).bet
    pot_multiple = current_bet/pot
    stack_multiple = pot/(stack+pot)
    for player in players_in_hand:
        if player.type == 'reg':
            num_regs += 1
        elif player.type == 'rec':
            num_recs += 1
    min_to_call = (max(stack_multiple, pot_multiple) ** (1/(4 + num_regs)) - 0.2) * 3/(2+len(players_in_hand))
    min_to_raise = min_to_call + 0.2
    bluff_frequency = min(0.3 - 0.1 * num_recs, 0.5 - stack_multiple)
    bluff_candidate = False

    print(classify_hand(hand+board))
    if classify_hand(hand + board)[-4:] == 'Draw' and bluff_frequency > 0:
        bluff_candidate = True
        min_to_call = max(min_to_call - 0.3, 0.25) 
    print("min equity to call: {}".format(min_to_call))
    print("min equity to raise: {}".format(min_to_raise))
    print("bluff frequency: {}".format(bluff_frequency))


    equity = 0
    for i in range(750):
        opp_hands_simulation = []
        cards_in_play = hand + board
        for player in players_in_hand:
            for opp_hand in opp_hands_simulation:
                cards_in_play += opp_hand
            opp_hands_simulation.append(random.choice(player.range.get_range_without_cards(cards_in_play)))
        equity += calculate_equity(hand, opp_hands_simulation, board)
    equity = equity/750
    print("Estimated equity: {}".format(equity))

    if current_bet == 0:
        bet = 0
        bluff_frequency += 0.2
        if equity > 0.55 * 3/(2+len(players_in_hand)):
            bet = int(pot * 0.5)
        elif bluff_candidate and random.random() < bluff_frequency:
            print("Random frequency hit. Bluffing!")
            bet = int(pot * 0.5)
    elif equity > min_to_raise:
        bet = 3*current_bet
    elif equity > min_to_call:
        bet = current_bet
        if bluff_candidate and random.random() < bluff_frequency:
            print("Random frequency hit. Bluffing!")
            bet = 3 * current_bet

    if bet > 0:
        for player in players_in_hand:
            player.remove_trash_hands_from_range(board, hand)
    
    return bet                   

