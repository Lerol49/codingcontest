import math


def compare_output_file(submit_file, control_filename) -> bool:
    submit_file = submit_file.read().decode("UTF-8")
    with open(control_filename, "rb") as f:
        control_file = f.read().decode("UTF-8")

    submit_list = list(map(str.strip, submit_file.replace("\r", "").split("\n")))
    control_list = list(map(str.strip, control_file.replace("\r", "").split("\n")))

    return submit_list == control_list



def compare_output_number(submission, control_filename):

    try:
        submission = float(submission)
    except ValueError:
        return False


    with open(control_filename, "r") as f:
        control_file = f.readlines()

    expected = float(control_file[0])
    margin_of_error = float(control_file[1])

    return abs(submission - expected) <= margin_of_error

