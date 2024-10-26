import random



class Hooman:
    elapsed_time = 0

    def __init__(self, on_time, off_time):
        self.on_time = on_time
        self.off_time = off_time


    def is_on(self):
        time = self.elapsed_time % (self.on_time + self.off_time)
        return time - self.on_time < 0


    @classmethod
    def inc_time(cls):
        cls.elapsed_time += 1







def create_input_file():
    output = ""
    for i in range(30):
        output += str(random.randint(1, 24)) + " " + str(random.randint(1, 24)) + "\n"

    with open("input.txt", "w") as f:
        f.write(output)



def create_output_file():
    with open("input.txt", "r") as f:
        content = f.readlines()

    hoomans = []
    for line in content:
        line = line.split()
        line = [int(line[i]) for i in range(len(line))]
        hoomans.append(Hooman(line[0], line[1]))


    while True:
        failed = False
        for hooman in hoomans:
            if hooman.is_on():
                failed = True
                break
        if not failed:
            with open("output.txt", "w") as f:
                f.write(str(Hooman.elapsed_time) + "\n0")
            break
        Hooman.inc_time()


# create_input_file()
create_output_file()



"""

21 3
19 21
18 1
10 21
9 12
12 2
24 24
24 4
17 20
17 16
5 3
10 17
22 2
24 24
6 18
18 5
15 9
24 13
11 24
14 11


"""
