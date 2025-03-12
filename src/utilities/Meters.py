from pymodbus.client import ModbusTcpClient
import utilities
import dataclasses
from enum import Enum
from datetime import datetime
from utilities import Retrieve_date
from pathlib import Path
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
    slave: int = 1


class Meter ():
    """ A generic class dedicated to programming and storing information on one of several types of meters. This loads in json config files to determine
        what type of meter it's connected to and how to read and interprit the meter's stored data.

        :meta public:

        :param metertype: The type of meter associated with this class
        :type metertype: meterType
        :param metername: The name of the meter associated with this class
        :type metername: str
        :param host: The unique IP address associated with the meter
        :type host: str
        :param measurements: A list of measurements the user would like this meter to record
        :type measurements: list
        :param port: The port associated with the meter, defaults to 502
        :type port: int
        :param addressBook: A JSON file that holds the modbus memory map—the register addresses of every measurement
        :type addressBook: dict
        :param slave: The slave number associated with this meter or submeter
        :type slave: int
        """
    
    def __init__(
        self,
        metertype: meterType,
        metername: str,
        host: str,
        measurements: list,
        port: int,
        slave: int
    ) -> None:

        if not hasattr ( self, "meter_params"):
            self.meter_params = meterParams (
                meter_type = metertype,
                meter_name = metername,
                measurements = measurements,
                host = host,
                port = port,
                #thinking of using a Json to hold all the register addresses.
                #code will load the Json and use that to retrieve data.
                slave = slave
            )
    
    def connectToMeter ( self ):
        """Connects to this specific meter and returns the connection test and the modbus client.

        :return: Returns a tuple, in the following format (connection, client)
        :rtype: (bool, ModbusTcpClient)
        """
        # IP / Port / Connection time wait before exit
        client = ModbusTcpClient ( self.meter_params.host, port=self.meter_params.port, timeout=1 )
        connection = client.connect()
        
        # try: 
        #     client.connect()
        #     if connection is False:
        #         raise errors.connectionError("ConnRection Error")

        # except errors.connectionError:
        #     print ( "Program failed to connect to meter." )

        if connection:
            print ( "Connection sucessful!" )
            return connection, client
        else:
            print ( "Connection unsucessful." )
            return connection, client

    def getData ( self ):
        connection, client = self.connectToMeter ()
        holder_dict = {}
        for measurement in self.meter_params.measurements:
            match ( self.meter_params.meter_type ):
                #This currently will not work as it does not account for the different lengts of data ( 32 or 16 )
                case meterType.EPM7000:
                    registerAddress = Read_data ('EPM7000', measurement)
                    pulledRegister = client.read_holding_registers ( address = int(registerAddress[0]), count = registerAddress[1] )
                    holder_dict[measurement] = pulledRegister.registers
                case meterType.PQMII:
                    registerAddress = Read_data ('PQMII', measurement)
                    pulledRegister = client.read_holding_registers ( address = int(registerAddress[0],16), count = registerAddress[1], slave=self.meter_params.slave )
                    holder_dict[measurement] = pulledRegister.registers
                # case meterType.EPM4500:
                #     registerAddress = Read_data ('EPM4500', measurement)
                case _:
                    print("No correct value found")
        client.close()
        return holder_dict
    
    def dataConversion ( self, data_dict ):
        # data_dict will be an input of data in the form of:
        # data_dict =  {"dataValue1": "[[500, 100]]", "dataValue2": "[[100, 200]]"}
        # "key": "value" format
        for key, value in data_dict.items():
            match (self.meter_params.meter_type):
                case meterType.EPM7000:
                    data_dict[key] = EPMConverssion(value, key)
                case meterType.PQMII:
                    data_dict[key] = PQMConversion(value)
        return data_dict

        
        #for measurement in self.meter_params.measurements:
            #the argument for reading_holding_registers should hold (address, coil, slave)


    # def bitData32 ( self ):
    #     """Retrieves the two raw 16-bit values from two registers and combines them into a 32-bit data entry.

       
    #     :return: The combined 32-bit data from the two corresponding registers
    #     :rtype: str
    #     """
    #     connection, client = self.connectToMeter ()
    #     if not connection:
    #         return "Error, connection not found."
    #     else:
    #         bit32Data = client.read_holding_registers( address=0x0230, count=4, slave=1 )
    #         upper16 = bit32Data[0]
    #         lower16 = bit32Data[1]

    #         combined32 = (upper16*2^16) + lower16

    #         if upper16 > 32767:
    #             combined32 = combined32 - 2^32

    #         return combined32
        

def EPMConverssion ( data, measurement ):
    match ( measurement ):
        case "3 phase watt total":
            val = floatConversion(data)
        case "Total Watt Hour":
            val = intConversions(data)

    return val
    
# Combine the epm7000 and pqmII conversions into a single function with match statements to the meterType
def PQMConversion ( data ):
    """
    Decodes a value from two PQMII Modbus registers.

    Args:
        data (list): A list of two integers [High_reg, Low_reg] representing the high and low registers.

    Returns:
        float: The interpreted floating-point value.
    """
    #Check PQMII manual for math
    A = data[0]
    B = data[1]
    val = (A*(2**16)) + B
    if A > 32767:
        val = val - 2^32
    #Convert to kw
    val_kw = val*0.01

    return val_kw

def floatConversion ( data ):
    """
    epm7000
    Decodes a floating-point value from two Modbus registers based on the IEEE 754 single-precision format.

    Args:
        data (list): A list of two integers [High_reg, Low_reg] representing the high and low registers.

    Returns:
        float: The interpreted floating-point value.
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


def intConversions ( data ):
    """
    epm7000
    Converts a Signed Int32 represented as [x, y] to a decimal value.

    Args:
        x (int): High 16 bits of the Signed Int32.
        y (int): Low 16 bits of the Signed Int32.

    Returns:
        int: The decimal equivalent of the Signed Int32.
    """
    # Combine x (high bits) and y (low bits) into a 32-bit value
    combined = (data[0] << 16) | data[1]

    # Check if the number is negative (32-bit signed integer)
    if combined & 0x80000000:  # If the highest bit is set
        combined -= 0x100000000  # Convert to negative using two's complement

    return combined


def Read_data ( targetMeter: str, Data_Value ):
    # Get the directory of the currently running script
    base_dir = Path(__file__).resolve().parent  # This ensures we are referencing the correct directory


    match targetMeter:
        case 'PQMII':
            file_path = base_dir / "Register_Dictionary_PQMII.JSON"
        case 'EPM7000':
            file_path = base_dir / "Register_Dictionary_EPM7000.JSON"
        case _:
            raise ValueError("Invalid targetMeter value")

    if not file_path.exists():  # Check if the file exists before opening
        raise FileNotFoundError(f"File not found: {file_path}")

    with file_path.open("r") as file:   # Open the json
        data = json.load(file)

    

    return data["Registers"][Data_Value][0]["Register"], data["Registers"][Data_Value][0]["Count"]


# #takes in the raw string value from a register and uncomplements them. 
# def uncomplement ( twosComplement :str ):
#     """
#     Takes raw string values stored in two's complement and reinterpets them into a useable format

#     Args:
#         twosComplement (str): A string containing the combined two values of the data registers.

#     Returns:
#         list: [firstByte,secondByte,combined]
#     """
#     twosComplementBinary = format ( abs(~(int(twosComplement) - 1)), '016b' )
#     firstByte = ( int( twosComplementBinary, base = 2 ) & 0b1111111100000000 ) >> 8
#     secondByte = int( twosComplementBinary, base = 2 ) & 0b0000000011111111
#     uncomplementedNum = str( firstByte ) + str ( secondByte )
                
#     return [firstByte,secondByte,uncomplementedNum]