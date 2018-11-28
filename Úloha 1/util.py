import os

def in_bounds(x, y, board):
    """Returns, whether coordinates are within the bounds of a 2D array."""
    return x >= 0 and y >= 0 and x < len(board[0]) and y < len(board)

def print_board(board_mask, time):
    """Essentially prints how it would look like with correct sensors."""
    for row in board_mask:
        for elem in row:
            if elem == -1:
                print(". ", end="")
            elif elem == 0:
                print("x ", end="")
            elif elem == time:
                print("* ", end="")
            else:
                print(str(elem)+" ", end="")
        print()
    print()
