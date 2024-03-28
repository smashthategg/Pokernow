from card import Card
from deck import Deck
from equity_calculator import *

c1 = Card('3','hearts')
c2 = Card('4','clubs')
c3 = Card('A','clubs')
c4 = Card('2','spades')
c5 = Card('T','diamonds')
c6 = Card('4','hearts')
c7 = Card('K','clubs')

cards = [c1,c2,c3,c4,c5,c6,c7]

print(find_best_combo(cards)[0])

for card in find_best_combo(cards)[1]:
    print(card)