import os

def compute(pp):
    u = [1] * 30    # The stack (of fixed size)
    u1, u2 = 0, 0   # The u1 and u2 pointers

    # Repeat, until the pointer isn't bigger than the size of pp array
    ppPointer = 0
    while ppPointer < len(pp):
        command = pp[ppPointer]

        if command == "A":      # Addition command
            u[u1] += u[u2]
        elif command == "S":    # Subtraction command
            u[u1] -= u[u2]
        elif command == "P":    # Print command
            print(u[u1])
        elif command[0] == "M": # Move command
            value = int(command.split(" ")[1]) - 1
            u2, u1 = u1, value
        elif command == "IN":   # The input command
            u[u1] = int(input("Input: "))

        # Stuff with moving the pointer
        if command[0] == "G":
            ppPointer = int(command.split(" ")[1]) - 1
        elif command == "IF" and u[u1] == 0:
            ppPointer += 2
        else:
            ppPointer += 1

    # Print the final state of the machine
    print("\n______/MACHINE STATUS\\______")
    print("U = "+str(u))
    print("U1 = "+str(u1)+", U2 = "+str(u2))

# File name
file_name = "2.2.txt"

# Location of this file
file_dir = os.path.dirname(os.path.realpath(__file__))

# Read the contents of the file and run the code
pp = open(os.path.join(file_dir, file_name)).read().splitlines()
compute(pp)
