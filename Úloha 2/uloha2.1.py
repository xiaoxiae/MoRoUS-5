def compute(pp):
    u = [1] * (len(pp) + 1)
    u1, u2 = 0, 0

    # Repeat, until the pointer isn't bigger than the size of pp array
    ppPointer = 0
    while ppPointer < len(pp):
        command = pp[ppPointer]

        if command == "A":      # Addition command
            u[u1] += u[u2]
        elif command[0] == "M": # Move command
            value = int(command.split(" ")[1]) - 1
            u2, u1 = u1, value

        ppPointer += 1

        # Return prematurely if we reach over 100
        if u[u1] > 100:
            return None

    return u[u1]

def recursivepp(list, depth, increment):
    """Recursively tries to find the best solution to problem 2.1."""
    # If we reached the end and the result is 100, print it
    if depth == 0:
        if compute(list) == 100:
            f = open("uloha2.1.txt", "a")
            f.write(str(len(list))+": "+str(list)+"\n")
        return

    # Add the A command
    list[len(list) - depth] = "A"
    recursivepp(list, depth - 1, increment)

    # Add m command and increment the increment
    list[len(list) - depth] = "M "+str(increment)
    recursivepp(list, depth - 1, increment + 1)

    # Add m command and leave the increment alone
    list[len(list) - depth] = "M "+str(increment)
    recursivepp(list, depth - 1, increment)

    # Add m command and decrement the increment (if we can)
    if increment >= 2:
        list[len(list) - depth] = "M "+str(increment)
        recursivepp(list, depth - 1, increment - 1)

i = 1
while True:
    recursivepp([0] * i, i, 2)
    i += 1
