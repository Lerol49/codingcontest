import math
import random


def create_input_file(length):
    output = ""
    for i in range(length):
        output += str(random.randint(1, 10 ** random.randint(2, 10))) + "\n"

    with open("input.txt", "w") as f:
        f.write(output)


create_input_file(20)


def solve():
    with open("input.txt", "r") as f:
        content = f.readlines()

    content = [int(content[i]) for i in range(len(content))]
    solution = math.lcm(*content)
    with open("output.txt", "w") as f:
        f.write(str(solution) + "\n0")


solve()
