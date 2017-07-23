# Rock-paper-scissors-lizard-Spock solution

import random

def name_to_number(name):
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        return "Error: invalid name"

def number_to_name(number):
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        return "Error: invalid number"       
        
def rpsls(player_choice): 
    print ""
    print "Player chooses",
    player_number = name_to_number(player_choice)
    print player_choice
   
    comp_number = random.randrange(0,5)
    comp_choice = number_to_name(comp_number)
    print "Computer chooses " + comp_choice
    
    dif = (player_number - comp_number) % 5
    if dif == 0:
        print "Player and computer tie!"
    elif dif == 1:
        print "Player wins!"
    elif dif == 2:
        print "Player wins!" 
    elif dif == 3:
        print "Computer wins!"
    elif dif == 4:
        print "Computer wins!"
    else:
        print "Error: Invalid number"

rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")



