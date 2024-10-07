from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('10.181.13.130',port=502,timeout=1)
connection = client.connect()
if connection:
    print("d Connection Sucessful!")

result = client.read_holding_registers(address=1506,count=2,slave=1)

print(result.registers)


#0 10101001 01010110000000000000000
client.close()
#1st bit = sign (1 = negative)
#next 8 bits = exponent
#Remaining bits = mantissa = value?

#00000000000000001010100101100110

print(float(2**42)*1.2818048)
