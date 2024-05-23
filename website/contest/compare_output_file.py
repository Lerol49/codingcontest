def compare_output_file(submit_filename, control_filename) -> bool:
    submit_file = submit_filename #open(submit_filename, "r")
    print(submit_file)
    control_file = open(control_filename, "rb").read()
    print(control_file)
    submit_file_content = submit_file
    control_file_content = control_file

    return submit_file_content == control_file_content

