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
    #create an empty dictionary for all the data
    df = {}
    for players in dict:
        VPIP = sum(map(lambda x: x != 'X' and x != 'F', dict[players]['preflop']))/ len(dict[players]['preflop'])
        SD = sum(dict[players]['showdown'])/len(dict[players]['showdown'])
        WSD = 0
        WTSD = 0
        for i in range(0, len(dict[players]['stack']) - 2):
            if dict[players]['showdown'][i]:
                WSD += (dict[players]['stack'][i+1] - dict[players]['stack'][i])
            else:
                WTSD += (dict[players]['stack'][i+1] - dict[players]['stack'][i]) 
        df.update({players: ['VPIP: ' + str(VPIP), 'SD: ' + str(SD), 
                             'WSD: ' + str(WSD), 'WTSD: ' + str(WTSD)]})
    
    return df
# VPIP: Voluntarily put into pot        
# SD: % went to showdown
# WSD: total won/lost at showdown
# WTSD: total won/lost without showdown

df = calculate_stats(dict)
print(df.get('smashthategg'))