# Imports
from pymodbus.client import ModbusTcpClient
import utilities
import dataclasses
from enum import Enum
from pathlib import Path
import json

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
                slave = slave
            )
    
    def connectToMeter ( self ):
        """Connects to this specific meter and returns the connection test and the modbus client.

        :return: Returns a tuple, in the following format (connection, client)
        :rtype: (bool, ModbusTcpClient)
        """
        # IP / Port / Connection time wait before exit
        client = ModbusTcpClient ( self.meter_params.host, port=self.meter_params.port, timeout=1, retries=0)
        connection = client.connect()

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
        # Close the client connection
        client.close()
        return holder_dict
    
    def dataConversion ( self, data_dict ):
        # data_dict will be an input of data in the form of:
        # data_dict =  {"dataValue1": "[[500, 100]]", "dataValue2": "[[100, 200]]"}
        # "key": "value" format
        for key, value in data_dict.items():
            match (self.meter_params.meter_type):
                case meterType.EPM7000:
                    data_dict[key] = EPMConversion(value, key)
                case meterType.PQMII:
                    data_dict[key] = PQMConversion(value, key)
        return data_dict



def EPMConversion ( data, measurement ):
    match ( measurement ):
        case "3 phase watt total":
            val = floatConversion(data)
        case "Total Watt Hour":
            val = intConversions(data)
    return val

def PQMConversion ( data, measurement ):
    match ( measurement ):
        case "3 phase real power":
            val = PQMConversionkW(data)
        case "3 Phase Positive Real Energy Used":
            val = PQMConversionkWh(data)
    return val
    
# Combine the epm7000 and pqmII conversions into a single function with match statements to the meterType
def PQMConversionkW ( data ):
    """
    Decodes a value from two PQMII Modbus registers.

    Args:
        data (list): A list of two integers [High_reg, Low_reg] representing the high and low registers.

    Returns:
        float: The interpreted floating-point value.
    """
    A, B = data
    val = (A << 16) + B
    if A > 32767:
        val -= 2**32
    return val * 0.01

def PQMConversionkWh ( data ):
    """
    Decodes a value from two PQMII Modbus registers.

    Args:
        data (list): A list of two integers [High_reg, Low_reg] representing the high and low registers.

    Returns:
        float: The interpreted floating-point value.
    """
    #Check PQMII manual for math
    A, B = data
    val = (A << 16) + B
    if A > 32767:
        val -= 2**32
    return val

def floatConversion ( data ):
    """
    epm7000
    Decodes a floating-point value from two Modbus registers based on the IEEE 754 single-precision format.

    Args:
        data (list): A list of two integers [High_reg, Low_reg] representing the high and low registers.

    Returns:
        float: The interpreted floating-point value.
    """
    #Check PQMII manual for the formula
    raw = (data[0] << 16) | data[1]
    sign = (raw >> 31) & 0x1
    exponent = (raw >> 23) & 0xFF
    mantissa = raw & 0x7FFFFF

    return (-1)**sign * 2**(exponent - 127) * (1 + mantissa / (2**23))


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
    combined = (data[0] << 16) | data[1]
    if combined & 0x80000000:
        combined -= 0x100000000
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