# Imports
import pandas as pd
import os
from datetime import datetime

def getDatetime():
    """
    Returns the current local datetime as a formatted string.
    Format: YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add_to_csv(file_path, new_values):
    """
    Efficiently appends a new row of values to a CSV.
    Adds a 'Datetime' field to the dictionary automatically.
    If the file does not exist, it creates it with headers.

    Args:
        file_path (str): Path to the CSV file.
        new_values (dict): Dictionary of column_name: value pairs.

    Returns:
        DataFrame: The single-row DataFrame that was appended.
    """
    # Add timestamp
    new_values["Datetime"] = getDatetime()

    # Create a DataFrame with one row
    df_new = pd.DataFrame([new_values])

    # Append to CSV (with headers only if the file doesn't exist)
    df_new.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)

    return df_new