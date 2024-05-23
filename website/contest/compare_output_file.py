def compare_output_file(submit_file, control_filename) -> bool:
    submit_file = submit_file.read().decode("UTF-8")
    control_file = open(control_filename, "rb").read().decode("UTF-8")
    submit_list = list(map(str.strip, submit_file.replace("\r","").split("\n")))
    control_list = list(map(str.strip, control_file.replace("\r","").split("\n")))
    print(submit_list)
    print(control_list)

    return submit_list == control_list

