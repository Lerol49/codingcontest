import hashlib
import random


allowed_chars_low = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
allowed_chars_cap = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "n", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "z"]
allowed_chars_spe = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "$", "%", "&", "!", "?", "#", ".", ","]

allowed_chars = allowed_chars_low + allowed_chars_spe + allowed_chars_cap


class Field:
    def __init__(self, size, password):
        self.password = random.choice([password, password[::-1]])
        self.password_hashed = hashlib.sha512(password.encode("utf-8")).hexdigest()
        self.size = size
        self.field = [[] for _ in range(self.size)]

        for i in range(self.size):
            for j in range(self.size):
                self.field[i].append(random.choice(allowed_chars))

        self._set_up_field()


    def _place_password_horizontal(self):
        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - len(self.password))

        for i in range(len(self.password)):
            self.field[x][y + i] = self.password[i]

    def _place_password_vertical(self):
        x = random.randint(0, self.size - len(self.password))
        y = random.randint(0, self.size - 1)

        for i in range(len(self.password)):
            self.field[x + i][y] = self.password[i]


    def _set_up_field(self):
        random.choice((self._place_password_horizontal, self._place_password_vertical))()
        for i in range(self.size):
            self.field[i] = "".join(self.field[i])

    def create_input(self):
        out = str(self.size) + "\n" + self.password_hashed + "\n"
        for row in self.field:
            out += row + "\n"
        out += "\n"
        with open("input.txt", "a") as f:
            f.write(out)




def check_substr(substr, hash_exp):
    hashed_normal = hashlib.sha512(substr.encode("utf-8")).hexdigest()
    hashed_reversed = hashlib.sha512(substr[::-1].encode("utf-8")).hexdigest()
    if hashed_normal == hash_exp:
        return substr
    elif hashed_reversed == hash_exp:
        return substr[::-1]
    else:
        return False



def check_row(content, index, hash_exp):
    for l in range(0, len(content[index])):
        for r in range(l, len(content[index])):
            substr = content[index][l:r]
            substr = check_substr(substr, hash_exp)
            if substr:
                return substr


def check_col(content, index, hash_exp):
    for u in range(0, len(content)):
        for d in range(u, len(content)):
            substr = ""
            for i in range(u, d + 1):
                substr += content[i][index]
            substr = check_substr(substr, hash_exp)
            if substr:
                return substr

def solve_instance(hash_exp, content):
    solution = None

    for i in range(len(content)):
        solution = solution or check_row(content, i, hash_exp) or check_col(content, i, hash_exp)

    return solution



def solve():
    with open("input.txt", "r") as f:
        content = f.readlines()

    solutions = ""
    index = 1
    for _ in range(int(content[0])):
        hash_exp = content[index + 1].strip()
        problem = content[index + 2: index + int(content[index]) + 2]
        solutions += solve_instance(hash_exp, problem) + "\n"
        index += int(content[index]) + 3


    with open("output.txt", "w") as f:
        f.write(solutions)






def append_input_file(password):
    field = Field(random.randint(len(password), 64), password)
    field.create_input()


def create_input_file():
    passwords = ["5l@t1sPiN4t", "4Pfe1mUss", "pf@nNkucH3n", "b4gu3t1e", "br0mb3Ere", "nvDe1@uf1auF", "erDBe3rt0r1E", "vollmilchschokoladenpudding"]
    # passwords = ["hi", "blub"]
    with open("input.txt", "w") as f:
        f.write(str(len(passwords)) + "\n")
    for password in passwords:
        append_input_file(password)



create_input_file()
solve()







