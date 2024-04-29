import re
from card import Card
from opponent import Opponent
from deck import Deck
import json
# from actions import read_log, get_cards

# with open('../Pokernow/stats.json') as json_file:
    # stats = json.load(json_file)

with open(r'C:\Users\uclam\Downloads\python_workspaces\pokernow\Pokernow\stats.json') as json_file:
    stats = json.load(json_file)


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
        self.board = []
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
            print(opponent)
        print("Opponents in hand: ")
        for opponent in self.opponents_in_hand:
            print(opponent)
        print("Opponents to act: ")
        for opponent in self.opponents_to_act:
            print(opponent)
        print("Opponents acted: ")
        for opponent in self.opponents_acted:
            print(opponent)
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
                try:
                    player_type = stats[player]['type']
                except:
                    player_type = 'rec'
                opponents.append(Opponent(player, player_type, player_stacks[player]))
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

        if match and match2:
            # match.group(1) captures the player's name
            # match.group(2) captures the numeric value of the big blind
            return [self.big_blind, match.group(1), True]
        elif match:
            return [self.big_blind, match.group(1), False]
        elif match2:
            return [self.big_blind, match2.group(1), False]
        else:
            # If no match is found, return None or raise an error depending on your error handling preference
            return [None, None, False]

    # helper function to update blinds
    def update_blinds_and_pot(self, big_blind, big_blind_name, small_blind=True):
        if big_blind != None and big_blind_name != None and big_blind_name in self.player_list:
            self.big_blind = big_blind
            self.big_blind_index = self.player_list.index(big_blind_name)
        else:
            self.big_blind_index = self.big_blind_index + 1 % len(self.player_list)

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
        self.board += board



    # helper function to update cards
    def update_cards(self, cards_list):
        cards = []
        cards.append(Card(cards_list[0], cards_list[1]))
        cards.append(Card(cards_list[2], cards_list[3]))
        self.cards = cards
        self.deck = Deck()
        self.deck = self.deck.remove(self.cards[0])
        self.deck = self.deck.remove(self.cards[1])
        

    # FUNCTION to reset game state for a new hand
    def new_hand(self, player_stacks, big_blind_info, cards_list):
        
        self.update_opponents_and_stacks(player_stacks)
        self.update_blinds_and_pot(big_blind_info[0], big_blind_info[1], big_blind_info[2])
        self.update_cards(cards_list)
        self.board = []
        self.playing = True


    def check_updated(self, new_log):
        if self.log == new_log:
            return False
        else:
            return True


    # UNTESTED
    def read_updates2(self, new_log):
            # Find the first instance where the new log diverges from the old log
        index = 0
        for i in range(min(len(new_log), len(self.log))):
            if new_log[i] != self.log[i]:
                break
            index += 1

        # New entries are everything from this point to the end of the new log
        new_entries = new_log[index:]

        # Update the log
        self.log = new_log

        # Return the new entries
        return new_entries
    

    def get_bot_position(self):
        num_players = len(self.player_list)
        relative_position = (self.player_index - self.big_blind_index - 1) % num_players

        # Define the positions based on the number of players
        if num_players == 2:
            # Heads-up play has different naming (SB is also BTN)
            if relative_position == 0:
                return 'BTN'  # Small Blind is also the Button
            elif relative_position == 1:
                return 'BB'
        else:
            # Position names for more than two players
            if relative_position == 0:
                return 'SB'
            elif relative_position == 1:
                return 'BB'
            elif relative_position == 2:
                return 'UTG'
            elif relative_position == 3:
                return 'UTG+1'
            elif relative_position == 4:
                return 'LJ'
            elif relative_position == 5:
                return 'HJ'
            elif relative_position == 6:
                return 'CO'
            elif relative_position == 7:
                return 'BTN'
            else:
                # For tables larger than 9, additional players are usually considered as being in early positions
                return 'UTG+{}'.format(relative_position - 2)
    

    
    def process_log_lines(self, log_lines):
        # Iterate through each line in the log lines
        for line in log_lines.split('\n'):
            # Extract the player name and action from the line
            match = re.match(r"(\w+) (folds|checks|calls|raises|bets)(?: to (\d+))?", line)
            if not match:
                continue

            player_name, action, amount = match.groups()
            amount = int(amount) if amount else 0

            # Find the opponent object
            opponent = next((o for o in self.opponents_in_hand if o.name == player_name), None)
            if not opponent:
                continue

            # Apply action logic
            if action == 'folds':
                self.opponents_in_hand.remove(opponent)
                self.opponents_to_act.remove(opponent)
            elif action in ['calls', 'checks']:
                self.opponents_to_act.remove(opponent)
                self.opponents_acted.append(opponent)
            elif action in ['raises', 'bets']:
                self.bet_to_call = amount
                self.opponents_to_act = list(self.opponents_in_hand)
                self.opponents_to_act.remove(opponent)
                self.opponents_acted = [opponent]


    def find_opponent_by_name(self, name):
        return next((op for op in self.opponents if op.name == name), None)
    




    def read_updates(self, new_log):
        # Find the first instance of a line containing `self.name` in the old log
        index = self.log.find(self.name)
        if index != -1:
            # Capture the portion of the line around `self.name` for matching
            # Assuming '10 characters after' might vary based on actual log format,
            # Adjust as necessary for adequate context
            end_index = index + len(self.name) + 10  # Adjust the 10 if more context is needed
            last_known_action = self.log[index:end_index]
            self.log = new_log

            # Find this snippet in the new log
            new_index = new_log.find(last_known_action)
            if new_index != -1:
                # Return everything before this snippet in the new log as new entries
                new_entries = new_log[:new_index].strip()
                return new_entries

        # If no previous action or snippet is found in the new log, consider the whole new log as new entries
        return new_log.strip()

    

    
    

if __name__ == "__main__":
    
    '''
    game = Game_State("luc1", ["luc1", "clankylemon8"], [Opponent("clankylemon8")],  "Player stacks: #1 luc1 (960) | #2 luc2 (1040)")
    # game.new_hand({'luc1': 960, "luc2" : 1040}, [20, 'luc1', True], ['2', 'spades', '7', 'hearts'])
    # game.print()
    

    
    new_entries = """
    "zechbeans" bets 530
    "Pinnochio" calls 350 and go all in
    "ChucklesPop" folds
    Uncalled bet of 180 returned to "zechbeans"
    "zechbeans" shows a T♠, K♥.
    "Pinnochio" shows a 9♥, 9♣.
    River: 8♠, 4♦, T♥, Q♥ [7♣]
    "zechbeans" collected 2200 from pot with Pair, 10's (combination: T♠, T♥, K♥, Q♥, 8♠)
    -- ending hand #10 --
    The player "Pinnochio" quits the game with a stack of 0.
    The game's small blind was changed from 20 to 30.
    The game's big blind was changed from 40 to 60.
    -- starting hand #11 (id: hjvf5ih5xbw4)  (No Limit Texas Hold'em) (dealer: "ChucklesPop") --
    Player stacks: #1 "ChucklesPop" (530) | #2 "Toup" (2210) | #5 "clankylemon8" (1680) | #7 "zechbeans" (3580)
    "Toup" posts a small blind of 30
    clankylemon8 posts a big blind of 60
    """
    print(game.read_blinds(new_entries))
    '''

    log = """
    luc1 folds
    12:55
    luc2 raises to 120
    """
    new_log = """
    luc2 posts a big blind of 20
    12:55
    luc1 posts a small blind of 10
    12:55
    Player stacks: #1 luc1 (960) | #2 luc2 (1040)
    12:55
    -- starting hand #3 (id: hvsqmmxaoe6z) (No Limit Texas Hold'em) (dealer: luc2) --     
    12:55
    -- ending hand #2 --
    12:55
    luc2 collected 160 from pot
    12:55
    Uncalled bet of 80 returned to luc2
    12:55
    luc1 folds
    12:55
    luc2 raises to 120
    """


    game = Game_State("luc1", ['luc1', "clankylemon8"], [Opponent("clankylemon8")], log)

    # game.read_updates()
    # game.update_player_actions({'luc1 ': 0, 'clankylemon8': 20})
    # game.print()
    print(game.read_updates(new_log))
    
