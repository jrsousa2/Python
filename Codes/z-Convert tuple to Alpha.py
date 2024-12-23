def tuple_to_hex(persistent_id_tuple):
    # Convert each integer in the tuple to its hexadecimal representation
    hex_digits = [format(num, 'x') for num in persistent_id_tuple]
    # Concatenate the hexadecimal digits into a single string
    persistent_id_hex = ''.join(hex_digits)
    return persistent_id_hex.upper()  # Convert to uppercase for consistency

# Example usage
persistent_id_tuple = (-882952057, 1928204403)
print("1",format(persistent_id_tuple[0], 'x'))
print("2",format(persistent_id_tuple[1], 'x'))

persistent_id_hex = tuple_to_hex(persistent_id_tuple)
print(persistent_id_hex)
