import os

from argon2.low_level import (
    hash_secret_raw,
    Type,
)

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Derive a 256-bit encryption key from the master password.
    """

    return hash_secret_raw(
        secret=master_password.encode("utf-8"),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=Type.ID,
    )


def generate_salt() -> bytes:
    """
    Generate a random salt for a vault.
    """

    return os.urandom(16)


def encrypt_data(data: str, key: bytes):
    """
    Encrypt data using AES-256-GCM.
    """

    nonce = os.urandom(12)

    aes = AESGCM(key)

    ciphertext = aes.encrypt(
        nonce,
        data.encode("utf-8"),
        None,
    )

    return ciphertext, nonce


def decrypt_data(ciphertext: bytes, nonce: bytes, key: bytes) -> str:
    """
    Decrypt AES-256-GCM encrypted data.
    """

    aes = AESGCM(key)

    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        None,
    )

    return plaintext.decode("utf-8")