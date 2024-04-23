# card.py

values = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
class Card():
    def __init__(self, value, suit):
        self.suit = suit # [♣ club,♦ diamond,♥ heart,♠ spade]
        self.value = value # [2,3,4,5,6,7,8,9,10,J,Q,K,A]
        self.num = values.index(value) + 2

    def __gt__(self, rhs):
        return self.num > rhs.num
    
    def __lt__(self, rhs):
        return self.num < rhs.num
    
    def equal_in_value(self, rhs):
        return self.num == rhs.num
    
    def __eq__(self, rhs):
        return self.num == rhs.num and self.suit == rhs.suit
    
    def __str__(self):
        suit_to_emoji = {
                            'clubs': '♣',
                            'diamonds': '♦',
                            'hearts': '♥',
                            'spades': '♠'
                        }
        return self.value + suit_to_emoji[self.suit]
    
    def __repr__(self):
        suit_to_emoji = {
                            'clubs': '♣',
                            'diamonds': '♦',
                            'hearts': '♥',
                            'spades': '♠'
                        }
        return self.value + suit_to_emoji[self.suit]