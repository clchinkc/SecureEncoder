import base64
import json
from collections import Counter
import heapq


def huffman_compress(data):
    huffman_algorithm = HuffmanCoding()
    return huffman_algorithm.compress(data)


def huffman_decompress(data):
    huffman_algorithm = HuffmanCoding()
    return huffman_algorithm.decompress(data)


class HuffmanCoding:
    class Node:
        def __init__(self, char=None, freq=None):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def __init__(self):
        self.huffman_tree = None

    def build_frequency_table(self, data):
        return Counter(data)

    def build_huffman_tree(self, freq_table):
        priority_queue = [self.Node(char, freq) for char, freq in freq_table.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            merged = self.Node(freq=left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(priority_queue, merged)

        self.huffman_tree = priority_queue[0]

    def build_codes(self, node, prefix="", codebook=None):
        if codebook is None:
            codebook = {}
        if node.char is not None:
            codebook[node.char] = prefix
        else:
            self.build_codes(node.left, prefix + "0", codebook)
            self.build_codes(node.right, prefix + "1", codebook)
        return codebook

    def serialize_tree(self, node):
        if node.char is not None:
            return {"char": node.char}
        return {
            "left": self.serialize_tree(node.left),
            "right": self.serialize_tree(node.right),
        }

    def deserialize_tree(self, data):
        if "char" in data:
            return self.Node(char=data["char"])
        node = self.Node()
        node.left = self.deserialize_tree(data["left"])
        node.right = self.deserialize_tree(data["right"])
        return node

    def compress(self, data):
        if not data:
            return ""
        if len(data) == 1:
            return data

        freq_table = self.build_frequency_table(data)
        self.build_huffman_tree(freq_table)
        codebook = self.build_codes(self.huffman_tree)
        encoded_data = "".join(codebook[char] for char in data)

        base64_encoded_data = base64.b64encode(encoded_data.encode()).decode("ascii")

        serialized_tree = self.serialize_tree(self.huffman_tree)

        combined_data = {
            "compressed_data": base64_encoded_data,
            "serialized_tree": serialized_tree,
        }

        combined_json = json.dumps(combined_data)
        combined_base64 = base64.b64encode(combined_json.encode()).decode("ascii")

        return combined_base64

    def decompress(self, combined_base64):
        if not combined_base64:
            return ""
        if len(combined_base64) == 1:
            return combined_base64
        combined_json = base64.b64decode(combined_base64.encode("ascii")).decode()
        combined_data = json.loads(combined_json)

        base64_encoded_data = combined_data["compressed_data"]
        serialized_tree = combined_data["serialized_tree"]

        encoded_string = base64.b64decode(base64_encoded_data.encode("ascii")).decode()

        self.huffman_tree = self.deserialize_tree(serialized_tree)

        decoded_data = []
        current_node = self.huffman_tree

        for bit in encoded_string:
            if bit == "0":
                current_node = current_node.left
            else:
                current_node = current_node.right

            if current_node.char is not None:
                decoded_data.append(current_node.char)
                current_node = self.huffman_tree

        return "".join(decoded_data)
