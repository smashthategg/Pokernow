from card import Card
from deck import Deck
from equity_calculator import *
from range import Range
import numpy as np

hero = Player('p1',1000)
o1 = Player('p2',1000)
o2 = Player('p3',1000)
o3 = Player('p4',1000)
opps = [o1]

def test_case1():
    d = Deck(shuffle = True)
    hero.deal(d.deal(2))
    print(hero.get_hand())
    for opp in opps:
        opp.deal(d.deal(2))
        print(opp.get_hand())
    opp_hands = [opp.hand for opp in opps]
    board = d.deal(3)
    print(board)

    print(calculate_equity(hero.hand,opp_hands,board))


def test_case2():
    equity = 0
    iterations = 100000
    for i in range(iterations):
        d = Deck(shuffle = True)
        hero.clear_hand()
        hero.deal(d.deal(2))
        for opp in opps:
            opp.clear_hand()
            opp.deal(d.deal(2))
        opp_hands = [opp.hand for opp in opps]
        board = d.deal(5)
        equity += calculate_equity(hero.hand,opp_hands,board)
        
    print(equity/iterations)

def test_case3(): 
    d = Deck(shuffle = True)
    hero.deal(d.deal(2))
    o1.add_card(Card('A', 'clubs'))
    o1.add_card(Card('A', 'hearts'))

    print(calculate_equity(hero.hand,[o1.hand],d.deal(3)))

np.set_printoptions(linewidth=100)


r = Range() # the number is the best X% of hands to be included in the range. (ex. 0.1 corresponds to 10%)
r.set_range(0.12)
r.set_custom_range(['66+','A7s+','KTs+','QJs','KJo+','ATo+'])
print(r.range)
print(r.simple_range)
print(r)


