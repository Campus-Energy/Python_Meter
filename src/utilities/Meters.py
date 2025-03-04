from pymodbus.client import ModbusTcpClient
import dataclasses
from enum import Enum
from datetime import datetime
from utilities import Retrieve_date
from pathlib import Path
import os
import json
import pandas as pd
import ipaddress

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

        for measurement in self.meter_params.measurements:

            match ( self.meter_params.meter_type ):
                #This currently will not work as it does not account for the different lengts of data ( 32 or 16 )
                case meterType.EPM7000:
                    registerAddress = Read_data ('EPM7000', measurement)
                    pulledRegister = client.read_holding_registers ( address = registerAddress[0], count = registerAddress[1] )
                    high_low_value = pulledRegister.registers
                    return high_low_value
                case meterType.PQMII:
                    registerAddress = Read_data ('PQMII', measurement)
                    pulledRegister = client.read_holding_registers ( address = registerAddress[0], count = registerAddress[1] )
                    high_low_value = pulledRegister.registers
                    return high_low_value
                # case meterType.EPM4500:
                #     registerAddress = Read_data ('EPM4500', measurement)
                case _:
                    print("No correct value found")

            
        
        #for measurement in self.meter_params.measurements:
            #the argument for reading_holding_registers should hold (address, coil, slave)


    def bitData32 ( self ):
        """Retrieves the two raw 16-bit values from two registers and combines them into a 32-bit data entry.

       
        :return: The combined 32-bit data from the two corresponding registers
        :rtype: str
        """
        connection, client = self.connectToMeter ()
        if not connection:
            return "Error, connection not found."
        else:
            bit32Data = client.read_holding_registers( address=0x0230, count=4, slave=1 )
            upper16 = bit32Data[0]
            lower16 = bit32Data[1]

            combined32 = (upper16*2^16) + lower16

            if upper16 > 32767:
                combined32 = combined32 - 2^32

            return combined32
    
def Read_data(targetMeter: str, Data_Value):
    # Get the directory of the currently running script
    base_dir = Path(__file__).resolve().parent  # This ensures we are referencing the correct directory

    match targetMeter:
        case 'PQMII':
            file_path = base_dir / "utilities/Register_Dictionary_PQMII.JSON"
        case 'EPM7000':
            file_path = base_dir / "utilities/Register_Dictionary_EPM7000.JSON"
        case _:
            raise ValueError("Invalid targetMeter value")

    if not file_path.exists():  # Check if the file exists before opening
        raise FileNotFoundError(f"File not found: {file_path}")

    with file_path.open("r") as file:   # Open the json
        data = json.load(file)

    return data["Registers"][Data_Value][0]["Register"], data["Registers"][Data_Value][0]["Count"]
    

    #change this to return the list of data in the json entry: address, coils, units, etc.
    # return x


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

# PQMII( metername='aloha', metertype=meterType.PQMII ,host = 'host', measurements=['time','kw'], port = 4, addressBook={} )





    # def getDatetime ( self ):
    #     """Retrieves the meter's current datetime stored in its internal clock

    #     :return: The complete datetime in the following format: yy-mm-dd hh:mm
    #     :rtype: str
        
    #     .. note:: Todo: Restructure this to compensate for the different addresses for the different meters. Write a function to find the address given the metertype
    #     """
    #     connection, client = self.connectToMeter ()
    #     if not connection:
    #         return "Error, connection not found."
    #     else:
    #         clockAddress = self.getData ( self, 'datetime' )
    #         clock = client.read_holding_registers ( address=0x0230, count=4, slave=1 )
    #         rawDatetime = clock.registers

    #         time = uncomplement(rawDatetime[0])
    #         date = uncomplement(rawDatetime[2])
    #         year = rawDatetime[3]

    #         datetime = str(year)+'-'+(str(date[0]).zfill(2))+'-'+(str(date[1]).zfill(2)) + ' ' + (str(time[0]).zfill(2))+':'+(str(time[1]).zfill(2))
    #         return datetime