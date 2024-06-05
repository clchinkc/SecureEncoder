import zlib
import brotli
import zstandard as zstd
import base64

def encode_number(n):
    """Encode a number using a simpler variable-length encoding."""
    bytes = []
    while n > 127:
        bytes.insert(0, (n & 0x7F) | 0x80)
        n >>= 7
    bytes.insert(0, n & 0x7F)
    return bytes

def lz77_compress(text, window_size=100, min_match_length=3):
    """Compress using LZ77 with reduced overhead for smaller matches."""
    if not text:
        return ""
    i = 0
    result = bytearray()
    while i < len(text):
        max_match = (0, 0)  # (offset, length)
        if i + min_match_length <= len(text):  # Ensures there is enough data to form a match
            for j in range(max(i - window_size, 0), i):
                k = 0
                while i + k < len(text) and k < window_size and text[j + k] == text[i + k]:
                    k += 1
                if k > max_match[1] and k >= min_match_length:
                    max_match = (i - j, k)

        if max_match[1] >= min_match_length:
            # Write a single flag byte plus encoded offset and length
            result.append(255)  # Match flag
            result.extend(encode_number(max_match[0]))  # offset
            result.extend(encode_number(max_match[1]))  # length
            i += max_match[1]
        else:
            # Handle literals and escape the flag byte
            if ord(text[i]) == 255:
                result.append(255)  # Escape flag byte
            result.append(ord(text[i]))
            i += 1

    # Encode the result as Base64 to handle binary data
    return base64.b64encode(result).decode('ascii')

def lz77_decompress(compressed):
    """Decompress data that was compressed with LZ77."""
    if not compressed:
        return ""
    data = base64.b64decode(compressed)
    result = []
    i = 0
    while i < len(data):
        if data[i] == 255:  # Match flag found
            i += 1
            if i < len(data) and data[i] == 255:  # Escaped flag byte
                result.append(chr(255))
                i += 1
                continue

            # Decode variable-length quantity encoded numbers
            offset, length = 0, 0
            while data[i] > 127:
                offset = (offset << 7) | (data[i] & 0x7F)
                i += 1
            offset = (offset << 7) | data[i]
            i += 1

            while data[i] > 127:
                length = (length << 7) | (data[i] & 0x7F)
                i += 1
            length = (length << 7) | data[i]
            i += 1

            start = len(result) - offset
            result.extend(result[start:start+length])
        else:
            result.append(chr(data[i]))
            i += 1
    return ''.join(result)

def lzw_compress(input_data):
    if not input_data:
        return ""
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    w = ""
    compressed = []
    for c in input_data:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            compressed.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        compressed.append(dictionary[w])

    # Encode numbers in the compressed list to handle dynamic dictionary sizes
    bits = max(dict_size.bit_length(), 8)  # At least 8 bits to handle up to 256 initial dictionary values
    compressed_bytes = bytearray()
    for number in compressed:
        compressed_bytes.extend(number.to_bytes((bits + 7) // 8, 'big'))

    return base64.b64encode(compressed_bytes).decode()

def lzw_decompress(compressed):
    if not compressed:
        return ""
    compressed_bytes = base64.b64decode(compressed)

    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    bits = max(dict_size.bit_length(), 8)
    byte_count = (bits + 7) // 8

    # Unpack integers according to the bit size used during compression
    compressed_integers = []
    for i in range(0, len(compressed_bytes), byte_count):
        number = int.from_bytes(compressed_bytes[i:i+byte_count], 'big')
        compressed_integers.append(number)

    w = result = dictionary[compressed_integers[0]]
    for k in compressed_integers[1:]:
        if k in dictionary:
            entry = dictionary[k]
        else:
            entry = w + w[0]
        result += entry
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return result

def zstd_compress(data):
    cctx = zstd.ZstdCompressor()
    compressed_data = cctx.compress(data.encode())
    return base64.b64encode(compressed_data).decode()

def zstd_decompress(compressed):
    dctx = zstd.ZstdDecompressor()
    compressed_data = base64.b64decode(compressed)
    return dctx.decompress(compressed_data).decode()

def deflate_compress(data):
    compressed_data = zlib.compress(data.encode(), level=9)
    return base64.b64encode(compressed_data).decode()

def deflate_decompress(compressed):
    compressed_data = base64.b64decode(compressed)
    return zlib.decompress(compressed_data).decode()

def brotli_compress(data):
    compressed_data = brotli.compress(data.encode())
    return base64.b64encode(compressed_data).decode()

def brotli_decompress(compressed):
    compressed_data = base64.b64decode(compressed)
    return brotli.decompress(compressed_data).decode()

