import dataclasses
from enum import Enum

class meterType(Enum):
    """Type of Meter."""

    EPM7000 = 1
    PQMII = 2

@dataclasses.dataclass
class meterParams:

    meter_name: str | None = None
    meter_type: meterType | None = None
    measurements: list | None = None
    host: str = "localhost" 
    port: int = 0
    address_book: dict | None = None