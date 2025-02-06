import pymodbus
import pandas as pd

def pullData(ip, slave_id=1, port_id=502,register_count=2):
    """
    Pulls data from the meters using modbus tcp.

    Args:
        ip (string): A string that tells the function what the ip of the meter is.
        slave_id (int): The slave id of the meter (default = 1, will change for epm's)
        port_id (int): The port number of the tcp connection (default = 502)
        register_count (int): The amount of registers you are pulling from starting from the given address (default = 2, data is a 32 bit value stored in 2 16 byte registers)

    Returns:
        registers (list): returns a list of data containing the unconverted values
    """

    client = ModbusTcpClient(ip,port=port_id,timeout=1)
    connection = client.connect()
    # if connection:
    #     print("Connection success")

    
    result = client.read_holding_registers(address=0x02F0,count=register_count,slave=slave_id)
    #The values will be stored in a list with a length depending on your count
    registers = result.registers

    return registers

