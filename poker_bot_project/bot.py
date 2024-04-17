from range import Range
from equity_calculator import *
import numpy as np
from ranges import *
from opponent import Opponent
import random

# def parse_data(log)
#   get the necessary parameters for get_strategy

# def get_strategy(hand, chips, position, players_acted, pot, board):
#   hand: bot's hand [Card, Card]
#   chips: bot's stack size
#   bbsize: how much the big blind currently is
#   position: bot's position
#   players_acted: dict of all players who checked/called/raised
#       { name: amount }
#   pot: size of pot in big blinds
#   board: list of Cards size 0 <= n <= 5.

#   return one of "call","check","raise","fold"

np.set_printoptions(linewidth=100)



def get_strategy(hand, stack, bbsize, position, players_acted, players_to_act, pot, board):
    stack_in_bbs = stack/bbsize
    bet = -1
    current_bet = 0
    if board == []: # if preflop, we decide our play based on position, stack size, and previous player action.
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
        if bet != stack:
            for player in players_acted + players_to_act:
                player.update_preflop_range(bet, bbsize)
        return bet
    else:
        '''advantage_to_value = 1.25
        advantage_to_bluff = 0.5
        for player in players_acted:
            if player.type == 'rec':
                advantage_to_bluff *= 1.3
            if player.type == 'reg':
                advantage_to_value *= 1.2'''

        equity = 0
        for i in range(750):
            opp_hands_simulation = []
            cards_in_play = hand + board
            for player in players_acted + players_to_act:
                for opp_hand in opp_hands_simulation:
                    cards_in_play += opp_hand
                opp_hands_simulation.append(random.choice(player.range.get_range_without_cards(cards_in_play)))
            equity += calculate_equity(hand, opp_hands_simulation, board)
        equity = equity/750
        if current_bet == 0:
            bet = 0
        if equity > 0.5:
            bet = bbsize
        if equity > 0.8:
            bet = stack
        
        return bet
                    


            


# ---- TESTING -------
positions = ['UTG','UTG+1','LJ','HJ','CO','BTN','SB','BB']
count = 0
for i in range(1):
    d = Deck(True)
    hand = d.deal(2)
    p1 = Opponent('p1', 'reg', 1000, 20)
    p2 = Opponent('p2', 'rec', 1000, 20)
    print(hand)
    print(get_strategy(hand, 1000, 20, 'BB', [p1], [p2], None, []))
    print(p1.range)
    print(p2.range)
