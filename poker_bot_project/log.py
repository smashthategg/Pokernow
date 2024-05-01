
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

def is_new_hand(new_string, substring="Player stacks: "):
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


def get_player_actions(players_string):
    player_actions = {}
    action = ""
    new_round = False
    log = players_string.split('\n')
    for line in log:
        if "posts a big blind" in line:
            break
        if line[:4] in ["Flop","Turn","Rive"]:
            new_round = True
            continue
        matches = re.findall(r"(calls|raises to|folds|bets|checks)", line)
        if len(matches) > 1: # if some rat's name also contains "calls" or "raises" etc
            matches = [(match.start(), match.end(), match.group()) for match in re.finditer(r"(call|raises|folds|checks)", line)]
            last_occurrence_start, last_occurrence_end, _ = matches[-1]
            name = line[:last_occurrence_start].strip()
            action = line[last_occurrence_start:last_occurrence_end].strip()
            bet = line[last_occurrence_end:].strip()
        elif len(matches) == 1:
            parts = re.split(r"(calls|raises to|folds|bets|checks)", line)
            action = parts[1]
            name = parts[0].strip()
            bet = parts[-1]
        if not new_round:
            if action in ['calls','bets','raises to']:
                player_actions[name] = int(re.search(r'\d+',bet).group())
            elif action == 'checks':
                player_actions[name] = 0
            else:
                player_actions[name] = -1
        else:
            if action == 'folds':
                player_actions[name] = -1
        
    return player_actions
    
def get_board(string):
    board = []
    postflop = re.search(r'(Flop|Turn|River):.*\[(.*)\]', string)
    if postflop:
        cards = postflop.group(2).split(', ')
        for card in cards:
            if card[0] == '1':
                val = 'T'
            else:
                val = card[0]
            if card[-1] == '♣':
                suit = 'clubs'
            elif card[-1] == '♦':
                suit = 'diamonds'
            elif card[-1] == '♥':
                suit = 'hearts'
            else:
                suit = 'spades'
            board.append(Card(val,suit))
    return board