import os
import pandas as pd
from pymodbus.client import ModbusTcpClient
from datetime import datetime

#Chiller, main1, main2
ip_address = {
     "ips":["10.181.185.135","10.181.185.130","10.181.185.131"],
     "slaves":[1,100,101]
     }

# Specify the file path
file_path = [r"C:\Users\Admin\Desktop\Test\Post_Chiller.csv",r"C:\Users\Admin\Desktop\Test\Post_main1.csv",r"C:\Users\Admin\Desktop\Test\Post_Main2.csv"]

i = 0

for x in ip_address["ips"]:
    print(x)
    client = ModbusTcpClient(x,port=502,timeout=1)
    connection = client.connect()
    # if connection:
    #     print("Connection success")
    #kw
    result = client.read_holding_registers(address=0x02F0,count=2,slave=ip_address["slaves"][i])
    registers = result.registers
    #kwh
    result2 = client.read_holding_registers(address=0x03D0,count=2,slave=ip_address["slaves"][i])
    registers2 = result2.registers
    #kw demand
    result3 = client.read_holding_registers(address=0x0404,count=2,slave=ip_address["slaves"][i])
    registers3 = result3.registers

    A = registers[0]
    B = registers[1]
    C = registers2[0]
    D = registers2[1]
    E = registers3[0]
    F = registers3[1]

    val = (A*(2**16)) + B
    val2 = (C*(2**16)) + D
    val3 = (E*(2**16)) + F


    if A > 32767:
            val = val - 2^32
    val_kw = val*0.01


    val_kwh = val2

    if E > 32767:
            val3 = val3 - 2^32
    val_kw_demand = val3*0.01

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
     #Define the variables containing the values to append
    new_values = {
        "Datetime": formatted_datetime,
        "Kw": val_kw,
        "Kw_Demand": val_kw_demand,
        "Kwh": val_kwh
    }

    # Check if the CSV file exists
    if not os.path.exists(file_path[i]):
        # Create an empty DataFrame with the specified columns if the file doesn't exist
        df = pd.DataFrame(columns=["Datetime", "Kw","Kw_Demand", "Kwh"])
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

