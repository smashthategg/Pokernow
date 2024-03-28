from player import Player
from deck import Deck

class Game:
    def __init__(self, numOfPlayers, playerList):
        self.deck = Deck()
        self.players = []
        for i in range(numOfPlayers):
            self.players.append(playerList[i])
        self.table = []
        self.graveYard = []  #aka burnpile
        self.pot = 0
        
    def start(self):
        self.deck.shuffle()
        self.burn1()
        for player in self.players:
            player.deal(self.deck.deal(2))

    def deal1(self):
        self.burn1()
        self.deck.deal(1)
        self.table.append(self.deck.deal(1))

    def bettingRound(self):
        for player in self.players:
            amount = int(input(f"{player.name}'s bet: "))
            if player.bet(amount) == -1:  #bet higher than remaining chips
                break
            else:
                self.pot += amount
    def burn1(self):
        self.graveYard.append(self.deck.deal(1))

    #def handEvaluation(self):
        
    
    #todo: add winner evaluation, gamestatus, and complete game logic
                
    def play(self):
        self.start()
        self.bettingRound()  #pre flop
        self.burn1()
        for i in range(3):   #flop
            self.deal1()
        self.bettingRound()
        self.burn1()
        self.deal1()    #turn
        self.bettingRound()
        self.burn1()
        self.deal1()    #river
        self.bettingRound()
        #compare hands and announce winners