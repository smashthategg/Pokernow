# deck.py
from card import Card
import random

class Deck():
    def __init__(self):
        self.cards = []
        for suit in ['♣','♦','♥','♠']:
            for value in ['2','3','4','5','6','7','8','9','T','J','Q','K','A']:
                self.cards.append(Card(value, suit))    
    def __str__(self):
        result = ""
        for card in self.cards:
            result += str(card) + ", "
        return result
    def shuffle(self):
        for i in range(0,50):
            j = random.randint(i,51)
            temp = self.cards[i]
            self.cards[i] = self.cards[j]
            self.cards[j] = temp
    def deal(self):
        return self.cards.pop()
    
