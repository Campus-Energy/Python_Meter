from utilities.Meters import Meter
from utilities import Meters
from utilities import Read_json
import json
from pathlib import Path

# A test main script to test individual modules, maybe create seperate branch on github for this purpose
# Using POST CHILLER
aloha = Meter( metername='POST_CHILLER', metertype=Meters.meterType.PQMII ,host = '10.181.185.135', measurements=['3 Phase Positive Real Energy Used','3 phase real power'], port=502,slave=1)




def main():
    # loop throught a  file containing all the meter names, metertypes, ips, measurements, ports, and slave.
    #meterList = read meter name list
    #for meter in meterList
    #   curretMeter = Meter( metername = meterList[metername], metertype = meterList[metertype], host = meterList[host], measurements = meterList[measurements], etc )
    #   currentData = currentMeter.getData()
    #   append currenData to csv 
    print(aloha.getData())
    



if __name__ == "__main__":
    main()
    



    