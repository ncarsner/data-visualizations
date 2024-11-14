import os


def read_file(file_path):
    """Read the contents of a file and return as a string."""
    with open(file_path, "r") as file:
        return file.read()


def write_file(file_path, content):
    """Write the given content to a file."""
    with open(file_path, "w") as file:
        file.write(content)


def append_to_file(file_path, content):
    """Append the given content to a file."""
    with open(file_path, "a") as file:
        file.write(content)


def file_exists(file_path):
    """Check if a file exists."""
    return os.path.isfile(file_path)


def delete_file(file_path):
    """Delete a file."""
    if file_exists(file_path):
        os.remove(file_path)
