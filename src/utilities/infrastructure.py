import dataclasses
from enum import Enum
from datetime import datetime
import os
import json
import pandas as pd


class meterType(Enum):
    """Type of Meter."""

    EPM7000 = 1
    PQMII = 2
    EPM4500 = 3

@dataclasses.dataclass
class meterParams:

    meter_name: str | None = None
    meter_type: meterType | None = None
    measurements: list | None = None
    host: str = "localhost" 
    port: int = 502
    address_book: dict | None = None
    slave: int = 1

def Read_data( targetMeter:str, Data_Value):
    #make this a match/case statement
    if targetMeter == 'PQMII':
        with open(r'Register_Dictionary_PQMII.JSON', 'r') as file:
            data = json.load(file)
    elif targetMeter == 'EPM7000':
        with open(r'Register_Dictionary_EPM7000.JSON', 'r') as file:
            data = json.load(file)

    return data["Registers"][Data_Value][0], data["Registers"][Data_Value][1]
    

    #change this to return the list of data in the json entry: address, coils, units, etc.
    return x


def floatConversion(data):
    """Decodes a floating-point value from two Modbus registers based on the IEEE 754 single-precision format.

        :return: The interpreted floating-point value.
        :rtype: float
    """
 


    # if len(data) != 2:
    #     raise ValueError("Input data must be a list with two elements: [R1, R2].")

    # Combine the two registers into a 32-bit integer
    raw_value = (data[0] << 16) | data[1]

    #Check PQMII manual for the formula

    # Extract sign(1st bit), exponent(next 8 bits), and mantissa(last 23 bits)
    sign = (raw_value >> 31) & 0x1
    exponent = (raw_value >> 23) & 0xFF
    mantissa = raw_value & 0x7FFFFF

    # Calculate the floating-point value ()
    value = (-1)**sign * 2**(exponent - 127) * (1 + mantissa / (2**23))
    
    return value

#takes in the raw string value from a register and uncomplements them. 
def uncomplement ( twosComplement :str ):
    """
    Takes raw string values stored in two's complement and reinterpets them into a useable format

    Args:
        twosComplement (str): A string containing the combined two values of the data registers.

    Returns:
        list: [firstByte,secondByte,combined]
    """
    twosComplementBinary = format ( abs(~(int(twosComplement) - 1)), '016b' )
    firstByte = ( int( twosComplementBinary, base = 2 ) & 0b1111111100000000 ) >> 8
    secondByte = int( twosComplementBinary, base = 2 ) & 0b0000000011111111
    uncomplementedNum = str( firstByte ) + str ( secondByte )
                
    return [firstByte,secondByte,uncomplementedNum]

def currentDatetime():
    #Grabs current datetime
    current_datetime = datetime.now()

    #Formats the datetime into Year-Month-Day Hour-Min-Sec
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime

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