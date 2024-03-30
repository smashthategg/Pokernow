from card import Card
from deck import Deck
from equity_calculator import *

d = Deck()
p1 = Player('p1',1000)
p2 = Player('p2',1000)
p1.deal(d.deal(2))
p2.deal(d.deal(2))
print(p1.get_hand())
print(p2.get_hand())