from card import Card
from deck import Deck
from player import Player
from game import Game

d = Deck()

print(d)

d.shuffle()

print(d)

d.shuffle()

print(d)

print()
dylan = Player("Dylan", 100)
dylan.status()
print()

johnny = Player("Johnny", 100)
johnny.status()
tempList = [dylan, johnny]
game = Game(2, tempList)
game.play()
dylan.status()
johnny.status()