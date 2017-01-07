"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
     play a game starting with the given player by making random moves,
     alternating between players. The function should return when the 
     game is over
    """
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        rand_square = random.choice(empty_squares)
        board.move(rand_square[0],rand_square[1],player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    takes a grid of scores (a list of lists) with the same dimensions
    as the Tic-Tac-Toe board, a board from a completed game, and which
    player the machine player is
    score the completed board and update the scores grid
    """
    player_won = board.check_win()
    dim = board.get_dim()
    if player_won == player:
        s_other = SCORE_OTHER
        s_current = SCORE_CURRENT
    elif player_won == provided.switch_player(player):
        s_current = SCORE_OTHER
        s_other = SCORE_CURRENT
    else :
        return
    for row in range(dim):
        for col in range(dim):
            square = board.square(row,col)
            if square == player_won:
                scores[row][col] += s_current
            elif square == provided.switch_player(player_won):
                scores[row][col] += -1 * s_other
                
                
def get_best_move(board, scores):
    """
    find all of the empty squares with the maximum score and randomly 
    return one of them as a (row, column) tuple
    """
    empty_squares = board.get_empty_squares()
    if empty_squares == [] :
        return
    (row,col) = empty_squares[0]
    for (idx,idy) in empty_squares:
        if scores[row][col] < scores[idx][idy]:
            row = idx
            col = idy
    return (row,col)
    
    
def mc_move(board, player, trials):
    """
    takes a current board, which player the machine player is,
    and the number of trials to run
    use the Monte Carlo simulation  to return 
    a move for the machine player in the form of a (row, column) tuple.
    """
    dim = board.get_dim()
    scores = [[ 0 * idx * idy for idx in range(dim)] for idy in range(dim)]
    while trials > 0:
        board_new = board.clone()
        mc_trial(board_new,player)
        mc_update_scores(scores, board_new, player)
        trials -= 1
    return get_best_move(board, scores)
    
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
