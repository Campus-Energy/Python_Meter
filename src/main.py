# Imports
from utilities import Meters
from utilities import csvAdd
from pathlib import Path
from datetime import date, timedelta
import pandas as pd
import os


# Change the measurement list to whatever values you want. (Will need different menthod of implementation if user interaction is desired)

def add_to_csv(path, data_dict):
    df_new = pd.DataFrame([data_dict])
    
    # Use append mode ('a') and only write header if file doesn't exist
    df_new.to_csv(path, mode='a', header=not os.path.exists(path), index=False)


def main():
    # Values will be given in a [high_value,low_value] storage system
    base_dir = Path(__file__).resolve().parent  # This ensures we are referencing the correct directory
    deet = pd.read_csv(base_dir / "config/Meter Deets.csv")

    # Replaces any spaces in the column names with an underscore
    deet.columns = deet.columns.str.replace(" ", "_").str.replace("-", "_")

    # Using itertuples for speed as we're not changing anything within meter_deets
    for row in deet.itertuples(index=False):
        meterType = row.METER_TYPE
        # Pull data from columns depending on meter type
        # Change/Add string values in the JSON in the list "Measurements" to change/add a new measurement
        match meterType:
            case "PQM2":
                meterName = row.METER_NAME
                ipAddress = row.MULTINET_ADDRESS
                modbusID = int(row.MODBUS_ID)
                Measurements = ['3 Phase Positive Real Energy Used','3 phase real power']
                meterType = Meters.meterType.PQMII
            case "GE EPM 7000":
                meterName = row.METER_NAME
                ipAddress = row.IP_ADDRESS
                modbusID = 1
                Measurements = ['Total Watt Hour','3 phase watt total']
                meterType = Meters.meterType.EPM7000
            case _:
                continue
        # print(meterName)
        try:
            # Creates the Meter class for the current meter iteration
            currentMeter = Meters.Meter(metername=meterName,metertype=meterType,host=ipAddress,measurements=Measurements,port=502,slave=modbusID)
            # Grab the data and assign it to a rawData varaible. (Is a dictionary)
            rawData = currentMeter.getData()
            # Apply data conversions to convert the high/low register values into a decimal kw/kwh
            dataValueDictionary = currentMeter.dataConversion(data_dict=rawData)

            today = date.today()
            start_of_week = today - timedelta(days=today.weekday()) # Uses monday as the first day of the week

            folder_path = Path(f"E:/MeterDataTest/{meterName}")
            folder_path.makedirs(parents=True, exist_ok=True)  # Make sure folder exists

            # Create a path to E drive of the workstation with the csv named as the meterName
            pathToSave = folder_path / f"{start_of_week}_{meterName}.csv"
            # Save the csv
            add_to_csv(pathToSave, dataValueDictionary)
        # Create an error log when any error is thrown (location is in the "Python meter" folder, one parent above the src folder)
        except Exception as e:
            error_message = f"[{csvAdd.getDatetime()}] {meterName}: Error occurred: {str(e)}"
            with open("errors.txt", "a") as file:
                file.write(error_message + "\n")


if __name__ == "__main__":
    main()