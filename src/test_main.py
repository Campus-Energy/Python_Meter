from utilities.Meters import Meter
from utilities import infrastructure
from utilities import Read_json
import json
from pathlib import Path

# A test main script to test individual modules, maybe create seperate branch on github for this purpose
# Using POST CHILLER
adminServ2 = Meter( metername='ADMIN_SERV_2', metertype=infrastructure.meterType.EPM7000 ,host = '10.181.5.140', measurements=['time','kw'], port=502,slave=1)




def main():
    # loop throught a  file containing all the meter names, metertypes, ips, measurements, ports, and slave.
    #meterList = read meter name list
    #for meter in meterList
    #   curretMeter = Meter( metername = meterList[metername], metertype = meterList[metertype], host = meterList[host], measurements = meterList[measurements], etc )
    #   currentData = currentMeter.getData()
    #   append currenData to csv 
    print("Hello World!")
    



if __name__ == "__main__":
    main()
    



    