#

# temporary fix (for short input files)
def read_options_from_file(file_path):
    options = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove trailing newline
            options.append({"label": line, "value": line})
    return options
