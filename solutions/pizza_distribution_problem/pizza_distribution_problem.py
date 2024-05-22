from math import gcd
from random import randint

def create_cf():
    def solve_one_line(n, m):
        return str(int(m / gcd(n, m)))


    output = ""

    with open("input.txt", "r") as inp:
        for line in inp.readlines()[1:]:
            line = line.split()
            output += solve_one_line(int(line[0]), int(line[1])) + "\n"

    with open("output.txt", "w") as out:
        out.write(output)


def create_inp():
    output = ""

    for i in range(1000):
        n = randint(1, 999)
        m = randint(n, 10000)
        output += str(n) + " " + str(m) + "\n"

    with open("input.txt", "w") as inp:
        inp.write(output)

create_cf()



