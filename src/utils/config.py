import configparser


def load_config(path="config/paths.ini"):
    """
    Read a project configuration file.

    Paths inside the file are relative to the repository root, matching the
    working directory expected by ``python -m src``.

    Parameters:
    path (str): Path to the .ini file.

    Returns:
    configparser.ConfigParser: The parsed configuration.

    Raises:
    FileNotFoundError: If the file does not exist.
    """
    parser = configparser.ConfigParser()
    if not parser.read(path):
        raise FileNotFoundError(f"Configuration file not found: {path}")
    return parser
