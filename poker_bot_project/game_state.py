import re
from card import Card
from opponent import Opponent
from deck import Deck
from actions import read_log, get_cards

class Game_State:

    # initialize
    def __init__(self, name, player_list, opponents, log, stack=1000, big_blind=20, 
                 cards=[Card('2', 'spades'), Card('7', 'hearts')], pot=0, 
                 deck=Deck(), big_blind_index=-1, is_playing=True, bet_to_call=0
                ):
        
        self.name = name # pokernow username
        self.player_list = player_list # list of all names in order, changed along with opponents
        self.opponents = opponents # list of opponent objects (names + stacks + style)
        self.opponents_in_hand = self.opponents # list of opponent objects in the hand
        self.opponents_to_act = self.opponents_in_hand
        self.log = log # current log

        self.stack = stack
        self.big_blind = big_blind
        self.cards = cards
        self.pot = pot
        self.deck = deck # used for tracking cards left in deck
        self.big_blind_index = big_blind_index # position of the big blind (to determine order)
        self.is_playing = is_playing # T/F if the bot is playing
        self.bet_to_call = bet_to_call # amount needed to call
        self.player_index = self.player_list.index(self.name) # index of the bot in the player list



    # print function
    def print(self):
        print(f"Players: {self.player_list}")
        print("Opponents: ")
        for opponent in self.opponents:
            print(f"{opponent.name} {opponent.stack}")
        print("Opponents in hand: ")
        for opponent in self.opponents_in_hand:
            print(f"{opponent.name} {opponent.stack}")
        print("Opponents to act: ")
        for opponent in self.opponents_to_act:
            print(f"{opponent.name} {opponent.stack}")

        print(f"log: {self.log}")
        print(f"stack: {self.stack}")
        print(f"big blind: {self.big_blind}")
        print(f"cards: {self.cards}") 
        print(f"pot: {self.pot}")
        print(f"deck: {self.deck}")
        print(f"big blind index: {self.big_blind_index}")
        print(f"is playing: {self.is_playing}")
        print(f"bet to call: {self.bet_to_call}")
        print(f"player index: {self.player_index}")


    # helper function to update opponents and stacks
    def update_opponents_and_stacks(self, player_stacks):

        # Next, update the stacks for existing opponents if they are found in player_stacks
        for opponent in self.opponents:
            if opponent.name in player_stacks:
                opponent.stack = player_stacks[opponent.name]

        # Next, new list of opponents with only opponents in player_stacks
        self.opponents = [opponent for opponent in self.opponents if opponent.name in player_stacks]

        # update opponents in hand
        self.opponents_in_hand = self.opponents

        # Update the stack for the bot
        if self.name in player_stacks:
            self.stack = player_stacks[self.name]

        # Update the player list (for when an opponent is knocked out)
        self.player_list = [player for player in self.player_list if player in player_stacks]     



    # helper function to update blinds
    def update_blinds_and_pot(self, big_blind, small_blind=True):
        self.big_blind = big_blind
        self.big_blind_index = (self.big_blind_index + 1) % len(self.player_list)

        # for updating pot
        if small_blind:
            self.pot = self.big_blind + self.big_blind/2
        else:
            self.pot = self.big_blind

        # for updating bet to call
        if self.big_blind_index == self.player_index:
            self.bet_to_call = 0 # when bot is big blind
        elif small_blind and self.big_blind_index - 1 == self.player_index:
            self.bet_to_call = self.big_blind/2 # when bot is small blind

        

    # FUNCTION to reset game state for a new hand
    def new_hand(self, player_stacks, big_blind, cards, deck=Deck()):
        
        self.update_opponents_and_stacks(player_stacks)
        self.update_blinds(big_blind)

        self.cards = cards

        self.deck = deck.remove(cards[0]) # removes cards from deck
        self.deck = deck.remove(cards[1])
        self.playing = True



    
    


if __name__ == "__main__":
    game = Game_State("luc1", ["luc1", "luc2"], [Opponent("luc2")],  "Player stacks: #1 luc1 (960) | #2 luc2 (1040)")
    # game.print()
    game.new_hand({'luc1': 960, "luc2" : 1040}, 20, [Card('2', 'spades'), Card('7', 'hearts')])
    game.print()

