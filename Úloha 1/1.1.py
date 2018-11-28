"""Solves grids where all of the sensor data is known but might be incorrect."""
from util import in_bounds, print_board
import os

def create_board(path):
    """Creates a 2D array from the file with specified path."""
    input = open(path).read().splitlines()

    time = int(input[0])    # The time it took the robot
    board = []              # Array representation of the board
    start_coords = None     # Coords of "x"
    end_coords = None       # Coords of "*"
    number_of_sensors = 0   # Number of sensors of the solution

    # Create the board
    for i in range(1,  len(input)):
        line = input[i].split(" ")

        # Parse each line
        board.append([])
        for j in range(0, len(line)):
            elem = line[j]
            if elem == ".":
                board[i - 1].append(None)
            elif elem == "x" or elem == "*":
                if elem == "x":
                    start_coords = (i - 1, j)
                if elem == "*":
                    end_coords = (i - 1, j)
                board[i - 1].append(elem)
            else:
                board[i - 1].append(int(elem))
                number_of_sensors += 1

    return [time, board, start_coords, end_coords, number_of_sensors]

def board_exploration(board, board_mask, depth, position, sensors):
    """Recursively explore the board and print the valid paths."""
    # If we managed to reach the start, time is 0 and we used all the sensors
    if sensors == 0 and board[position[0]][position[1]] == 'x' and depth == 0:
        print_board(board_mask, time)
        return

    steps = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    # Try to take steps in all of the directions

    for step in steps:
        x, y = position[0] + step[0], position[1] + step[1]

        # If we are within bounds and there is sensor data and we haven't been there
        if in_bounds(x, y, board) and board[x][y] != None and board_mask[x][y] == -1:

            # If it's either the start or we are within the error
            if board[x][y] == "x" or abs(depth - int(board[x][y])) <= 5:
                # Recursively try the possibilities
                board_mask[x][y] = depth - 1

                # If it was a sensor, subtract from sensors
                if (board[x][y] != "x" and board[x][y] != "*"):
                    board_exploration(board, board_mask, depth - 1, (x, y), sensors - 1)
                else:
                    board_exploration(board, board_mask, depth - 1, (x, y), sensors)

                board_mask[x][y] = -1

# The path to the input file
file_name = "01.in"
file_dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(file_dir, file_name)

# Get information about the input
board_info = create_board(path)

# Name the information
time = board_info[0]
board = board_info[1]
start_coords = board_info[2]
end_coords = board_info[3]
number_of_sensors = board_info[4]

# Board mask (tracks where we have been and how long did it take to get there)
board_mask = [[-1] * len(board[0]) for _x in range(len(board))]
board_mask[end_coords[0]][end_coords[1]] = time

# Explore the board (and print the valid paths)
board_exploration(board, board_mask, time, end_coords, number_of_sensors)
