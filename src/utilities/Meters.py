# Imports
from pymodbus.client import ModbusTcpClient
import utilities
import dataclasses
from enum import Enum
from pathlib import Path
import json

class meterType(Enum):
    # Type of Meter.
    EPM7000 = 1
    PQMII = 2
    EPM4500 = 3

@dataclasses.dataclass
class meterParams:
    # Parameters used to define a meter's configuration
    meter_name: str | None = None
    meter_type: meterType | None = None
    measurements: list | None = None
    host: str = "localhost"
    port: int = 502
    slave: int = 1

class Meter:
    """ 
    A generic class dedicated to programming and storing information on one of several types of meters.
    This loads in json config files to determine what type of meter it's connected to and how to read and interpret the meter's stored data.
    register_cache = {}  # Shared cache of registers across all Meter instances
    """

    def __init__(self, metertype: meterType, metername: str, host: str, measurements: list, port: int, slave: int) -> None:
        # Store the meter parameters
        self.meter_params = meterParams(
            meter_type=metertype,
            meter_name=metername,
            measurements=measurements,
            host=host,
            port=port,
            slave=slave
        )

        # Load and cache the register map for the meter type
        meter_key = metertype.name
        if meter_key not in Meter.register_cache:
            Meter.register_cache[meter_key] = self._load_register_map(meter_key)
        self.registers = Meter.register_cache[meter_key]

    def _load_register_map(self, meter_key):
        # Loads the appropriate register map JSON file
        base_dir = Path(__file__).resolve().parent
        file_map = {
            "PQMII": base_dir / "Register_Dictionary_PQMII.JSON",
            "EPM7000": base_dir / "Register_Dictionary_EPM7000.JSON"
        }

        file_path = file_map.get(meter_key)
        if file_path is None or not file_path.exists():
            raise FileNotFoundError(f"Register file for {meter_key} not found at {file_path}")

        with file_path.open("r") as f:
            return json.load(f)["Registers"]

    def connectToMeter(self):
        # Connects to this specific meter and returns the connection test and the modbus client
        client = ModbusTcpClient(self.meter_params.host, port=self.meter_params.port, timeout=1, retries=1)
        connection = client.connect()

        if connection:
            print("Connection successful!")
        else:
            print("Connection unsuccessful.")
        return connection, client

    def getData(self):
        # Retrieves data for each requested measurement from the meter
        connection, client = self.connectToMeter()
        holder_dict = {}
        for measurement in self.meter_params.measurements:
            match self.meter_params.meter_type:
                case meterType.EPM7000:
                    reg = self.registers[measurement][0]
                    pulledRegister = client.read_holding_registers(address=int(reg["Register"]), count=reg["Count"])
                    holder_dict[measurement] = pulledRegister.registers
                case meterType.PQMII:
                    reg = self.registers[measurement][0]
                    pulledRegister = client.read_holding_registers(address=int(reg["Register"], 16), count=reg["Count"], slave=self.meter_params.slave)
                    holder_dict[measurement] = pulledRegister.registers
                case _:
                    print("No correct value found")
        client.close()
        return holder_dict

    def dataConversion(self, data_dict):
        # Converts raw register data into meaningful values (float, int, etc.)
        for key, value in data_dict.items():
            match self.meter_params.meter_type:
                case meterType.EPM7000:
                    data_dict[key] = EPMConversion(value, key)
                case meterType.PQMII:
                    data_dict[key] = PQMConversion(value, key)
        return data_dict

# Conversion functions for various meters
def EPMConversion(data, measurement):
    match measurement:
        case "3 phase watt total":
            val = floatConversion(data)
        case "Total Watt Hour":
            val = intConversions(data)
    return val

def PQMConversion(data, measurement):
    match measurement:
        case "3 phase real power":
            val = PQMConversionkW(data)
        case "3 Phase Positive Real Energy Used":
            val = PQMConversionkWh(data)
    return val

def PQMConversionkW(data):
    # Decodes a value from two PQMII Modbus registers to kilowatts
    A, B = data[0], data[1]
    val = (A * (2**16)) + B
    if A > 32767:
        val -= 2**32
    return val * 0.01

def PQMConversionkWh(data):
    # Decodes a value from two PQMII Modbus registers to kilowatt-hours
    A, B = data[0], data[1]
    val = (A * (2**16)) + B
    if A > 32767:
        val -= 2**32
    return val

def floatConversion(data):
    # Decodes a floating-point value from two Modbus registers using IEEE 754 format
    raw_value = (data[0] << 16) | data[1]
    sign = (raw_value >> 31) & 0x1
    exponent = (raw_value >> 23) & 0xFF
    mantissa = raw_value & 0x7FFFFF
    return (-1)**sign * 2**(exponent - 127) * (1 + mantissa / (2**23))

def intConversions(data):
    # Converts a Signed Int32 represented as [high, low] to a decimal value
    combined = (data[0] << 16) | data[1]
    if combined & 0x80000000:
        combined -= 0x100000000
    return combined
