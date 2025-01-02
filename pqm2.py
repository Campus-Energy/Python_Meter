import os
import pandas as pd
from pymodbus.client import ModbusTcpClient
from datetime import datetime

#Chiller, main1, main2
ip_address = ["10.181.185.135","10.181.185.130","10.181.185.131"]

# Specify the file path
file_path = r"C:\Users\Justin Liang\Desktop\New folder\pqm2.csv"

for x in ip_address:
    client = ModbusTcpClient(x,port=502,timeout=1)
    connection = client.connect()
    # if connection:
    #     print("Connection success")
    result = client.read_holding_registers(address=752,count=2,slave=1)
    result2 = client.read_holding_registers(address=752,count=2,slave=1)
    registers = result.registers
    registers2 = result2.registers
    A = registers[0]
    B = registers[1]
    C = registers2[0]
    D = registers2[1]

    val = (A*2^16) + B
    val2 = (C*2^16) + D

    if A > 32767:
            val = val - 2^32
    val_kw = val*0.1

    if C > 32767:
            val2 = val2 - 2^32
    val_kwh = val2

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


# Define the variables containing the values to append
new_values = {
    "Datetime": formatted_datetime,
    "Kw": val_kw,
    "Kwh": val_kwh
}

# Check if the CSV file exists
if not os.path.exists(file_path):
    # Create an empty DataFrame with the specified columns if the file doesn't exist
    df = pd.DataFrame(columns=["Column1", "Column2", "Column3"])
    df.to_csv(file_path, index=False)
    print(f"File '{file_path}' did not exist. Created an empty CSV file.")
else:
    # Load the existing DataFrame
    df = pd.read_csv(file_path)

# Append the new values as a new row using pd.concat
df = pd.concat([df, pd.DataFrame([new_values])], ignore_index=True)

# Save the updated DataFrame back to the CSV file
df.to_csv(file_path, index=False)
print(f"New values appended to '{file_path}'.")
