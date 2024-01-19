import os
import re
import pandas as pd

# Iterate through each pokernow.club csv file in game_logs
def csv_to_df(player):

    games = [] # Will compile the data frames from each file into this list before concatenating them all
    parsed_files_file = open("./parsed_files.txt", "w")
    parsed_files = [] # Will also store the filenames so we know which ones have already been parsed

    for fileName in os.listdir('./game_logs'): 
        logs = pd.read_csv('./game_logs/{}'.format(fileName))
        parsed_files.append('{}\n'.format(fileName))
        
        # Put each row entry into an array
        entries = []
        for i in range(logs.shape[0]):
            entries.append(logs.loc[i, 'entry'])

            # (Reformatting) Replace all instances of "username @xxxxxxxx" with "username"
            entries[i] = re.sub(r'\s@.*?"','"',entries[i])

        entries = entries[::-1] # Reverse the order of the array (to Oldest -> Newest entry)

        # Lists to store various data
        btn_players = []
        players = []
        mystacksbb = []
        mystacks = []
        stacks = []
        bbs = []
        hands = []
        blinds = []
        
        # Keep track of target player, only read hands with player in table.
        playerQuit = False
        my_player_index = 0
        index = 0
        stacks_index = 0

        # Now to iterate through the log line by line
        while index < len(entries) and not playerQuit:

            # First line will always be "Starting hand ... Button is (some_player)" (may not be necessary to record)
            btn_player = re.search(r'\(de.*?"', entries[index])
            if btn_player:
                btn_players.append(btn_player.group()[11:-1])
            else:
                btn_players.append('*dead button*')
            index += 1

            # Skip occasional filler lines
            while entries[index][0] != 'P':
                index += 1

            # Record all current players and stacks in table
            players.append(re.findall(r'"(.*?)"', entries[index]))
            stacks.append(re.findall(r'\((.*?)\)', entries[index]))
            stacks[stacks_index] = list(map(int, stacks[stacks_index]))

            # Get target player-specific info (hand and position)
            my_player_index = players[stacks_index].index(player)
            index += 1
            hands.append(entries[index][13:])
            index += 1

            # Record the current blind level
            if 'posts a big blind' in entries[index]:
                blinds.append(int(entries[index].split()[-1]))
            else:
                index += 1
                blinds.append(int(entries[index].split()[-1]))

            # Divide all stacks by bb size to get stacks in bbs. Also record target player's stack
            bbs.append([round(x / blinds[stacks_index], 1) for x in stacks[stacks_index]])
            mystacks.append(stacks[stacks_index][my_player_index])
            mystacksbb.append(bbs[stacks_index][my_player_index])
            stacks_index += 1
            
            # Skip over lines until reader arrives at next hand. Also quits reading if target player is no longer in game.
            while index < len(entries) and entries[index][:4] != '-- s':
                if 'The player "{}" quits'.format(player) in entries[index]:
                    playerQuit = True
                    break
                index += 1

        # Create data frame for current file
        data =  {
                    'Hands': hands,
                    'My Stack Size': mystacks,
                    'My Stack Size (BBs)': mystacksbb,
                    'Players': players,
                    'Stacks (BBs)': bbs
                }
    
    
    parsed_files_file.writelines(parsed_files)
    parsed_files_file.close()
    games.append(pd.DataFrame(data))
    return(pd.concat(games))






