# implementation of card game - Memory

import simplegui
import random
state = 0

l1 = "01234567"
l2 = "01234567"
cards = "".join((l1,l2))
list_cards = list(cards)
random.shuffle(list_cards)
exposed = [False] * 16

ind1 = 0
ind2 = 0

set_text = 0

# helper function to initialize globals
def new_game():
    global state, set_text, ind1, ind2, list_cards
    random.shuffle(list_cards)
    state = 0
    set_text = 0
    ind1 = 0
    ind2 = 0
    for i in range(len(exposed)):
        exposed[i] = False

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, ind1, ind2, exposed, set_text
    index = pos[0] // 50
    
    if exposed[index]:
        return None
    
    if state == 0:
        exposed[index] = True
        ind1 = index
        state = 1
        
    elif state == 1:
        exposed[index] = True
        ind2 = index
        state = 2
        set_text += 1
        
    elif state == 2: 
        if list_cards[ind1] != list_cards[ind2]:
            exposed[ind1] = False
            exposed[ind2] = False
        ind1 = index
        exposed[index] = True
        state = 1
            
            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for card_index in range(len(cards)):
        card_pos = 50 * card_index + 15
        canvas.draw_text(str(list_cards[card_index]), (card_pos, 60), 50, "white")
        
    for i in range(len(cards)):
        if False == exposed[i]:
            canvas.draw_polygon([(50*i, 0), (50 * i, 100),
                             (50 * i + 50,100), (50 * i + 50, 0)],
                             5, "green", "green")
            
    for i in range(len(cards)):
        canvas.draw_line([50*i, 0], [50*i, 100], 1, "white")

    label.set_text("Turns = " + str(set_text))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(set_text))



# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
