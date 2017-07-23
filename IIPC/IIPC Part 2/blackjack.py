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

# user-inputted globals
prompt = ""


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
    global my_hand, dealer_hand
    my_hand = []
    dealer_hand = []
    def __init__(self):
        self.card = []

    def __str__(self):
        ans = ""
        for i in range(len(self.card)):
            ans += str(self.card[i]) + " " 
        return "Hand contains " + ans
        
    def add_card(self, card):
        self.card.append(card)

    def get_value(self):
        value = 0
        aces = 0
        for i in range(len(self.card)):
            value += VALUES[self.card[i].rank]
            if self.card[i].rank == "A":
                aces += 1
        if aces > 0:
            if value <= 11:
                value += 10
            else:
                value
        return value

    def draw(self, canvas, pos):
        for i in range(len(self.card)):
            card = self.card[i]
            position = [pos[0] + CARD_CENTER[0] + i * (30 + CARD_SIZE[0]), pos[1] + CARD_CENTER[1]]            
            card.draw(canvas, position)

          
# define deck class 
class Deck:
    def __init__(self, deck):
        self.deck = []
        ans = ""
        for suit in SUITS:
            for rank in RANKS:
                decks = Card(suit, rank)
                self.deck.append(decks)
        
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        ans = ""
        for i in range(len(self.deck)):
            ans += str(self.deck[i]) + " " 
        return "Deck contains " + ans 


# globals
deck = 0
my_deck = Deck(deck)
dealer_hand = Hand()
my_hand = Hand()


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, hand, my_hand, dealer_hand, prompt, outcome, score
    
    if in_play:
        score -= 1
        
    my_deck = Deck(deck)
    my_deck.shuffle()
    
    my_hand = Hand()
    my_hand.add_card(my_deck.deal_card())
    my_hand.add_card(my_deck.deal_card())
    
    dealer_hand = Hand()
    dealer_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
  
    in_play = True
    prompt = "Hit or stand?"
    outcome = ""


def hit():
    global score, in_play, my_hand, outcome, prompt
    # replace with your code below
    if not in_play:
        return None
    
    if my_hand.get_value() <= 21:
        my_hand.add_card(my_deck.deal_card())
    
    if my_hand.get_value() > 21:
        outcome = "You went bust and lost."
        prompt = "New deal?"
        in_play = False        
        score -= 1
  
    # if busted, assign a message to outcome, update in_play and score


def stand():
    global outcome, in_play, score, prompt
    
    if not in_play:
        return None
    
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(my_deck.deal_card())
        
    if my_hand.get_value() > 21:
        outcome = "You went bust and lose."
        prompt = "New deal?"
        score -= 1
        print outcome
        
    elif dealer_hand.get_value() > 21:
        outcome = "Dealer busted. You win."
        prompt = "New deal?"
        score += 1
        
    elif dealer_hand.get_value() >= my_hand.get_value():
        outcome = "Dealer wins"
        prompt = "New deal?"
        score -= 1
        
    else:
        outcome = "You win"
        prompt = "New deal?"
        score += 1
    
    in_play = False

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score


# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    # draw title
    canvas.draw_text("Blackjack", [75, 100], 50, "white")

    # draw score
    canvas.draw_text("Score: " + str(score), [350, 100], 30, "black")
    
    # draw titles, outcome, and prompt
    canvas.draw_text("Dealer       " + outcome, [75, 175], 30, "black")
    canvas.draw_text("Player       " + prompt, [75, 350], 30, "black")
    
    #draw card

    my_cards = my_hand
    my_cards.draw(canvas, [50, 325])
    
    dealer_cards = dealer_hand
    if in_play:
        dealer_cards.draw(canvas, [50, 150])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [122, 246],CARD_BACK_SIZE)
    else:
        dealer_cards.draw(canvas, [50, 150])


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
