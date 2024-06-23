import random
import sys



def create_maze(dimension):
    sys.setrecursionlimit(max(dimension ** 2, 1000))
    queue = []


    dimension = int(dimension / 2) + 1
    maze = [[0 for i in range(dimension)] for j in range(dimension)]


    def get_neighbours(row, column):
        adj_list = []
        if row > 0:
            adj_list.append((row - 1, column))
        if row < dimension - 1:
            adj_list.append((row + 1, column))
        if column > 0:
            adj_list.append((row, column - 1))
        if column < dimension - 1:
            adj_list.append((row, column + 1))

        random.shuffle(adj_list)

        return adj_list



    start_vertex = (0, 0)
    queue.append(start_vertex)
    maze[start_vertex[0]][start_vertex[1]] = 1

    path = []



    def dfs():
        current_row = queue[-1][0]
        current_column = queue[-1][1]
        adjacent_verticies = get_neighbours(current_row, current_column)
        non_visited_verticies = [vertex for vertex in adjacent_verticies if maze[vertex[0]][vertex[1]] == 0]
        if len(non_visited_verticies) == 0:
            queue.pop()
            return
        for vertex in non_visited_verticies:
            if maze[vertex[0]][vertex[1]] == 0:
                maze[vertex[0]][vertex[1]] = 1
                path.append(((current_row, current_column), (vertex[0], vertex[1])))
                queue.append(vertex)
                dfs()


    while len(queue) > 0:
        dfs()
    # here the entire maze will be filled with 1 since we have visited every single vertex


    acutal_maze = [[0 for i in range(dimension * 2 - 1)] for j in range(dimension * 2 - 1)]


    # we need to connect each vertex in the maze and leave the rest as walls
    for connection in path:
        start_vertex = (2 * connection[0][0], 2 * connection[0][1])
        end_vertex = (2 * connection[1][0], 2 * connection[1][1])
        edge = (start_vertex[0] + connection[1][0] - connection[0][0], start_vertex[1] + connection[1][1] - connection[0][1])
        acutal_maze[start_vertex[0]][start_vertex[1]] = 1
        acutal_maze[end_vertex[0]][end_vertex[1]] = 1
        acutal_maze[edge[0]][edge[1]] = 1

    # surround the entire thing with 0, could be done better but not really worth the struggle i think
    acutal_maze.insert(0, [0 for i in range(dimension * 2 - 1)])
    acutal_maze.append([0 for i in range(dimension * 2 + 1)])
    for i in range(dimension * 2):
        acutal_maze[i].insert(0, 0)
        acutal_maze[i].append(0)

    acutal_maze[-1][-2] = 2

    return acutal_maze




def create_input_file():
    # this number should only be odd. dont ask why
    dimension = 97
    output = str(dimension + 2) + "\n"
    maze = create_maze(dimension)
    for row in maze:
        for column in row:
            output += str(column) + " "
        output += "\n"

    with open("input.txt", "w") as f:
        f.write(output)


create_input_file()



