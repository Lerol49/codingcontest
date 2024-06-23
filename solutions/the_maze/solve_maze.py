import sys
sys.setrecursionlimit(100 ** 2)


with open("input.txt", "r") as f:
    text = f.readlines()



maze = []
for i in range(1, int(text[0].strip()) + 1):
    maze.append(text[i].strip().split(" "))
    maze[-1] = [int(num) for num in maze[-1]]



def find_next(row, column, path):
    if maze[row][column] == 2:
        with open("output.txt", "w") as f:
            f.write(path)
        return

    if maze[row][column] == 3:
        return path

    maze[row][column] = 3

    if maze[row - 1][column] != 0:
        find_next(row - 1, column, path + "w")

    if maze[row + 1][column] != 0:
        find_next(row + 1, column, path + "s")

    if maze[row][column - 1] != 0:
        find_next(row, column - 1, path + "a")

    if maze[row][column + 1] != 0:
        find_next(row, column + 1, path + "d")


result = find_next(1, 1, "")

