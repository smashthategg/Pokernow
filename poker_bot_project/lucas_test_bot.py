from actions import *
from log import *
from game_state import Game_State
from bot import get_preflop_strategy
import time


# LOGIN + GO TO GAME
chromedriver_path = r"C:\Users\uclam\Downloads\python_workspaces\pokernow\Pokernow\poker_bot_project\pokernow_actions\chromedriver.exe"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

discord_login(driver, "pokertest0915@gmail.com", "Pokernowbot")

# crib_go_to_game(driver, "pokertest0915@gmail.com", "Pokernowbot")
# register_for_game(driver) # remove if already a game in progress
# go_to_game2(driver)

time.sleep(10)
driver.get(r"https://www.pokernow.club/games/pgl2DU_IERjgn3gojbVHVo387")
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

game = Game_State("luc", player_list, [], log)
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

                # gets needed values
                player_stacks = get_opponents_and_stacks(new_entries)
                big_blind_info = game.read_blinds(new_entries)
                cards_list = get_cards(driver)

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
    else:
        print("not bot's turn")


