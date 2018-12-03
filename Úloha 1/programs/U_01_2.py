"""Solves grids where not all of the sensor data is known and is correct."""
from util import in_bounds, print_board
import os

def create_board(path):
    """Gets positions of sensors and their values from the file."""
    input = open(path).read().splitlines()

    time = int(input[0])    # The time it took the robot
    sensor_locations = []   # A list storing the sensors

    board_width =  len(input[1].split(" "))  # Width of the board
    board_height = len(input) - 1            # Height of the board

    for i in range(1,  len(input)):
        line = input[i].split(" ")
        for j in range(0, len(line)):
            elem = line[j]
            if elem == ".":
                continue
            elif elem == "x":
                sensor_locations.append((i - 1, j, 0))
            elif elem == "*":
                sensor_locations.append((i - 1, j, time))
            else:
                sensor_locations.append((i - 1, j, int(elem)))

    return [sensor_locations, board_width, board_height]


def board_exploration(board_mask, position, goal, sensors, depth):
    """Recursively explore the board and print the valid paths, where not all of
    the sensor data is known, but is correct."""
    # if our path depth corresponds to how far is the next sensor
    if depth == sensors[goal][2]:
        # an it is the sensor that we're looking for
        if position == sensors[goal][0:2]:
            if position == sensors[-1][0:2]:    # if it's the very last sensor
                print_board(board_mask, depth)
                return
            else:   # else set a new goal and continue the recursion
                board_exploration(board_mask, position, goal + 1, sensors, depth)
        # return (we have no more steps left!)
        return

    # try to take steps in all directions
    steps = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for step in steps:
        x, y = position[0] + step[0], position[1] + step[1]

        if in_bounds(x, y, board_mask):
            if  board_mask[x][y] == -1:     # if we're not steping on sensor data
                board_mask[x][y] = depth + 1
                board_exploration(board_mask, (x, y), goal, sensors, depth + 1)
                board_mask[x][y] = -1
            elif board_mask[x][y] == depth + 1:     # if it is, don't overwrite it
                board_exploration(board_mask, (x, y), goal, sensors, depth + 1)

# The path to the input file
file_name = input("Enter name of the file: ")
file_dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(file_dir, file_name)

# Get sensor values and locations
board_data = create_board(path)

sensors = sorted(board_data[0], key=lambda v: v[2])
width = board_data[1]
height = board_data[2]

# information about the explored paths on the board
board_mask = [[-1] * width for _x in range(height)]
for sensor in sensors:
    board_mask[sensor[0]][sensor[1]] = sensor[2]

board_exploration(board_mask, (sensors[0][0], sensors[0][1]), 1, sensors, 0)
input("Done.")