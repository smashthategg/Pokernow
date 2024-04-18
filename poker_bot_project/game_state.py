import re
from card import Card
from opponent import Opponent
from deck import Deck
from actions import read_log

class Game_State:

    # initialize
    def __init__(self, opponents, log, stack=1000, big_blind=20, 
                 cards=[Card('2', 'spades'), Card('7', 'hearts')], pot=0, deck=Deck(), big_blind_index=-1
                ):
        
        self.opponents = opponents
        self.opponents_in_hand = opponents
        self.log = log


        self.stack = stack
        self.big_blind = big_blind
        self.cards = cards
        self.pot = pot
        self.deck = deck
        self.big_blind_index = big_blind_index

    # print
    def print(self):
        for opponent in self.opponents:
            print(opponent.name, opponent.stack)
        for opponent in self.opponents_in_hand:
            print(opponent.name, opponent.stack)
        print(self.log)
        print(self.stack)
        print(self.big_blind)
        print(self.cards)
        print(self.pot)
        print(self.deck)
        print(self.big_blind_index)

    # reset game state for a new hand
    def new_hand(self, opponents, stack, big_blind, cards, pot, deck, big_blind_index):
        self.opponents = opponents
        self.opponents_in_hand = opponents
        self.stack = stack
        self.big_blind = big_blind
        self.cards = cards
        self.pot = pot
        self.deck = deck.remove(cards[0])
        self.deck = deck.remove(cards[1])
        self.big_blind_index = big_blind_index

    


if __name__ == "__main__":
    game = Game_State([Opponent("luc1"), Opponent("luc2")], "Player stacks: #1 luc1 (960) | #2 luc2 (1040)")
    # game.print()
    game.new_hand([Opponent("luc1"), Opponent("luc2")], 1000, 20, [Card('2', 'spades'), Card('7', 'hearts')], 0, Deck(), -1)
    game.print()

