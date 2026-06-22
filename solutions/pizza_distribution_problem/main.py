def read_input_file(filename: str):
    with open(filename, "r") as f:
        raw_data = f.readlines()
    n = int(raw_data.pop().strip())

