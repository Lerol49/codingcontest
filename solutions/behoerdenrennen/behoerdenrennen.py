import random

def create_inp():
    # you may need to run this mutliple times. If a value is not shuffled
    # you will be stuck in an infinite loop
    numbers = [i for i in range(1000)]
    random.shuffle(numbers)
    output = "1000\n"
    for num in numbers:  # i know this is slow, but i dont care
        output += str(num) + "\n"

    with open("input.txt", "w") as inp:
        inp.write(output)


def solve():
    data = ""
    with open("input.txt", "r") as inp:
        data = inp.readlines()

    output = ""
    i = 1
    while int(data[i].strip()) != 0:
        output += str(int(data[i])) + "\n"
        i = int(data[i])


    with open("output.txt", "w") as out:
        out.write(output)


create_inp()
solve()
