import os
import pandas as pd
from pymodbus.client import ModbusTcpClient
from datetime import datetime
import struct

def convert_modbus_to_float(data):
    """
    Converts two Modbus registers (16-bit each) into an IEEE 754 floating-point value.

    Args:
        data (list): A list containing two integers [R1, R2], where R1 is the high-order register and R2 is the low-order register.

    Returns:
        float: The converted floating-point value.
    """
    if len(data) != 2:
        raise ValueError("Input data must be a list with two elements: [R1, R2].")
    
    # Extract the registers
    R1, R2 = data
    
    # Combine the registers into a single 32-bit raw value
    raw_value = (R1 << 16) | R2
    
    # Convert the raw value to a floating-point number (IEEE 754 format)
    return struct.unpack('>f', struct.pack('>I', raw_value))[0]



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


def pullData( ip, slave_id ):
    """
    Pulls data from the specified ip and slase addresses

    Args:
        ip: ip address of the device
        slave: slave address of the device

    Returns:
        pandas df: The data frame containing the 15 minute interval data 
    """
   
    client = ModbusTcpClient(ip,port=502,timeout=1)
    connection = client.connect()

    #Datetime
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


    #kw
    result = client.read_holding_registers(address=1017,count=2,slave=slave_id)
    val_kw = result.registers

    # #kwh_recieved
    # result3 = client.read_holding_registers(address=1499,count=2,slave=slave_id)
    # sint32_value_kwhr = result3.registers
    # val_kwh_recieved = sint32_to_decimal_xy(sint32_value_r[0], sint32_value_r[1])
    


    # #kwh_delivered
    # result4 = client.read_holding_registers(address=1501,count=2,slave=slave_id)
    # sint32_value_d = result4.registers
    # val_kwh_delivered = sint32_to_decimal_xy(sint32_value_d[0], sint32_value_d[1])

    # #kwh_net
    # result5 = client.read_holding_registers(address=1503,count=2,slave=slave_id)
    # sint32_value_n = result5.registers
    # val_kwh_net = sint32_to_decimal_xy(sint32_value_n[0], sint32_value_n[1])


    #kwh_total
    result2 = client.read_holding_registers(address=1505,count=2,slave=slave_id)
    sint32_value = result2.registers
    val_kwh_total = sint32_to_decimal_xy(sint32_value[0], sint32_value[1])

 #Define the variables containing the values to append
    new_values = {
        "Datetime": formatted_datetime,
        "3_phase_Kw_total": val_kw,
        "Kwh_total": val_kwh_total
        
    }

    # Check if the CSV file exists
    if not os.path.exists(file_path[i]):
        # Create an empty DataFrame with the specified columns if the file doesn't exist
        df = pd.DataFrame(columns=["Datetime", "3_phase_Kw_total","Kwh_recieved","Kwh_delivered","Kwh_net", "Kwh_total"])
        df.to_csv(file_path[i], index=False)
        # print(f"File '{file_path}' did not exist. Created an empty CSV file.")
    else:
        # Load the existing DataFrame
        df = pd.read_csv(file_path[i])

    # Append the new values as a new row using pd.concat
    df = pd.concat([df, pd.DataFrame([new_values])], ignore_index=True)
    client.close()
    df.to_csv(file_path[i], index=False)


    return df

# for x in ip_address["ips"]:
    # client = ModbusTcpClient(x,port=502,timeout=1)
    # connection = client.connect()

    # #Datetime
    # current_datetime = datetime.now()
    # formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


    # #kw
    # result = client.read_holding_registers(address=1017,count=2,slave=ip_address["slaves"][i])
    # val_kw = result.registers
    # # print(cft_float)
    # # val_kw = convert_modbus_to_float(cft_float)/1000


    # #kwh_recieved
    # result3 = client.read_holding_registers(address=1499,count=2,slave=ip_address["slaves"][i])
    # sint32_value_r = result3.registers
    # val_kwh_recieved = sint32_to_decimal_xy(sint32_value_r[0], sint32_value_r[1])
    


    # #kwh_delivered
    # result4 = client.read_holding_registers(address=1501,count=2,slave=ip_address["slaves"][i])
    # sint32_value_d = result4.registers
    # val_kwh_delivered = sint32_to_decimal_xy(sint32_value_d[0], sint32_value_d[1])

    # #kwh_net
    # result5 = client.read_holding_registers(address=1503,count=2,slave=ip_address["slaves"][i])
    # sint32_value_n = result5.registers
    # val_kwh_net = sint32_to_decimal_xy(sint32_value_n[0], sint32_value_n[1])


    # #kwh_total
    # result2 = client.read_holding_registers(address=1505,count=2,slave=ip_address["slaves"][i])
    # sint32_value = result2.registers
    # val_kwh_total = sint32_to_decimal_xy(sint32_value[0], sint32_value[1])



    # #Define the variables containing the values to append
    # new_values = {
    #     "Datetime": formatted_datetime,
    #     "3_phase_Kw_total": val_kw,
    #     "Kwh_recieved": val_kwh_recieved,
    #     "Kwh_delivered": val_kwh_delivered,
    #     "Kwh_net": val_kwh_net,
    #     "Kwh_total": val_kwh_total
        
    # }

    # # Check if the CSV file exists
    # if not os.path.exists(file_path[i]):
    #     # Create an empty DataFrame with the specified columns if the file doesn't exist
    #     df = pd.DataFrame(columns=["Datetime", "3_phase_Kw_total","Kwh_recieved","Kwh_delivered","Kwh_net", "Kwh_total"])
    #     df.to_csv(file_path[i], index=False)
    #     # print(f"File '{file_path}' did not exist. Created an empty CSV file.")
    # else:
    #     # Load the existing DataFrame
    #     df = pd.read_csv(file_path[i])

    # # Append the new values as a new row using pd.concat
    # df = pd.concat([df, pd.DataFrame([new_values])], ignore_index=True)
    # client.close()
    # df.to_csv(file_path[i], index=False)

    # i = i + 1

