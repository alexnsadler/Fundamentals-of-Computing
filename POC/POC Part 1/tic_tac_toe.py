"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
# do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


def mc_trial(board, player):
    """
    Generates a game of Tic-Tac_Toe based on a given board and player
    until the game is over by draw or by a winner.
    """
    while board.check_win() == None:
        rand_choice = random.choice(board.get_empty_squares())
        player = provided.switch_player(player)
        board.move(rand_choice[0], rand_choice[1], player)


def mc_update_scores(scores, board, player):
    """
    Function that updates a given grid of scores based on who
    the machine player is and who won the game.
    """
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            # Gets the value for each square on a board
            pos = board.square(row,col)
            
            # Add SCORE_CURRENT to each square in the scores grid 
            # corresponding to where the given player has their tiles on the
            # board and subtract SCORE_OTHER from the scores grid corresponding
            # to where the other player has their tiles on the board
            if board.check_win() == player: 
                if pos == 1:
                    scores[row][col] += 0
                elif pos == board.check_win():
                    scores[row][col] += SCORE_CURRENT
                elif pos != board.check_win():
                    scores[row][col] -= SCORE_OTHER
            elif board.check_win() == provided.switch_player(player):
                if pos == 1:
                    scores[row][col] += 0
                elif pos == board.check_win():
                    scores[row][col] += SCORE_OTHER
                elif pos != board.check_win():
                    scores[row][col] -= SCORE_CURRENT
                    
            # If the game is a tie, add 0 (nothing) to the scores board
            elif board.check_win() == 4:
                scores[row][col] += 0


def get_best_move(board, scores):
    """
    Function that returns where the best move is based on the max value
    from a given grid of scores.
    """
    if len(board.get_empty_squares()) == 0:
        return None
    
    # Gets a new list from the scores grid where there is
    # a corresponding empty square on the board
    max_list = []
    for idx in board.get_empty_squares():
        max_list.append(scores[idx[0]][idx[1]])
        
    # Takes the position of the max value from max_list in order to return
    # a tuple of where the next move should be made on the board
    max_pos = max_list.index(max(max_list))
    return board.get_empty_squares()[max_pos]


def mc_move(board, player, trials):
    """
    Function that chooses the best move for the machine player based
    on MonteCarlo simulations.
    """
    # Sets score to a grid of zeros
    scores = [[0 for dummycol in range(board.get_dim())] 
                 for dummyrow in range(board.get_dim())]
    
    # Switches who the machine player is
    play = provided.switch_player(player)
    
    # Decrements trials by one for each iteration and runs a 
    # Monte Carlo simulation/ updates scores
    
    while trials > 0:
        trials -= 1
        empty_board = board.clone()
        mc_trial(empty_board, play)
        mc_update_scores(scores, empty_board, play)
       
    return get_best_move(board, scores)


#mc_move(provided.TTTBoard(3, False, [[2, 1, 1], [1, 3, 1], [1, 2, 1]]), 3, 10)

#mc_trial(provided.TTTBoard(3,False,[[1,1,1],[1,1,1],[1,1,1]]),3)
#mc_update_scores([[0, 0, 0], [0, 0, 0], [0, 0, 0]],provided.TTTBoard(3, False, [[2, 2, 3], [3, 2, 1], [1, 2, 3]]), 2)
#get_best_move(provided.TTTBoard(3, False, [[2, 1, 1], [1, 3, 1], [1, 2, 1]]), [[1, 4, 2], [2, 0, 3], [5, 0, 2]])   


# Test game with the console or the GUI.  Uncomment whichever you prefer.
# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
