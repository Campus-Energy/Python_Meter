from utilities.Meters import Meter
from utilities import Meters
from utilities import Read_json
from pathlib import Path
import json


aloha = Meter( metername='POST_CHILLER', metertype=Meters.meterType.PQMII ,host = '10.181.185.135', measurements=['3 Phase Positive Real Energy Used','3 phase real power'], port=502,slave=1)

def main():
    #Change to a dictionary here and in meters.py
    #Values will be given in a [high_value,low_value] storage system
    registerValues = []
    registerValues.append(aloha.getData())

    aloha.PQMConversion(registerValues[0])


if __name__ == "__main__":
    main()