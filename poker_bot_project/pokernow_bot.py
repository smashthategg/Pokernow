from actions import *
from log import *
from game_state import Game_State
from bot import get_preflop_strategy
import time


# LOGIN + GO TO GAME
chromedriver_path = r"C:\Users\jzlin\OneDrive\Documents\Pokernow\poker_bot_project\pokernow_actions\chromedriver.exe"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

discord_login(driver, "johnnylin310@gmail.com", "johnnysucks123")

# crib_go_to_game(driver, "pokertest0915@gmail.com", "Pokernowbot")
# register_for_game(driver) # remove if already a game in progress
# go_to_game2(driver)

time.sleep(10)
driver.get(r"https://www.pokernow.club/games/pglcZfUcL3t_1GejQ2g1kkKrv")
time.sleep(10)



# INITIALIZE GAME STATE: 
log = read_log(driver)

player_stacks = get_opponents_and_stacks(log)
player_list = []
for player in player_stacks:
    player_list.append(player)

print("player stacks")
print(player_stacks)
print("player list")
print(player_list)

game = Game_State("smashthategg", player_list, [Opponent('P1')], log)
# game.print()
game.initial_get_opponents_and_stacks(player_stacks)



# TO BE LOOPED: 
while True:
    time.sleep(4)
    if check_turn(driver): # if its our turn
        print("bot's turn")
        new_log = read_log(driver) # read log
        if game.check_updated(new_log): # check log updated
            print("updated")
            new_entries = game.read_updates(new_log) # read updates
            print("new entries")
            print(new_entries)
            pot = read_pot(driver)
            print("pot:")
            print(pot)
            if is_new_hand(new_entries): # check if new hand
                print("new hand")
                print(new_entries)
                # gets needed values
                player_stacks = get_opponents_and_stacks(new_entries)
                game.update_opponents_and_stacks(player_stacks)
                big_blind_info = game.read_blinds(new_entries)
                cards_list = get_cards(driver)
                player_actions = get_player_actions(new_entries)
                print(player_actions)
                game.update_player_actions(get_player_actions(new_entries))

                # for informative purposes
                print(player_stacks)
                print(big_blind_info)
                print(cards_list)

                # resets everything
                game.new_hand(player_stacks, big_blind_info, cards_list)
            else:
                print("not new hand")

        else:
            print("same turn")
        
        hand = game.cards
        stack = game.stack
        bbsize = game.big_blind
        position = game.get_bot_position()
        players_acted = game.opponents_acted
        players_in_hand = game.opponents_in_hand
        
        print(hand)
        print(stack)
        print(bbsize)
        print(position)
        
        

        # get action
        bet = get_preflop_strategy(hand, stack, bbsize, position, players_acted, players_in_hand)
        if bet == -1:
            fold(driver)
        elif bet == 0:
            check(driver)
        else:
            raise_func(driver, bet)
    else:
        print("not bot's turn")


'''
# TO BE LOOPED: 
while True:
    new_log = read_log(driver)
    # print(new_log)
    if game.check_updated(new_log):
        print("updated")
        time.sleep(1)
        new_log = read_log(driver)
        new_entries = game.read_updates(new_log)
        # PROBLEMS WITH READ_UPDATES (LEAVES OUT PARTS SOMETIMES)
        print("new entries")
        print(new_entries)
        # print(is_new_hand(new_entries))
        if is_new_hand(new_entries):
            print("new hand")
            player_stacks = get_opponents_and_stacks(new_entries)
            big_blind_info = read_blinds(new_entries)
            # PROBLEMS WITH READ_BLINDS (FAILS TO READ SOMETIMES)
            cards_list = get_cards(driver)

            print(player_stacks)
            print(big_blind_info)
            print(cards_list)
            game.new_hand(player_stacks, big_blind_info, cards_list)
            # game.print()
        else:
            print("not new hand")
        
        


        if game.check_turn():
            print("bot's turn")
            hand = game.cards
            stack = game.stack
            bbsize = game.big_blind
            position = game.get_bot_position()
            players_acted = game.opponents_acted
            players_to_act = game.opponents_to_act


            # get action
            bet = get_preflop_strategy(hand, stack, bbsize, position, players_acted, players_to_act)
            if bet == -1:
                fold(driver)
            elif bet == 0:
                check(driver)
            else:
                raise_func(driver, bet)

            


    else:
        print("not updated")
'''


