# player.py

from card import Card

class Player():
    def __init__(self):
        self.hand = [None, None]

    def add_to_hand(self, card):
        if not self.hand[0]:
            self.hand[0] = card
        elif not self.hand[1]:
            self.hand[1] = card
        else:
            raise Exception('Hand is full!')

    def get_hand(self):
        return [str(self.hand[0]),str(self.hand[1])]