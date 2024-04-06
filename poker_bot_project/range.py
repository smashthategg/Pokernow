# range.py aims to construct a list of all the default poker hands ordered by profitability.
# Hands in parantheses are "suited"
# Order provided by ProPokerTools.com

from card import Card
import numpy as np

''' ------------- DOCUMENTATION ------------------

# def __init__(self, percent = 1)  
#   percent: the top % of default poker hands to be included in the range.

# def build_range(percent) 
#   is only used for the __init__

# def visualize_range()
#   prints out the range in readable format like below
#   no real purpose other than for human testing.

#   it is not actually perfectly readable because of line width restrictions. you will need to add the lines:
#
#   1.   import numpy as np
#   2.   np.set_printoptions(linewidth=100)


#   example range (best 12% of hands):
    [
    ['AA' 'AKs' 'AQs' 'AJs' 'ATs' 'A9s' 'A8s' 'A7s' '   ' '   ' '   ' '   ' '   ']
    ['AKo' 'KK' 'KQs' 'KJs' 'KTs' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ']
    ['AQo' 'KQo' 'QQ' 'QJs' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ']
    ['AJo' 'KJo' '   ' 'JJ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ']
    ['ATo' '   ' '   ' '   ' 'TT' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ']
    ['   ' '   ' '   ' '   ' '   ' '99' '   ' '   ' '   ' '   ' '   ' '   ' '   ']
    ['   ' '   ' '   ' '   ' '   ' '   ' '88' '   ' '   ' '   ' '   ' '   ' '   ']
    ['   ' '   ' '   ' '   ' '   ' '   ' '   ' '77' '   ' '   ' '   ' '   ' '   ']
    ['   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '66' '   ' '   ' '   ' '   ']
    ['   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '  ' '   ' '   ' '   ']
    ['   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '  ' '   ' '   ']
    ['   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '  ' '   ']
    ['   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '   ' '  ']
    ]
 '''

class Range():
    def __init__(self, percent = 1): 
        self.simple_range = []
        self.range = self.build_range(percent)

    def build_range(self, percent): # returns the first *percent* x 1326 elements of the list. the best X% of default hands.

        output = []

        ordered_range = ["AA","KK","QQ","JJ","TT","AKs","AKo","AQs",
                        "99","AJs","AQo","88","ATs","AJo","KQs","77",
                        "KJs","ATo","KQo","A9s","KTs","66","A8s","QJs",
                        "A7s","KJo","QTs","A5s","A9o","A6s","JTs","55",
                        "K9s","A4s","KTo","A3s","A8o","QJo","Q9s","A2s",
                        "K8s","J9s","44","K7s","T9s","QTo","A7o","K6s",
                        "A5o","JTo","Q8s","K9o","A6o","K5s","J8s","T8s",
                        "A4o","33","98s","K4s","A3o","Q7s","Q6s","Q9o",
                        "K3s","K2s","A2o","J7s","K8o","J9o","T7s","87s",
                        "T9o","Q5s","97s","K7o","22","Q4s","K6o","J6s",
                        "Q8o","86s","76s","T6s","Q3s","K5o","96s","J8o",
                        "J5s","T8o","Q2s","98o","K4o","65s","J4s","Q7o",
                        "75s","Q6o","J3s","K3o","J7o","95s","85s","T5s",
                        "T7o","K2o","87o","54s","J2s","97o","Q5o","T4s",
                        "64s","T3s","74s","Q4o","76o","J6o","84s","T2s",
                        "94s","T6o","53s","Q3o","86o","J5o","93s","96o",
                        "Q2o","63s","92s","65o","43s","J4o","73s","75o",
                        "83s","52s","J3o","85o","T5o","82s","95o","54o",
                        "J2o","42s","T4o","62s","64o","72s","32s","T3o",
                        "74o","84o","T2o","53o","94o","93o","43o","63o","92o","73o",
                        "83o","52o","82o","42o","62o","72o","32o"]


        suits = ["clubs","diamonds","hearts","spades"]
        for hand in ordered_range:
            if len(output) > percent * 1326:
                break
            else:
                self.simple_range.append(hand)
                if len(hand) == 2: # if hand is a pocket pair (6 combos)
                    for i in range(0,4):
                        for j in range(i+1,4):
                            output.append([Card(hand[0], suits[i]), Card(hand[1], suits[j])])
                elif hand[2] == "s": # if hand is suited (4 combos)
                    for suit in suits:
                        output.append([Card(hand[0], suit), Card(hand[1], suit)])
                else: # if hand is offsuit (12 combos)
                    for i in range(0,4): 
                        for j in range(i+1,4):
                            output.append([Card(hand[0], suits[i]), Card(hand[1], suits[j])])
                            output.append([Card(hand[0], suits[j]), Card(hand[1], suits[i])])
        while len(output) > percent * 1326: # clears out extra hands
            output.pop()
        return output
    
    def visualize_range(self):
        visual = np.array([
        ['AA','AKs','AQs','AJs','ATs','A9s','A8s','A7s','A6s','A5s','A4s','A3s','A2s'],
        ['AKo','KK','KQs','KJs','KTs','K9s','K8s','K7s','K6s','K5s','K4s','K3s','K2s'],
        ['AQo','KQo','QQ','QJs','QTs','Q9s','Q8s','Q7s','Q6s','Q5s','Q4s','Q3s','Q2s'],
        ['AJo','KJo','QJo','JJ','JTs','J9s','J8s','J7s','J6s','J5s','J4s','J3s','J2s'],
        ['ATo','KTo','QTo','JTo','TT','T9s','T8s','T7s','T6s','T5s','T4s','T3s','T2s'],
        ['A9o','K9o','Q9o','J9o','T9o','99','98s','97s','96s','95s','94s','93s','92s'],
        ['A8o','K8o','Q8o','J8o','T8o','98o','88','87s','86s','85s','84s','83s','82s'],
        ['A7o','K7o','Q7o','J7o','T7o','97o','87o','77','76s','75s','74s','73s','72s'],
        ['A6o','K6o','Q6o','J6o','T6o','96o','86o','76o','66','65s','64s','63s','62s'],    
        ['A5o','K5o','Q5o','J5o','T5o','95o','85o','75o','65o','55','54s','53s','52s'],
        ['A4o','K4o','Q4o','J4o','T4o','94o','84o','74o','64o','54o','44','43s','42s'],
        ['A3o','K3o','Q3o','J3o','T3o','93o','83o','73o','63o','53o','43o','33','32s'],
        ['A2o','K2o','Q2o','J2o','T2o','92o','82o','72o','62o','52o','42o','32o','22'],
        ])
        for i in range(0,13):
            for j in range(0,13):
                if visual[i,j] not in self.simple_range:
                    visual[i,j] = ' ' * len(visual[i,j])
        print(visual)

