import os
import pandas as pd
from pymodbus.client import ModbusTcpClient
from datetime import datetime

def cft_float2_to_decimal(cft_float):
    """
    Converts a CFT_float2 input to a decimal value.

    Args:
        cft_float (list): A list of two integers representing the CFT_float2 input.

    Returns:
        float: The decimal equivalent of the input.
    """
    if not isinstance(cft_float, list) or len(cft_float) != 2:
        raise ValueError("Input must be a list of two integers [integer_part, fractional_part].")
    
    integer_part, fractional_part = cft_float
    # Combine integer and fractional parts, assuming fractional part needs division by 65536
    fractional_value = fractional_part / 65536  # Adjust based on the scale of the fractional part
    return integer_part + fractional_value



def sint32_to_decimal_xy(x, y):
    """
    Converts a Signed Int32 represented as [x, y] to a decimal value.

    Args:
        x (int): High 16 bits of the SInt32.
        y (int): Low 16 bits of the SInt32.

    Returns:
        int: The decimal equivalent of the SInt32.
    """
    # Combine x (high bits) and y (low bits) into a 32-bit value
    combined = (x << 16) | y

    # Check if the number is negative (32-bit signed integer)
    if combined & 0x80000000:  # If the highest bit is set
        combined -= 0x100000000  # Convert to negative using two's complement

    return combined


#Chiller, main1, main2
ip_address = {
     "ips":["10.181.5.140","10.181.61.130"],
     "slaves":[1,1]
     }

# Specify the file path
file_path = [r"C:\Users\Admin\Desktop\Test\Admin_Serv_2.csv",r"C:\Users\Admin\Desktop\Test\Gartley_Main.csv"]

i = 0

for x in ip_address["ips"]:
    print(x)
    client = ModbusTcpClient(x,port=502,timeout=1)
    connection = client.connect()
    # if connection:
    #     print("Connection success")
    #kw
    result = client.read_holding_registers(address=1017,count=2,slave=ip_address["slaves"][i])

    # Example usage
    cft_float = result.registers
    val_kw = cft_float2_to_decimal(cft_float)/1000

    #kwh
    result2 = client.read_holding_registers(address=1505,count=2,slave=ip_address["slaves"][i])
 
    sint32_value = result2.registers
    val_kwh = sint32_to_decimal_xy(sint32_value[0], sint32_value[1])

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
     #Define the variables containing the values to append
    new_values = {
        "Datetime": formatted_datetime,
        "3_phase_Kw_total": val_kw,
        "Kwh_total": val_kwh
    }

    # Check if the CSV file exists
    if not os.path.exists(file_path[i]):
        # Create an empty DataFrame with the specified columns if the file doesn't exist
        df = pd.DataFrame(columns=["Datetime", "3_phase_Kw_total", "Kwh_total"])
        df.to_csv(file_path[i], index=False)
        # print(f"File '{file_path}' did not exist. Created an empty CSV file.")
    else:
        # Load the existing DataFrame
        df = pd.read_csv(file_path[i])

    # Append the new values as a new row using pd.concat
    df = pd.concat([df, pd.DataFrame([new_values])], ignore_index=True)
    client.close()
    df.to_csv(file_path[i], index=False)

    i = i + 1

