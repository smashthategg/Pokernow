from card import Card
from player import Player
from deck import Deck

# testing

d = Deck()
p1 = Player()
p2 = Player()
p1.add_to_hand(d.deal())
p2.add_to_hand(d.deal())
p1.add_to_hand(d.deal())
p2.add_to_hand(d.deal())

def calculate_equity(players, board):
    return

'''
1 high card
2 pair
3 two pair
4 trips
5 straight
6 flush
7 full house
8 quads
9 straight flush
10 royal flush      
'''

def calculate_hand_strength(cards): # takes in a list of 7 cards, determines best 5-card combination, assigns it a value
    cards.sort(reverse = True)
    for i in range(0,5):
        print(cards[i])
