from range import Range
from ranges import *

class Opponent():
    def __init__(self, name, type, stack, bet):
        self.name = name
        self.stack = stack
        self.type = type
        self.range = Range()
        self.bet = bet

    def update_preflop_range(self, bet, bbsize):
        percent_stack = bet/self.stack
        if self.type == 'rec':
            new_range = rec_ranges
        elif self.type == 'reg':
            new_range = reg_ranges
        if bet <= bbsize:
            self.range = new_range['limp']
        elif percent_stack <= 0.15:
            self.range = new_range['15%']
        else:
            self.range = new_range['30%']
