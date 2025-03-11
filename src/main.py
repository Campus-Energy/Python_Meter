from utilities.Meters import Meter
from utilities import Meters
from utilities import Read_json
from utilities import csvAdd
from pathlib import Path
import pandas as pd



def main():
    #Change to a dictionary here and in meters.py
    #Values will be given in a [high_value,low_value] storage system
    POST_CHILLER_PLANT_MAIN = Meter( metername='POST_CHILLER_PLANT_MAIN', metertype=Meters.meterType.PQMII ,host = '10.181.185.135', measurements=['3 Phase Positive Real Energy Used','3 phase real power'], port=502,slave=1)
    data_test1 = POST_CHILLER_PLANT_MAIN.getData()
    register_dict1 = POST_CHILLER_PLANT_MAIN.dataConversion(data_dict=data_test1)
    csvAdd.add_to_csv("E:\\MeterDataTest\\POST_CHILLER_PLANT_MAIN.csv",register_dict1)

    # POST_MAIN_1 = Meter( metername='POST_MAIN_1', metertype=Meters.meterType.PQMII ,host = '10.181.185.130', measurements=['3 Phase Positive Real Energy Used','3 phase real power'], port=502,slave=100)
    # data_test2 = POST_MAIN_1.getData()
    # register_dict2 = POST_MAIN_1.dataConversion(data_dict=data_test2)
    # csvAdd.add_to_csv("E:\\MeterDataTest\\POST_MAIN_1.csv",register_dict2)

    # POST_MAIN_2 = Meter( metername='POST_MAIN_2', metertype=Meters.meterType.PQMII ,host = '10.181.185.131', measurements=['3 Phase Positive Real Energy Used','3 phase real power'], port=502,slave=101)
    # data_test3 = POST_MAIN_2.getData()
    # register_dict3 = POST_MAIN_2.dataConversion(data_dict=data_test3)
    # csvAdd.add_to_csv("E:\\MeterDataTest\\POST_MAIN_2.csv",register_dict3)
    
    #----------------------------------------------------------------------------------------------------------------
    # ADMIN_SERV_2_MAIN_MTR = Meter( metername='ADMIN_SERV_2_MAIN_MTR', metertype=Meters.meterType.EPM7000 ,host = '10.181.5.140', measurements=['3 phase watt total','Total Watt Hour'], port=502,slave=1)
    # data_test = ADMIN_SERV_2_MAIN_MTR.getData()
    # register_dict = ADMIN_SERV_2_MAIN_MTR.dataConversion(data_dict=data_test)
    # csvAdd.add_to_csv("E:\\MeterDataTest\\ADMIN_SERV_2_MAIN_MTR.csv",register_dict)

    # GARTLEY_HALL_MAIN_MTR = Meter( metername='GARTLEY_HALL_MAIN_MTR', metertype=Meters.meterType.EPM7000 ,host = '10.181.61.130', measurements=['3 phase watt total','Total Watt Hour'], port=502,slave=1)
    # data_test = GARTLEY_HALL_MAIN_MTR.getData()
    # register_dict = GARTLEY_HALL_MAIN_MTR.dataConversion(data_dict=data_test)
    # csvAdd.add_to_csv("E:\\MeterDataTest\\GARTLEY_HALL_MAIN_MTR.csv",register_dict)

    # GEORGE_HALL_MAIN_MTR = Meter( metername='GEORGE_HALL_MAIN_MTR', metertype=Meters.meterType.EPM7000 ,host = '10.181.65.130', measurements=['3 phase watt total','Total Watt Hour'], port=502,slave=1)
    # data_test = GEORGE_HALL_MAIN_MTR.getData()
    # register_dict = GEORGE_HALL_MAIN_MTR.dataConversion(data_dict=data_test)
    # csvAdd.add_to_csv("E:\\MeterDataTest\\GEORGE_HALL_MAIN_MTR.csv",register_dict)


if __name__ == "__main__":
    main()