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


def clean_data(df):
    """
    Clean the DataFrame by handling missing values and removing duplicates.

    Parameters:
    df (pd.DataFrame): The DataFrame to clean.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
    # Drop rows with any missing values
    df = df.dropna()

    # Remove duplicate rows
    df = df.drop_duplicates()

    return df


def save_cleaned_data(df, file_path):
    """
    Save the cleaned DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): The cleaned DataFrame.
    file_path (str): The path to save the cleaned CSV file.
    """
    df.to_csv(file_path, index=False)
