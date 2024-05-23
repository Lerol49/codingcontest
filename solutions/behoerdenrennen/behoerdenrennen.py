import random

def create_inp():
    numbers = [i for i in range(1000)]
    random.shuffle(numbers)
    output = ""
    for num in numbers:  # i know this is slow, but i dont care
        output += str(num) + "\n"

    with open("input.txt", "w") as inp:
        inp.write(output)


def create_out():
    data = ""
    with open("input.txt", "r") as inp:
        data = inp.readlines()

    output = "0\n"
    i = 0
    while int(data[i].strip()) != 0:
        output += str(int(data[i])) + "\n"
        i = int(data[i])

    with open("output.txt", "w") as out:
        out.write(output)

