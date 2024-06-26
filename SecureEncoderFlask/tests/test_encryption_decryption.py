import pytest
import os

from src.encryption_decryption import (
    ensure_aes_key,
    aes_encrypt,
    aes_decrypt,
    generate_rsa_keys,
    rsa_encrypt,
    rsa_decrypt,
)


def setup_module(module) -> None:
    """Setup any state specific to the execution of the given module."""
    global original_key_file
    original_key_file = "aes_key.bin"  # This should match your production key file path
    global test_key_file
    test_key_file = "tests/test_aes_key.bin"
    # Ensure the test directory exists
    os.makedirs(os.path.dirname(test_key_file), exist_ok=True)


def teardown_module(module) -> None:
    """Teardown any state that was previously setup with a setup_module method."""
    if os.path.exists(test_key_file):
        os.remove(test_key_file)


def test_ensure_aes_key_generation() -> None:
    """Test that a new key is generated when the key file is missing."""
    if os.path.exists(test_key_file):
        os.remove(test_key_file)  # Ensure the key file is not present before the test
    assert not os.path.exists(
        test_key_file
    ), "Key file should not exist before the test"
    key = ensure_aes_key(test_key_file)
    assert os.path.exists(
        test_key_file
    ), "Key file should be created after calling ensure_aes_key"
    with open(test_key_file, "rb") as f:
        assert f.read() == key, "Key file should contain the generated key"


def test_ensure_aes_key_retrieval() -> None:
    """Test that an existing key is retrieved when the key file is present."""
    key = os.urandom(32)
    with open(test_key_file, "wb") as f:
        f.write(key)
    assert os.path.exists(test_key_file), "Key file should exist before the test"
    retrieved_key = ensure_aes_key(test_key_file)
    assert retrieved_key == key, "Retrieved key should match the one in the key file"


def test_aes_encrypt_decrypt() -> None:
    """Test that text is correctly encrypted and decrypted back to its original form."""
    key = ensure_aes_key(test_key_file)  # Use the helper function to manage the key
    plaintext = "Hello, World!"
    encrypted = aes_encrypt(plaintext, key)
    decrypted = aes_decrypt(encrypted, key)
    assert decrypted == plaintext, "Decrypted text should match the original"


def test_aes_encryption_decryption_empty_string() -> None:
    """Test encryption and decryption of an empty string."""
    key = ensure_aes_key(test_key_file)
    plaintext = ""
    encrypted = aes_encrypt(plaintext, key)
    decrypted = aes_decrypt(encrypted, key)
    assert (
        decrypted == plaintext
    ), "Decrypted text should be an empty string for empty input"


def test_aes_encryption_uniqueness() -> None:
    """Test that encrypting the same text with different keys or nonces results in different ciphertexts."""
    plaintext = "Repeatable text"
    key1 = ensure_aes_key(test_key_file)
    key2 = os.urandom(32)  # Ensure a different key
    encrypted1 = aes_encrypt(plaintext, key1)
    encrypted2 = aes_encrypt(plaintext, key2)
    assert (
        encrypted1 != encrypted2
    ), "Encryption with different keys should produce different outputs"
    # Test with the same key but expect different nonces to generate different ciphertexts
    encrypted3 = aes_encrypt(plaintext, key1)
    assert (
        encrypted1 != encrypted3
    ), "Encryption with the same key but different nonces should produce different outputs"


def test_aes_encryption_decryption_invalid_key() -> None:
    """Test that decryption fails with an incorrect key."""
    key = ensure_aes_key(test_key_file)
    plaintext = "Secret message"
    encrypted = aes_encrypt(plaintext, key)
    wrong_key = os.urandom(32)  # Ensure a different key
    with pytest.raises(ValueError) as excinfo:
        aes_decrypt(encrypted, wrong_key)
    assert "Decryption failed or wrong key used" in str(
        excinfo.value
    ), "Decryption should fail with an incorrect key and raise a ValueError"


def test_rsa_encrypt_decrypt() -> None:
    """Test that text is correctly encrypted and decrypted back to its original form using RSA."""
    private_key, public_key = generate_rsa_keys()
    plaintext = "Hello, RSA World!"
    encrypted = rsa_encrypt(plaintext, public_key)
    decrypted = rsa_decrypt(encrypted, private_key)
    assert decrypted == plaintext, "Decrypted text should match the original plaintext"


def test_rsa_encryption_uniqueness() -> None:
    """Test that RSA encryption of the same text results in different ciphertexts."""
    _, public_key = generate_rsa_keys()
    plaintext = "Repeatable text"
    encrypted1 = rsa_encrypt(plaintext, public_key)
    encrypted2 = rsa_encrypt(plaintext, public_key)
    assert (
        encrypted1 != encrypted2
    ), "RSA encryption should produce different outputs for the same input"


def test_rsa_encrypt_decrypt_with_multiple_keys() -> None:
    """Test RSA encryption and decryption using multiple key pairs."""
    private_key1, public_key1 = generate_rsa_keys()
    private_key2, public_key2 = generate_rsa_keys()
    plaintext = "Shared Secret!"

    encrypted_with_key1 = rsa_encrypt(plaintext, public_key1)
    decrypted_with_key1 = rsa_decrypt(encrypted_with_key1, private_key1)
    encrypted_with_key2 = rsa_encrypt(plaintext, public_key2)
    decrypted_with_key2 = rsa_decrypt(encrypted_with_key2, private_key2)

    assert (
        decrypted_with_key1 == plaintext
    ), "Decrypted text should match the original with key pair 1"
    assert (
        decrypted_with_key2 == plaintext
    ), "Decrypted text should match the original with key pair 2"
    assert (
        encrypted_with_key1 != encrypted_with_key2
    ), "Different key pairs should produce different ciphertexts"


def test_rsa_large_data_encryption() -> None:
    """Test RSA encryption and decryption with a chunking approach (demonstrative)."""
    private_key, public_key = generate_rsa_keys()
    plaintext = "A" * 1000  # Demonstrative chunking
    chunk_size = 190  # Based on RSA key size minus padding overhead
    encrypted_chunks = [
        rsa_encrypt(plaintext[i : i + chunk_size], public_key)
        for i in range(0, len(plaintext), chunk_size)
    ]
    decrypted_chunks = [rsa_decrypt(chunk, private_key) for chunk in encrypted_chunks]
    decrypted_text = "".join(decrypted_chunks)
    assert (
        decrypted_text == plaintext
    ), "Decrypted text should match the original large plaintext"


def test_rsa_decryption_with_wrong_key() -> None:
    """Test RSA decryption fails when using a wrong private key."""
    private_key1, public_key1 = generate_rsa_keys()
    private_key2, _ = generate_rsa_keys()  # Correct private key is not used
    plaintext = "Critical data"
    encrypted = rsa_encrypt(plaintext, public_key1)
    try:
        rsa_decrypt(encrypted, private_key2)
        assert False, "Decryption should fail but succeeded"
    except Exception as e:
        assert (
            "decryption failed" in str(e).lower()
        ), "Expected decryption failure did not occur"


def test_rsa_public_key_reuse() -> None:
    """Test reusing the same public key for multiple encryptions."""
    private_key, public_key = generate_rsa_keys()
    plaintexts = ["Message 1", "Message 2", "Message 3"]

    encrypted_texts = [rsa_encrypt(pt, public_key) for pt in plaintexts]
    decrypted_texts = [rsa_decrypt(et, private_key) for et in encrypted_texts]

    assert all(
        dt == pt for dt, pt in zip(decrypted_texts, plaintexts)
    ), "All decrypted texts should match their original plaintexts"


def test_rsa_padding_oracle_attack_scenario() -> None:
    """Simulate a scenario that should be resistant to padding oracle attacks."""
    private_key, public_key = generate_rsa_keys()
    plaintext = "Very sensitive data"
    encrypted = rsa_encrypt(plaintext, public_key)
    # Correct XOR operation for tampering demonstration
    encrypted_bytes = bytes.fromhex(encrypted)
    tampered_ciphertext = encrypted_bytes[:-1] + bytes([encrypted_bytes[-1] ^ 0x01])
    tampered_hex = tampered_ciphertext.hex()
    try:
        decrypted = rsa_decrypt(tampered_hex, private_key)
        assert (
            decrypted != plaintext
        ), "Tampering should lead to decryption failure or incorrect output"
    except ValueError:
        # This is expected in some cases where tampering leads to an outright decryption error
        pass
    except Exception as e:
        # Catch unexpected exceptions to ensure they are handled correctly
        assert (
            False
        ), f"Unexpected exception type: {type(e).__name__}, message: {str(e)}"
