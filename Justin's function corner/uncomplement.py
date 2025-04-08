#takes in the raw string value from a register and uncomplements them. This returns a list with the following format: [firstByte,secondByte,combined]
def uncomplement ( twosComplement :str ):
                twosComplementBinary = format ( abs(~(int(twosComplement) - 1)), '016b' )
                firstByte = ( int( twosComplementBinary, base = 2 ) & 0b1111111100000000 ) >> 8
                secondByte = int( twosComplementBinary, base = 2 ) & 0b0000000011111111
                uncomplementedNum = str( firstByte ) + str ( secondByte )
                
                return [firstByte,secondByte,uncomplementedNum]