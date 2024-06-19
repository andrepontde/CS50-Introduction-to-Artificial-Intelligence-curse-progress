import tictactoe as ttt
EMPTY = None

board = [[EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]]

# board = [['X', 'O', EMPTY],
#         ['O', 'O', 'X'],
#         [EMPTY, EMPTY, EMPTY]]

# print(ttt.player(board))

# new_board = board
# new_board[1][1] = 'X'
#Test to finally understand that a list is a mutable object always 
mylist = [1,2,3,4,5]
mylist.append(6)
print(mylist.pop())

