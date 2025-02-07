def PQMConversion(data):
    """
    Decodes a value from two PQMII Modbus registers.

    Args:
        data (list): A list of two integers [High_reg, Low_reg] representing the high and low registers.

    Returns:
        float: The interpreted floating-point value.
    """
    #check PQMII manual for math
    
    A = data[0]
    B = data[1]

    val = (A*(2**16)) + B

    if A > 32767:
        val = val - 2^32

    #Convert to kw
    val_kw = val*0.01

    return val_kw
