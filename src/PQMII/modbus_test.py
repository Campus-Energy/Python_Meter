from pymodbus.client import ModbusTcpClient
import pandas as pd



with open( r"C:\Users\Admin\Desktop\modbustime.txt", "a" ) as timeLog:
#Hamilton_main_1

        client = ModbusTcpClient('10.181.69.131',port=502,timeout=1)
        connection = client.connect()
        if connection:
                print("Connection Sucessful!")


        result = client.read_holding_registers(address=752,count=2,slave=1)


        result2 = client.read_holding_registers(address=0x0230,count=4,slave=1)
        # result3 = client.write_registers( address=0x0230,values=1054,slave=1 )


        registers = result.registers
        A = registers[0]
        B = registers[1]

        val = (A*2^16) + B

        if A > 32767:
                val = val - 2^32

        val_kw = val*0.1


        if result.isError():
                print("problem")
        else:
                print(f'{val_kw} kw')

        print(result2.registers)
        data = result2.registers
        #print(result3.registers)

        #takes in the raw string value from a register and uncomplements them. This returns a list with the following format: [firstByte,secondByte,combined]
        def uncomplement ( twosComplement :str ):
                twosComplementBinary = format ( abs(~(int(twosComplement) - 1)), '016b' )
                firstByte = ( int( twosComplementBinary, base = 2 ) & 0b1111111100000000 ) >> 8
                secondByte = int( twosComplementBinary, base = 2 ) & 0b0000000011111111
                uncomplementedNum = str( firstByte ) + str ( secondByte )
                
                return [firstByte,secondByte,uncomplementedNum]
               


        
        #results = [ f"{int(uncomplement(data[data.index(coil)])):04d}" if data.index(coil) % 2 == 0 else f"{int(coil):04d}" for coil in data]
        
        #kw reading
        kw = val_kw        

        #Eventually want time in a MM/DD/YYYY MMMM
        #HHMM reading datetime
        time = uncomplement(data[0])
        date = uncomplement(data[2])
        year = data[3]

        datetime = str(year)+'-'+(str(date[0]).zfill(2))+'-'+(str(date[1]).zfill(2)) + ' ' + (str(time[0]).zfill(2))+':'+(str(time[1]).zfill(2))

        #Checks if csv is there else make a new csv
        try:
                df=pd.read_csv("PQM2 Reading Test.csv")
        except FileNotFoundError:
                df = pd.DataFrame(columns=['kw reading', 'datetime'])

        #all scalar values so dict has to be wrapped in list
        rowEntry = pd.DataFrame([{'kw reading': kw,'datetime': datetime}])

        #slap the stuff at bottom of csv
        df = pd.concat([df,rowEntry])

        #index=False removes index, having index causes problems
        df.to_csv("PQM2 Reading Test.csv",index=False)
        print(data)
        client.close()