# range.py aims to construct a list of all the default poker hands ordered by profitability.
# Hands in parantheses are "suited"
# Order provided by ProPokerTools.com

from card import Card

# def build_range(percent): returns the first *percent* x 1326 elements of the list. the best X% of default hands.
def build_range(percent = 1): 

    output = []

    simplified_range = ["AA","KK","QQ","JJ","TT","(AK)","AK","(AQ)",
                    "99","(AJ)","AQ","88","(AT)","AJ","(KQ)","77",
                    "(KJ)","AT","KQ","(A9)","(KT)","66","(A8)","(QJ)",
                    "(A7)","KJ","(QT)","(A5)","A9","(A6)","(JT)","55",
                    "(K9)","(A4)","KT","(A3)","A8","QJ","(Q9)","(A2)",
                    "(K8)","(J9)","44","(K7)","(T9)","QT","A7","(K6)",
                    "A5","JT","(Q8)","K9","A6","(K5)","(J8)","(T8)",
                    "A4","33","(98)","(K4)","A3","(Q7)","(Q6)","Q9",
                    "(K3)","(K2)","A2","(J7)","K8","J9","(T7)","(87)",
                    "T9","(Q5)","(97)","K7","22","(Q4)","K6","(J6)",
                    "Q8","(86)","(76)","(T6)","(Q3)","K5","(96)","J8",
                    "(J5)","T8","(Q2)","98","K4","(65)","(J4)","Q7",
                    "(75)","Q6","(J3)","K3","J7","(95)","(85)","(T5)",
                    "T7","K2","87","(54)","(J2)","97","Q5","(T4)",
                    "(64)","(T3)","(74)","Q4","76","J6","(84)","(T2)",
                    "(94)","T6","(53)","Q3","86","J5","(93)","96",
                    "Q2","(63)","(92)","65","(43)","J4","(73)","75",
                    "(83)","(52)","J3","85","T5","(82)","95","54",
                    "J2","(42)","T4","(62)","64","(72)","(32)","T3",
                    "74","84","T2","53","94","93","43","63","92","73",
                    "83","52","82","42","62","72","32"]


    suits = ["clubs","diamonds","hearts","spades"]
    for hand in simplified_range:
        if len(output) > percent * 1326:
            break
        else:
            if hand[0] == "(": # if hand is suited (4 combos)
                for suit in suits:
                    output.append((Card(hand[1], suit), Card(hand[2], suit)))
            elif hand[0] == hand[1]: # if hand is a pocket pair (6 combos)
                for i in range(0,4):
                    for j in range(i+1,4):
                        output.append((Card(hand[0], suits[i]), Card(hand[1], suits[j])))
            else: # if hand is offsuit (12 combos)
                for i in range(0,4): 
                    for j in range(i+1,4):
                        output.append((Card(hand[0], suits[i]), Card(hand[1], suits[j])))
                        output.append((Card(hand[0], suits[j]), Card(hand[1], suits[i])))
    while len(output) > percent * 1326: # clears out extra hands
        output.pop()
    return output

