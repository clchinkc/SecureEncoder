from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import os

def ensure_aes_key(key_file):
    """Ensure there is an AES key available, and return it."""
    if not os.path.exists(key_file):
        key = os.urandom(32)  # AES-256 key
        with open(key_file, 'wb') as kf:
            kf.write(key)
        print(f"New AES key generated and saved to {key_file}")
    else:
        with open(key_file, 'rb') as kf:
            key = kf.read()
    return key

def aes_encrypt(plaintext: str, key: bytes):
    """Encrypt a string using AES encryption with the provided key."""
    # Generate a random IV
    iv = os.urandom(16)
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Encrypt the plaintext
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    # Return IV + Ciphertext for decryption
    return iv + ciphertext

def aes_decrypt(ciphertext: bytes, key: bytes):
    """Decrypt a string using AES decryption with the provided key."""
    # Extract IV from the beginning of the ciphertext
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    # Decrypt the ciphertext
    return decryptor.update(actual_ciphertext) + decryptor.finalize()

def generate_rsa_keys():
    """Generate RSA private and public keys."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_rsa_key(key, key_file, is_private=True):
    """Save an RSA key (private or public) to a file."""
    with open(key_file, "wb") as kf:
        if is_private:
            kf.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        else:
            kf.write(key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

def ensure_rsa_public_key(public_key_file):
    """Ensure the RSA public key is available and return it."""
    if not os.path.exists(public_key_file):
        # If the public key is missing, generate both keys to ensure matching pairs
        private_key_file = public_key_file.replace("public", "private")
        if not os.path.exists(private_key_file):
            private_key, public_key = generate_rsa_keys()
            save_rsa_key(private_key, private_key_file, is_private=True)
            save_rsa_key(public_key, public_key_file, is_private=False)
        else:
            # Load the existing private key and derive the public key
            with open(private_key_file, "rb") as kf:
                private_key = serialization.load_pem_private_key(
                    kf.read(),
                    password=None,
                    backend=default_backend()
                )
            public_key = private_key.public_key()
            save_rsa_key(public_key, public_key_file, is_private=False)
    else:
        # Load the existing public key
        with open(public_key_file, "rb") as kf:
            public_key = serialization.load_pem_public_key(
                kf.read(),
                backend=default_backend()
            )
    return public_key

def ensure_rsa_private_key(private_key_file):
    """Ensure the RSA private key is available and return it."""
    if not os.path.exists(private_key_file):
        # If the private key is missing, generate both keys to ensure matching pairs
        public_key_file = private_key_file.replace("private", "public")
        private_key, public_key = generate_rsa_keys()
        save_rsa_key(private_key, private_key_file, is_private=True)
        save_rsa_key(public_key, public_key_file, is_private=False)
    else:
        # Load the existing private key
        with open(private_key_file, "rb") as kf:
            private_key = serialization.load_pem_private_key(
                kf.read(),
                password=None,
                backend=default_backend()
            )
    return private_key

def rsa_encrypt(plaintext: str, public_key):
    """Encrypt a string using RSA public key."""
    ciphertext = public_key.encrypt(
        plaintext.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def rsa_decrypt(ciphertext: bytes, private_key):
    """Decrypt a string using RSA private key."""
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()

