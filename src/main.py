from utilities.Meters import Meter
from utilities import Meters
from utilities import Read_json
from utilities import csvAdd
from pathlib import Path
import pandas as pd
import traceback



def main():
    # Values will be given in a [high_value,low_value] storage system

    base_dir = Path(__file__).resolve().parent  # This ensures we are referencing the correct directory
    deet = pd.read_csv(base_dir / "config/Meter Deets.csv")

    deet.columns = deet.columns.str.replace(" ", "_").str.replace("-", "_")

    for row in deet.itertuples(index=False):
        meterType = row.METER_TYPE
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
        print(meterName)
        try:
            currentMeter = Meter(metername=meterName,metertype=meterType,host=ipAddress,measurements=Measurements,port=502,slave=modbusID)
            rawData = currentMeter.getData()     
            dataValueDictionary = currentMeter.dataConversion(data_dict=rawData)
            pathToSave = f"E:\\MeterDataTest\\{meterName}.csv"
            csvAdd.add_to_csv(pathToSave, dataValueDictionary)
        # except TypeError:
        #     continue
        except Exception as e:
            error_message = f"[{rawData}] {meterName}: Error occurred: {str(e)}\n{traceback.format_exc()}"
            with open("errors.txt", "a") as file:
                file.write(error_message + "\n")

            


    # HIG_SUBSTATION_1_MAIN_MTR = Meter( metername='HIG_SUBSTATION_1_MAIN_MTR', metertype=Meters.meterType.PQMII ,host = '10.181.77.130', measurements=['3 Phase Positive Real Energy Used','3 phase real power'], port=502,slave=1)
    # data_test1 = HIG_SUBSTATION_1_MAIN_MTR.getData()
    # register_dict1 = HIG_SUBSTATION_1_MAIN_MTR.dataConversion(data_dict=data_test1)
    # csvAdd.add_to_csv("E:\\MeterDataTest\\HIG_SUBSTATION_1_MAIN_MTR.csv",register_dict1)

    # POST_MAIN_1 = Meter( metername='POST_MAIN_1', metertype=Meters.meterType.PQMII ,host = '10.181.185.130', measurements=['3 Phase Positive Real Energy Used','3 phase real power'], port=502,slave=100)
    # data_test2 = POST_MAIN_1.getData()
    # register_dict2 = POST_MAIN_1.dataConversion(data_dict=data_test2)
    # csvAdd.add_to_csv("E:\\MeterDataTest\\POST_MAIN_1.csv",register_dict2)

    # POST_MAIN_2 = Meter( metername='POST_MAIN_2', metertype=Meters.meterType.PQMII ,host = '10.181.185.131', measurements=['3 Phase Positive Real Energy Used','3 phase real power'], port=502,slave=101)
    # data_test3 = POST_MAIN_2.getData()
    # register_dict3 = POST_MAIN_2.dataConversion(data_dict=data_test3)
    # csvAdd.add_to_csv("E:\\MeterDataTest\\POST_MAIN_2.csv",register_dict3)
    
    # #----------------------------------------------------------------------------------------------------------------
    # ADMIN_SERV_2_MAIN_MTR = Meter( metername='ADMIN_SERV_2_MAIN_MTR', metertype=Meters.meterType.EPM7000 ,host = '10.181.5.140', measurements=['Total Watt Hour','3 phase watt total'], port=502,slave=1)
    # data_test4 = ADMIN_SERV_2_MAIN_MTR.getData()
    # register_dict4 = ADMIN_SERV_2_MAIN_MTR.dataConversion(data_dict=data_test4)
    # csvAdd.add_to_csv("E:\\MeterDataTest\\ADMIN_SERV_2_MAIN_MTR.csv",register_dict4)

    # GARTLEY_HALL_MAIN_MTR = Meter( metername='GARTLEY_HALL_MAIN_MTR', metertype=Meters.meterType.EPM7000 ,host = '10.181.61.130', measurements=['Total Watt Hour','3 phase watt total'], port=502,slave=1)
    # data_test5 = GARTLEY_HALL_MAIN_MTR.getData()
    # register_dict5 = GARTLEY_HALL_MAIN_MTR.dataConversion(data_dict=data_test5)
    # csvAdd.add_to_csv("E:\\MeterDataTest\\GARTLEY_HALL_MAIN_MTR.csv",register_dict5)

    # GEORGE_HALL_MAIN_MTR = Meter( metername='GEORGE_HALL_MAIN_MTR', metertype=Meters.meterType.EPM7000 ,host = '10.181.65.130', measurements=['Total Watt Hour','3 phase watt total'], port=502,slave=1)
    # data_test6 = GEORGE_HALL_MAIN_MTR.getData()
    # register_dict6 = GEORGE_HALL_MAIN_MTR.dataConversion(data_dict=data_test6)
    # csvAdd.add_to_csv("E:\\MeterDataTest\\GEORGE_HALL_MAIN_MTR.csv",register_dict6)


if __name__ == "__main__":
    main()