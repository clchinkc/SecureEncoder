import pytest
from src.huffman import huffman_compress, huffman_decompress

TEST_TEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit."
SPECIAL_TEST_TEXT = "~!#$%^&*()_+"


def test_huffman_compression_cycle():
    """Test Huffman compression and decompression."""
    encoded_data = huffman_compress("he")
    assert (
        encoded_data
        == "eyJjb21wcmVzc2VkX2RhdGEiOiAiTVRBPSIsICJzZXJpYWxpemVkX3RyZWUiOiB7ImxlZnQiOiB7ImNoYXIiOiAiZSJ9LCAicmlnaHQiOiB7ImNoYXIiOiAiaCJ9fX0="
    )

    decoded_data = huffman_decompress(encoded_data)
    assert decoded_data == "he"


# Additional tests for edge cases
@pytest.mark.parametrize("text", ["", "a", TEST_TEXT, SPECIAL_TEST_TEXT])
def test_compression_with_varied_text(text):
    """Test compression algorithms with varied text inputs."""
    functions = [
        (huffman_compress, huffman_decompress),
    ]
    for compress, decompress in functions:
        encoded = compress(text)
        decoded = decompress(encoded)
        assert decoded == text, f"{compress.__name__} failed with text: {text}"
