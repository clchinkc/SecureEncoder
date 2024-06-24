import pytest
from src.compression_decompression import (
    lz77_compress,
    lz77_decompress,
    lzw_compress,
    lzw_decompress,
    zstd_compress,
    zstd_decompress,
    deflate_compress,
    deflate_decompress,
    brotli_compress,
    brotli_decompress,
)

TEST_TEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit."
SPECIAL_TEST_TEXT = "~!#$%^&*()_+"


def test_lz77_compression_cycle():
    """Test LZ77 compression and decompression."""
    compressed = lz77_compress(TEST_TEXT)
    decompressed = lz77_decompress(compressed)
    assert decompressed == TEST_TEXT, "LZ77 decompression does not match the original"


def test_lzw_compression_cycle():
    """Test LZW compression and decompression."""
    compressed = lzw_compress(TEST_TEXT)
    decompressed = lzw_decompress(compressed)
    assert decompressed == TEST_TEXT, "LZW decompression does not match the original"


def test_zstd_compression_cycle():
    """Test Zstandard compression and decompression."""
    compressed = zstd_compress(TEST_TEXT)
    decompressed = zstd_decompress(compressed)
    assert decompressed == TEST_TEXT, "Zstd decompression does not match the original"


def test_deflate_compression_cycle():
    """Test Deflate compression and decompression."""
    compressed = deflate_compress(TEST_TEXT)
    decompressed = deflate_decompress(compressed)
    assert (
        decompressed == TEST_TEXT
    ), "Deflate decompression does not match the original"


def test_brotli_compression_cycle():
    """Test Brotli compression and decompression."""
    compressed = brotli_compress(TEST_TEXT)
    decompressed = brotli_decompress(compressed)
    assert decompressed == TEST_TEXT, "Brotli decompression does not match the original"


# Additional tests for edge cases
@pytest.mark.parametrize("text", ["", "a", TEST_TEXT, SPECIAL_TEST_TEXT])
def test_compression_with_varied_text(text):
    """Test compression algorithms with varied text inputs."""
    functions = [
        (lz77_compress, lz77_decompress),
        (lzw_compress, lzw_decompress),
        (zstd_compress, zstd_decompress),
        (deflate_compress, deflate_decompress),
        (brotli_compress, brotli_decompress),
    ]
    for compress, decompress in functions:
        encoded = compress(text)
        decoded = decompress(encoded)
        assert decoded == text, f"{compress.__name__} failed with text: {text}"
