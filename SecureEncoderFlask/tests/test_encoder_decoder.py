from src.encoder_decoder import encode_base64, decode_base64, encode_hex, decode_hex, encode_utf8, decode_utf8, encode_latin1, decode_latin1, encode_ascii, decode_ascii, encode_url, decode_url


def test_encode_base64():
    """Test Base64 encoding of a string."""
    input_text = "Hello, World!"
    expected_output = "SGVsbG8sIFdvcmxkIQ=="
    assert encode_base64(input_text) == expected_output, "Base64 encoding failed"

def test_decode_base64():
    """Test decoding of a Base64-encoded string."""
    encoded_text = "SGVsbG8sIFdvcmxkIQ=="
    expected_output = "Hello, World!"
    assert decode_base64(encoded_text) == expected_output, "Base64 decoding failed"

def test_encode_hex():
    """Test Hex encoding of a string."""
    input_text = "Hello, World!"
    expected_output = "48656c6c6f2c20576f726c6421"
    assert encode_hex(input_text) == expected_output, "Hex encoding failed"

def test_decode_hex():
    """Test decoding of a Hex-encoded string."""
    encoded_text = "48656c6c6f2c20576f726c6421"
    expected_output = "Hello, World!"
    assert decode_hex(encoded_text) == expected_output, "Hex decoding failed"
    
def test_encode_utf8():
    """Test UTF-8 encoding of a string."""
    input_text = "Hello, World!"
    expected_output = "48656c6c6f2c20576f726c6421"
    encoded_text = encode_utf8(input_text)
    assert encoded_text == expected_output, f"UTF-8 encoding failed: {encoded_text} != {expected_output}"

def test_decode_utf8():
    """Test decoding of a UTF-8 encoded byte array."""
    input_bytes = "48656c6c6f2c20576f726c6421"
    expected_output = "Hello, World!"
    output_text = decode_utf8(input_bytes)
    assert output_text == expected_output, f"UTF-8 decoding failed: {output_text} != {expected_output}"

def test_encode_latin1():
    """Test Latin-1 encoding of a string."""
    input_text = "Café"
    expected_output = "436166e9"
    encoded_text = encode_latin1(input_text)
    assert encoded_text == expected_output, f"Latin-1 encoding failed: {encoded_text} != {expected_output}"

def test_decode_latin1():
    """Test decoding of a Latin-1 encoded byte array."""
    input_bytes = "436166e9"
    expected_output = "Café"
    output_text = decode_latin1(input_bytes)
    assert output_text == expected_output, f"Latin-1 decoding failed: {output_text} != {expected_output}"

def test_encode_ascii():
    """Test ASCII encoding of a string."""
    input_text = "Hello, World!"
    expected_output = "72 101 108 108 111 44 32 87 111 114 108 100 33"
    encoded_text = encode_ascii(input_text)
    assert encoded_text == expected_output, f"ASCII encoding failed: {encoded_text} != {expected_output}"
    
def test_decode_ascii():
    """Test decoding of an ASCII-encoded string."""
    encoded_text = "72 101 108 108 111 44 32 87 111 114 108 100 33"
    expected_output = "Hello, World!"
    output_text = decode_ascii(encoded_text)
    assert output_text == expected_output, f"ASCII decoding failed: {output_text} != {expected_output}"

def test_encode_url():
    """Test URL encoding of a string."""
    input_text = "Hello, World! @2023"
    expected_output = "Hello%2C%20World%21%20%402023"
    encoded_text = encode_url(input_text)
    assert encoded_text == expected_output, f"URL encoding failed: {encoded_text} != {expected_output}"

def test_decode_url():
    """Test decoding of a URL-encoded string."""
    encoded_text = "Hello%2C%20World%21%20%402023"
    expected_output = "Hello, World! @2023"
    output_text = decode_url(encoded_text)
    assert output_text == expected_output, f"URL decoding failed: {output_text} != {expected_output}"