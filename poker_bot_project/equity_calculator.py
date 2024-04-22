from card import Card
from player import Player
from deck import Deck
from collections import Counter
from itertools import combinations
from math import comb
import array 

def calculate_equity(hero_hand, opp_hands, board): 
    rankings = ['High Card','Pair','Two Pair','Three of a Kind','Straight','Flush','Full House','Four of a Kind','Straight Flush','Royal Flush']
    if len(board) == 5:
        num_winners = 1
        hero = find_best_combo(board + hero_hand)
        for opp_hand in opp_hands:
            opp = find_best_combo(board + opp_hand)
            if rankings.index(hero[0]) < rankings.index(opp[0]):
                return 0
            if rankings.index(hero[0]) == rankings.index(opp[0]):
                if hero[1] < opp[1]:
                    return 0
                equal = True
                for i in range(5):
                    if not hero[1][i].equal_in_value(opp[1][i]):
                        equal = False
                        break
                num_winners += equal
        return 1/num_winners
    else:
        deck = Deck() 
        for card in hero_hand:
            deck.remove(card)
        for hand in opp_hands:
            for card in hand:
                deck.remove(card)
        for card in board:
            deck.remove(card)
        outcomes = []
        for runout in combinations(deck.cards, 5-len(board)):
            outcomes.append(calculate_equity(hero_hand,opp_hands,board + list(runout)))
        return round(sum(outcomes)/comb(len(deck.cards),5-len(board)),2)
        


    
         
# takes in a list of 7 cards, determines best 5-card combination
# returns a tuple (String *type of hand*, List of cards *best combo*)
def find_best_combo(cards): 
    cards.sort(reverse = True)
    
    straight_combo = find_straight(cards) # either a 5-card straight or None
    flush_combo = find_flush(cards) # either a 5/6/7-card flush or None

    if straight_combo and flush_combo:
        straight_flush_combo = find_straight(flush_combo)
        if straight_flush_combo:
            if straight_flush_combo[0].value == 'A':
                return ('Royal Flush', straight_flush_combo)
            else:
                return ('Straight Flush', straight_flush_combo)
    
    # sorts the combo into quads/full house/trips/2pair/pair/high card (more duplicate values get sorted to start of list)
    counts = Counter(card.num for card in cards) 
    repeat_combo = sorted(cards, key = lambda x: -counts[x.num])[:5]
    # count the duplicates to tell us what type of hand we are working with
    val_count = list(counts.values())
    val_count.sort(reverse = True)

    if val_count[0] == 4:
        return ('Four of a Kind', repeat_combo)
    elif val_count[0] == 3 and val_count[1] == 2:
        return ('Full House', repeat_combo)
    elif flush_combo:
        return ('Flush', flush_combo[:5])
    elif straight_combo:
        return ('Straight', straight_combo)
    elif val_count[0] == 3:
        return ('Three of a Kind', repeat_combo)
    elif val_count[0] == 2 and val_count[1] == 2:
        return ('Two Pair', repeat_combo)
    elif val_count[0] == 2:
        return ('Pair', repeat_combo)
    else:
        return ('High Card', repeat_combo)

def find_straight(cards):
    # first, let's get rid of duplicate value cards (but append another ace card if it exists for the low straights)
    unique_cards = [cards[0]]
    for i in range(1,len(cards)):
        if cards[i] != cards[i-1]:
            unique_cards.append(cards[i])
    if unique_cards[0].value == 'A':
        unique_cards.append(cards[0])
    # now look for 5 in a row
    if len(unique_cards) >= 5:
        i = 0
        while i < len(unique_cards) - 4:
            straight = True
            for j in range(i, i+4):
                if unique_cards[j].num - unique_cards[j+1].num not in [1,-12]: # -12 checks for 2, A (where Ace has value 14).
                    straight = False
                    break
            if straight:
                return unique_cards[i:i+5]
            i += 1
    return None

def find_flush(cards):
    # count the suits
    suit_count = {}
    for card in cards:
        if card.suit in suit_count:
            suit_count[card.suit] += 1
        else:
            suit_count[card.suit] = 1
    max_suit = max(suit_count, key = suit_count.get)
    max_count = suit_count[max_suit]

    # if flush
    if max_count >= 5:
        flush_combo = []
        for card in cards:
            if card.suit == max_suit:
                flush_combo.append(card)
        return flush_combo
    else:
        return None
    
def classify_hand(cards): 
    hand_type = find_best_combo(cards)[0]
    if hand_type == 'High Card':
        strdraw = find_straight_draw(cards)
        flshdraw = find_flush_draw(cards)
        if strdraw and flshdraw:
            return strdraw + " + " + flshdraw
        if strdraw:
            return strdraw
        if flshdraw:
            return flshdraw
    return hand_type 
  
def find_straight_draw(cards):
    # first, let's get rid of duplicate value cards (but append another ace card if it exists for the low straights)
    unique_cards = [cards[0]]
    for i in range(1,len(cards)):
        if cards[i] != cards[i-1]:
            unique_cards.append(cards[i])
    if unique_cards[0].value == 'A':
        unique_cards.append(cards[0])
    # now look for 5 in a row
    if len(unique_cards) >= 4:
        i = 0
        while i < len(unique_cards) - 4:
            gutshot = 0
            straight_draw = True
            for j in range(i, i+3):
                if unique_cards[j].num - unique_cards[j+1].num not in [1,-12]: # -12 checks for 2, A (where Ace has value 14).
                    if unique_cards[j].num - unique_cards[j+1].num == 2:
                        gutshot += 1
                        straight_draw = False
                    else:
                        straight_draw = False
                        gutshot = False
                        break
                    if gutshot > 1:
                        gutshot = False
                        break
            if straight_draw:
                return "Open-Ended Straight Draw"
            if gutshot:
                return "Gutshot Straight Draw"
            i += 1
    return None

def find_flush_draw(cards):
 # count the suits
    suit_count = {}
    for card in cards:
        if card.suit in suit_count:
            suit_count[card.suit] += 1
        else:
            suit_count[card.suit] = 1
    max_suit = max(suit_count, key = suit_count.get)
    max_count = suit_count[max_suit]

    # if flush
    if max_count == 3:
        return "Backdoor Flush Draw"
    if max_count == 4: 
        return "Flush Draw"
    return None

