from PQMII.PQMII_module import PQMII_Class
from utilities.Meters import Meter
from utilities import infrastructure
from utilities import Read_json



aloha = Meter( metername='aloha', metertype=infrastructure.meterType.PQMII ,host = 'host', measurements=['time','kw'], port = 4, addressBook={})

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()
    



    