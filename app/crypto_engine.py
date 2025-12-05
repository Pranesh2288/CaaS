from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA, DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import base64

# --- Hybrid Encryption Logic ---
def encrypt_file_hybrid(file_data: bytes, user_public_key_pem: str):
    """
    1. Generates ephemeral AES key.
    2. Encrypts data with AES.
    3. Encrypts AES key with User's RSA Public Key.
    """
    # 1. Generate AES Session Key (256 bit)
    aes_key = get_random_bytes(32)
    
    # 2. Encrypt Data (AES-GCM)
    cipher_aes = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher_aes.encrypt_and_digest(file_data)
    
    # 3. Encrypt AES Key (RSA)
    recipient_key = RSA.import_key(user_public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    
    return {
        "ciphertext": ciphertext,
        "nonce": cipher_aes.nonce,
        "tag": tag,
        "encrypted_aes_key": encrypted_aes_key
    }

# --- DSA Logic (MFA) ---
# In prod, load this from Secret Manager
server_dsa_key = DSA.generate(1024) 

def sign_otp(otp_code: str):
    h = SHA256.new(otp_code.encode('utf-8'))
    signer = DSS.new(server_dsa_key, 'fips-186-3')
    signature = signer.sign(h)
    return signature

def verify_otp_signature(otp_code: str, signature: bytes):
    try:
        h = SHA256.new(otp_code.encode('utf-8'))
        verifier = DSS.new(server_dsa_key.publickey(), 'fips-186-3')
        verifier.verify(h, signature)
        return True
    except ValueError:
        return False