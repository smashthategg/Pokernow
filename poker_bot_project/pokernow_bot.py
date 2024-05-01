from actions import *
from log import *
from game_state import Game_State
from strategy import *
import time


# LOGIN + GO TO GAME
chromedriver_path = r"((((PATH FILE HERE))))\Pokernow\poker_bot_project\pokernow_actions\chromedriver.exe"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

discord_login(driver, "email", "password")

# crib_go_to_game(driver, "pokertest0915@gmail.com", "Pokernowbot")
# register_for_game(driver) # remove if already a game in progress
# go_to_game2(driver)

time.sleep(8)
driver.get(r"(LINK HERE)")
time.sleep(8)

game = Game_State("smashthategg")
# TO BE LOOPED: 
while True:
    time.sleep(1)
    if check_turn(driver): # if its our turn
        print("----------BOT's TURN---------")
        new_log = read_log(driver) # read log
        new_entries = game.read_updates(new_log) # read updates
        print("----------NEW ENTRIES--------")
        print(new_entries)
        if is_new_hand(new_entries): # check if new hand
            print("--------(NEW HAND)--------")
            # gets needed values
            player_stacks = get_opponents_and_stacks(new_entries)
            if game.opponents == []:
                game.initial_get_opponents_and_stacks(player_stacks)
            deadsb = game.read_blinds(new_entries)
            cards_list = get_cards(driver)

            # resets everything
            game.new_hand(player_stacks, cards_list)
        
        pot = read_pot(driver)
        board = get_board(new_entries)
        game.update_board(board)
        position = game.get_bot_position(deadsb)
        players_actions = get_player_actions(new_entries)
        print("Player actions: " + str(players_actions))
        game.update_player_actions(players_actions)
        players_in_hand = game.opponents_in_hand

        
        print("Pot: {}".format(pot))
        print("Board: " + str(game.board))
        print("Hand: " + str(game.cards))
        print("Stack: " + str(game.stack))
        print("BB Size: " + str(game.big_blind))
        print("Position: " + str(position))
        print("Opponents acted: " + str(game.opponents_acted))
        print("Opponents in hand: " + str(game.opponents_in_hand))
        



        # get action
        if game.board == []:
            print("---------USING PREFLOP STRATEGY-------")
            bet = get_preflop_strategy(game.cards, game.stack, game.big_blind, position, game.opponents_acted, players_in_hand)
        else:
            print("--------CALCULATING POSTFLOP STRATEGY---------")
            bet = get_postflop_strategy(game.cards, game.stack, players_in_hand, pot, game.board)
        print("Chosen Bet Size: {}".format(bet))
        if bet == -1:
            fold(driver)
        elif bet == 0:
            check(driver)
        else:
            raise_func(driver, str(bet))

    else:
        print("not bot's turn")

