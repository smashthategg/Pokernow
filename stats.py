from reader import Reader
import os
import json
player_stats_dic = []
r = Reader("smashthategg") 
for fileName in os.listdir('./game_logs'): 
    r.set_csv(fileName)
    r.csv_to_txt()
    r.csv_to_data()

dict = r.players
def calculate_stats(dict):
    # create an empty dictionary for all the data
    df = {}
    for players in dict:
        VPIP = sum(map(lambda x: x != 'X' and x != 'F', dict[players]['preflop'])) / len(dict[players]['preflop'])
        # VPIP: Using map function to remove checks and folds
        SD = sum(dict[players]['showdown'])/len(dict[players]['showdown'])
        # showdown true / all games
        WSD = 0
        WTSD = 0
        numhands = len(dict[players]['stack']) 
        for i in range(0, len(dict[players]['stack']) - 2):
            if dict[players]['showdown'][i]:
                WSD += (dict[players]['stack'][i+1] - dict[players]['stack'][i])
                # gains 
            else:
                WTSD += (dict[players]['stack'][i+1] - dict[players]['stack'][i])
        last = int(dict[players]['net'][-1] * dict[players]['blinds'][-1][1])
        if dict[players]['showdown'][-1]:
            WSD += last
        else:
            WTSD += last
        type = 'rec'
        if (WSD > WTSD and WSD > 0 or VPIP < 0.3) and numhands > 50:
            type = 'reg'
        df.update({players: {'VPIP': VPIP, 'SD': SD, 
                             'WSD': WSD, 'WTSD': WTSD,
                             'numhands': numhands, 'type': type}})
    
    return df
# VPIP: Voluntarily put into pot        
# SD: % went to showdown
# WSD: total won/lost at showdown
# WTSD: total won/lost without showdown


df = calculate_stats(dict)
# print(df.get('smashthategg')) # use this format to get a specific player
stats = json.dumps(df, indent = 4) # use this format to get ALL players

with open('stats', 'w') as player_stats:
    json.dump(df, player_stats)



# TESTING
totalWSD =0
count =0
for player in df:
    if df[player]['type'] == 'reg':
        print(player)
        print(df[player])
        count += 1
        totalWSD += df[player]['WSD']
print(totalWSD/count)
    


print(df['Shawnkemp40'])