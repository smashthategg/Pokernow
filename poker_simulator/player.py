from deck import Deck

class Player:
  def __init__(self, name, chips):
    self.name = name
    self.hand = []
    self.chips = chips

  def deal(self, cards):
    for card in cards:
      self.hand.append(card)

  def bet(self, amount):
    if amount <= self.chips:
      self.chips -= amount
      return amount
    else:
      print(f"{self.name} doesn't have enough chips to bet {amount}.")
      return -1
  
  def status(self):
    print(f"{self.name} {self.hand} {self.chips}")
    for card in self.hand:
      print(f"{card}", end = "")
    print()
    
    def get_hand(self):
        return [str(self.hand[0]),str(self.hand[1])]
