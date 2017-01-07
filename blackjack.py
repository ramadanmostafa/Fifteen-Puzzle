"""
it's a gambling game i built using python via codeskulptor.org.open the website,paste the code then click execute button
"""
# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.lst_hand=[]

    def __str__(self):
        s=[]
        for obj in self.lst_hand :
            s.append(str(obj))
        return str(s)

    def add_card(self, card):
        self.lst_hand.append(card)

    def get_value(self):
        # compute the value of the hand, see Blackjack video
        value=0
        has_ace=False
        for item in self.lst_hand:
            rank=item.get_rank()
            value+=VALUES[rank]
            if rank =='A':has_ace=True
                
        if has_ace and value+10 <= 21:
            value+=10
        return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        self.lst_hand[0].draw(canvas,pos)
        pos[0]+=100
        self.lst_hand[1].draw(canvas,pos)
        l=len(self.lst_hand)
        if l > 2 :
            pos[0]+=100
            self.lst_hand[2].draw(canvas,pos)
        if l > 3 :
            pos[0]+=100
            self.lst_hand[3].draw(canvas,pos)
        if l > 4 :
            pos[0]+=100
            self.lst_hand[4].draw(canvas,pos)
        

        
# define deck class 
class Deck:
    def __init__(self):
        self.lst_deck=[]
        for s in SUITS:
            for r in RANKS:
                tmp=Card(s,r)
                self.lst_deck.append(tmp)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.lst_deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.lst_deck.pop()
    
    def __str__(self):
        s=[]
        for obj in self.lst_deck :
            s.append(str(obj))
        return str(s)



#define event handlers for buttons
def deal():
    global outcome, in_play,deck_cards,hand_player,hand_dealer,score
    if in_play :
        print "You Pressed the Deal button in the middle of the round","You Lose"
        in_play=False
        score-=1
        outcome="You Lose, New Deal?"
    deck_cards=Deck()
    deck_cards.shuffle()
    hand_player=Hand()
    hand_dealer=Hand()
    hand_player.add_card(deck_cards.deal_card())
    hand_player.add_card(deck_cards.deal_card())
    hand_dealer.add_card(deck_cards.deal_card())    
    hand_dealer.add_card(deck_cards.deal_card())    
    print "Deck:",str(deck_cards)
    print "player:",str(hand_player),hand_player.get_value()
    print "dealer:",str(hand_dealer)
    outcome ="Hit Or Stand?"
    in_play = True

def hit():
    global in_play,outcome,score,hand_player,deck_cards
    if not in_play : return
    # if the hand is in play, hit the player
    if in_play and hand_player.get_value() <= 21:
        hand_player.add_card(deck_cards.deal_card())
        print "player hand",str(hand_player),hand_player.get_value()
    if hand_player.get_value() > 21 :
        print "You have busted"
        in_play=False
        score-=1
        outcome="Busted,You Lose,New Deal?"
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global in_play,hand_dealer,hand_player,outcome,score
    if not in_play : return
    val_p=hand_player.get_value()
    val_d=hand_dealer.get_value()
    if val_p > 21 : 
        print "you busted,lose"
        outcome="busted,You Lose,New Deal?"
        print "dealer:",val_d,"Player:",val_p
        in_play=False
        score-=1
        return
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while in_play and hand_dealer.get_value() < 17 :
        hand_dealer.add_card(deck_cards.deal_card())
    # assign a message to outcome, update in_play and score
    val_d=hand_dealer.get_value()
    if val_d > 21 : 
        print "Dealer busted,you won"
        outcome="You Won,New Deal?"
        print "dealer:",val_d,"Player:",val_p
        in_play=False
        score+=1
        return
    if val_p <= val_d :
        outcome="you Lose,New Deal?"
        print "you Lose,dealer won" 
        score-=1
    else:
        outcome="You Won,New Deal?"
        print "you won"
        score+=1
        
    print "dealer:",val_d,"Player:",val_p    
    in_play=False
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BlackJack", [200,50], 45, "Black")
    canvas.draw_text("Score:"+str(score), [400,100], 35, "Black")
    canvas.draw_text("Dealer:", [50,170], 35, "Black")
    canvas.draw_text("Player:", [50,350], 35, "Black")
    canvas.draw_text(outcome, [200,350], 33, "Black")
    hand_dealer.draw(canvas,[70,200])
    hand_player.draw(canvas,[70,380])
    if in_play : 
        c=[70+CARD_BACK_CENTER[0],200+CARD_BACK_CENTER[1]]
        canvas.draw_image(card_back,CARD_BACK_CENTER,CARD_BACK_SIZE,c,CARD_BACK_SIZE)
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
