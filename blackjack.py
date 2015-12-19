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

DEALER_POS = [100, 50]
PLAYER_POS = [100, 450]

# initialize some useful global variables
in_play = False
outcome = ""
forfeit = ""
score = 0
deck = None
dealer_hand = None
player_hand = None


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
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                          [pos[0] + CARD_CENTER[0],
                           pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.contents = []

    def __str__(self):
        hand = [str(card) for card in self.contents]
        return " ".join(hand)

    def add_card(self, card):
        self.contents.append(card)

    def get_value(self):
        value = 0
        contains_ace = False
        for card in self.contents:
            value += VALUES[card.get_rank()]
            if card.get_rank() == "A":
                contains_ace = True
        if contains_ace and value <= 11:
            return value + 10
        else:
            return value
   
    def draw(self, canvas, pos):
        for i in range(len(self.contents)):
            card = self.contents[i]
            card.draw(canvas, [pos[0] + 72 * i, pos[1]])
            
    def get_cover_offset(self):
        # added to change the color of the dealer's hole card appropriately
        suit = self.contents[0].get_suit()
        if suit == "C" or suit == "S":
            return 0
        else:
            return 1

# define deck class 
class Deck:
    def __init__(self):
        self.contents = []
        for suit in SUITS:
            for rank in RANKS:
                self.contents.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.contents)

    def deal_card(self):
        return self.contents.pop(0)
    
    def __str__(self):
        deck = [str(card) for card in self.contents]
        return " ".join(deck)

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_hand, player_hand, score, forfeit
    if in_play:
        score -= 1
        forfeit = "Player forfeits"
    outcome = ""
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    in_play = True

def hit():
    global in_play, player_hand, dealer_hand, deck, outcome, score, forfeit
    forfeit = ""
 
    if in_play:
        player_hand.add_card(deck.deal_card())

        if player_hand.get_value() > 21:
            outcome = "Player busts, dealer wins."
            in_play = False
            score -= 1
        
def stand():
    global in_play, player_hand, dealer_hand, deck, outcome, score, forfeit
    forfeit = ""
    
    if in_play:
        in_play = False
        while(dealer_hand.get_value() < 17):
            dealer_hand.add_card(deck.deal_card())

        if dealer_hand.get_value() > 21:
            outcome = "Dealer busts, player wins."
            score += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = "Dealer has " + str(dealer_hand.get_value()) + ", player has " + str(player_hand.get_value()) + ", dealer wins."
            score -= 1
        else:
            outcome = "Player has " + str(player_hand.get_value()) + ", dealer has " + str(dealer_hand.get_value()) + ", player wins."
            score += 1

# draw handler    
def draw(canvas):
    dealer_hand.draw(canvas, DEALER_POS)
    player_hand.draw(canvas, PLAYER_POS)
    if in_play:
        card_loc = (DEALER_POS[0] + CARD_BACK_CENTER[0],
                    DEALER_POS[1] + CARD_BACK_CENTER[1])
        card_cover_pos = (CARD_BACK_CENTER[0] + 72 * dealer_hand.get_cover_offset(),
                          CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_cover_pos, CARD_BACK_SIZE, card_loc,
                          CARD_BACK_SIZE)
        canvas.draw_text("Hit or stand?", [100, 350], 20, "White")
    else:
        canvas.draw_text("New deal?", [100, 350], 20, "White")
    canvas.draw_text(outcome, [100, 250], 20, "White")
    canvas.draw_text(forfeit, [100, 200], 20, "Red")
    canvas.draw_text("Score: " + str(score), [400, 575], 20, "White")

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