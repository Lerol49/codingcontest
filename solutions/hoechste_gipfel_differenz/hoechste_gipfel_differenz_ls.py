

with open("input.txt") as f:
    text = f.readlines()

output = ""
for i in range(1, int(text[0]) + 1):
    line = text[i].split(" ")
    max_dist = 0
    for j in range(1, int(line[0])):
        dist = abs(int(line[j]) - int(line[j + 1]))
        if dist > max_dist:
            max_dist = dist

    output += str(max_dist) + "\n"

with open("output.txt", "w") as f:
    f.write(output)
