from math import gcd

def solve_one_line(n, m):
    return str(int(m / gcd(n, m)))

output = ""

with open("input.txt", "r") as inp:
    for line in inp.readlines()[1:]:
        line = line.split()
        output += solve_one_line(int(line[0]), int(line[1])) + "\n"

with open("output.txt", "w") as out:
    out.write(output)




