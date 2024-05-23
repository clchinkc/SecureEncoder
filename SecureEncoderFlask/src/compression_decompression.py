import zlib
import brotli
import zstandard as zstd
import base64
import heapq
import base64
import base64
import collections
import heapq

def build_tree(text):
    frequency = collections.Counter(text)
    # Handle single-character edge case
    if len(frequency) == 1:
        char = next(iter(frequency))
        frequency[char] = 1
        frequency['\0'] = 1
    heap = [(freq, count, char, None, None) for count, (char, freq) in enumerate(frequency.items())]
    heapq.heapify(heap)
    count = len(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = (left[0] + right[0], count, None, left, right)
        heapq.heappush(heap, merged)
        count += 1
    return heap[0] if heap else None

def codes_from_node(node, prefix="", code={}):
    if node is None:
        return code
    _, _, char, left, right = node
    if char is not None:
        code[char] = prefix
    codes_from_node(left, prefix + "0", code)
    codes_from_node(right, prefix + "1", code)
    return code

def binary_to_ascii(binary):
    base = 95
    packed_int = int(binary, 2)
    result = []
    while packed_int > 0:
        result.append(chr((packed_int % base) + 32))
        packed_int //= base
    return ''.join(reversed(result))

def ascii_to_binary(ascii_str):
    base = 95
    total = 0
    for char in ascii_str:
        total = total * base + (ord(char) - 32)
    return bin(total)[2:]

def huffman_compress(text):
    if not text:
        return ""
    root = build_tree(text)
    huffman_code = codes_from_node(root)
    encoded_text = ''.join(huffman_code[char] for char in text)
    encoded_ascii = binary_to_ascii(encoded_text)
    dict_string = ','.join(f"{ord(char)}:{int('1' + code, 2)}" for char, code in huffman_code.items())
    return f"{len(dict_string)}:{dict_string}{encoded_ascii}"

def huffman_decompress(combined):
    if not combined:
        return ''
    dict_length_end = combined.index(':')
    dict_length = int(combined[:dict_length_end])
    dict_string = combined[dict_length_end+1:dict_length_end+1+dict_length]
    huffman_code = {chr(int(item.split(':')[0])): bin(int(item.split(':')[1]))[3:] for item in dict_string.split(',')}
    reverse_code = {v: k for k, v in huffman_code.items()}
    encoded_ascii = combined[dict_length_end+1+dict_length:]
    encoded_text = ascii_to_binary(encoded_ascii)
    decoded_text = []
    current_code = ""
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_code:
            decoded_text.append(reverse_code[current_code])
            current_code = ""
    return ''.join(decoded_text)


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


# Example usage
if __name__ == "__main__":
    # text = "Hello, world! This is an example of text compression."
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit."
    print("Original Text:", text)
    print("Original Text Size:", len(text))
    
    # Test Huffman
    encoded = huffman_compress(text)
    print("Huffman Encoded:", encoded)
    print("Huffman Encoded Size:", len(encoded))
    print("Huffman Decoded Correctly:", huffman_decompress(encoded) == text)
    
    # Test LZ77
    compressed = lz77_compress(text)
    print("LZ77 Compressed:", compressed)
    print("LZ77 Compressed Size:", len(compressed))
    print("LZ77 Decompressed Correctly:", lz77_decompress(compressed) == text)
    
    # Test LZW
    compressed = lzw_compress(text)
    print("LZW Compressed:", compressed)
    print("LZW Compressed Size:", len(compressed))
    print("LZW Decompressed Correctly:", lzw_decompress(compressed) == text)
    
    # Test Zstd
    compressed = zstd_compress(text)
    print("Zstd Compressed:", compressed)
    print("Zstd Compressed Size:", len(compressed))
    print("Zstd Decompressed Correctly:", zstd_decompress(compressed) == text)
    
    # Test deflate
    compressed = deflate_compress(text)
    print("Deflate Compressed:", compressed)
    print("Deflate Compressed Size:", len(compressed))
    print("Deflate Decompressed Correctly:", deflate_decompress(compressed) == text)
    
    # Test Brotli
    compressed = brotli_compress(text)
    print("Brotli Compressed:", compressed)
    print("Brotli Compressed Size:", len(compressed))
    print("Brotli Decompressed Correctly:", brotli_decompress(compressed) == text)
    

