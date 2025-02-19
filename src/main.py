import utilities

import utilities.Meters
import utilities.infrastructure

aloha = utilities.Meters( metername='aloha', metertype=utilities.infrastructure.meterType.PQMII ,host = 'host', measurements=['time','kw'], port = 4, addressBook={})
def main():
    print(aloha.metername)

if __name__ == "__main__":
    main()