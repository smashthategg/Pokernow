from card import Card
from deck import Deck
from equity_calculator import calculate_hand_strength

c1 = Card('3','♣')
c2 = Card('5','♣')
c3 = Card('5','♦')
c4 = Card('J','♣')
c5 = Card('T','♣')
c6 = Card('9','♣')
c7 = Card('8','♣')

cards = [c1,c2,c3,c4,c5,c6,c7]
calculate_hand_strength(cards)