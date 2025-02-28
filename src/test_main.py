from utilities.Meters import Meter
from utilities import infrastructure
from utilities import Read_json

# A test main script to test individual modules, maybe create seperate branch on github for this purpose

aloha = Meter( metername='aloha', metertype=infrastructure.meterType.PQMII ,host = 'host', measurements=['time','kw'], port = 4, addressBook={})



def main():
    print("Hello World!")
    aloha.connectToMeter()
    aloha.getData()



if __name__ == "__main__":
    main()
    



    