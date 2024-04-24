from range import Range
from ranges import *
from equity_calculator import classify_hand

class Opponent():
    def __init__(self, name, type='rec', stack=1000):
        self.name = name
        self.stack = stack # we update stack and bet with set_stack() and set_bet()
        self.bet = 0
        self.type = type
        self.range = Range()

    def update_preflop_range(self, bet, bbsize):
        percent_stack = bet/self.stack
        if self.type == 'rec':
            new_range = rec_ranges
        elif self.type == 'reg':
            new_range = reg_ranges
        else:
            new_range = rec_ranges
        if bet <= bbsize:
            self.range = new_range['limp']
        elif percent_stack <= 0.15:
            self.range = new_range['15%']
        else:
            self.range = new_range['30%']

    def remove_trash_hands_from_range(self, board, hero_hand):
        self.range.range = self.range.get_range_without_cards(board + hero_hand)
        for hand in self.range.range:
            if classify_hand(hand + board) == 'High Card':
                self.range.range.remove(hand)

    def set_stack(self, stack):
        self.stack = stack

    def set_bet(self, bet):
        self.bet = bet
