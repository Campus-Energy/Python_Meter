from pymodbus.client import ModbusTcpClient
from infrastructure import meterParams, meterType
from uncomplement import uncomplement
import errors


class PQMII ():
    """Generic class for storing information for PQMII meters"""

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
        
        """Initialize new meter."""
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

    def getData ( self ):
        connection, client = self.connectToMeter ()
        #for measurement in self.meter_params.measurements:
            #the argument for reading_holding_registers should hold (address, coil, slave)
           

    def bitData32 ( self ):
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