import os
import re
import pandas as pd

'''
                    !!! IMPORTANT NOTES !!!
    If a csv file is downloaded from a game played by someone else,
    it must be edited at the bottom to include that player's exact username.
    This will change the "you" player to them, which is necessary because
    otherwise the program will not function properly :)

    Also, hands played without the "you" player 
    (after they go broke) will not be recorded.
 '''

# Iterate through each pokernow.club csv file in game_logs
def csv_to_df():

    # !!! IMPORTANT !!! This is the "you" player by default. CSV files from this player need not be edited
    you = "smashthategg" 

    hand_id = 0
    positions = ['UTG','UTG+1','LJ','HJ','CO','BTN','SB','BB']
    players = {} 
    # Will be the single storage of all csv data, a massive dictionary with key-value pairs string and another dictionary
    '''
    { 
        name : {
                'hand_ids' : []     list of integers
                'stacks' : []             ^^^
                'stacksinbbs' : []        ^^^
                'blinds' : []       list of ordered pair of integers (sb, bb)
                'hands' : []        list of strings either the player's hand or 'none' if it was never revealed
                'positions': []     list of strings taken from the list 'positions'
                'action' : []       list of strings
               }
    }
    '''

    for fileName in os.listdir('./game_logs'): 
        logs = pd.read_csv('./game_logs/{}'.format(fileName))
        
        # Put each row entry into an array
        entries = []
        for i in range(logs.shape[0]):
            entries.append(logs.loc[i, 'entry'])

            # (Reformatting) Replace all instances of "username @xxxxxxxx" with "username"
            entries[i] = re.sub(r'\s@.*?"','"',entries[i])

        entries = entries[::-1] # Reverse the order of the array (to Oldest -> Newest entry)

        # If the file is from a game played by someone else, the script needs to know that.
        if len(entries[0]) < 20:
            you = entries[0]

        # Now to iterate through the log line by line
        index = 0
        while index < len(entries):

            # First line will always be "Starting hand ... Button is (some_player)" (may not be necessary to record)
            '''
            btn_player = re.search(r'\(de.*?"', entries[index])
            if btn_player:
                btn_players.append(btn_player.group()[11:-1])
            else:
                btn_players.append('*dead button*')
            index += 1
            '''

            # Skip filler lines
            while entries[index][0] != 'P':
                index += 1

            players_in_hand = re.findall(r'"(.*?)"', entries[index])
            if you not in players_in_hand:
                break
            stacks = re.findall(r'\((.*?)\)', entries[index])
            for name in players_in_hand:
                if name not in players:
                    # Initialize the key-value pair in players if player has not been added yet.
                    players[name] = {
                                     'hand_ids' : [],
                                     'hands': [],
                                     'stacks': [],
                                     'stacksinbbs': [],
                                     'blinds': [],
                                     'positions': [],
                                     'action': []
                                    }
                # Record the player's current stack and hand_id
                players[name]['stacks'].append(int(stacks[players_in_hand.index(name)]))
                players[name]['hand_ids'].append(hand_id)
            index += 1
            
            # Record the "you" player's hand
            players[you]['hands'].append(entries[index][13:])
            index += 1

            # Record the current blind level
            if 'posts a big blind' in entries[index]:
                bb = int(entries[index].split()[-1])
            else:
                index += 1
                bb = int(entries[index].split()[-1])
            for name in players_in_hand:
                players[name]['blinds'].append((bb//2, bb))
            index += 1

            # Divide all stacks by bb size to get stacks in bbs.
            for name in players_in_hand:
                players[name]['stacksinbbs'].append(round(players[name]['stacks'][-1] / bb, 1))
            
            # Record each player's position
            if index + 7 < len(entries):
                for i in range(8-len(players_in_hand),8):
                    curr_player = re.search(r'"(.*?)"', entries[index]).group(1)
                    print(entries[index])
                    players[curr_player]['positions'].append(positions[i])
                    index += 1

            # Skip over lines until reader arrives at next hand. Also quits reading if target player is no longer in game.
            while index < len(entries) and entries[index][:4] != '-- s':
                index += 1

            hand_id += 1

    print(players[you]['positions'])