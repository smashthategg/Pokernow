from card import Card
from deck import Deck
from player import Player

d = Deck()

print(d)

d.shuffle()

print(d)

d.shuffle()

print(d)

print()
dylan = Player("Dylan", 100)
dylan.status()