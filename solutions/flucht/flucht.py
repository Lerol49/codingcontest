import random


array = [2, 3, 1, 0, 2, 0, 3, 7, 0, 2, 0, 2, 0, 1, 1, -1]
#        0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15


def solve_instance(street):
    possible_paths = []

    def goto(street, index, path):
        if street[index] == -1:
            possible_paths.append(path)
            return

        left_index = index - street[index]
        right_index = index + street[index]
        street[index] = 0

        if left_index >= 0 and street[left_index] != 0 and left_index not in path:
            path_left = path.copy()
            path_left.append(left_index)
            goto(street, left_index, path_left)
        if right_index < len(street) and street[right_index] != 0 and right_index not in path:
            path_right = path.copy()
            path_right.append(right_index)
            goto(street, right_index, path_right)
        return

    goto(street, 0, [0])

    return min(possible_paths, key=len)






def find_next_step(street, index):
    new_index = index
    length = len(street)
    count = 5
    while True:
        count += 1
        offsett = (round(-1 * length ** 2 * (1 / (random.randint(0, count) + length)) + length + 1))
        new_index = index + offsett * random.choice([1, 1, -1])
        if new_index >= 0 and new_index < length and street[new_index] == 0:
            break
    return new_index, offsett




def create_one_instance(size):
    total_steps = int(size * random.randint(40, 90) / 100)
    street = [0 for i in range(size)]
    index = 0

    for i in range(total_steps):
        new_index, offsett = find_next_step(street, index)
        street[index] = offsett
        index = new_index

    street[index] = -1

    return street


def create_input_file():
    number_of_problems = 1000
    min_size = 10
    max_size = 500
    output = str(number_of_problems) + "\n"
    for _ in range(number_of_problems):
        size = random.randint(min_size, max_size)
        street = create_one_instance(size)
        length = len(street)
        street = " ".join(str(x) for x in street)
        output += str(length) + " " + street + "\n"

    with open("input.txt", "w") as f:
        f.write(output)



def create_output_file():
    output = ""
    with open("input.txt", "r") as f:
        content = f.readlines()

    for i in range(1, int(content[0]) + 1):
        street = content[i].split(" ")
        street = [int(street[i]) for i in range(1, int(street[0]) + 1)]
        solution = solve_instance(street)
        solution = " ".join(str(x) for x in solution)
        output += solution + "\n"

    with open("output.txt", "w") as f:
        f.write(output)


create_output_file()

