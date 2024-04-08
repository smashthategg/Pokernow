import os
from reader import Reader

'''
                    !!! IMPORTANT NOTES !!!
    If a csv file is downloaded from a game played by someone else,
    it must be edited at the bottom to include that player's exact username.
    This will change the "you" player to them, which is necessary because
    otherwise the program will not function properly :)

    Also, hands played without the "you" player 
    (after they go broke) will not be recorded.
 '''

r = Reader("smashthategg") 

for fileName in os.listdir('./game_logs'): 
    r.set_csv(fileName)
    r.csv_to_txt()
    r.csv_to_data()

print(r.get_player_df('cpncandy'))

