import pandas as pd


def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The loaded DataFrame.
    """
    return pd.read_csv(file_path)


def save_cleaned_data(df, file_path):
    """
    Save the cleaned DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): The cleaned DataFrame.
    file_path (str): The path to save the cleaned CSV file.
    """
    df.to_csv(file_path, index=False)
