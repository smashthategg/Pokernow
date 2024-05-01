from actions import *
from log import *
from game_state import Game_State
from bot import get_preflop_strategy, get_postflop_strategy
import time
import datetime




def initialize_game(driver, bot_name):
    print("INITIALIZING GAME STATE: ")
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
    game.initial_get_opponents_and_stacks(player_stacks)
    print("--------------------- GAME STATE INITIALIZED ---------------------")
    return game




def decide_preflop_action(driver, game):
    position = game.get_bot_position()
    print("GETTING PREFLOP STRATEGY: ")

    bet = get_preflop_strategy(hand=game.cards, stack=game.stack, bbsize=game.big_blind, 
                         position=position, players_acted=game.opponents_acted, 
                         players_in_hand=game.opponents_in_hand)
    if bet <= 0:
        print("CHECK / FOLD")
    else:
        print(f"RAISE TO {bet}")




def decide_postflop_action(driver, game):
    print("GETTING POSTFLOP STRATEGY: ")
    bet = get_postflop_strategy(hand=game.cards, stack=game.stack, players_in_hand=game.opponents_in_hand, 
                                pot=game.pot, board=game.board) # PROBLEM
    if bet <= 0:
        print("CHECK / FOLD")
    else:
        print(f"RAISE TO {bet}")





def play(driver, game):
    while True:
        time.sleep(4)
        now = datetime.datetime.now()
        print(f"{now} CHECKING TURN: ")
        if check_turn(driver): # if its our turn
            print("bot's turn")
            game.reset_turn() # reseting opponent lists
            new_log = read_log(driver) # read log
            if game.check_updated(new_log): # check log updated
                print("LOG UPDATED: ")
                new_entries = game.read_updates(new_log) # read updates
                # print("new entries")
                # print(new_entries)
                game.process_log_lines(new_entries) # process updates

                pot = read_pot(driver) # FOR POT
                print("POT:")
                game.pot = pot
                print(game.pot)

                print("BOARD: ") # FOR BOARD
                game.update_board(get_board(new_entries))
                print(game.board)

                if is_new_hand(new_entries): # check if new hand
                    print("--------------------- NEW HAND ---------------------")
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

                    # STRATEGY:
                    decide_preflop_action(driver, game)

                else:
                    print("not new hand")
                    if game.board != []: # if preflop
                        # STRATEGY:
                        decide_postflop_action(driver, game)
                    else: 
                        decide_preflop_action(driver, game)

            else:
                print("same turn")
        else:
            print("not bot's turn")




if __name__ == "__main__":

    # LOGIN + GO TO GAME
    chromedriver_path = r"C:\Users\uclam\Downloads\python_workspaces\pokernow\Pokernow\poker_bot_project\pokernow_actions\chromedriver.exe"
    # REPLACE WITH PATH TO CHROMEDRIVER
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)

    discord_login(driver, "pokertest0915@gmail.com", "Pokernowbot")
    # REPLACE WITH DISCORD LOGIN

    time.sleep(10)
    driver.get(r"https://www.pokernow.club/games/pgl2DU_IERjgn3gojbVHVo387")
    # NEEDS TO BE A LINK TO IN PROGRESS PRIVATE GAME, WITH THE BOT'S ACCOUNT ALREADY JOINED
    # AFTER ENTERING THE LINK YOU MUST MANUALLY GO TO SETTINGS AND DISABLE POST GAME REVIEW NOTIFICATION

    time.sleep(10)

    # FUNCTION
    game = initialize_game(driver, "luc")


    # FUNCTION 2
    play(driver, game)



