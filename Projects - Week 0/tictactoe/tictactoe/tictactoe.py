"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    player_turn = ' '
    x_num = 0
    O_num = 0
 
    
    for place_y in board:
        for place_x in place_y:
            if place_x == X:
                x_num = x_num + 1
            elif place_x == O:
                O_num = O_num + 1
        
    if x_num <= O_num:
        player_turn = X
    elif x_num == 0 and O_num == 0 :
        player_turn = X
    else:
        player_turn = O
    
    return player_turn


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = []
    
    counterY = 0
    counterX = 0
    
    for placeY in board:
        for placeX in placeY:
            if placeX == EMPTY:
                action_set.append((counterY,counterX))
            counterX = counterX + 1
        counterY = counterY + 1
        counterX = 0
    
    return set(action_set)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid action")
    new_board = [row[:] for row in board]  # Create a deep copy of the board
    #This is done because if I simply copy like: new_board = board and edit it, I would also be modifying the initial board
    new_board[action[0]][action[1]] = player(board)
    return new_board
     
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    if board[0][0] == X and board[0][1] == X and board[0][2] == X:
        return X
    elif board[1][0] == X and board[1][1] == X and board[1][2] == X:
        return X
    elif board[2][0] == X and board[2][1] == X and board[2][2] == X:
        return X
    elif board[0][0] == X and board[1][0] == X and board[2][0] == X:
        return X
    elif board[0][1] == X and board[1][1] == X and board[2][1] == X:
        return X
    elif board[0][2] == X and board[1][2] == X and board[2][2] == X:
        return X
    elif board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    elif board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X

    if board[0][0] == O and board[0][1] == O and board[0][2] == O:
        return O
    elif board[1][0] == O and board[1][1] == O and board[1][2] == O:
        return O
    elif board[2][0] == O and board[2][1] == O and board[2][2] == O:
        return O
    elif board[0][0] == O and board[1][0] == O and board[2][0] == O:
        return O
    elif board[0][1] == O and board[1][1] == O and board[2][1] == O:
        return O
    elif board[0][2] == O and board[1][2] == O and board[2][2] == O:
        return O
    elif board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    elif board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    
    else:
        return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    posible = winner(board)
    
    if posible == X:
        return True
    elif posible == O:
        return True
    
    Scounter= 0
    for positionX in board:
        for positionY in positionX:
            if positionY == X or positionY == O:
                Scounter = Scounter + 1
    
    if Scounter == 9:
        return True
    else:
        return False
    
    
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    the_winner = winner(board)
    
    if the_winner == X:
        return 1
    elif the_winner == O:
        return -1
    else:
        return 0

#Version 3 - "Last stand" update
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    last_action = ()
    if player(board) == X:
        player_action_set = actions(board)
        best_value = -1000
        for action_player in player_action_set:
            player_board = result(board, action_player)
            if utility(player_board) == 1:
                return action_player
            enemy_action_set = actions(player_board)
            worst_value = 0
            
            for action_enemy in enemy_action_set:
                enemy_board = result(player_board, action_enemy)
                current_value = utility(enemy_board)
                worst_value = worst_value + current_value
            if best_value < worst_value:
                last_action = action_player
                if worst_value == 0:
                    return action_player
                else:
                    best_value = worst_value
        return last_action
    
    #Player X works fine
    
    else:
        player_action_set = actions(board)
        best_value = 1000
        for action_player in player_action_set:
            player_board = result(board, action_player)
            if utility(player_board) == -1:
                return action_player
            enemy_action_set = actions(player_board)
            worst_value = 0
            
            for action_enemy in enemy_action_set:
                enemy_board = result(player_board, action_enemy)
                current_value = utility(enemy_board)
                worst_value = worst_value + current_value
            if best_value > worst_value:
                last_action = action_player
                if worst_value == 0:
                    return action_player
                else:
                    best_value = worst_value
        return last_action
#Player 2 works fine now :D
            
                
#Version 2 - Working                
    # if player(board) == X:
    #     player_action_set = actions(board)
    #     for action_player in player_action_set:
    #         player_board = result(board, action_player)
    #         enemy_action_set = actions(player_board)
    #         worst_value = 1000
    #         best_value = -1000
    #         for action_enemy in enemy_action_set:
    #             enemy_board = result(player_board, action_enemy)
    #             current_value = utility(enemy_board)
    #             if worst_value > current_value:
    #                 worst_value = current_value
    #         if best_value < worst_value:
    #             last_action = action_player
    #             if worst_value == 0:
    #                 return action_player
    #             else:
    #                 best_value = worst_value
    #     return last_action            
                
                
                
                




#Version 1 - Does not work
    # if terminal(board):
    #     return None
    # posibilities = []
    
    # vmax = 10
    # vmin = -10
    
    # actions_max = actions(board)
    # actions_min = actions(board)
    
    
    # if player(board) == X:
    #     for action_max in actions_max:
    #         max_new_board = result(board, action_max)
    #         if utility(max_new_board) == 1:
    #             return action_max
    #         actions_min = actions(max_new_board)
    #         for action_min in actions_min:
    #             min_new_board = result(max_new_board, action_min)
    #             if vmax > utility(min_new_board):
    #                 vmax = utility(min_new_board)
    #         if vmin < vmax:
    #             posibilities.append(action_max)
    #             vmin = vmax
    #     return posibilities.pop()

    # else:
    #     for action_max in actions_max:
    #         max_new_board = result(board, action_max)
    #         if utility(max_new_board) == 1:
    #             return action_max
    #         actions_min = actions(max_new_board)
    #         for action_min in actions_min:
    #             min_new_board = result(max_new_board, action_min)
    #             if vmin > utility(min_new_board):
    #                 vmin = utility(min_new_board)
    #         if vmax < vmin:
    #             posibilities.append(action_max)
    #             vmax = vmin
    #         vmax = 10
    #     return posibilities.pop()
