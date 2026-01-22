# Imports
from utilities import Meters
from utilities import csvAdd
from pathlib import Path
from datetime import date, timedelta
import pandas as pd
import os
import time



""" Main Topic 1 """
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
            #2b
            case "PQM2":
                meterName = row.METER_NAME
                ipAddress = row.MULTINET_ADDRESS
                modbusID = int(row.MODBUS_ID)
                Measurements = ['3 Phase Positive Real Energy Used','3 phase real power']
                meterType = Meters.meterType.PQMII
            #2a
            # case "GE EPM 7000":
            #     meterName = row.METER_NAME
            #     ipAddress = row.IP_ADDRESS
            #     modbusID = 1
            #     Measurements = ['Total Watt Hour','3 phase watt total']
            #     meterType = Meters.meterType.EPM7000
            case _:
                continue
        # print(meterName)
        # 3c
        try:
            # Creates the Meter class for the current meter iteration
            currentMeter = Meters.Meter(metername=meterName,metertype=meterType,host=ipAddress,measurements=Measurements,port=502,slave=modbusID)
            # Grab the data and assign it to a rawData varaible. (Is a dictionary)
            rawData = currentMeter.getData()
            # Apply data conversions to convert the high/low register values into a decimal kw/kwh
            dataValueDictionary = currentMeter.dataConversion(data_dict=rawData)

            today = date.today()
            start_of_week = today - timedelta(days=today.weekday()) # Uses monday as the first day of the week

            folder_path = Path(f"C://Users//Admin//Documents//MeterDataTest//{meterName}")
            os.makedirs(folder_path, exist_ok=True)  # Make sure folder exists

            # Create a path to E drive of the workstation with the csv named as the meterName
            pathToSave = folder_path / f"{start_of_week}_{meterName}.csv"
            # Save the csv
            csvAdd.add_to_csv(pathToSave, dataValueDictionary)
        # Create an error log when any error is thrown (location is in the "Python meter" folder, one parent above the src folder)
        except Exception as e:
            # 1a
            error_message = f"[{csvAdd.getDatetime()}] {meterName}: Error occurred: {str(e)}"
            with open("errors.txt", "a") as file:
                file.write(error_message + "\n")


if __name__ == "__main__":
    # start = time.time()
    # main()
    # end = time.time()
    # print(f"{end - start:.4f} seconds")
    while True:
        start = time.time()
        try:
            main()
        except Exception as e:
            # Catch any unexpected crash at the script level
            error_message = f"[{csvAdd.getDatetime()}] Script-level error: {str(e)}"
            with open("errors.txt", "a") as file:
                file.write(error_message + "\n")
        end = time.time()
        elapsed = end - start
        print(f"Execution took {elapsed:.2f} seconds")

        # Wait so it runs every 60 seconds total
        sleep_time = max(0, 60 - elapsed)
        time.sleep(sleep_time)