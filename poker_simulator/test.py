from card import Card
from deck import Deck
from equity_calculator import *


hero = Player('p1',1000)
o1 = Player('p2',1000)
o2 = Player('p3',1000)
o3 = Player('p4',1000)
opps = [o1,o2]

d = Deck()
hero.deal(d.deal(2))
print(hero.get_hand())
for opp in opps:
    opp.deal(d.deal(2))
    print(opp.get_hand())
opp_hands = [opp.hand for opp in opps]
board = d.deal(4)
print(board)

print(calculate_equity(hero.hand,opp_hands,board))

'''
equity = 0
for i in range(2500):
    d = Deck()
    hero.clear_hand()
    hero.deal(d.deal(2))
    for opp in opps:
        opp.clear_hand()
        opp.deal(d.deal(2))
    opp_hands = [opp.hand for opp in opps]
    board = d.deal(5)
    equity += calculate_equity(hero.hand,opp_hands,board)
    
print(equity/2500)
'''