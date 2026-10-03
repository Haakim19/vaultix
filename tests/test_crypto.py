from app.security.crypto import(
    generate_salt,
    derive_key,
    encrypt_data,
    decrypt_data,
)
import pytest
from cryptography.exceptions import InvalidTag

def test_encrypt_decrypt():
    salt = generate_salt()
    key = derive_key("test-password", salt)

    original_data = "My secret password"
    ciphertext, nonce = encrypt_data(original_data, key)

    decrypted_data = decrypt_data(ciphertext, nonce, key)

    assert decrypted_data == original_data

def test_decrypt_with_wrong_key():
    salt = generate_salt()
    correct_key = derive_key("correct-password", salt)
    wrong_key = derive_key("wrong-password", salt)

    ciphertext, nonce = encrypt_data("Secret data", correct_key)

    with pytest.raises(InvalidTag):
        decrypt_data(ciphertext, nonce, wrong_key)
    

def test_decrypt_tampered_data():
    salt = generate_salt()
    key = derive_key("test-password", salt)

    ciphertext, nonce = encrypt_data("Secret data", key)

    tampered_ciphertext = bytearray(ciphertext)
    tampered_ciphertext[0] ^= 1

    with pytest.raises(InvalidTag):
        decrypt_data(bytes(tampered_ciphertext), nonce, key)

def test_generate_salt():
    salt1 = generate_salt()
    salt2 = generate_salt()

    assert len(salt1) == 16
    assert len(salt2) == 16
    assert salt1 != salt2

def test_different_salt_produce_differen_key():
    password = "test-password"
    
    salt1 = generate_salt()
    salt2 = generate_salt()
    
    key1 = derive_key(password, salt1)
    key2 = derive_key(password, salt2)
    
    assert key1 != key2