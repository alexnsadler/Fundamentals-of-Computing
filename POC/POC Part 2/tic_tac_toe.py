"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
#codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}


def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    
    if board.check_win() != None:
        return SCORES[board.check_win()]
    
    else:
        for idx in board.get_empty_squares():
            
            clone = board.clone()
            #SCORES[player] *= SCORES[player]
            clone.move(idx[0], idx[1], player)
                        
            #print clone, SCORES[player]
            
            
            if clone.check_win() == None:
                score = 0
            else:
                score = SCORES[clone.check_win()]
            
            print clone, clone.check_win(), "\n"
            if SCORES[player] == -1 and score != 0:
                ans = 1
                if score < ans:
                    ans = score
                return ans, idx
            elif SCORES[player] == 1 and score != 0:
                ans = -1
                if score > ans:
                    ans = score
                return ans, idx
            
                
        return mm_move(clone, provided.switch_player(player))
            #if player != clone.check_win():
            #    mm_move(clone, provided.switch_player(player))
            #elif player == clone.check_win():
            #    return player
            #else:
            #    return mm_move(clone, provided.switch_player(player))
        

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]


# Test game with the console or the GUI.
# Uncomment whichever you prefer.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

#TTT = provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.EMPTY, provided.PLAYERX, provided.PLAYERX], [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]])
#TTT = provided.TTTBoard(3, False, [[provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.PLAYERX, provided.PLAYERO, provided.PLAYERX]])
TTT = provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]])
print TTT.clone()
print mm_move(TTT, provided.PLAYERX)
#print TTT.get_empty_squares()
#print mm_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.EMPTY, provided.PLAYERX], [provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY]]), provided.PLAYERO)
