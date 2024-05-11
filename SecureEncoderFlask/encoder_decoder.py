import base64
import binascii
import urllib.parse

def encode_base64(input_text: str) -> str:
    """Encode a string using Base64."""
    return base64.b64encode(input_text.encode()).decode()

def decode_base64(encoded_text: str) -> str:
    """Decode a Base64 encoded string."""
    return base64.b64decode(encoded_text.encode()).decode()

def encode_hex(input_text: str) -> str:
    """Encode a string using Hex encoding."""
    return binascii.hexlify(input_text.encode()).decode()

def decode_hex(encoded_text: str) -> str:
    """Decode a Hex encoded string."""
    return binascii.unhexlify(encoded_text.encode()).decode()

def encode_utf8(input_text: str) -> bytes:
    """Encode a string using UTF-8."""
    return input_text.encode('utf-8').hex()

def decode_utf8(encoded_text: str) -> str:
    """Decode a UTF-8 encoded byte array."""
    return bytes.fromhex(encoded_text).decode('utf-8')

def encode_latin1(input_text: str) -> bytes:
    """Encode a string using ISO-8859-1 (Latin-1)."""
    return input_text.encode('iso-8859-1').hex()

def decode_latin1(encoded_text: str) -> str:
    """Decode a ISO-8859-1 (Latin-1) encoded byte array."""
    return bytes.fromhex(encoded_text).decode('iso-8859-1')

def encode_ascii(input_text: str) -> str:
    """Encode a string to ASCII values separated by spaces."""
    return ' '.join(str(ord(char)) for char in input_text)

def decode_ascii(encoded_text: str) -> str:
    """Decode ASCII values separated by spaces to a string."""
    return ''.join(chr(int(code)) for code in encoded_text.split())

def encode_url(input_text: str) -> str:
    """Encode a string for safe URL transmission."""
    return urllib.parse.quote(input_text)

def decode_url(encoded_text: str) -> str:
    """Decode a URL-encoded string."""
    return urllib.parse.unquote(encoded_text)

