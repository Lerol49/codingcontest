import subprocess
import io
from contextlib import redirect_stdout
from typing import Callable

def read_input_file(filename: str) -> tuple[int, list[list[int]]]:
    """
    Make sure the file you provide with `filename` is in the 
    same directory as you run the function. Otherwise you will
    need to handle the filepath yourself. 

    -----
    returns `(n, data)`:
    `n`: number of lines in data
    `data`: all the rows in the input file converted to integer
    """
    with open(filename, "r") as f:
        raw_data = f.readlines()
    n = int(raw_data.pop(0).strip())

    # if something goes wrong with this, we are all in trouble
    data = list(map(lambda x: list(map(int, x.split())), raw_data))

    return n, data

def _output_file_name(input_file):
    return input_file.replace("input", "output")

def run_file(python_file, input_file):
    """
    Use this if you want to use input() and output() in your
    solution. 
    ---
    `python_file`: the name of the python file that contains your solution
    `input_file`: the name of the input file with .txt
    Make sure to give the ENTIRE filenaming, for example "main.py" and "input.txt".
    """

    with open(input_file, "r") as infile, open(_output_file_name(input_file), "w") as outfile:
        subprocess.run(
            ["python", python_file],
            stdin=infile,
            stdout=outfile,
        )

def run_function(func: Callable[[int, list[list[int]]], None], input_file: str):
    """
    `func` should have the signature `func(n, data)` where `n` is the number
    lines in the input file and `data` ist a list of lists of integers from 
    the input file.

    This function automatically handles the creation of an output file. Just
    `print` what you want to have in the output file and it will be generated
    """
    n, data = read_input_file(input_file)

    f = io.StringIO()
    with redirect_stdout(f):
        func(n, data)
    out = f.getvalue()

    with open(_output_file_name(input_file), "w") as f:
        f.write(out)



