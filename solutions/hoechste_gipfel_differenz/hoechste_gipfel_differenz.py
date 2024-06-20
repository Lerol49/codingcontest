import random


def create_input_file():
    lines = 1000
    text = str(lines) + "\n"
    for i in range(lines):
        n = random.randint(1, 1000)
        text += str(n) + " "
        for j in range(n):
            lower_limit = random.randint(1, 500)
            upper_limit = random.randint(lower_limit, 1000)
            text += str(random.randint(lower_limit, upper_limit)) + " "
        text += "\n"

    with open("input.txt", "w") as f:
        f.write(text)



def solve():
    with open("input.txt") as f:
        text = f.readlines()

    output = ""
    for i in range(1, int(text[0])):
        line = text[i].split(" ")
        max_dist = 0
        for j in range(1, int(line[0])):
            dist = abs(int(line[j]) - int(line[j + 1]))
            if dist > max_dist:
                max_dist = dist

        output += str(max_dist) + "\n"

    with open("output.txt", "w") as f:
        f.write(output)


create_input_file()
solve()
