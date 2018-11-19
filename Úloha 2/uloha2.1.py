def recursivepp(depth, u, u1, u2, stack):
    """Recursively tries to find the best solution to problem 2.1."""
    # If were at depth 0, we return (or potentially save the list)
    if depth == 0:
        # If the sum is 100 and the last command isn't M
        if u[u1] == 100 and stack[-1][0] != "M":
            f = open("uloha2.1.txt", "a")
            f.write(str(len(stack))+": "+str(stack)+"\n")
        return

    # ADD command
    temp = u[u1]
    u[u1] += u[u2]
    stack.append("A")
    recursivepp(depth - 1, u, u1, u2, stack)
    stack.pop()
    u[u1] = temp

    # MOVE command (to itself)
    stack.append("M "+str(u1 + 1))
    recursivepp(depth - 1, u, u1, u1, stack)
    stack.pop()

    # MOVE command (forward)
    stack.append("M "+str(u1 + 2))
    recursivepp(depth - 1, u, u1 + 1, u1, stack)
    stack.pop()

    # MOVE command (backward, only if we can)
    if u1 != 0:
        stack.append("M "+str(u1 ))
        recursivepp(depth - 1, u, u1 - 1, u1, stack)
        stack.pop()

i = 1
while True:
    recursivepp(i, [1] * (i + 1), 0, 0, [])
    i += 1
