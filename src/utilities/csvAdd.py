# Imports
import pandas as pd
import os
from datetime import datetime

def getDatetime():
    #Grabs current datetime
    current_datetime = datetime.now()

    #Formats the datetime into Year-Month-Day Hour-Min-Sec
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime


def add_to_csv ( file_path, new_values ):
    """
    Checks if a csv exists at a given location, creates an empty dataframe if it doesn't exist, then appends the argument new_values to the dataframe.

    Args:
        file_path (string): A string that tells the function where the csv is.
        new_values (dictionary): A dictionary of values with key values corresponding to the dataframe column names (Can be changed when csv format is decided)

    Returns:
        df (dataframe): The new dataframe with the new values added at the end. (allows the df to be assinged to a variable in main() for modifications)
    """

    # Creates a column list to store data value names
    cols = []

    #Add datetime to cols so Datetime is added to the csv if it doesn't exist in the path location
    cols.append("Datetime")

    for key in new_values.keys():
        cols.append(key)

    # Check if the CSV file exists
    if not os.path.exists(file_path):
        # Create an empty DataFrame with the specified columns if the file doesn't exist (Format of csv isn't decided yet)
        df = pd.DataFrame(columns=cols)
        df.to_csv(file_path, index=False)
        # print(f"File '{file_path}' did not exist. Created an empty CSV file.")
    else:
        # Load the existing DataFrame
        df = pd.read_csv(file_path)

    # Add current datetime from local machine to the datetime key within the new_values dictionary as a value
    new_values["Datetime"] = getDatetime()
    # Append the new values as a new row using pd.concat
    df = pd.concat([df, pd.DataFrame([new_values])], ignore_index=True)


    #Update the csv with the new data (Maybe add it to a different function)
    df.to_csv(file_path, index=False)

    return df
