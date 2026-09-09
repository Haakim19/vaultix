from app.security.crypto import(
    generate_salt,
    derive_key,
    encrypt_data,
    decrypt_data,
)

def main ():
    # 1. Create a random salt
    salt = generate_salt()

    # 2. User's master password
    master_password = "Haakimahamed"
    
    # 3. Derive the vault key using Argon2id
    key = derive_key(master_password, salt)
    
    print("Key generated successfully.")
    print("Key length:", len(key), "bytes")
    
    # 4. Encrypt some test data
    original_data = "My secret password"

    ciphertext, nonce = encrypt_data(
        original_data,
        key,
    )

    print("Data encrypted successfully.")

    # 5. Decrypt it
    decrypted_data = decrypt_data(
        ciphertext,
        nonce,
        key,
    )

    print("Decrypted data:", decrypted_data)

    # 6. Verify
    if decrypted_data == original_data:
        print("✅ Encryption test PASSED!")
    else:
        print("❌ Encryption test FAILED!")
        
if __name__ == "__main__":
    main()