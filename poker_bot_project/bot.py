from range import Range
from equity_calculator import *
import numpy as np


# def parse_data(log)
#   get the necessary parameters for get_strategy

# def get_strategy(hand, stack, position, players_in_hand, pot, board):
#   hand: bot's hand [Card, Card]
#   stack: bot's stack size in big blinds
#   position: bot's position
#   players_in_hand: dict of all players who checked/called/raised
#       { name: amount }
#   pot: size of pot in big blinds
#   board: list of Cards size 0 <= n <= 5.

#   return one of "call","check","raise","fold"

np.set_printoptions(linewidth=100)



positions = ['UTG','UTG1','LJ','HJ','CO','BTN','SB','BB']

def get_strategy(hand, stack, position, players_in_hand, pot, board):
    if board == []: # if preflop, we decide our play based on position, stack size, and previous player action.
        # in general, the later our position, the more hands we can play
        # the lower our stack, the tighter we play.
        # under 10BB, we construct a shove open range.
        percent_raise = 0.12 * 1.2 ^ positions.index(position)
        open_range = Range(percent_raise)
        if hand in open_range:
            return "raise"
