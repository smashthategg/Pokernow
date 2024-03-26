from deck import Deck

class Player:
  def __init__(self, name, chips):
    self.name = name
    self.hand = []
    self.chips = chips

  def deal(self, cards):
    self.hand = cards

  def bet(self, amount):
    if amount <= self.chips:
      self.chips -= amount
      return True
    else:
      print(f"{self.name} doesn't have enough chips to bet {amount}.")
      return False
    
  def status(self):
    print(f"{self.name} {self.hand} {self.chips}")