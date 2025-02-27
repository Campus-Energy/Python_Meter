import utilities


halealoha = utilities.Meters.Meter( metername='aloha', slave=1, metertype=utilities.infrastructure.meterType.PQMII, host = 'host', measurements=['time','kw'], port = 4)
def main():
    print(halealoha.meter_params.meter_name)
    halealoha.getData( )

if __name__ == "__main__":
    main()