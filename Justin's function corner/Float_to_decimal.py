def floatConversion(data):
    """
    Decodes a floating-point value from two Modbus registers based on the IEEE 754 single-precision format.

    Args:
        data (list): A list of two integers [High_reg, Low_reg] representing the high and low registers.

    Returns:
        float: The interpreted floating-point value.
    """
    # if len(data) != 2:
    #     raise ValueError("Input data must be a list with two elements: [R1, R2].")

    # Combine the two registers into a 32-bit integer
    raw_value = (data[0] << 16) | data[1]

    #Check PQMII manual for the formula

    # Extract sign(1st bit), exponent(next 8 bits), and mantissa(last 23 bits)
    sign = (raw_value >> 31) & 0x1
    exponent = (raw_value >> 23) & 0xFF
    mantissa = raw_value & 0x7FFFFF

    # Calculate the floating-point value ()
    value = (-1)**sign * 2**(exponent - 127) * (1 + mantissa / (2**23))
    
    return value