import os
import re
import io
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
class Reader():
    # Assign "global" variables
    def __init__(self, you = "smashthategg"):
        self.players_in_hand = []
        self.bb = 0
        self.you = you
        self.curr_player = ""
        self.csv = ""
        self.fileName = ""
        self.log = [] 
        self.hand_id = 0
        self.players = {} # Will be the single storage of all csv data, a massive dictionary with key-value pairs string and another dictionary
        '''
        { 
            name : {
                    'hand_id' : []     list of integers
                    'stack' : []             ^^^
                    'stackinbbs' : []  list of floats rounded to 1/10.
                    'blinds' : []       list of ordered pair of integers (sb, bb)
                    'hand' : []        list of strings either the player's hand or 'none' if it was never revealed
                    'position': []     list of strings taken from the list 'positions'

                                    'preflop': [] # list of strings 
                                    'flop': []             ^
                                    'turn': []             ^
                                    'river': []            ^
     
                    'net' : []          list of floats rounded to 1/10
                    'showdown': []        list of booleans
                    }
        }
        '''
    
    # Assign the csv to be parsed, also reset the stored log in memory
    def set_csv(self, fileName):
        self.fileName = fileName
        self.csv = pd.read_csv('./game_logs/{}'.format(fileName))
        self.log = []

    # Converts csv to array of strings and readable text format. Used before main function
    def csv_to_txt(self):
        # Put each row entry into an self.logs
        for i in range(self.csv.shape[0]):
            self.log.append(self.csv.loc[i, 'entry'])

            # (Reformatting) Replace all instances of "username @xxxxxxxx" with "username"
            self.log[i] = re.sub(r'\s@.*?"','"', self.log[i])
            # Might as well replace every poker card '10' with 'T' 
            self.log[i] = re.sub(r'10(?=[♣♠♦♥])', 'T', self.log[i])

        self.log.append(self.csv.get('at').get(0)[0:10]) # Add the date at the top (may be useful)
        self.log = self.log[::-1] # Reverse the order of the array (to Oldest -> Newest entry)

        # Write the now readable log into files inside logs_viewer
        with io.open("./logs_viewer/{}".format(self.fileName), 'w', encoding='utf-8') as file:
            for line in self.log:
                file.write(line + "\n")

        # If the file is from a game played by someone else, the script needs to know that.
        if len(self.log[1]) < 20:
            self.you = self.log[1]

    # !!! THE MAIN FUNCTION !!! 
    def csv_to_data(self):
        # Now to iterate through the log line by line
        index = 0
        while index < len(self.log):
            positions = ['UTG','UTG+1','LJ','HJ','CO','BTN','SB','BB']
            # Skip filler lines
            while self.log[index][0] != 'P':
                index += 1

            self.players_in_hand = re.findall(r'"(.*?)"', self.log[index])
            stacks = re.findall(r'\((.*?)\)', self.log[index])
            for name in self.players_in_hand:
                if name not in self.players:
                    # Initialize the key-value pair in players if player has not been added yet.
                    self.players[name] = {
                                            'hand_id' : [],
                                            'hand': [],
                                            'stack': [],
                                            'stackinbbs': [],
                                            'blinds': [],
                                            'position': [],
                                            'preflop': [],
                                            'flop': [],
                                            'turn': [],
                                            'river': [],
                                            'net': [],
                                            'showdown': [],
                                            'board': []
                                         }
                # Record the player's current stack and hand_id
                self.players[name]['stack'].append(int(stacks[self.players_in_hand.index(name)]))
                self.players[name]['hand_id'].append(self.hand_id)
                
                # Initialize default values for player in this hand.
                self.players[name]['position'].append("BB")
                self.players[name]['hand'].append("NA")
                self.players[name]['preflop'].append("NA")
                self.players[name]['flop'].append("NA")
                self.players[name]['turn'].append("NA")
                self.players[name]['river'].append("NA")
                self.players[name]['net'].append(0)
                self.players[name]['showdown'].append(False)
                self.players[name]['board'].append("NA")

            index += 1
            
            # Record the "you" player's hand
            if self.log[index][0] == 'Y': 
                self.players[self.you]['hand'][-1] = self.log[index][13:]
                index += 1

            # Record the current blind level
            dead_sb = False
            if 'posts a big blind' in self.log[index]:
                self.bb = int(self.log[index].split()[-1])
                self.players[self.update_curr_player(self.log[index])]['net'][-1] -= 1
            else:
                if self.log[index] == 'Dead Small Blind':
                    positions.remove('SB')
                    dead_sb = True
                else:
                    self.players[self.update_curr_player(self.log[index])]['net'][-1] -= 0.5
                index += 1
                self.bb = int(self.log[index].split()[-1])
                
                self.players[self.update_curr_player(self.log[index])]['net'][-1] -= 1
            for name in self.players_in_hand:
                self.players[name]['blinds'].append((self.bb//2, self.bb))
            index += 1

            # Divide all stacks by bb size to get stacks in bbs.
            for name in self.players_in_hand:
                self.players[name]['stackinbbs'].append(round(self.players[name]['stack'][-1] / self.bb, 1))
            
            # Record each player's position
            if index + 7 < len(self.log):
                for i in range(8-len(self.players_in_hand),8):
                    self.players[self.update_curr_player(self.log[index])]['position'][-1] = positions[i-dead_sb]
                    self.record_action(self.log[index], 'preflop')
                    index += 1
                while index < len(self.log) and self.log[index][:4] not in ['Flop', '-- s']: # Until the flop/end of hand...
                    if self.log[index][0] in ['"', 'U']:
                        self.update_curr_player(self.log[index])
                        self.record_action(self.log[index], 'preflop')
                    index += 1
                if index < len(self.log) and self.log[index][:4] == 'Flop':
                    for name in self.players_in_hand:
                        self.players[name]['board'][-1] = self.log[index][6:]
                    index += 1
                    while index < len(self.log) and self.log[index][:4] not in ['Turn', '-- s']:
                        if self.log[index][0] in ['"', 'U']:
                            self.update_curr_player(self.log[index])
                            self.record_action(self.log[index], 'flop')
                        index += 1
                    if index < len(self.log) and self.log[index][:4] == 'Turn':
                        for name in self.players_in_hand:
                            self.players[name]['board'][-1] = "[" + re.sub(r'[\[\]]','',self.log[index][6:]) + "]"
                        index += 1
                        while index < len(self.log) and self.log[index][:4] not in ['Rive', '-- s']:
                            if self.log[index][0] in ['"', 'U']:
                                self.update_curr_player(self.log[index])
                                self.record_action(self.log[index], 'turn')
                            index += 1
                        if index < len(self.log) and self.log[index][:4] == 'Rive':
                            for name in self.players_in_hand:
                                self.players[name]['board'][-1] = "[" + re.sub(r'[\]\[]','',self.log[index][7:]) + "]"
                            index += 1
                            while index < len(self.log) and self.log[index][:4] != '-- s':
                                if self.log[index][0] in ['"', 'U']:
                                    self.update_curr_player(self.log[index])
                                    self.record_action(self.log[index], 'river')
                                index += 1
            if len(self.players_in_hand) > 1:
                for name in self.players_in_hand:
                    self.players[name]['showdown'][-1] = True
            # Skip over lines until reader arrives at next hand
            while index < len(self.log) and self.log[index][:4] != '-- s':
                index += 1

            self.hand_id += 1
        
        return



    ### HELPER FUNCTIONS FOR CSV_TO_DATA() ###
                
    def update_curr_player(self, line):
        self.curr_player = re.search(r'"(.*?)"', line).group(1)
        return self.curr_player

    def record_action(self, line, stage):
        nline = re.sub(r'"(.*?)" ', "", line).split()
        action = "NA"
        amount = 0
        match nline[0]:
            case 'folds':
                self.players_in_hand.remove(self.curr_player)
                action = 'F'
            case 'checks':
                action = 'X'
            case 'calls':
                amount = round(int(nline[1])/self.bb, 1)
                action = 'C'
            case 'raises':
                amount = round(int(nline[2])/self.bb, 1)
                action = 'R'
            case 'bets':
                amount = round(int(nline[1])/self.bb, 1)
                action = 'B'
            case 'Uncalled':
                amount = round(int(nline[3])/self.bb, 1)
            case 'shows':
                self.players[self.curr_player]['hand'][-1] = nline[-2] + " " + nline[-1][:-1]
            case 'collected':
                amount = round(int(nline[1])/self.bb, 1)
            case _:
                return
        if stage == 'preflop' and  self.players[self.curr_player][stage][-1] == 'NA': 
            if action in ['C','R'] and self.players[self.curr_player]['position'][-1] == 'SB':
                self.players[self.curr_player]['net'][-1] += 0.5
            if action in ['C','R'] and self.players[self.curr_player]['position'][-1] == 'BB':
                self.players[self.curr_player]['net'][-1] += 1
        if action != 'NA': 
            if amount != 0: # If player called/bet/raised, we want to include the amount.
                action += str(amount)
            if self.players[self.curr_player][stage][-1] == 'NA': # If this is the player's first action in the stage
                self.players[self.curr_player][stage][-1] = action
            else:
                self.players[self.curr_player][stage][-1] += "-" + action
            # Now we change the "net" values.
            if amount < 0: # If the player c/b/r
                for past_action in self.players[self.curr_player][stage][-1].split('-'):
                    if past_action[0] in ['B','C','R']: # We dont also want to deduct past bets in the same stage.
                        self.players[self.curr_player]['net'][-1] += float(past_action[1:])
            self.players[self.curr_player]['net'][-1] -= amount
        else:
            self.players[self.curr_player]['net'][-1] += amount

        return
    
    pd.set_option('display.max_rows', 500)
    # Test Function
    def print_player_as_df(self, name):
        df = pd.DataFrame(self.players[name])
        df.index.name = name
        print(df)

    def get_player_df(self, name):
        df = pd.DataFrame(self.players[name])
        return df
    
    def print_all_players_as_df(self):
        for name in self.players.keys():
            df = pd.DataFrame(self.players[name])
            df.index.name = name
            print(df)


    
    