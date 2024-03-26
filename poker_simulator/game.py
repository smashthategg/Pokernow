from player import Player
from deck import Deck

class Game:
    def __init__(self, numOfPlayers, playerList):
        self.deck = Deck()
        self.players = []
        for i in range(numOfPlayers):
            self.players.append(playerList[i])
        self.graveYard = []  #aka burnpile
        self.pot = 0
        
    def start(self):
        self.deck.shuffle()
        self.graveYard.append(self.deck.deal(1))  #burn 1
        for player in self.players:
            player.deal(self.deck.deal(2))

    def bettingRound(self):
        for player in self.players:
            amount = int(input(f"{player.name}'s bet: "))
            if player.bet(amount) == -1:  #bet higher than remaining chips
                break
            else:
                self.pot += amount
    
    #todo: add winner evaluation, gamestatus, and complete game logic
                
    def play(self):
        self.start()
        self.bettingRound()
