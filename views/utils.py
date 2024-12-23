
def get_name_of_file(filename):
    file_arr = filename.split(".")
    file_arr.pop()
    return ".".join(file_arr)
