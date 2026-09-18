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
