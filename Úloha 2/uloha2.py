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

# Vypíše číslo 100
pp = ["A", "A", "A", "M 2", "A", "A", "A", "M 2", "A", "A", "P"]

# Druhé mocniny
#pp = ["IN", "M 2", "M 2", "A", "P", "M 3", "M 1", "S", "IF", "G 2"]

# Vypíše to větší ze dvou čísel
#pp = ["IN", "M 2", "IN", "M 3", "M 3", "S", "M 4", "M 4", "S", "M 1", "M 3", "A", "M 2", "M 4", "A", "M 1", "IF", "G 24", "M 4", "P", "M 5", "M 5", "S", "M 2", "IF", "G 32", "M 3", "P", "M 5", "M 5", "S", "M 5", "IF", "G 36", "G 43", "M 6", "M 1", "S", "M 6", "M 2", "S", "G 16", "S"]

compute(pp)
