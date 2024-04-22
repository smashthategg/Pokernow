from actions import *
from log import *
from game_state import Game_State


# LOGIN + GO TO GAME
chromedriver_path = r"C:\Users\uclam\Downloads\python_workspaces\pokernow\Pokernow\poker_bot_project\pokernow_actions\chromedriver.exe"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

discord_login(driver, "pokertest0915@gmail.com", "Pokernowbot")

# crib_go_to_game(driver, "pokertest0915@gmail.com", "Pokernowbot")
# register_for_game(driver) # remove if already a game in progress
# go_to_game2(driver)

time.sleep(10)
driver.get(r"https://www.pokernow.club/games/pglb44qfiEGg_R2R7oM_0EBnS")
time.sleep(2)



# INITIALIZE GAME STATE: 
log = read_log(driver)

player_stacks = get_opponents_and_stacks(log)
player_list = []
for player in player_stacks:
    player_list.append(player)

print(player_stacks)
print(player_list)

game = Game_State("luc", player_list, [], log)
# game.print()
game.initial_get_opponents_and_stacks(player_stacks)



# TO BE LOOPED: 
player_stacks = get_opponents_and_stacks(log)
big_blind_info = read_blinds(log)
cards_list = get_cards(driver)

#print(big_blind_info)
#print(cards_list)
game.new_hand(player_stacks, big_blind_info, cards_list)
game.print()

