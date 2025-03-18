from pathlib import Path
from utilities import Meters
import pandas as pd


# 0: MeterName, 7: MeterType, 13: IP Address, 16: Multinet Address, 17: Slave id

def readMeterDeets ( df, rowNumber ):
    meterName = df.iloc[rowNumber]["METER NAME"]
    slaveID = 1
    Measurements = []

    meterType = df.iloc[rowNumber]['METER TYPE']
    match meterType:
        case "PQM2":
            ipAddress = df.iloc[rowNumber]["MULTINET ADDRESS"]
            meterTypeReturn = Meters.meterType.PQMII
            slaveID = df.iloc[rowNumber]["MODBUS ID"]
            Measurements = ['3 Phase Positive Real Energy Used','3 phase real power']
        case "GE EPM 7000":
            ipAddress = df.iloc[rowNumber]["IP ADDRESS"]
            meterTypeReturn = Meters.meterType.EPM7000
            Measurements = ['Total Watt Hour','3 phase watt total']
    
    return meterName, meterTypeReturn, ipAddress, slaveID, Measurements


    


    # For loop through length of df column
    # Inside For loop:
    #   Match Statement for meter type
    #       PQM: Grab MeterName, Multinet address, Slave id
    #       EPM: Grab MeterName, IP Address, Slave id default to 1


# base_dir = Path(__file__).resolve().parent  # This ensures we are referencing the correct directory
# deet = pd.read_csv(base_dir / "config/Meter Deets.csv")


# readMeterDeets(deet, 5)