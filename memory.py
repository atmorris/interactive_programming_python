# implementation of card game - Memory

import simplegui
import random

card_deck = []
exposed = []
selected = 0
card1_index = card2_index = None
hide_last_round = False
turns = 0

# helper function to initialize globals
def new_game():
    global card_deck, exposed, turns, card1_index, card2_index, hide_last_round
    card_deck = [n / 2 for n in range(0, 16)]
    random.shuffle(card_deck)
    exposed = [False] * 16
    turns = 0
    label.set_text("Turns = " + str(turns))
    card1_index = card2_index = None
    hide_last_round = False
     
# define event handlers
def mouseclick(pos):
    global selected, card1_index, card2_index, hide_last_round, turns
    if not exposed[pos[0] / 50]:
        if hide_last_round:
            exposed[card1_index] = exposed[card2_index] = False
            card1_index = card2_index = None
            hide_last_round = False
        exposed[pos[0] / 50] = True
        if card1_index == None:
            turns = turns + 1
            label.set_text("Turns = " + str(turns))
            card1_index = pos[0] / 50
            exposed[card1_index] = True
            selected = 1
        elif card2_index == None:
            card2_index = pos[0] / 50
            exposed[card2_index] = True
            selected = 2
        if selected == 2:
            if card_deck[card1_index] == card_deck[card2_index]:
                card1_index = card2_index = None
                selected = 0
                hide_last_round = False
            else:
                hide_last_round = True
                selected = 0
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for index in range(16):
        canvas.draw_text(str(card_deck[index]),
                         [50 * index, 77], 84,
                         "White", "monospace")
        if not exposed[index]:
            canvas.draw_polygon([(50 * index, 0),
                                 (50 * (index + 1), 0),
                                 (50 * (index + 1), 100),
                                 (50 * index, 100)], 1,
                                "Black", "Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric