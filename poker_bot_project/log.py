
import re
from actions import read_log
from opponent import Opponent
from card import Card
from deck import Deck
from game_state import Game_State


# ----------------- LOG FUNCTIONS -------------------

# read_full_log(log) - TESTED

# read_log(driver) - TESTED

# is_new_hand(log) - TESTED

# get_opponnents_and_stacks(stacks_string) - TESTED

# read_blinds(blinds_string) - TESTED

# read_table_cards(table_cards_string)

# check_turn(log, player_name)

# check_log_for_updates(log, new_log)

# update_game_actions(action)

# read_updates(new_lines) - determine which function to use




# ----------------- CHECKS START OF NEW HAND FUNCTION -------------------

def is_new_hand(new_string, substring="posts a big blind of"):
    # Convert both strings to lower case to make the search case-insensitive
    new_string = new_string.lower()
    substring = substring.lower()
    
    # Optionally strip whitespace from the new_string
    new_string = new_string.strip()
    
    # Use str.find() to search for the substring in the text
    if new_string.find(substring) != -1:
        return True  # Return True if the substring is found
    return False



# ----------------- READ STACKS AND OPPONENTS FUNCTION -------------------

def get_opponents_and_stacks(stacks_string):
       # Dictionary to store player names as keys to stack sizes
    player_stacks = {}
    
    # Find the line containing "Player stacks:"
    stack_line = next((line for line in stacks_string.split('\n') if "Player stacks:" in line), None)

    if stack_line:
        # Use regular expression to extract relevant parts of the string
        # This regex finds "#", followed by a digit (\d), and captures the player name and stack size
        matches = re.findall(r"#\d+ ([^(]+) \((\d+)\)", stack_line)
        
        # Iterate through all found matches and populate the dictionary
        for match in matches:
            player_name = match[0].strip()  # Remove any trailing whitespace
            stack_size = int(match[1])
            player_stacks[player_name] = stack_size

    return player_stacks


'''
# ----------------- READ BLINDS FUNCTION -------------------

def read_blinds(blinds_string):
    # Regular expression to find the player's name and the "big/small blind" text and extract both the name and the amount
    match = re.search(r'(\w+) posts a big blind of (\d+)', blinds_string)
    match2 = re.search(r'(\w+) posts a small blind of (\d+)', blinds_string)
    if match and match2:
        # match.group(1) captures the player's name
        # match.group(2) captures the numeric value of the big blind
        return [int(match.group(2)), match.group(1), True]
    elif match:
        return [int(match.group(2)), match.group(1), False]
    elif match2:
        return [None, match2.group(1), False]
    else:
        # If no match is found, return None or raise an error depending on your error handling preference
        return [None, None, False]

'''


# READ FLOP / TURN / RIVER FUNCTION

# DETECT RAISE / FOLD / CALL / CHECK FUNCTION







'''
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
12:55
luc1 bets 40
12:55
luc2 checks
12:55
Flop: [Q♣, 7♠, 8♣]
12:55
luc1 calls 40
12:55
luc2 raises to 40
12:55
luc1 calls 20
12:55
luc2 posts a big blind of 20
12:55
luc1 posts a small blind of 10
12:55
Player stacks: #1 luc1 (1040) | #2 luc2 (960)
12:55
-- starting hand #2 (id: 7vuwhjcxxsj1) (No Limit Texas Hold'em) (dealer: luc1) --     
12:55

'''

if __name__ == "__main__":
    '''Example usage:
    stacks_string = "Player stacks: #1 luc_ 1 (960) | #2 luc2 (1040)"
    player_stacks = get_opponents_and_stacks(stacks_string)
    print(player_stacks)
    # output: {'luc1': 960, 'luc2': 1040}'''

    '''
    game = Game_State("luc1", [Opponent("luc2"), Opponent("luc3")], "Player stacks: #1 luc1 (1000) | #2 luc2 (1000)")
    game.print()

    game.new_hand({'luc1': 960, 'luc2': 1040}, 20, [Card('2', 'spades'), Card('7', 'hearts')], 0, Deck(), -1)    
    game.print()
    '''
    # print(read_blinds("luc2 posts a big blind of 20"))
    print(is_new_hand("Player posts a big blind of 20"))  # Expected: True
    print(is_new_hand("player POSTS a big blind of 20"))  # Expected: True, testing case insensitivity
    print(is_new_hand("  player posts a big blind of 20  "))  # Expected: True, testing whitespace
    print(is_new_hand("player posts small blind of 20"))  # Expected: False, different substring


'''
    def record_action(self, line, stage):
        nline = re.sub(r'"(.*?)" ', "", line).split()
        action = "NA"
        amount = 0
        match nline[0]:
            case 'folds':
                self.players_in_hand.remove(self.curr_player)
                action = 'F'
            case 'checks':
                action = 'X'
            case 'calls':
                amount = round(int(nline[1])/self.bb, 1)
                action = 'C'
            case 'raises':
                amount = round(int(nline[2])/self.bb, 1)
                action = 'R'
            case 'bets':
                amount = round(int(nline[1])/self.bb, 1)
                action = 'B'
            case 'Uncalled':
                amount = round(int(nline[3])/self.bb, 1)
            case 'shows':
                self.players[self.curr_player]['hand'][-1] = nline[-2] + " " + nline[-1][:-1]
            case 'collected':
                amount = round(int(nline[1])/self.bb, 1)
            case _:
                return
        if stage == 'preflop' and  self.players[self.curr_player][stage][-1] == 'NA': 
            if action in ['C','R'] and self.players[self.curr_player]['position'][-1] == 'SB':
                self.players[self.curr_player]['net'][-1] += 0.5
            if action in ['C','R'] and self.players[self.curr_player]['position'][-1] == 'BB':
                self.players[self.curr_player]['net'][-1] += 1
        if action in ['X','F','B','C','R']:
            if self.players[self.curr_player][stage][-1] == 'NA': # If this is the player's first action in the stage
                self.players[self.curr_player][stage][-1] = action   
            else:
                self.players[self.curr_player][stage][-1] += "-" + action         
        if action in ['B','C','R']: 
            self.players[self.curr_player][stage][-1] += str(amount)
            # Now we change the "net" values.
            for past_action in self.players[self.curr_player][stage][-1].split('-')[:-1]:
                if past_action[0] in ['B','C','R']: # We dont also want to deduct past bets in the same stage.
                    self.players[self.curr_player]['net'][-1] += float(past_action[1:])
            self.players[self.curr_player]['net'][-1] -= amount
        else:
            self.players[self.curr_player]['net'][-1] += amount
            self.players[self.curr_player]['net'][-1] = round(self.players[self.curr_player]['net'][-1], 1)
        return

'''