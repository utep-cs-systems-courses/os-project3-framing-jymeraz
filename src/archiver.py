def send_msg(message):
    byte_array = bytearray()
    with open(message, "rb") as file:
        byte_array += file.read()
    byte_array = f"{len(byte_array):08d}".encode() + byte_array
    return byte_array


def receive_msg(file_name, encoded_message):
    if len(encoded_message) == 0:
        return ""

    message = ''

    with open(file_name, "wb") as f:
        length_message = int(encoded_message[:8]) # First bytes are the length of the message.
        specific_message = encoded_message[8:]
        message = specific_message
        f.write(specific_message)

    return message


