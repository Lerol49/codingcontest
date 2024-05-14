def compare_output_file(submit_filename, control_filename) -> bool:
    submit_file = open(submit_filename, "r")
    control_file = open(control_filename, "r")
    submit_file_content = submit_file.readlines()
    control_file_content = control_file.readlines()

    return submit_file_content == control_file_content

