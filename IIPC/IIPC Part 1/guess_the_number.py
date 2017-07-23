# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

num_range = 100
secret_number = 0
num_tries = 7

# helper function to start and restart the game
def new_game():
    global secret_number
    global num_tries
    global num_tries
    if num_range == 100:
        num_tries = 7
        secret_number = random.randrange(1,100)
        print "New Game. Range is from 0 to 100"
        print "Number of remaining guesses is", num_tries
        print
    elif num_range == 1000:
        secret_number = random.randrange(1,1000)
        num_tries = 10
        print "New Game. Range is from 0 to 1000"
        print "Number of remaining guesses is", num_tries
        print


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global num_range
    num_range = 100
    new_game()
    

def range1000():
    global num_range
    num_range = 1000
    new_game()


def input_guess(guess):
    global secret_number
    global num_tries
    num_tries -= 1
    print "Guess was", int(guess)
    print "Number of remaining guesses is", int(num_tries)
    if secret_number == int(guess):
        print "Correct!"
        print
        new_game()
    else:
        if num_tries == 0:
            print "You ran out of guesses. The number was", secret_number
            print
            new_game()
        elif secret_number > int(guess):
            print "Higher!"
            print
        elif secret_number < int(guess):
            print "Lower!"
            print
    
# create frame
f = simplegui.create_frame("Guess The Number", 200, 200)

f.add_button("Range is [0, 100)", range100)
f.add_button("Range is [0, 1000)", range1000)
f.add_input("Input Guess", input_guess, 100)

# call new_game 
new_game()

# register event handlers for control elements and start frame
f.start()
