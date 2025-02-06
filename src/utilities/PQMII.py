from pymodbus.client import ModbusTcpClient
from infrastructure import meterParams, meterType, uncomplement, Read_data
import errors


class Meter ():
    """ A class dedicated to programming and storing information an a specific PQMII meter.

        :meta public:

        :param metertype: The type of meter associated with this class
        :type metertype: str
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
        metertype: str,
        metername: str,
        host: str,
        measurements: list,
        port: int,
        addressBook: dict,
        slave: int
    ) -> None:
        """The basic constructor for this class

        :meta public:

        :param metertype: The type of meter associated with this class
        :type metertype: str
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

        if not hasattr ( self, "meter_params"):
            self.meter_params = meterParams (
                meter_type = metertype,
                meter_name = metername,
                measurements = measurements,
                host = host,
                port = port,
                #thinking of using a Json to hold all the register addresses.
                #code will load the Json and use that to retrieve data.
                address_book = addressBook,
                slave = slave
            )
    
    def connectToMeter ( self ):
        """Connects to this specific meter and returns the connection test and the modbus client.

        :return: Returns a tuple, in the following format (connection, client)
        :rtype: (bool, ModbusTcpClient)
        """
        client = ModbusTcpClient ( self.meter_params.host, port=self.meter_params.port, timeout=1 )
        connection = client.connect()
        
        # try: 
        #     client.connect()
        #     if connection is False:
        #         raise errors.connectionError("Connection Error")

        # except errors.connectionError:
        #     print ( "Program failed to connect to meter." )

        if connection:
            print ( "Connection sucessful!" )
            return connection, client
        else:
            print ( "Connection unsucessful." )
            return connection, client

    def getDatetime ( self ):
        """Retrieves the meter's current datetime stored in its internal clock

       
        :return: The complete datetime in the following format: yy-mm-dd hh:mm
        :rtype: str
        """
        connection, client = self.connectToMeter ()
        if not connection:
            return "Error, connection not found."
        else:
            clock = client.read_holding_registers ( address=0x0230, count=4, slave=1 )
            rawDatetime = clock.registers

            time = uncomplement(rawDatetime[0])
            date = uncomplement(rawDatetime[2])
            year = rawDatetime[3]

            datetime = str(year)+'-'+(str(date[0]).zfill(2))+'-'+(str(date[1]).zfill(2)) + ' ' + (str(time[0]).zfill(2))+':'+(str(time[1]).zfill(2))
            return datetime

    def getData ( self, measurement ):
        connection, client = self.connectToMeter ()
        registerAddress, count = Read_data ('PQMII', measurement)
        rawData = client.read_holding_registers ( address=registerAddress, count=count, slave=1 )
        return rawData
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
            bit32Data = client.read_holding_registers ( address=0x0230, count=4, slave=1 )
            upper16 = bit32Data[0]
            lower16 = bit32Data[1]

            combined32 = (upper16*2^16) + lower16

            if upper16 > 32767:
                combined32 = combined32 - 2^32

            return combined32
        


    

# PQMII( metername='aloha', metertype=meterType.PQMII ,host = 'host', measurements=['time','kw'], port = 4, addressBook={} )