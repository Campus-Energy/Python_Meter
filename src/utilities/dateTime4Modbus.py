from pymodbus.client import ModbusTcpClient
from uncomplement import uncomplement 

# client = ModbusTcpClient ( '10.181.69.131', port=502, timeout=1 )
# connection = client.connect()
# if connection:
#         print ( "Connection Sucessful!" )
# clock = client.read_holding_registers ( address=0x0230, count=4, slave=1 )

# meterTime = clock.registers

# properTime = [ f"{int(uncomplement(meterTime[meterTime.index(coil)])):04d}" if meterTime.index(coil) % 2 == 0 else f"{int(coil):04d}" for coil in meterTime]
# print(properTime)
# with open ( r"C:\Users\Admin\Desktop\modbustime.txt", "a" ) as timeLog:
# #Hamilton_main_1
   
#     timeLog.write (str(properTime)+'\n')

#     client.close()