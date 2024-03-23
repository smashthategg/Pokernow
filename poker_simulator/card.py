# card.py


values = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
class Card():
    def __init__(self, value, suit):
        self.suit = suit # [♣,♦,♥,♠]
        self.value = value # [2,3,4,5,6,7,8,9,T,J,Q,K,A]
    
    def __gt__(self, rhs):
        return values.index(self.value) > values.index(rhs.value)
    
    def __lt__(self, rhs):
        return values.index(self.value) < values.index(rhs.value)
    
    def __eq__(self, rhs):
        return values.index(self.value) == values.index(rhs.value)

    def __str__(self):
        return self.value + self.suit