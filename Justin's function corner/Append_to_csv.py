import os
import pandas as pd
    
def add_to_csv(file_path, new_values):
    """
    Checks if a csv exists at a given location, creates an empty dataframe if it doesn't exist, then appends the argument new_values to the dataframe.

    Args:
        file_path (string): A string that tells the function where the csv is.
        new_values (dictionary): A dictionary of values with key values corresponding to the dataframe column names (Can be changed when csv format is decided)

    Returns:
        df (dataframe): The new dataframe with the new values added at the end. (allows the df to be assinged to a variable in main() for modifications)
    """

    # Check if the CSV file exists
    if not os.path.exists(file_path):
        # Create an empty DataFrame with the specified columns if the file doesn't exist (Format of csv isn't decided yet)
        df = pd.DataFrame(columns=["Datetime", "Kw","Kw_Demand", "Kwh"])
        df.to_csv(file_path, index=False)
        # print(f"File '{file_path}' did not exist. Created an empty CSV file.")
    else:
        # Load the existing DataFrame
        df = pd.read_csv(file_path)

    # Append the new values as a new row using pd.concat
    df = pd.concat([df, pd.DataFrame([new_values])], ignore_index=True)

    return df



