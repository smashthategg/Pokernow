# deck.py
from card import Card
import random

class Deck():
    def __init__(self, shuffle = False):
        self.cards = []
        for suit in ['clubs','diamonds','hearts','spades']:
            for value in ['2','3','4','5','6','7','8','9','T','J','Q','K','A']:
                self.cards.append(Card(value, suit))
        if shuffle:
            self.shuffle()
    def __str__(self):
        return str(self.cards)
    def shuffle(self):
        for i in range(0,50):
            j = random.randint(i,51)
            temp = self.cards[i]
            self.cards[i] = self.cards[j]
            self.cards[j] = temp
    def deal(self, number):  #returns array of cards added
        dealtCards = []
        for i in range(number):
            dealtCards.append(self.cards.pop())
        return dealtCards
    def remove(self, card):
        self.cards.remove(card)
        return self
    
