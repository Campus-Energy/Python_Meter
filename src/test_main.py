from utilities.Meters import Meter
from utilities import infrastructure
from utilities import Read_json

# A test main script to test individual modules, maybe create seperate branch on github for this purpose
# Using POST CHILLER
aloha = Meter( metername='ADMIN_SERV_2', metertype=infrastructure.meterType.EPM7000 ,host = '10.181.5.140', measurements=['time','kw'], port=502,slave=1)


def main():
    print("Hello World!")
    print(aloha.getData())



if __name__ == "__main__":
    main()
    



    