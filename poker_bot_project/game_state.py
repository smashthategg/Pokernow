import re
from card import Card
from opponent import Opponent
from deck import Deck
# from actions import read_log, get_cards

class Game_State:

    # initialize
    def __init__(self, name, player_list, opponents, log, stack=1000, big_blind=20, big_blind_index=-1,
                 cards=[Card('2', 'spades'), Card('7', 'hearts')], pot=0, 
                 deck=Deck(), is_playing=True, bet_to_call=0
                ):
        
        self.name = name # pokernow username
        self.player_list = player_list # list of all names in order, changed along with opponents
        self.opponents = opponents # list of opponent objects (names + stacks + style)
        self.opponents_in_hand = self.opponents # list of opponent objects in the hand
        self.opponents_to_act = self.opponents_in_hand
        self.opponents_acted = []
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
        self.is_turn = False




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
        print("Opponents acted: ")
        for opponents in self.opponents_acted:
            print(f"{opponents.name} {opponents.stack}")
        # print(f"log: {self.log}")
        print(f"stack: {self.stack}")
        print(f"big blind: {self.big_blind}")
        print(f"cards: {self.cards}") 
        print(f"pot: {self.pot}")
        # print(f"deck: {self.deck}")
        print(f"big blind index: {self.big_blind_index}")
        print(f"is playing: {self.is_playing}")
        print(f"bet to call: {self.bet_to_call}")
        print(f"player index: {self.player_index}")
        print(f"is turn: {self.is_turn}")


    def initial_get_opponents_and_stacks(self, player_stacks):
        # get opponents and stacks
        opponents = []
        for i, player in enumerate(player_stacks):
            if player != self.name:
                opponents.append(Opponent(player, player_stacks[player]))
        self.opponents = opponents
        self.opponents_in_hand = self.opponents
        self.opponents_to_act = self.opponents_in_hand
        self.opponents_acted = []


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
        self.opponents_to_act = self.opponents_in_hand
        self.opponents_acted = []

        # Update the stack for the bot
        if self.name in player_stacks:
            self.stack = player_stacks[self.name]

        # Update the player list (for when an opponent is knocked out)
        self.player_list = [player for player in self.player_list if player in player_stacks]     



    # helper function to update blinds
    def update_blinds_and_pot(self, big_blind, big_blind_name, small_blind=True):
        self.big_blind = big_blind
        if big_blind_name in self.player_list:
            self.big_blind_index = self.player_list.index(big_blind_name)
        else:
            raise ValueError(f"Player name '{big_blind_name}' not found in player list.")
        # self.big_blind_index = (self.big_blind_index + 1) % len(self.player_list)

        # for updating pot
        if small_blind:
            self.pot = self.big_blind + self.big_blind/2
        else:
            self.pot = self.big_blind

        # for updating bet to call
        if self.big_blind_index == self.player_index:
            self.bet_to_call = 0 # when bot is big blind
            # self.stack -= self.big_blind
        elif small_blind and self.big_blind_index - 1 == self.player_index:
            self.bet_to_call = self.big_blind/2 # when bot is small blind
            # self.stack -= self.big_blind/2


    # helper function to update cards
    def update_cards(self, cards_list):
        cards = []
        cards.append(Card(cards_list[0], cards_list[1]))
        cards.append(Card(cards_list[2], cards_list[3]))
        self.cards = cards
        

    # FUNCTION to reset game state for a new hand
    def new_hand(self, player_stacks, big_blind_info, cards_list, deck=Deck()):
        
        self.update_opponents_and_stacks(player_stacks)
        self.update_blinds_and_pot(big_blind_info[0], big_blind_info[1], big_blind_info[2])
        self.update_cards(cards_list)

        self.deck = deck.remove(self.cards[0]) # removes cards from deck
        self.deck = deck.remove(self.cards[1])
        self.playing = True



    # UNTESTED
    def check_turn(self):
        # Calculate the first player to act after the big blind
        first_to_act_index = (self.big_blind_index + 1) % len(self.player_list)
        if self.player_index == first_to_act_index:
            # The bot is first to act
            self.is_turn = True
        else:
            # Determine if the player right before the bot has acted
            prev_player_index = (self.player_index - 1) % len(self.player_list)
            prev_player_name = self.player_list[prev_player_index]
            acted_names = [opponent.name for opponent in self.opponents_acted]
            if prev_player_name in acted_names:
                self.is_turn = True
            else:
                self.is_turn = False
        
        return self.is_turn


    # UNTESTED
    def check_updated(self, new_log):
        if self.log == new_log:
            return False
        else:
            return True


    # UNTESTED
    def check_updates(self, new_log):
        # This variable will store the earliest point in new_log that matches the start of the old log
        earliest_match_index = len(new_log)

        # We'll check various start points of the old log to find if any part of it is in the new log
        for start in range(len(self.log)):
            index = new_log.find(self.log[start:])
            if index != -1 and index < earliest_match_index:
                earliest_match_index = index

        # Determine the new entries
        if earliest_match_index != len(new_log):
            new_entries = new_log[:earliest_match_index]  # New log entries added before part of the old log found
        else:
            # If no part of the old log is found in the new log, consider all as new
            new_entries = new_log

        # Update the log to the new log
        self.log = new_log

        # Return the new entries
        return new_entries

    
    

if __name__ == "__main__":
    game = Game_State("luc1", ["luc1", "luc2"], [Opponent("luc2")],  "Player stacks: #1 luc1 (960) | #2 luc2 (1040)")
    # game.print()
    game.new_hand({'luc1': 960, "luc2" : 1040}, [20, 'luc1', True], ['2', 'spades', '7', 'hearts'])
    game.print()

