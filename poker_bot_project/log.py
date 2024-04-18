
import re
from actions import read_log
from opponent import Opponent
from card import Card
from deck import Deck
from game_state import Game_State


# ----------------- LOG FUNCTIONS -------------------

# read_log(log) - TESTED

# is_new_hand(log) - DONE

# get_opponnents_and_stacks(stacks_string) - DONE

# update_opponents_and_stacks(Game_State, opponents) - TESTED

# read_blinds(blinds_string) 

# update_blinds(Game_State, big_blind)

# later:

# update_game_actions(action)

# is_turn() 

# is_updated(log, new_log)

# check_updates(log, new_log) - determine which function to use


# how to tell what position is the bot in? use in setup()
# maybe read the ledger at beginning of game



# ----------------- CHECKS START OF NEW HAND FUNCTION -------------------

def is_new_hand(new_string, substring="starting hand #"):
    # Use str.find() to search for the substring in the text
    if new_string.find(substring) != -1:
        return True  # Return True if the substring is found
    return False



# ----------------- READ STACKS AND OPPONENTS FUNCTION -------------------

def get_opponents_and_stacks(stacks_string):
    # dictionary to store player names as keys to stack sizes
    player_stacks = {}
    
    # Use regular expression to extract relevant parts of the string
    # finds "#", finds digit \d
    # finds word string ([^(]+)
    # finds "(", finds digit \d, finds ")"

    matches = re.findall(r"#\d+ ([^(]+) \((\d+)\)", stacks_string)

    
    # Iterate through all found matches and populate the dictionary
    for match in matches:
        player_name = match[0]
        stack_size = int(match[1])
        player_stacks[player_name] = stack_size
    
    return player_stacks


# ----------------- UPDATE OPPONENTS FUNCTION -------------------

def update_opponents_and_stacks(Game_State, player_stacks):
    for opponent in Game_State.opponents:
        for player in player_stacks:
            if opponent.name == player:
                opponent.stack = player_stacks[player]



# ----------------- READ BLINDS FUNCTION -------------------

def read_blinds(blinds_string):
    big_blind = 20
    return big_blind


# ----------------- UPDATE BLINDS FUNCTION -------------------

def update_blinds(Game_State, big_blind):
    pass


    



# ----------------- CHECK UPDATES FUNCTION -------------------

def check_updates(log, new_log):
    # check if new log is different from old log
    # if different,
    # check if new hand - 
        # update player stacks
        # check blinds - update blinds
    # check for new actions - 
        # update game actions
    # check if player before bot has acted
        # return is_turn()

    pass





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

    game = Game_State([Opponent("luc1"), Opponent("luc2")], "Player stacks: #1 luc1 (1000) | #2 luc2 (1000)")
    # game.print()
    game.new_hand([Opponent("luc1"), Opponent("luc2")], 1000, 20, [Card('2', 'spades'), Card('7', 'hearts')], 0, Deck(), -1)
    
    update_opponents_and_stacks(game, {'luc1': 960, 'luc2': 1040})

    game.print()

