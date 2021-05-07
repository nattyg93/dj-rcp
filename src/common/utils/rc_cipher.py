"""Utils for encoding and decoding strings - namely Ratings Central passwords."""
from base64 import b64decode, b64encode


def _get_initial_cipher_key():
    """Get the initial cipher key."""
    # this constant has been arbitrarity chosen by Ratings Central
    return 62345


def _get_next_cipher_key(byte: int, key: int) -> int:
    """Update the current cipher key."""
    unsigned_16bit_divisor = 2 ** 16
    # these constants have been arbitrarity chosen by Ratings Central
    cipher_const_1 = 52845
    cipher_const_2 = 22719
    return (((byte + key) * cipher_const_1) + cipher_const_2) % unsigned_16bit_divisor


def encode(plain_text: str) -> str:
    """Return the encoded string."""
    byte_array = bytearray(plain_text, "utf8")
    output = []
    cipher_key = _get_initial_cipher_key()
    for byte in byte_array:
        encoded_byte = byte ^ (cipher_key >> 8)
        cipher_key = _get_next_cipher_key(encoded_byte, cipher_key)
        output.append(encoded_byte)
    return b64encode(bytes(output)).decode("utf-8")


def decode(encoded_text: str) -> str:
    """Return the decoded string."""
    byte_array = bytearray(b64decode(encoded_text.encode("utf-8")))
    output = []
    cipher_key = _get_initial_cipher_key()
    for encoded_byte in byte_array:
        decoded_byte = encoded_byte ^ (cipher_key >> 8)
        # here we use the already encoded byte to calculate the next
        # cipher key that was used to encode the original string
        cipher_key = _get_next_cipher_key(encoded_byte, cipher_key)
        output.append(decoded_byte)
    return bytes(output).decode("utf-8")
