from pathlib import Path
# from utilities import Meters
import pandas as pd


# 0: MeterName, 7: MeterType, 13: IP Address, 16: Multinet Address, 17: Slave id

# def readMeterDeets ( df, rowNumber ):
#     meterName = df.iloc[rowNumber]["METER NAME"]
#     slaveID = 1
#     Measurements = []

#     meterType = df.iloc[rowNumber]['METER TYPE']
#     match meterType:
#         case "PQM2":
#             ipAddress = df.iloc[rowNumber]["MULTINET ADDRESS"]
#             meterTypeReturn = Meters.meterType.PQMII
#             slaveID = df.iloc[rowNumber]["MODBUS ID"]
#             Measurements = ['3 Phase Positive Real Energy Used','3 phase real power']
#         case "GE EPM 7000":
#             ipAddress = df.iloc[rowNumber]["IP ADDRESS"]
#             meterTypeReturn = Meters.meterType.EPM7000
#             Measurements = ['Total Watt Hour','3 phase watt total']
    
#     return meterName, meterTypeReturn, ipAddress, slaveID, Measurements


base_dir = Path(__file__).resolve().parent.parent
deet = pd.read_csv(base_dir / "config/Meter Deets.csv")

deet.columns = deet.columns.str.replace(" ", "_").str.replace("-", "_")


# Iterate over DataFrame using itertuples()
for row in deet.itertuples(index=False):
    meterType = row.METER_TYPE
    match meterType:
        case "PQM2":
            meterName = row.METER_NAME
            ipAddress = row.MULTINET_ADDRESS
            slaveID = row.MODBUS_ID
        case "GE EPM 7000":
            meterName = row.METER_NAME
            ipAddress = row.IP_ADDRESS
            slaveID = 1

    # Measurements = row.Measurements
    print(meterName, meterType,ipAddress,slaveID)


    


    # For loop through length of df column
    # Inside For loop:
    #   Match Statement for meter type
    #       PQM: Grab MeterName, Multinet address, Slave id
    #       EPM: Grab MeterName, IP Address, Slave id default to 1


# base_dir = Path(__file__).resolve().parent  # This ensures we are referencing the correct directory
# deet = pd.read_csv(base_dir / "config/Meter Deets.csv")


# readMeterDeets(deet, 5)