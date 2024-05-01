import re
from card import Card
from opponent import Opponent
from deck import Deck
import json
# from actions import read_log, get_cards

# with open('../Pokernow/stats.json') as json_file:
#    stats = json.load(json_file)

with open(r'C:\Users\uclam\Downloads\python_workspaces\pokernow\Pokernow\stats.json') as json_file:
    stats = json.load(json_file)


class Game_State:

    # initialize
    def __init__(self, name, is_playing = True):
        
        self.name = name # pokernow username
        self.player_list = [] # list of all names in order, changed along with opponents
        self.opponents = [] # list of opponent objects (names + stacks + style)
        self.opponents_in_hand = self.opponents # list of opponent objects in the hand
        self.opponents_acted = []
        self.log = "" # current log
        self.board = []
        self.stack = 1000
        self.big_blind = 20
        self.cards = []
        self.pot = 0
        self.big_blind_index = -1 # position of the big blind (to determine order)
        self.player_index = -1 # index of the bot in the player list
        self.is_playing = is_playing # T/F if the bot is playing



    # print function
    def print(self):
        print(f"Players: {self.player_list}")
        print("Opponents: ")
        for opponent in self.opponents:
            print(f"{opponent.name} {opponent.stack}")
        print("Opponents in hand: ")
        for opponent in self.opponents_in_hand:
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
        print(f"player index: {self.player_index}")


    def initial_get_opponents_and_stacks(self, player_stacks):
        # get opponents and stacks
        opponents = []
        for i, player in enumerate(player_stacks):
            self.player_list.append(player)
            if player != self.name:
                try:
                    player_type = stats[player]['type']
                except:
                    player_type = 'rec'
                opponents.append(Opponent(player, player_type, player_stacks[player]))
        self.opponents = opponents
        self.opponents_in_hand = opponents
        self.opponents_acted = []
        self.player_index = self.player_list.index(self.name)


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
        self.opponents_acted = []

        # Update the stack for the bot
        if self.name in player_stacks:
            self.stack = player_stacks[self.name]

        # Update the player list (for when an opponent is knocked out)
        self.player_list = [player for player in self.player_list if player in player_stacks]
        self.player_index = self.player_list.index(self.name)     

    def read_blinds(self, blinds_string):
        # Regular expression to find the player's name and the "big/small blind" text and extract both the name and the amount
        match = re.search(r'(\w+) posts a big blind of (\d+)', blinds_string)
        match2 = re.search(r'(\w+) posts a small blind of (\d+)', blinds_string)

        # Regular expression to detect changes in the big blind
        match3 = re.search(r'The game\'s big blind was changed from \d+ to (\d+)', blinds_string)

        # Check if there's a change in the big blind and update
        if match3:
            new_big_blind = int(match3.group(1))
            self.big_blind = new_big_blind
            print(f"Big blind updated to {self.big_blind}")
        
            
        self.big_blind_index = self.player_list.index(match.group(1))
        print('BB Index is {}, {}'.format(self.big_blind_index, match.group(1)))

        if match2:
            return False
        else:
            return True

    # helper function to update player actions
    def update_player_actions(self, player_actions):
        for player in player_actions:
            bet = player_actions[player]
            if bet == -1:
                for opp in self.opponents_in_hand:
                    if player == opp.name:
                        self.opponents_in_hand.remove(opp)
            else:
                for opp in self.opponents_in_hand:
                    if player == opp.name:
                        opp.set_bet(bet)
                        self.opponents_acted.append(opp)

    def update_board(self, board):
        # We should reset player bet's if the board updates as that signifies a new round of betting.
        for opponent in self.opponents_in_hand:
            opponent.set_bet(0)
            self.opponents_acted = []
        self.board += board

    # helper function to update cards
    def update_cards(self, cards_list):
        cards = []
        cards.append(Card(cards_list[0], cards_list[1]))
        cards.append(Card(cards_list[2], cards_list[3]))
        self.cards = cards

        

    # FUNCTION to reset game state for a new hand
    def new_hand(self, player_stacks, cards_list):
        self.update_opponents_and_stacks(player_stacks)
        self.update_cards(cards_list)
        self.board = []
        self.playing = True

    def read_updates(self, new_log):
        # Find the first instance where the new log diverges from the old log
        new_lines = []
        for line in new_log.split('\n'):
            if len(line) > 5:
                new_lines.append(line)

        print("------SELF.LOG-----")
        print(self.log)
        print("------NEW_LOG---------")
        print(new_lines)

        # If original log was empty/we are on a new hand, we just set it to the new log.
        if self.log == '' or (new_lines[-1] != self.log[-1] and new_lines[-1][:14] == 'Player stacks:'):
            self.log = new_lines
            return "\n".join(new_lines)
        else:
            while self.log[-1] != new_lines[-1]:
                self.log.pop()
            updated_entries = "\n".join(new_lines[:len(new_lines) - len(self.log)])
            self.log = new_lines
            return updated_entries
        

    def get_bot_position(self, deadsb):
        positions = ['UTG','UTG+1','LJ','HJ','CO','BTN','SB','BB']
        if deadsb:
            positions.remove('SB')
        relative_position = self.player_index - self.big_blind_index - 1
        return positions[relative_position]
    


    def process_log_lines(self, log_lines):
        # Regex pattern to capture player actions with two possible formats for amount
        action_pattern = re.compile(r"([^ ]+) (folds|checks|calls|raises|bets)(?: to (\d+)| (\d+))?")

        for line in log_lines.split('\n'):
            line = line.strip()
            if not line:
                continue

            # Apply regex pattern
            match = action_pattern.match(line)
            if not match:
                # print("No valid action found in line:", line)
                continue
            
            player_name, action, amount_to, amount_direct = match.groups()
            # Determine the correct amount, whether it's after "to" or directly after the action
            amount = int(amount_to if amount_to else amount_direct) if amount_to or amount_direct else 0

            # Find the opponent object
            opponent = next((o for o in self.opponents_in_hand if o.name == player_name), None)
            if not opponent:
                print(f"Opponent {player_name} not found")
                continue

            # Apply action logic
            if action == 'folds':
                print(f"{player_name} folds")
                self.opponents_in_hand.remove(opponent)
                self.opponents_to_act.remove(opponent)
            elif action in ['calls', 'checks']:
                print(f"{player_name} {action}")
                self.opponents_to_act.remove(opponent)
                self.opponents_acted.append(opponent)
            elif action in ['raises', 'bets']:
                print(f"{player_name} {action} to {amount}")
                self.bet_to_call = amount
                self.opponents_to_act = list(self.opponents_in_hand)
                self.opponents_to_act.remove(opponent)
                self.opponents_acted = [opponent]

    def find_opponent_by_name(self, name):
        return next((op for op in self.opponents if op.name == name), None)