def intConversions(data):
    """
    Converts a Signed Int32 represented as [x, y] to a decimal value.

    Args:
        x (int): High 16 bits of the Signed Int32.
        y (int): Low 16 bits of the Signed Int32.

    Returns:
        int: The decimal equivalent of the Signed Int32.
    """
    # Combine x (high bits) and y (low bits) into a 32-bit value
    raw_value = (data[0] << 16) | data[1]

    # Check if the number is negative (32-bit signed integer)
    if combined & 0x80000000:  # If the highest bit is set
        combined -= 0x100000000  # Convert to negative using two's complement

    return combined